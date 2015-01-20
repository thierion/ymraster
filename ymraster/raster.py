# -*- coding: utf-8 -*-

"""
Raster manipulation library
===========================

This module contains classes for manipulating raster images. It is based on:

    * GDAL_ for general raster reading,

    * NumPy_ for computations,

    * rasterio_ for reading and writing raster efficiently

:: _GDAL: http://gdal.org/
:: _NumPy: http://www.numpy.org/
:: _rasterio: https://github.com/mapbox/rasterio


The ``Raster`` class
--------------------

The ``Raster`` class define an Image readed from a file.
"""

from osgeo import gdal
import numpy as np
import rasterio


class Raster():
    """Represents a raster image that was read from a file

    The whole raster *is not* loaded into memory. Instead this class records
    useful information about the raster (number and position of bands,
    resolution, ...) and provide useful methods for comparing raster,
    computing some indices, etc.

    """

    def __init__(self, filename, *bands):
        """Create a new raster object read from a filename, and compute
        useful properties

        :param filename: a string containing the path of the image to read
        :param bands: band names (eg. 'blue', 'red', 'infrared, etc.)
        """
        self.filename = filename
        # Create 'idx_blue', 'idx_green', etc. attributes
        self.__dict__.update({'idx_' + band: i for i, band in enumerate(bands)})

        # Read information from image
        ds = gdal.Open(filename, gdal.GA_ReadOnly)
        assert ds is not None, \
            'Error in reading {}. Check file name and permissions'.format(
                filename)
        self.width = ds.RasterXSize
        self.height = ds.RasterYSize
        self.number_bands = ds.RasterCount
        self.crs = ds.GetProjection()
        self.geotransform = ds.GetGeoTransform()
        self.topleft_x = self.geotransform[0]
        self.topleft_y = self.geotransform[3]
        self.pixel_width = self.geotransform[1]
        self.pixel_height = self.geotransform[5]

    def array(self):
        """Return a Numpy array corresponding to the image"""
        # Initialize an empty array of correct size and type
        array = np.empty((self.height,
                          self.width,
                          self.number_bands),
                         dtype='float64')

        # Fill the array
        with rasterio.drivers(CPL_DEBUG=True):  # Register GDAL format drivers
            with rasterio.open(self.filename) as img:
                for i in range(self.number_bands):
                    array[:, :, i] = img.read_band(i)

    def ndvi_array(self):
        """Return the Normlized Difference Vegetation Index (NDVI) of the image
        """

        band_red = image[:, :, self.idx_red]
        band_infrared = image[:, :, self.idx_infrared]
        band_red = np.where(band_infrared + band_red == 0, 1, band_red)
        return (band_infrared - band_red) / (band_infrared + band_red)

    def ndmi_array(self, out_filename):
        """Return the Normalized Difference Moisture Index (NDMI) of an image


        """
        band_infrared = image[:, :, i_infrared]
        band_midred = image[:, :, i_midred]
        band_infrared = np.where(band_midred + band_infrared == 0, 1, band_infrared)
        return (band_infrared - band_midred) / (band_infrared + band_midred)

    def ndsi_array(self, out_filename):
        """Return the Normalized Difference Snow Index (NDSI) of an image

        image: a 3+-dimensional numpy array containing pixels from which to compute
               NDVI
        i_green: index of the red band in image (starts at 0)
        i_midred: index of the infrared band in image (starts at 0)

        """
        band_green = image[:, :, i_green]
        band_midred = image[:, :, i_midred]
        band_green = np.where(band_midred + band_green == 0, 1, band_green)
        return (band_green - band_midred) / (band_green + band_midred)