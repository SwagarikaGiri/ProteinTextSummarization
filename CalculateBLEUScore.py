from MakeProteinGotermList import importcsvAndStoreDf,prepareAllGotermAnnotation
from nltk.translate.bleu_score import sentence_bleu
import string
import pandas as pd

goaDF = pd.read_pickle('ProteinDefination.pkl')
goaDF = goaDF.set_index('proteins')
print(goaDF)
print(goaDF.loc['P31946','defination'])


def cleanAndSplitSentence(a_string):
    a_string=a_string.strip()
    new_string = a_string.translate(str.maketrans('', '', string.punctuation))
    return new_string.split()




def printBlueScores(reference,candidate):
    print('Individual 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
    print('Individual 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 1, 0, 0)))
    print('Individual 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 1, 0)))
    print('Individual 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 0, 1)))
    print('Individual 1-2-gram equal weight: %f' % sentence_bleu(reference, candidate, weights=(0.5, 0.5, 0, 0)))



reference1 = [
    'this is a dog'.split()
]


candidate1 = 'it is dog'.split()
# printBlueScores(reference1,candidate1)

reference_df = importcsvAndStoreDf()
# candidate_df = prepareAllGotermAnnotation()
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

for row in reference_df.iterrows():
    protein = row[0]
    print(protein)
    description = row[1][0]
    # print(str(description))
    refDescription = cleanAndSplitSentence(str(description))
    # print(refDescription)
    # print(goaDF.loc[str(row[0]),'defination'])
    predDescription=cleanAndSplitSentence(goaDF.loc[str(row[0]),'defination'])
    # print(predDescription)
    print("length of refDescription \t"+str(len(refDescription)))
    print("length of predDescription \t"+str(len(predDescription)))
    print("length of intersection \t"+str(len(intersection(refDescription,predDescription))))
    print(intersection(refDescription,predDescription))
    printBlueScores(refDescription,predDescription)
    printBlueScores(predDescription,refDescription)
    




  