# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:32:33 2024

@author: ArthurRodrigues
"""

from gensim.models import Word2Vec
from getData import getData
from guns import Guns
import numpy as np




class Model:
    
     def __init__(self, datasetClass : getData):
         
         self.dataset        = datasetClass.dataset
         self.product_tokens = self.dataset.loc[:,'product_tokens']
         self.model          = []
         self._trainIT()
         self._updateDataSet()
         self.prod_vec       = self._product_vectors()
         self.guns           = Guns()

     def _trainIT(self):
         
         """
         we have to conditionate this to update == 'train from the beggining' or 'add new vocabulary' 
         
         """
         
         self.model = Word2Vec(sentences= self.product_tokens, vector_size=100, window=10, min_count=1, workers=7, epochs=50)
         return self.model


     def _updateDataSet(self):
         
         self.dataset.loc[:,'product_vectors'] = [pv for pv in self._product_vectors()]
         return self.dataset


     def _product(self, sentence):
          
         """
         cria um vetor que indica o Produto, 
         somando os vetores correspondentes de cada palavra
         que compõem o Título em um index : idx
        
         """
        
         product = 0
         for token in sentence:
             product+=self.model.wv[token]
         return product  

        
     def _product_vectors(self):
         
         product_vec = np.array([\
                                     self._product(tokens)\
                                     for tokens in self.product_tokens\
                                    ])
         return product_vec

        
     def _update_v(self, tolkens : list, target : str) -> np.array:
         
         """
         update the first tolken of tolkens (represents the product) into the
         same direction of the target (represents the EAN)
         
         do the OPPOSITE. the target will be product (sum of tolken in a sentence)
         and the EAN will be moved.
         
         when EAN repeats, create a condition such mean or deviation. 
         
         """
         
         item      = self._product(tolkens[:-1])
         target_wv = self.model.wv[target] 
         
         cc = self.guns.rotate_to(target_wv, item)
         self.model.wv[target] = cc  #the first tolken to be updated   

        
     def _update_all(self):
         
         """
         Update all the vectors to make a back propagation
         
         """
         
         
         targets = [tolken[-1] for tolken in self.product_tokens.tolist()]
         
         mem_targets = []
         
         for tolkens, target in zip(self.product_tokens.tolist(), targets ):
             mem_targets.append(target)
             try:
                 if target in mem_targets[:-1]:
                     item      =  self._product(tolkens[:-1])
                     target_wv = self.model.wv[target] 
                     
                     cc = self.guns.rotate_to(target_wv, item)
                     self.model.wv[target] = 0.5*(cc + target_wv)  
                 else:
                     self._update_v(tolkens, target)
             except:
                 self._update_v(tolkens, target)
             
     def _trainITagain(self, cicles : int, update : bool = True):
         
         """
         we have to conditionate this to update == 'train from the beggining' or 'add new vocabulary' 
         
         """
         i=0
         if update:
             while i<=cicles:
                self._update_all() 
                self.model.train(self.product_tokens, total_examples = len(self.product_tokens), epochs = self.model.epochs)
                i+=1
         else:
             while i<=cicles:
                self.model.train(self.product_tokens, total_examples = len(self.product_tokens), epochs = self.model.epochs)
                i+=1
         return self.model        
             
         
         
#model = Model(getData('CMattos'))

       