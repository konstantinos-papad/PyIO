#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:35:34 2022

@author: costaspapad
"""

from osgeo import gdal

import GDALRasterBand as dbse
import numpy

class GDALRaster:
    """! The GDALRaster class
    
    Defines a class for managing raster databases using GDAL libraries.
    """
    
    def __init__(self, file_format):
        """! Instantiates GDALRaster for the given file format.
        
        @param file_format the identified driver, or NULL if no match is found (list of available format can be found in the gdal website https://gdal.org/drivers/raster/index.html)
        
        @return returns an instance of a GDALRaster object
        """
        self._driver = gdal.GetDriverByName(file_format)
        self._driver.Register()
        
        self._raster = None
        self.__geotransform = None
        self.xref = None
        self.dx = None
        self.rx = None
        self.yref = None
        self.ry = None
        self.dy = None
        
        self.number_of_bands = None
        self.ncols = None
        self.nrows = None
        
        self.projection = None
        self.metadata = None
        self.description = None
        self.datatype = None
        
        self.dataset = None
        
        
    def __translate_geotransform(self):
        self.xref = self.__geotransform[0]
        self.dx = self.__geotransform[1]
        self.rx = self.__geotransform[2]
        self.yref = self.__geotransform[3]
        self.ry = self.__geotransform[4]
        self.dy = self.__geotransform[5]
        
    
        
    def __read(self, filepath):
        """! Method to read the raster database from the given filename.
        
        @param filename the path to the data file
        
        """
        
        self._raster = gdal.Open(filepath)
        
        self.__geotransform = self._raster.GetGeoTransform()
        self.__translate_geotransform()
        
        self.number_of_bands = (self._raster).RasterCount
        self.ncols = (self._raster).RasterXSize
        self.nrows = (self._raster).RasterYSize
        
        self.projection = (self._raster).GetProjection()
        self.metadata = (self._raster).GetMetadata()
        self.description = (self._raster).GetDescription()
        self.datatype = type(self._raster)
        
        self.dataset = []
        for i in range(self.number_of_bands):
            tmp = dbse.GDALRasterBand((self._raster).GetRasterBand(i+1))
            self.dataset.append(tmp)
        
        del tmp
            
    def read(self, filepath):
        """! Method to read the raster database from the given filename.
        
        @param filename the path to the data file
        
        """
        self.__read(filepath)
    
    def create(self, filename: str, size_x: int, size_y: int, datatype: numpy.dtype):
        band = 1
        if datatype is numpy.intc:
            self._raster = (self._driver).Create(filename, size_x, size_y, band, gdal.GDT_Int32)
        elif datatype is numpy.int_:
            self._raster = (self._driver).Create(filename, size_x, size_y, band, gdal.GDT_Int64)
        elif datatype is numpy.single:
            self._raster = (self._driver).Create(filename, size_x, size_y, band, gdal.GDT_Float32)
        elif datatype is numpy.double:
            self._raster = (self._driver).Create(filename, size_x, size_y, band, gdal.GDT_Float64)
    
    def geotransform(self):
        return self.__geotransform
    
    def set_geotransform(self, matrix):
        if self._raster:
            self.__geotransform = matrix
            self.__translate_geotransform()
            self._raster.SetGeoTransform(self.__geotransform)
        
    def get_geotransform(self):
        if self._raster:
            self.__geotransform = self._raster.GetGeoTransform()
            self.__translate_geotransform()
            return self.__geotransform
        else:
            return None
        
    def raster_dbase(self, dbase = None):
        if dbase:
            self._raster = dbase
        else:
            return self._raster
    
    def raster_driver(self, driver = None):
        if driver:
            self._driver = driver
        else:
            return self._driver
        