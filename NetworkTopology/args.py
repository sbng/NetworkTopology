#!/usr/bin/env python
"""
This module get the arguments for the various founction for processing
Any new argument can be added to this file to consolidate and reuse all possible
arguments used. Use need to add the boolean keyword of the new argument and use the 
boolean variable to capture the argument needed when this module is called.
"""
import argparse

def show_file_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--infile",
        metavar="",
        type=str,
        help=" Filename of show output command",
        default="/tmp/text",
    )


def outfile_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--outfile",
        metavar="",
        type=str,
        help=" Filename of output file [.xml,.png,.html,.drawio]",
        default="Null",
    )

def template_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--template",
        metavar="",
        type=str,
        help=" Type of TTP template specifed using file path ",
        default="template/show_all.txt",
    )

def edge_type_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--edge_type",
        metavar="",
        type=str,
        help=" Style to parse using [mac|cdp] (Default: cdp)",
        default="cdp",
    )

def framework_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--framework",
        metavar="",
        type=str,
        help=" Using framework [d3|drawio] (Default: d3)",
        default="d3",
    )

def graph_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--graph",
        metavar="",
        type=str,
        help=" Type of graph Graph, DiGraph or MultiGraph (Default: Graph)",
        default="Graph",
    )

def restore_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--restore",
        metavar="",
        type=str,
        help=" Restore the previous position of devices on the topology base upon saved svg provided (path of svg file)",
        default="Null",
    )

def get_args(options):
    """
    Input: keywords boolean of the desire argument
    Output: The argument obtained from the command line
    Caveat: Boolean variable allows the desired argument to be captured
    """
    parser = argparse.ArgumentParser()
    for arg in options:
        arg(parser)
    return parser

def main():
    """
    main function define to test the function before integeration
    """
    parser = get_args([show_file_arg, outfile_arg, template_arg, \
                       edge_type_arg, framework_arg, graph_arg, restore_arg])
    args = parser.parse_args()
    del args
    return 0


if __name__ == "__main__":
    main()
