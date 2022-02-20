
import pickle
import numpy as np
import pandas as pd
from GoDefination import get_gene_ontology


def extractDataFromPickleFile(filename):
    datalist = pd.read_pickle('combined-multimodal-bp.pkl')
    accessions = datalist[['accessions', 'gos']]
    return accessions


def allParentList(goterm):
    data = pd.read_csv("AllParentList.csv", index_col=0)
    parentList = data.loc['GO:0000001'][1]
    return parentList.split()


def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list


def getGoTermUniqueList(row):
    uniprot_gos = row['gos']
    goterm_list = []
    for ele in uniprot_gos:
        goterm_list.append(ele)
        list_ = allParentList(ele)
        goterm_list.extend(list_)
    print(len(goterm_list))
    goterm_list = unique(goterm_list)
    print(len(goterm_list))
    return goterm_list

def prepareDocument(geneOntology,goterm_list):
    doc_defination=""
    for go in goterm_list:
        go_details = geneOntology[go]
        defination = go_details['def']
        doc_defination=doc_defination+defination
    print(doc_defination)
    doc_defination= doc_defination.replace('"', "")
    return doc_defination


def prepareAllGotermAnnotation():
    geneOntology = get_gene_ontology()
    protein_goterm_annotation = extractDataFromPickleFile(
        'combined-multimodal-bp.pkl')
    # print(protein_goterm_annotation)
    all_gos_list = []
    for index, row in protein_goterm_annotation.iterrows():
        uniprot_gos = row['gos']
        goterm_list= getGoTermUniqueList(row)
        prepareDocument(geneOntology,goterm_list)
        # print(len(goterm_list))


prepareAllGotermAnnotation()
