import numpy as np
import pandas as pd
import csv
from GoDefination import get_gene_ontology
from nltk.translate.bleu_score import sentence_bleu

geneOntology = get_gene_ontology()
def importCsvAndStoreInDf(filename, seperator):
    df = pd.read_csv(filename, sep = seperator)
    return df

def setIndexWithParticularColumn(df,column):
    return df.set_index(column)


def removeGotermNotIncluded(gotermList):
    filteredGotermList=""
    erroredGoterm=""
    try:
        gotermList=gotermList.split()
    except:
       gotermList=[] 
    for goterm in gotermList:
        try:
            geneOntology[goterm]
            filteredGotermList+=str(goterm + ";")
        except:
            erroredGoterm+=str(goterm+";")
    filteredGotermList = filteredGotermList[:-1]
    filteredGotermList += ''
    erroredGoterm = erroredGoterm[:-1]
    erroredGoterm += ''
    return filteredGotermList,erroredGoterm


def updateTheAllParentList(df):
    with open('AllParentListUpdatedOn2022Goa.csv','w' ,newline='', encoding='utf-8') as output_csvfile:
        spamwriter = csv.writer(output_csvfile, delimiter=',')
        list_=[]
        list_.extend(['goterm','no of parents', 'parents','erroredgoterm'])
        spamwriter.writerow(list_)
        for index,row in df.iterrows():
            print(index)
            goterm= row['Go term ID']
            parentList = row['All parents list']
            noOfParents = row['No of parents']
            updatedParentList,erroredGoterm=removeGotermNotIncluded(parentList)
            spamwriter.writerow([goterm,len(updatedParentList.split(';')), updatedParentList,erroredGoterm])
            







def main():
    df = importCsvAndStoreInDf("AllParentList.csv",",")
    updateTheAllParentList(df)
    

if __name__ == "__main__":
    main()
