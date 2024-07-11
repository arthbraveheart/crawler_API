# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:33:36 2024

@author: ArthurRodrigues
"""
from getData import getBase, getData
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd



class Weapons:
    
    def __init__(self, target, data : getBase): 
        
        self.kvectors = Word2Vec.load('C:/Users/ArthurRodrigues/Codes/Pricing/pricing_pckg/report/abc.model').wv
        self.pipe     = data.pipe
        self.dataset  = data.dataset
        self.target   = target
        
        
    def sentence_over_sentence(self,sentence_1, sentence_2, similarity= None):
        
        return self.kvectors.n_similarity(sentence_1, sentence_2)

    
    def product(self,tokens):
        
        """
        cria um vetor que indica o Produto, 
        somando os vetores correspondentes de cada palavra
        que compõem o Título
        
        """
        p = 0
        for token in tokens:
            p+=self.trained.wv[token]
        return p  


    def sentence_over_vocab(self, sentence, similarity= None):
        
        """
        Compare a set of tolkens, not necessarily on the vocab, with all sets of tokens on the vocab of the model.
        In our case, we compare a product of another seller with the products of the model seller.
        
        """
        #n         = len(self.Mdl.product_tokens)
        vocab     = self.Mdl.product_tokens.tolist()
        adjacency = []
        for tolkenSet_vector in vocab:
            adjacency.append(self.kvectors.n_similarity(sentence,tolkenSet_vector))
        
        #for i in range(n):
            #adjacency.append(self.kvectors.n_similarity(sentence, next(vocab)))
        
        adjacency = np.array(adjacency, dtype=np.float16)
        
        if similarity is None:    
            return adjacency
        else:
            adjacency = (adjacency > similarity).astype(int)
            return adjacency
  
        
    def vocab_over_vocab(self, vocab_1, similarity= None):
        
        """
        idem to `sentence_over_vocab`, but we compare all the products of a seller with ours to get similarities.
        
        """
        
        adjacency = []
        for sentence in vocab_1:
            adjacency.append( self.sentence_over_vocab(sentence))
        
        adjacency = np.array(adjacency)
        
        if similarity is None:    
            return adjacency
        else:
            adjacency = (adjacency > similarity).astype(int)
            return adjacency

        
    def vector_over_vectors(self,  similarity= None):
        
        adjacency = cosine_similarity(self.Mdl.prod_vec)
        if similarity is None:    
            return adjacency
        else:
            adjacency = (adjacency > similarity).astype(int)
            return adjacency


    def Msentence_over_vocab(self, sentence, vocab, similarity= None):
        
        """
        Compare a set of tolkens, not necessarily on the vocab, with all sets of tokens on the vocab of the model.
        In our case, we compare a product of another seller with the products of the model seller.
        
        """
        n         = len(sentence)
        #vocab     = self.Mdl.product_tokens.tolist()
        adjacency = []
        for tolkenSet_vector in vocab:
            nn      = len(tolkenSet_vector) 
            matches = len(set(sentence)&set(tolkenSet_vector))
            similar = matches/(n-matches + nn-matches) * self.kvectors.n_similarity(sentence,tolkenSet_vector) # Jaccard Similarity
            adjacency.append(similar)
        
        #for i in range(n):
            #adjacency.append(self.kvectors.n_similarity(sentence, next(vocab)))
        
        adjacency = np.array(adjacency, dtype=np.float16)
        
        if similarity is None:    
            return adjacency
        else:
            adjacency = (adjacency > similarity).astype(int)
            return adjacency   

    def Mvocab_over_vocab(self, vocab_1, similarity= None):
        
        """
        idem to `sentence_over_vocab`, but we compare all the products of a seller with ours to get similarities.
        
        """
        
        adjacency = []
        for sentence in vocab_1:
            adjacency.append( self.Msentence_over_vocab(sentence))
        
        adjacency = np.array(adjacency)
        
        if similarity is None:    
            return adjacency
        else:
            adjacency = (adjacency > similarity).astype(int)
            return adjacency
    
    
    def _find(self, similarity= None):
        
        vocab_1 = self.target
        matches = []
        for sentence in vocab_1:
            q = self.pipe
            for i in range(4):
                qq       = q.iloc[:,i].drop_duplicates()
                comp     = self.Msentence_over_vocab(sentence,qq)
                
                if sum(comp)!=0:
                    #verificar matches iguais, ou seja, se no vetor _comp_ têm números iguais.
                    max_value= np.max(comp)
                    
                    if i>0:
                        idx = np.where(comp == max_value) 
                    else:
                        idx = np.argwhere(comp > 0)[0]  #selecionar os com o retorno maior do que 0 apenas pois se trata da Marca.
                    
                    if isinstance(qq.iloc[idx],pd.Series):
                        to_query = qq.iloc[idx] 
                    else:
                        to_query = tuple([qq.iloc[idx]])
                else:
                    to_query = tuple(list(qq))
                q = q.query(f"q_{i} in @to_query") 
            matches.append(to_query)
        
        return matches    
     
        
    def update_v(self,tolkens : list, target : str) -> np.array:
        
        """
        update the first tolken of tolkens (represents the product) into the
        same direction of the target (represents the EAN)
        
        """
        
        item =  self.product(tolkens)
        item_r = self.trained.wv[tolkens[1:]] 
        
        cc = self.rotate_to(item, target)
        self.trained.wv[tolkens[0]] = cc - item_r  #the first tolken to be updated
        
base = getBase('abc_f_ean')
target = (getData('CMattos').dataset).loc[:100,'product_tokens']        
weapons = Weapons(target,base)
new_match = weapons._find()       


