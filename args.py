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
        "--show_command",
        metavar="",
        type=str,
        help="Filename of show output command",
        default="/tmp/text",
    )


def outfile_arg(parser):
    """define arguments to be added"""
    return parser.add_argument(
        "--out",
        metavar="",
        type=str,
        help="Filename of output file [.xml,.png,.html]",
        default="",
    )

def main():
    """
    main function define to test the function before integeration
    """
    parser = get_args([show_file_arg, outfile_arg])
    args = parser.parse_args()
    del args
    return 0


if __name__ == "__main__":
    main()
