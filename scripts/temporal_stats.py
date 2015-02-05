# -*- coding: utf-8 -*-

import argparse
from ymraster import Raster, temporal_stats

from datetime import datetime


def valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def date2float(dt, dt0):
    """Returns number of days between the two given datetime objects."""
    delta = dt - dt0
    return delta.days


def compute_temporal_stats():
    # Command-line parameters
    parser = argparse.ArgumentParser(
        description="Compute pixel-wise statistics from a given list of "
        "multitemporal, but spatially identical, images. Only one band in each "
        "image is considered (by default: the first one).\n\n"
        "Output is a multi-band image where each band contains a result (eg. "
        "maximum, mean). For results taken from original values (eg. maximum), "
        "there is an additional band which gives the date/time at which the "
        "result has been found in numeric format (eg. maximum has occured on "
        "Apr 25, 2013 (midnight) -> 1366840800.0)")
    parser.add_argument("rasters", nargs='+',
                        help="List of input images")
    parser.add_argument("-s", "--stat", nargs='+',
                        help="Space separated list of statistics to compute")
    parser.add_argument("-b", "--idx_band", type=int, default=1,
                        help="Index of the band to compute statistics on, "
                        "the same for all images (default: 1)")
    parser.add_argument("-d", "--date-from", type=valid_date,
                        help="Date from which to compute statis "
                        "the input images and whose values are dates in "
                        "numeric format. If specified, statistical dates are "
                        "computed relative to the dates in this raster")
    parser.add_argument("-t", "--time_raster",
                        help="Path to a mono-band raster with same extent than "
                        "the input images and whose values are dates in "
                        "numeric format. If specified, statistical dates are "
                        "computed relative to the dates in this raster")
    parser.add_argument("-o", "--out_file", default='./stats.tif',
                        help="Path to the output file (default: 'stats.tif' in "
                        "the current folder)")
    args = parser.parse_args()

    # Do the actual work
    rasters = [Raster(filename) for filename in args.rasters]
    kw = {}
    if args.idx_band is not None:
        kw['idx_band'] = args.idx_band
    if args.stat is not None:
        kw['stats'] = list(args.stat)
    temporal_stats(list(rasters), args.out_file, 'GTiff', **kw)


if __name__ == "__main__":
    compute_temporal_stats()
