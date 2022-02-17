# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 23:24:03 2022

@author: swaga
"""
import pickle 
import numpy as np
import pandas as pd

print("Hello")

# =============================================================================
# with open('combined-multimodal-bp.pkl', 'rb') as handle:
#     b = pickle.load(handle)
# print(b)
# =============================================================================


val = pd.read_pickle('combined-multimodal-bp.pkl')
print(val.index)
head = val.head()
print(head.columns)
accessions = val[['accessions','gos']]
print(accessions)
# print(val['accessions'])

accessions.to_csv('accessions.csv')