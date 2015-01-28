# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 14:26:20 2015

@author: sig
"""
if __name__ == "__main__":
    """
    """
    import argparse
    from ymraster import *
     
    #Set of the parse arguments
    parser = argparse.ArgumentParser(description= "Perform a Large-Scale Mean"+
                                    "-Shift segmentation in four step:  a " +
                                    "mean shift fitlering, a segmentation, " +
                                    " a merge of small regions (optional)" +
                                    ", a vectorisation (optional). This " +
                                    "application works using LSMS otb " +
                                    "application.") 
    parser.add_argument("--xs_file", "-xs", help="Path of the multi-spectral" +
                        "image.",required = True)
    parser.add_argument("--spatialr", "-spr", help="Spatial radius of the " +
                        "neighborhooh",required = True, type = int)
    parser.add_argument("--ranger", "-rg", help="Range radius defining the " +
                        "radius (expressed in radiometry unit) in the multi" +
                        "-spectral space.",required = True, type = float)
    parser.add_argument("--maxiter", "-max", help="Maximum number of " + 
                        "iterations of the algorithm used in "+
                        "MeanSiftSmoothing application (default value is 10)",
                        type = int, default = 10)
    parser.add_argument("--thres", "-th", help="Mean shift vector threshold" +
                        "(default value is 0.1).", type = float, default = 0.1)                
    parser.add_argument("--rangeramp", "-rga", help="Range radius coefficient"+
                        ": This coefficient makes dependent the ranger of the"+
                        " colorimetry of the filtered pixel : y = rangeramp" +
                        " * x + ranger(default value is 0).", type = float,
                         default = 0)
    parser.add_argument("--modesearch", "-mos", help="Mean shift vector thres"+
                        "hold (default value is 0)",type = int,default = 0)
    parser.add_argument("--tilesizex", "-tx",help="Size of tiles along the "+
                        "X-axis (default value is 256)", type = int, default =
                        256)
    parser.add_argument("--tilesizey", "-ty",help="Size of tiles along the "+
                        "Y-axis (default value is 256)", type = int, default =
                        256)
    parser.add_argument("--mstep", "-m",help="Do the merge step if notified",
                        action = "store_true")
    parser.add_argument("--minsize", "-ms",help="minimum size of a label",
                        type = int)
    parser.add_argument("--vstep", "-v",help="Do the vectorisation step if "+
                        "notified", action = "store_true")
    parser.add_argument("-pref", "--prefixe", help ="Prefixe to add to the " +
                        "file to be written", default = "", type = str)
    parser.add_argument("-dir","--dir_file", default = "", help = "Path of "+
                        "the folder where the outputs will be written" )
    args = parser.parse_args()
    
    #control the coherency of the arguments
    if not(args.mstep) and args.minsize:
        print "Warning : --msize shouldn't be specified without --mstep"
        
    
    #Symbol to add in function of the optional parse arguments, to have a 
    #proper path
    if args.dir_file:
        args.dir_file += '/'
    if args.prefixe:
        args.prefixe += '_'
    print args
    
    #first step : smoothing
    xs = Raster(args.xs_file)
    output_filtered_image = args.dir_file + args.prefixe + "_spr_" + \
                            str(args.spatialr) + "_rg_" + str(args.ranger) + \
                            "_max_" + str(args.maxiter) + "_rga_" + \
                            str(args.rangeramp) + "_th_" + str(args.thres)\
                            + "filtered.tif"
    output_spatial_image = args.dir_file + args.prefixe + 'spatial.tif'
    smooth_img,pos_img = xs.lsms_smoothing(output_filtered_image, 
                                           args.spatialr, args.ranger,
                                           output_spatial_image, thres = 
                                           args.thres, rangeramp = 
                                           args.rangeramp, maxiter = 
                                           args.maxiter, modesearch = 
                                           args.modesearch)   
    print "smoothing step has been realized succesfully"
    
    #second step : segmentation
    output_seg = args.dir_file + args.prefixe + 'lsms_seg.tif'
    seg_img = smooth_img.lsms_seg (pos_img, output_seg, args.spatialr, 
                                   args.ranger, tilesizex = args.tilesizex,
                                   tilesizey = args.tilesizey)
    print "segmentation step has been realized succesfully"
    
    #third step (optional) : merging small regions
    if args.mstep: 
        output_merged = args.dir_file + args.prefixe + 'lsms_merged.tif'
        merged_img = seg_img.lsms_merging(smooth_img, output_merged, 
                                          args.minsize, tilesizex = \
                                          args.tilesizex,tilesizey = \
                                          args.tilesizey)
        print "merging step has been realized succesfully"
    else:
        merged_img = seg_img
    #fourth step (optional) : vectorization
    if args.vstep: 
        output_vector = args.dir_file + args.prefixe + 'lsms_vect.shp'
        merged_img.lsms_vectorisation(xs, output_vector, tilesizex = \
                                    args.tilesizex,tilesizey = args.tilesizey)
        print "vectorisation step has been realized succesfully"