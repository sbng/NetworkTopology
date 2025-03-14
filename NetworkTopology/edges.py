import os.path
import gravis as gv
import networkx as nx
import xml.etree.ElementTree as ET

from N2G import drawio_diagram

from ttp import ttp
import pprint

def gen_device_mac(parsed_data):
    '''
    Create a lookup table for mac address and corresponding device(hostname)
    '''
    device_mac = {}
    for host in parsed_data["hosts"]:
        for intf in host["interface"]:
            device_mac[intf["macaddress"]] = (host["hostname"], intf["interface"])
    return device_mac

def lookup_mac_address(device_db, mac_address):
    '''
    Using mac address to lookup the corresponding device(hostname)
    '''
    if mac_address in device_db.keys():
        return (device_db[mac_address])
    else:
        return "Null"

def gen_edges(parsed_data, edge_type):
    '''
    Generate all edges base upon the TTP template parsed data mac address or CDP
    the edges returns a tuple of source host, target host, source interface, target interface
    '''
    edges = []
    if edge_type == "mac":
        db = gen_device_mac(parsed_data)
        for info in parsed_data['hosts']:
            for mac in info['mac_table']:
                neighbor = lookup_mac_address(db, mac['mac'])
                if neighbor != "Null" :
                    '''
                    create a list that comprise of device(hostname), neighbor device and 
                    the source port/interface used to connect and target port/interface
                    '''
                    edges.append((info['hostname'], neighbor[0], mac['port'], neighbor[1]))
    if edge_type == "cdp":
        for info in parsed_data['hosts']:
            for cdp_info in info['cdp']:
                edges.append((info['hostname'],cdp_info['target']['id'].split('.')[0], cdp_info['src_label'], cdp_info['trgt_label']))
    return list(set(edges))

def gen_nodes(edges):
    '''
    Generate a list of nodes base on edges as the edges are node to node connections
    '''
    hosts = []
    for i in edges:
        for h in i[0:1]:
            hosts.append(h)
    return list(set(hosts))

def remove_interfaces(links):
    '''
    links argument comprise of (Node1, Node2, interface), this function remove the last 
    element and return (Node1,Node2) as the graph would not need the interfaces 
    '''
    clean_links = []
    for i in list(links):        
        clean_links.append(tuple((i[0],i[1])))
    return clean_links

def cdp_edges(parsed_data):
    '''
    Generate all edges base upon the TTP template parsed data base on CDP properties
    Return the list of generated edges
    '''
    edges = [] 
    for info in parsed_data['hosts']:
        for cdp_info in info['cdp']:
            edges.append((info['hostname'],cdp_info['target']['id'].split('.')[0]))
    return list(set(edges))

def drawio_gen_nodes(nodes):
    router = "shape=mxgraph.cisco.routers.router;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    drawio_nodes = []
    for i in nodes:
        nodes_attribute = {}
        nodes_attribute = {'id': i, 'style': router, 'label': i, 'width': 78, 'height': 53}
        drawio_nodes.append(nodes_attribute)
    return drawio_nodes

def drawio_gen_edges(edges):
    connection = "endArrow=none;html=1;rounded=0;strokeColor=#788AA3;fontColor=#46495D;fillColor=#B2C9AB;"
    #connection = "rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.25;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;curved=1;"
    drawio_edges = []
    for i in edges:
        edges_attribute = {}
        edges_attribute = {'source': i[0], 'target': i[1], 'style': connection, 'src_label': i[2] , 'trgt_label': i[3]}
        drawio_edges.append(edges_attribute) 
    return drawio_edges

def d3_graph(nodes, links, outfile, graph_type, restore):
    # Setup the graph
    router_img = gv.convert.image_to_data_url("images/router.svg", data_format=None, return_data_format=False)
    if "multi" in graph_type:
        g = nx.MultiGraph()
    elif "di" in graph_type:
        g = nx.DiGraph()
    else:
        g = nx.Graph() 
    g.graph['background_color'] = "black"
    g.graph['edge_color'] = "white"
    g.graph['node_label_color'] = "white"
    g.graph['opacity'] = 100
    g.graph['arrow_size'] = 2
    g.add_nodes_from(nodes)
    g.add_edges_from(remove_interfaces(links))
    for n in g:
         g.nodes[n]["name"] = f"{n}" 
         g.nodes[n]["hover"] = '<a href="https://www.cisco.com/search?q={n}">Cisco</a>'
         g.nodes[n]["image"] = router_img 
    '''
    if there is a need to restore the position of a node with reference to the svg file provided
    '''
    if (restore != "Null") and (os.path.isfile(restore)):
        all_positions = find_all_label_positions(restore)
        for label, position in all_positions.items():
            g.nodes[label]['x'],g.nodes[label]['y']= position[0], position[1]

    fig = gv.d3(g, node_label_data_source='name', node_hover_neighborhood=True, \
        show_edge_label=True, edge_label_data_source='label', \
        node_label_size_factor=0.3, node_drag_fix=True, show_node_image=True, \
        node_image_size_factor=2.0, edge_curvature=0.08, graph_height=800, zoom_factor=2,\
        edge_size_factor=0.2, use_edge_size_normalization=True, \
        edge_size_normalization_min=1, edge_size_normalization_max=10, \
        layout_algorithm_active=True)

    if outfile == "Null":
        fig.display()
    else:
        fig.export_html(outfile, overwrite=True)
    return

def drawio_graph(nodes, links, outfile):
   if not outfile == "Null":
       drawio_graph = {'nodes': drawio_gen_nodes(nodes), \
                       'links': drawio_gen_edges(links)}
       drawio = drawio_diagram(link_duplicates='update')
       drawio.from_dict(drawio_graph, width=1300, height=1200)
       drawio.layout(algo="kk")
       drawio.dump_file(filename=outfile)
   return

def find_all_label_positions(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}

    label_positions = {}  # Dictionary to store positions

    for text_elem in root.findall(".//svg:text", namespace):
        label = text_elem.text.strip() if text_elem.text else None
        x = text_elem.get("x")
        y = text_elem.get("y")

        if label and x is not None and y is not None:
            label_positions[label] = (float(x), float(y))
    return label_positions
