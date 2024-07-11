# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:33:21 2024

@author: ArthurRodrigues
"""

from enhance import Model
from getData import getData
from weapons import Weapons
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

model = Model(getData('CMattos'))#Model(getData('ABC'))#Model(getData('abcCM')) #Model(getData('CMattos'))#Model(getData('abcCM')) #Model(getData('CMattos'))
#model._trainITagain(10)

def Compare(model):
    compare = []
    for p_v in model.prod_vec:
        compare.append(model.model.wv.cosine_similarities(p_v, model.prod_vec))
    return compare

#Compared = np.vstack(tuple(Compare(model)))

# Alternative way to compare and get the same result (the precision is a little bit different)

#Comp = cosine_similarity(model.prod_vec) # is equivalent to the matrix 'Compared'

# Conditional matches

#adj_mtrx = (Comp>0.999).astype(int) # if True shows 1, else shows 0 (Adjacency Matrix ?)

compare              = Weapons(model)
ABC                  = getData('ABC')#('Titles')
datasetABC           = ABC.dataset
datasetCM            = model.dataset
both                 = datasetCM.reset_index().merge(datasetABC.reset_index(), on='EAN')
both.loc[:,'match2'] = list(zip(list(both.index),both.loc[:,'index_x']))
#where1 = compare.sentence_over_sentence(['ducha', 'higienica', 'registro', 'gioia', '2195', 'cromada', 'tigre'], ['ducha', 'higienica', 'tigre', 'acquajet', 'gioia', 'cromado'])
#where2 = compare.sentence_over_vocab(['ducha', 'higienica', 'registro', 'gioia', '2195', 'cromada', 'tigre'])
#where3 = compare.sentence_over_vocab(['ducha', 'higienica', 'registro', 'gioia', '2195', 'cromada', 'tigre'], similarity = 0.9999)
#where4 = compare.sentence_over_sentence(['ducha', 'higienica', 'registro', 'gioia', '2195', 'cromada', 'tigre'], ['cabide', 'banheiro', 'docol', 'trip', 'cromado'])

# Basic Comparison

rand    = both.loc[:,'index_y']#np.random.randint(0,35996,100)
vec     = compare.Mvocab_over_vocab(datasetABC.loc[rand,'product_tokens']) #compare the first 100th products of ABC over CMattos
maxx    = np.argmax(vec, axis=0)
matches = list(enumerate(maxx)) #can we construct a networkx Graph?
correct = set(both.loc[:,'match2'])&set(matches)

# train again and compare
model._trainITagain(10)

#s2 = pd.Series([datasetCM.loc[matches[i][1],'product_tokens']  for i in range(1508)  ], name='CM')
#s1 = pd.Series([datasetABC.loc[matches[i][0],'product_tokens']  for i in range(1508)  ], name='ABC')

#tolkens_matched = pd.DataFrame([s1,s2])
