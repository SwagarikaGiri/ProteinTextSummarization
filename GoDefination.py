# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 10:58:39 2022

@author: swaga
"""
import pandas as pd
import csv
def get_gene_ontology(filename='go.obo'):
    # Reading Gene Ontology from OBO Formatted file
    go = dict()
    obj = None
    with open( filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == '[Term]':
                if obj is not None:
                    go[obj['id']] = obj
                obj = dict()
                obj['is_a'] = list()
                obj['part_of'] = list()
                obj['regulates'] = list()
                obj['is_obsolete'] = False
                continue
            elif line == '[Typedef]':
                obj = None
            else:
                if obj is None:
                    continue
                l = line.split(": ")
                if l[0] == 'id':
                    obj['id'] = l[1]
                elif l[0]=='def':
                    obj['def']= l[1]
                elif l[0] == 'is_a':
                    obj['is_a'].append(l[1].split(' ! ')[0])
                elif l[0] == 'name':
                    obj['name'] = l[1]
                elif l[0] == 'is_obsolete' and l[1] == 'true':
                    obj['is_obsolete'] = True
    if obj is not None:
        go[obj['id']] = obj
    # for go_id in go.keys():
    #     if go[go_id]['is_obsolete']:
    #         del go[go_id]
    for go_id, val in go.items():
        if 'children' not in val:
            val['children'] = set()
        for p_id in val['is_a']:
            if p_id in go:
                if 'children' not in go[p_id]:
                    go[p_id]['children'] = set()
                go[p_id]['children'].add(go_id)
    return go

# gene_ontology= get_gene_ontology()
# go_term = gene_ontology['GO:0000001']
# print(go_term['def'])
# go_dataframe = pd.DataFrame.from_dict(gene_ontology)
# print(go_dataframe)
# go_dataframe.to_csv('go-dataframe.csv')
# filename = 'go-1-dataframe.csv'
# with open(filename, 'w') as f:
#     w = csv.writer(f)
#     for k,v in gene_ontology.items():
#         print(k)
#         print(v['def'])
#         # input()
#         w.writerow([k, v['def']])

