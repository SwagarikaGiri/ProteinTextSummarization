# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:17:41 2022
get rouge score
@author: swaga
"""
import pickle 
import numpy as np
import pandas as pd
from rouge import Rouge


model_out = "he began by starting a five person war cabinet and included chamberlain as lord president of the council"

reference = "he began his premiership by forming a five-man war cabinet which"
rouge = Rouge()

print(rouge.get_scores(model_out, reference))

# val = pd.read_pickle('combined-multimodal-bp.pkl')
# accessions = val[['accessions','gos']]

# for accession, gos in accessions.items():
#     print(accession)
#     print(gos)