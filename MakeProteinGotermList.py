
import pickle
import numpy as np
import pandas as pd
import csv
from GoDefination import get_gene_ontology
import string
from nltk.translate.bleu_score import sentence_bleu

def extractDataFromPickleFile(filename):
    datalist = pd.read_pickle('combined-multimodal-bp.pkl')
    accessions = datalist[['accessions', 'gos']]
    return accessions


def allParentList(goterm):
    parentList=""
    data = pd.read_csv("AllParentList.csv", index_col=0)
    try:
        parentList = data.loc[goterm][1]
    except:
        parentList=""
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
    # print(len(goterm_list))
    goterm_list = unique(goterm_list)
    # print(len(goterm_list))
    return goterm_list

def prepareDocument(geneOntology,goterm_list):
    doc_defination=""
    print(len(goterm_list))
    erroredGoterm=[]
    counter =0
    for go in goterm_list:
        try:
            go_details = geneOntology[go]
            defination = go_details['def']
            doc_defination=doc_defination+defination
        except:
            counter = counter + 1
            erroredGoterm.append(go)
            print("some issue with goterm")
    # print(doc_defination)
    print("the actual no of goterm"+ str(len(goterm_list)))
    print("errored value is"+ str(counter))
    print("errored goterm")
    print(erroredGoterm)
    doc_defination= doc_defination.replace('"', "")
    doc_defination=doc_defination.strip()
    doc_defination=doc_defination.replace("\n", "")
    return doc_defination


def prepare_csv_file(protein,gos,defination):
    with open('ProteinGOAUpdated.csv','w' ,newline='', encoding='utf-8') as output_csvfile:
        spamwriter = csv.writer(output_csvfile, delimiter=',')
        list_=[]
        list_.extend(['protein','gos predictions', 'defination'])
        spamwriter.writerow(list_)
        for i in range(0,len(protein)):
            print(protein[i])
            print(gos[i])
            print(defination[i])
            print([protein[i],gos[i], defination[i]])
            spamwriter.writerow([protein[i],gos[i], defination[i]])

            
def importcsvAndStoreDf():
    df = pd.read_csv("ProteinDescription.csv", sep = '^')
    df = df.set_index('Protein')
    print(df)
    return df

    # with open('ProteinDescription.txt') as f:
    #     lines = f.readlines()
    #     # print(lines)
    #     for line in lines:
    #         line =line.strip()
    #         line_split = line.split("^")
    #         print(line_split)
def removePuntuationFromString(a_string):
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    return new_string

def prepareAllGotermAnnotation():
    geneOntology = get_gene_ontology()
    protein_goterm_annotation = extractDataFromPickleFile(
        'combined-multimodal-bp.pkl')
    # print(protein_goterm_annotation)
    protein_goterm_annotation=protein_goterm_annotation
    all_gos_list = []
    protein_accession=[]
    protein_goterm_list=[]
    protein_defination=[]
    for index, row in protein_goterm_annotation.iterrows():
        print(index)
        protein_accession.append(index)
        uniprot_gos = row['gos']
        goterm_list= getGoTermUniqueList(row)
        protein_goterm_list.append(goterm_list)
        defination = prepareDocument(geneOntology,goterm_list)
        protein_defination.append(defination.strip())
    prepare_csv_file(protein_accession,protein_goterm_list,protein_defination)
    df = pd.DataFrame(
        {
            'proteins': protein_accession, 'predictions': protein_goterm_list,
            'defination':protein_defination })
    print(df)
    df.to_pickle('ProteinDefinationUpdated.pkl')
    return df
    # input()
    # # print(len(goterm_list))


proteinDF= prepareAllGotermAnnotation()

# descriptionDF=importcsvAndStoreDf()
# for row in descriptionDF.iterrows():
#     print(row[0]) 
#     print(removePuntuationFromString(str(row[1])))
#     input()


