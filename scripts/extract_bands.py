#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from ymraster import Raster

import argparse


def command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Remove specified band(s) from the given raster(s)")
    parser.add_argument("raster", nargs='+',
                        help="Space separated list of rasters from which to "
                        "extract one or more bands")
    parser.add_argument("-i", "--idxs", type=int, nargs='+', required=True,
                        help="Space separated list of indices of bands to "
                        "remove (starts at 1 for the first band)")
    parser.add_argument("-o", "--out_file",
                        help="Path of the output file. "
                        "The original raster file is overwritten if omitted")
    return parser.parse_args()


def remove_bands(args):
    for filename in args.raster:
        raster = Raster(filename)
        raster.remove_bands(*args.idxs, out_filename=args.out_file)


def main():
    args = command_line_arguments()
    remove_bands(args)


if __name__ == "__main__":
    main()
