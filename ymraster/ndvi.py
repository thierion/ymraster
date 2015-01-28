# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:39:20 2015

@author: sig
"""

if __name__ == "__main__":
    """Executable of the ndvi band creation
    """
    
    import argparse
    from ymraster import *
    
    #Set of the parse arguments
    parser = argparse.ArgumentParser(description= "Write the NDVI of the " +
    "given image, given the index of the red and nir band. Indexation starts" + 
    " at 1.\n Example : python ndvi.py ../../Donnees/Donnes_supp/" +
    "Spot6_MS_31072013.tif 3 4 -pref A -dir data_example_seg") 
    parser.add_argument("--xs_file","-xs", help="Path of the multi-spectral " +
                        "image", required = True)
    parser.add_argument("--idx_red","-red", help="Chanel number of the red " +
                        "band", type = int, required = True)
    parser.add_argument("--idx_nir", "-nir", help="Chanel number of the nir " +
                        "band", type = int, required = True)    
    parser.add_argument("-out", "--out_file", help ="Name of the output file",
                        required = True, type = str)
    parser.add_argument("-d","--dir", default = "", help = "Path of the " +
                        "folder where the output will be written. The \"/\"" +
                        " or \"\\\" have to be added at the end.")
    args = parser.parse_args()
    print args

    output_ndvi = args.dir + args.out_file 
    #set of the instance    
    spot_xs = Raster(args.xs_file)
    
    #Execution of the method
    ndvi_img = spot_xs.ndvi(output_ndvi, args.idx_red, args.idx_nir)
    print "Writting the ndvi image has been realized succesfully\n" 