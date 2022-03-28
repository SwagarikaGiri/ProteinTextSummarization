import pickle
import numpy as np
import pandas as pd
import csv
import string
from nltk.translate.bleu_score import sentence_bleu

import matplotlib.pyplot as plt


#natural language processing packages
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
porter = PorterStemmer()
lancaster=LancasterStemmer()
from nltk.stem import SnowballStemmer
snowball = SnowballStemmer(language='english')


def oneGramBleuScore(reference,candidate):
    return sentence_bleu(reference, candidate, weights=(1, 0, 0, 0))


def twoGramBleuScore(reference,candidate):
    return sentence_bleu(reference, candidate, weights=(0, 1, 0, 0))

def intersection(lst1, lst2):
    result = list(set(lst1) & set(lst2))
    return result
    
def makeString(list):
    return " ".join(list)


def plotGraph(ref,pred,xlabel,ylabel,imagename):
    xpoints = np.array(ref)
    ypoints = np.array(pred)
    fig = plt.figure()
    plt.ylim(min(ref+pred)-0.01,max(ref+pred)+0.01)
    plt.xlim(min(ref+pred)-0.01,max(ref+pred)+0.01)
    plt.plot(xpoints, ypoints, 'o')
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    xpoints = ypoints = plt.xlim()
    plt.plot(xpoints, ypoints, linestyle='--', color='k', lw=3, scalex=False, scaley=False)
    fig.savefig(str(imagename)+".jpg")
    plt.show()

def stemmingRemoveStopWords(a_string):
    a_string=a_string.strip()
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    words = [snowball.stem(word) for word in new_string.split() if word.lower() not in sw_nltk]
    return words


def removeStopWords(a_string):
    a_string=a_string.strip()
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    words = [word for word in new_string.split() if word.lower() not in sw_nltk]
    return words

def importCsvFile(filename):
    data = pd.read_csv(filename, index_col=0)
    data = data[['GO Description','Uniprot Description']]
    return data


def makeResultsFile(data):
    print(data)
    proteinList=[]
    uniprotAsRefGoaAsPred=[]
    goaAsRefUniprotasPred=[]
    uniprotAsRefGoaAsPredStem=[]
    goaAsRefUniprotasPredStem=[]
    with open('ResultBlueSvore.csv','w' ,newline='', encoding='utf-8') as output_csvfile:
        spamwriter = csv.writer(output_csvfile, delimiter=',')
        list_=[]
        list_.extend(['protein','length of Uniprot description', 'length of Goa description','length of intersection','intersection','One gram bleu score'])
        spamwriter.writerow(list_)
        for index,row in data.iterrows():
            print(index)
            list_=[]
            try:
                goaDescriptionCleaned= stemmingRemoveStopWords(row[0])
                uniProtDescriptionCleaned= stemmingRemoveStopWords(row[1])
                goaDescription= removeStopWords(row[0])
                uniProtDescription= removeStopWords(row[1])
                proteinList.append(index)
                uniprotAsRefGoaAsPred.append(oneGramBleuScore(uniProtDescription,goaDescription))
                goaAsRefUniprotasPred.append(oneGramBleuScore(goaDescription,uniProtDescription))
                uniprotAsRefGoaAsPredStem.append(oneGramBleuScore(uniProtDescriptionCleaned,goaDescriptionCleaned))
                goaAsRefUniprotasPredStem.append(oneGramBleuScore(goaDescriptionCleaned,uniProtDescriptionCleaned))
                list_=[index,len(uniProtDescriptionCleaned),len(goaDescriptionCleaned),len(intersection(uniProtDescriptionCleaned,goaDescriptionCleaned)),makeString(intersection(uniProtDescriptionCleaned,goaDescriptionCleaned)),oneGramBleuScore(goaDescriptionCleaned,uniProtDescriptionCleaned)]
                print(list_)
                spamwriter.writerow(list_)

            except:
                pass
    plotGraph(uniprotAsRefGoaAsPred,uniprotAsRefGoaAsPredStem,"uniprotAsRefGoaAsPred","uniprotAsRefGoaAsPredStem",'Uniprot As Ref Goa As Pred')
    plotGraph(goaAsRefUniprotasPred,goaAsRefUniprotasPredStem,"goaAsRefUniprotasPred","goaAsRefUniprotasPredStem",'Goa As Ref Uniprot as Pred')
    plotGraph(uniprotAsRefGoaAsPredStem,goaAsRefUniprotasPredStem,"uniprotAsRefGoaAsPredStem","goaAsRefUniprotasPredStem",'Uniprot as Ref vs Goa as Ref')


    




def main():
    # proteinList=[]
    # uniprotAsRefGoaAsPred=[]
    # goaAsRefUniprotasPred=[]
    # uniprotAsRefGoaAsPredStem=[]
    # goaAsRefUniprotasPredStem=[]
    filename='ProteinAndItsDescriptionCombined.csv'
    data = importCsvFile(filename)
    data = data.head(300)
    makeResultsFile(data)
    # for index,row in data.iterrows():
    #     print(index)
    #     try:
    #         goaDescriptionCleaned= stemmingRemoveStopWords(row[0])
    #         uniProtDescriptionCleaned= stemmingRemoveStopWords(row[1])
    #         goaDescription= removeStopWords(row[0])
    #         uniProtDescription= removeStopWords(row[1])
    #         proteinList.append(index)
    #         uniprotAsRefGoaAsPred.append(oneGramBleuScore(uniProtDescription,goaDescription))
    #         goaAsRefUniprotasPred.append(oneGramBleuScore(goaDescription,uniProtDescription))
    #         uniprotAsRefGoaAsPredStem.append(oneGramBleuScore(uniProtDescriptionCleaned,goaDescriptionCleaned))
    #         goaAsRefUniprotasPredStem.append(oneGramBleuScore(goaDescriptionCleaned,uniProtDescriptionCleaned))
    #     except:
    #         pass

    # plotGraph(uniprotAsRefGoaAsPred,uniprotAsRefGoaAsPredStem,"uniprotAsRefGoaAsPred","uniprotAsRefGoaAsPredStem",'Uniprot As Ref Goa As Pred')
    # plotGraph(goaAsRefUniprotasPred,goaAsRefUniprotasPredStem,"goaAsRefUniprotasPred","goaAsRefUniprotasPredStem",'Goa As Ref Uniprot as Pred')




if __name__ == "__main__":
    main()