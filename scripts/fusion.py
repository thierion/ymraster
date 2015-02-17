# -*- coding: utf-8 -*-

import argparse
from ymraster import Raster


def command_line_arguments():
    parser = argparse.ArgumentParser(description="Merge a raster with its "
                                     "panchromatic image in order to improve "
                                     "resolution")
    parser.add_argument("raster", help="Path to the raster to sharpen")
    parser.add_argument("-p", "--pan_file", required=True, help="Path to the "
                        "panchromatic image")
    parser.add_argument("-o", "--out_file", help="Path to the output file. "
                        "By default, the original raster is overwritten")
    return parser.parse_args()


def pan_sharpen(args):
    raster = Raster(args.raster)
    pan_raster = Raster(args.pan_file)
    raster.fusion(pan_raster, out_filename=args.out_file)


def main():
    args = command_line_arguments()
    pan_sharpen(args)

if __name__ == "__main__":
    main()
