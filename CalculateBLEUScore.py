from MakeProteinGotermList import importcsvAndStoreDf,prepareAllGotermAnnotation
from nltk.translate.bleu_score import sentence_bleu
import string
import pandas as pd

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


#importing pickle files
goaDF = pd.read_pickle('ProteinDefination.pkl')
goaDF = goaDF.set_index('proteins')



def cleanAndSplitStemming(a_string):
    a_string=a_string.strip()
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    # words = [word for word in new_string.split() if word.lower() not in sw_nltk]
    # print(words)
    words = [snowball.stem(word) for word in new_string.split() if word.lower() not in sw_nltk]
    # print(words)
    # input()
    # new_text = " ".join(words)
    return words

def cleanAndSplitSentence(a_string):
    a_string=a_string.strip()
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    return new_string.split()


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def printBlueScores(reference,candidate):
    print('Individual 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
    print('Individual 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 1, 0, 0)))
    print('Individual 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 1, 0)))
    print('Individual 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 0, 1)))
    print('Individual 1-2-gram equal weight: %f' % sentence_bleu(reference, candidate, weights=(0.5, 0.5, 0, 0)))


reference_df = importcsvAndStoreDf()

for row in reference_df.iterrows():
    protein = row[0]
    print(protein)
    description = row[1][0]
    refDescriptionStem = cleanAndSplitStemming(str(description))
    predDescriptionStem=cleanAndSplitStemming(goaDF.loc[str(row[0]),'defination'])
    refDescription = cleanAndSplitSentence(str(description))
    predDescription=cleanAndSplitSentence(goaDF.loc[str(row[0]),'defination'])
    # print("length of refDescription \t"+str(len(refDescription)))
    # print("length of predDescription \t"+str(len(predDescription)))
    # print("length of intersection \t"+str(len(intersection(refDescription,predDescription))))
    # print("length of refDescriptionStem \t"+str(len(refDescriptionStem)))
    # print("length of predDescriptionStem \t"+str(len(predDescriptionStem)))
    # print("length of intersectionStem \t"+str(len(intersection(refDescriptionStem,predDescriptionStem))))
    print("Intersection of normal sentence just removed the puntuation")
    print(intersection(refDescription,predDescription))
    print("Intersection of  sentence stemming and stopwords removed")
    print(intersection(refDescriptionStem,predDescriptionStem))
    print("Blue of sentence uniprot ref, goa pred")
    printBlueScores(refDescription,predDescription)
    print("Blue of sentence goa ref, uniprot pred ")
    printBlueScores(predDescription,refDescription)
    print("Blue of  Stemmed and removed stopwords sentence uniprot ref, goa pred")
    printBlueScores(refDescriptionStem,predDescriptionStem)
    print("Blue of Stemmed and removed stopwords sentence goa ref, uniprot pred ")
    printBlueScores(predDescriptionStem,refDescriptionStem)
    




  