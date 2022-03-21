import pickle
import numpy as np
import pandas as pd
import csv
from GoDefination import get_gene_ontology
import string
from nltk.translate.bleu_score import sentence_bleu

#load uniprot data 
def loadUniprotData():
    df = pd.read_csv ('UniptotData2022.tab',sep='\t')
    df = df[['Entry','Function [CC]','Gene ontology IDs']]
    df = df.rename(columns={"Entry": "Protein", "Function [CC]": "Uniprot Description","Gene ontology IDs":"Goterm Annotation"})
    df = df.set_index('Protein')
    return df
    # print(df.loc['Q04917'])
    # val = df.loc['Q04917']
    # print(type(val['Goterm Annotation']))
    # input()
    # loadUniprotData()


#given a goterm return all parent information
#use recent go term information for all parent list, filter using go.obo ontology information
def allParentList(goterm):
    parentList=""
    data = pd.read_csv("AllParentListUpdatedOn2022Goa.csv", index_col=0)
    try:
        parentList = data.loc[goterm][2]
    except:
        parentList=""
    return parentList.split(";")


print(allParentList('GO:0000001'))



