#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:38:42 2022

@author: costaspapad
"""

class GDALRasterBand:
    
    def __init__(self, band):
        
        self._band = band
        
        self.ncols = self._band.XSize
        self.nrows = self._band.YSize
        self.datatype = self._band.DataType
        self.nodata = self._band.GetNoDataValue()
        self.maximum = self._band.GetMaximum()
        self.minimum = self._band.GetMinimum()
        
        self.data = self._band.ReadAsArray(0, 0, self.ncols, self.nrows)
        
        self.properties = {
            'ncols': self.ncols,
            'nrows': self.nrows,
            'format':self.datatype, 
            'nodata': self.nodata,
            'data': self.data,
            'max': self.maximum,
            'min': self.minimum
            }
        
    def __read_block_by_block(self, block_cols, block_rows):
        
        tiles = []
        for i in range(0, self.nrows, block_rows):
            if i + block_rows < self.nrows:
                block_row_num = block_rows
            else:
                block_row_num = block_rows - i
            for j in range(0, self.cols, block_cols):
                if i + block_cols < self.ncols:
                    block_col_num = block_cols
                else:
                    block_col_num = self.ncols - j
                
                block_data = self._band.ReadAsArray(j, i, block_col_num, block_row_num)
                tile = {'col_ref' : j, 
                        'row_ref' : i, 
                        'col_num' : block_col_num,
                        'row_num' : block_row_num,
                        'data' : block_data }
                tiles.append(tile)
                
        return tiles

        
        
# write    def __init__(self)