# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:32:11 2024

@author: ArthurRodrigues
"""

import pandas as pd
from typing import Dict
from wrangling import Tokens
PATH = 'C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/'

class getData:
      
      """
      get a dataframe stored in a pickle file that contains information abaout products
      
      """
      
      def __init__(self, datasetName: str):
          
          self.dataset     = pd.read_pickle(PATH + datasetName + '.pkl')
          self._parsed() 

        
      def _checkTable(self):
          
          if isinstance(self.dataset,pd.core.frame.DataFrame):
             pass
          elif isinstance(self.dataset, Dict):
              self.dataset = pd.DataFrame.from_dict(self.dataset).copy()
          else:
              assert "Your pickle is not a table at all..."
      
      
      def _checkColumns(self):
          
          cols = self.dataset.columns
          if not 'EAN' in cols:
              shape = self.dataset.shape[0]
              self.dataset.loc[:'EAN'] = [ 0*i for i in range(shape) ]
          
          self.dataset = self.dataset.loc[:,['EAN','Nome','Seller', 'nameEncoded']]  
          
    
      def _checkDTypes(self):
          
          self.dataset = self.dataset.astype({'EAN':'int64', 'Nome':'string', 'Seller':'string'}).copy()
       
      
      def _checkIdx(self):
          
          self.dataset = self.dataset.reset_index().iloc[:,1:].copy()
       
      
      def _update(self):
          
          sentences = self.dataset.loc[:,'nameEncoded'].copy()
          self.dataset.loc[:,'product_tokens'] = Tokens().simple(sentences)
          
          return self.dataset


      def _parsed(self):
          
          self._checkTable()
          self._checkColumns()
          self._checkDTypes()
          self._checkIdx()
          return self._update()
          
          
          
          
          
          