import pickle
import numpy as np
import pandas as pd
import csv
from GoDefination import get_gene_ontology
import string
from nltk.translate.bleu_score import sentence_bleu


geneOntology = get_gene_ontology()

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def getAllGotermAnnotation(gos):
    gos=gos.split(";")
    all_parent_list=[]
    for go in gos:
       parents=allParentList(go.strip())
       all_parent_list +=parents
    return(set(all_parent_list))

#load uniprot data 
def loadUniprotData():
    df = pd.read_csv('UniptotData2022.tab',sep='\t')
    df = df[['Entry','Function [CC]','Gene ontology IDs']]
    df = df.rename(columns={"Entry": "Protein", "Function [CC]": "Uniprot Description","Gene ontology IDs":"Goterm Annotation"})
    df = df.set_index('Protein')
    return df
    # print(df.loc['Q04917'])
    # val = df.loc['Q04917']
    # print(type(val['Goterm Annotation']))
    # input()
    # loadUniprotData()

def combineAllParentDefination(gotermList):
    doc_defination=""
    erroredGoterm=[]
    for go in gotermList:
        try:
            go_details = geneOntology[go]
            defination = go_details['def']
            doc_defination=doc_defination+defination
        except:
            erroredGoterm.append(go)
    return doc_defination

    
#given a goterm return all parent information
#use recent go term information for all parent list, filter using go.obo ontology information
def allParentList(goterm):
    parentList=""
    data = pd.read_csv("AllParentListUpdatedOn2022Goa.csv", index_col=0)
    try:
        parentList = data.loc[goterm][1]
    except:
        parentList=""
    
    parents =parentList.split(";")
    parents.append(goterm)
    return parents


      

def main():
    with open('ProteinAndItsDescriptionCombined.csv','w' ,newline='', encoding='utf-8') as output_csvfile:
        spamwriter = csv.writer(output_csvfile, delimiter=',')
        list_=[]
        list_.extend(['Protein','Goterms', 'GO Description','Uniprot Description'])
        spamwriter.writerow(list_)
        df = loadUniprotData()
        for index,row in df.iterrows():
            print(index)
            gos=row['Goterm Annotation']
            allParents = getAllGotermAnnotation(gos)
            allParentsString= ' '.join(allParents)
            goaDefination= combineAllParentDefination(allParents)
            uniProtDefination= row['Uniprot Description']
            spamwriter.writerow([index,allParentsString,goaDefination,uniProtDefination])



if __name__ == "__main__":
    main()