#!/usr/bin/env python

from args import (
    get_args,
    show_file_arg,
    outfile_arg,
    template_arg,
    edge_type_arg,
    framework_arg,
)

from ttp import ttp
import pprint

from edges import (
        gen_edges, 
        gen_nodes,
        d3_graph,
        drawio_graph,
)

def parse(infile, template):
    parser = ttp(data=infile, template=template)
    parser.parse()
    return parser.result()[0][0]

def main():
    parser = get_args(
        [
            show_file_arg,
            outfile_arg,
            template_arg,
            edge_type_arg,
            framework_arg,
        ]
    )

    args = parser.parse_args()
    results = parse(args.infile, args.template)
    links = gen_edges(results, args.edge_type)
    nodes = gen_nodes(links)
    
    if args.framework == "d3":
        d3_graph(nodes, links, args.outfile)
    if args.framework == "drawio":
        drawio_graph(nodes, links, args.outfile)

if __name__ == "__main__":
    main()
