#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 18:49:22 2022

@author: costaspapad
"""

import numpy
import gdal
#import ogr
import GDALRaster

def GDALRasterizeLayer(VectorFile:str, RasterFileOut:str, RasterFormat:str, RasterOutType: numpy.dtype, RasterFileIn:str = None, RasterObject:GDALRaster = None):
    
    RasterDbase = None
    RasterDbaseOut = None
    
    if RasterFileIn and RasterFormat:
        RasterDbase = GDALRaster.GDALRaster(RasterFormat)
        RasterDbase.read(RasterFileIn)
    elif RasterObject:
        RasterDbase = RasterObject
    else:
        return None
    
    RasterDbaseOut = GDALRaster.GDALRaster(RasterFormat)
    RasterDbaseOut.create(RasterFileOut, RasterDbase.ncols, RasterDbase.nrows, RasterOutType)
    RasterDbaseOut.set_geotransform(RasterDbase.get_geotransform())
 
    vector_driver = gdal.GetDriverByName('ESRI Shapefile') 
    vector_driver.Register()
    vector_database = gdal.Open(VectorFile)
    vector_layer = vector_database.GetLayer()
    
    tmp_copy = RasterDbaseOut.raster_dbase()
    gdal.RasterizeLayer(tmp_copy, [1], vector_layer)
    tmp_copy.GetRasterBand(1).SetNoDataValue(0.0)
    
    return tmp_copy
    