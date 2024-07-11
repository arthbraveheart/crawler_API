# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:32:22 2024

@author: ArthurRodrigues
"""

from unidecode import unidecode
import re




class Tokens:
    
    """
    Tokenization process
    
    """
    
    #def __init__(self, datasetClass : getData):
     #   self.dataset = datasetClass.dataset
    
    def simple(self,sentence):
        """
        pega somente os caracteres, sem espaço e alguns conectores, do Título dos produtos

        """
        processed = []
        for s in sentence:
            ss = re.split(r'\s+por\s+|\s+e\s+|\s+de\s+|\s+para\s+|\s+e\s+|\s+com\s+|\s+', unidecode(s.lower()).strip())
            processed.append( ss )
        return processed 
    
    

    