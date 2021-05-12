# -*- coding: utf-8 -*-
"""
Created on Thu May 13 02:40:55 2021

@author: WJ
"""

# getting friendly with pandas

import pandas as pd

OriginalData = pd.read_csv('data_renew.csv', header = None)
#OriginalData

# excercise on pandas basic features
print(type(OriginalData), '\r\n')
    
# no labels yet
print('About Columns...', OriginalData.columns, '\r\n')
    
# shows
print(OriginalData.index, '\r\n')

print(OriginalData.axes)

NCols = OriginalData.columns.size
NRows = OriginalData.index.size


Column_Names = [None] * NCols
for i in range(NCols):
    Column_Names[i] = 'col' + str( OriginalData.columns[i])


OriginalData.columns = Column_Names


print(OriginalData.columns)

#OriginalData.columns =




