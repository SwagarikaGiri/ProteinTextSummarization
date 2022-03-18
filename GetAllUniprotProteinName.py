import pickle
import numpy as np
import pandas as pd
import csv

def extractDataFromPickleFile(filename, resultFile):
    datalist = pd.read_pickle(filename)
    accessions = datalist[['accessions']]
    print(accessions)
    with open(resultFile, 'w' ,newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in accessions.itertuples():
            ele= row.accessions
            ele=ele.strip()
            col1=[]
            col1.append(ele)
            print(col1)
            writer.writerow(col1)



extractDataFromPickleFile('combined-multimodal-bp.pkl','accession-no-bp.csv')
extractDataFromPickleFile('combined-multimodal-cc.pkl','accession-no-cc.csv')
extractDataFromPickleFile('combined-multimodal-mf.pkl','accession-no-mf.csv')








