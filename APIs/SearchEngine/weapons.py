# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:33:36 2024

@author: ArthurRodrigues
"""
from enhance import Model
from getData import getData
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



class Weapons:
    
    def __init__(self,model : Model): 
        
        self.kvectors = model.model.wv
        self.Mdl      = model
        self.trained  = model.model
        
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


    def Msentence_over_vocab(self, sentence, similarity= None):
        
        """
        Compare a set of tolkens, not necessarily on the vocab, with all sets of tokens on the vocab of the model.
        In our case, we compare a product of another seller with the products of the model seller.
        
        """
        n         = len(sentence)
        vocab     = self.Mdl.product_tokens.tolist()
        adjacency = []
        for tolkenSet_vector in vocab:
            matches    = len(set(sentence)&set(tolkenSet_vector))
            similar = matches/n
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
    
    def update_v(self,tolkens : list, target : str) -> np.array:
        
        """
        update the first tolken of tolkens (represents the product) into the
        same direction of the target (represents the EAN)
        
        """
        
        item =  self.product(tolkens)
        item_r = self.trained.wv[tolkens[1:]] 
        
        cc = self.rotate_to(item, target)
        self.trained.wv[tolkens[0]] = cc - item_r  #the first tolken to be updated
        
        
       

