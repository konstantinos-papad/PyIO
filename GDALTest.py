"""
Created on Sun Jul 10 07:30:46 2022

@author: costaspapad
"""

import GDALRaster


example_filename = '/home/costaspapad/Downloads/nz3065_DSM_2M.asc'
example_fileformat = 'AAIGrid'

example_database = GDALRaster.GDALRaster(example_fileformat)
example_database.read(example_filename)

example_dataset = example_database.dataset[-1]
example_data = example_dataset.data
example_data_rows = example_database.nrows
example_data_cols = example_database.ncols

print('Number of rows in matrix = ' + str(example_data_rows))
print('Number of columns in matrix = ' + str(example_data_cols))