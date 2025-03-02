import gravis as gv
import networkx as nx
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
            device_mac[intf["macaddress"]] = host["hostname"]
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
                    the port/interface used to cconnect
                    '''
                    edges.append((info['hostname'],neighbor,mac['port']))
    if edge_type == "cdp":
        for info in parsed_data['hosts']:
            for cdp_info in info['cdp']:
                edges.append((info['hostname'],cdp_info['target']['id'].split('.')[0], cdp_info['src_label']))
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
    router = "image;html=1;image=img/lib/clip_art/networking/Router_Icon_128x128.png"
    drawio_nodes = []
    for i in nodes:
        nodes_attribute = {}
        nodes_attribute = {'id': i, 'style': router, 'label': i, 'width': 78, 'height': 53}
        drawio_nodes.append(nodes_attribute)
    return drawio_nodes

def drawio_gen_edges(edges):
    connection = "endArrow=none;html=1;rounded=0;strokeColor=#788AA3;fontColor=#46495D;fillColor=#B2C9AB;"
    drawio_edges = []
    for i in edges:
        edges_attribute = {}
        edges_attribute = {'source': i[0], 'label': '', 'target': i[1], 'style': connection}
        drawio_edges.append(edges_attribute) 
    return drawio_edges

def d3_graph(nodes, links, outfile, graph_type):
    # Setup the graph
    router_img = gv.convert.image_to_data_url("images/router.svg", data_format=None, return_data_format=False)
    if "multi" in graph_type:
        g = nx.MultiGraph()
    elif "di" in graph_type:
        g = nx.DiGraph()
    else:
        g = nx.Graph() 
    g.graph['background_color'] = "white"
    g.graph['arrow_size'] = 2
    g.add_nodes_from(nodes)
    g.add_edges_from(remove_interfaces(links))
    for n in g:
         g.nodes[n]["name"] = f"{n}" 
         g.nodes[n]["hover"] = '<a href="https://www.cisco.com/search?q={n}">Cisco</a>'
         g.nodes[n]["image"] = router_img 
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
                       'links': drawio_gen_edges(remove_interfaces(links))}
       drawio = drawio_diagram()
       drawio.from_dict(drawio_graph, width=1300, height=1200)
       drawio.layout(algo="kk")
       drawio.dump_file(filename=outfile)
   return
