# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:06:45 2024

@author: letou
"""
from Mot import Mot
import jsonlines
class MotPositionne():
    def __init__(self, mot, dico, x, y, orientation , numero, definition = '', categorie = ''):
        self.mot = mot
        self.taille = len(mot)
        self.numero = numero
        self.orientation = orientation
        self.xmin = x
        self.ymin = y
        if orientation == 'V': # Calcul des coordonnées maximales en fonction de l'orientation
            self.xmax = x + len(mot)-1
            self.ymax = y
        if orientation == 'H':
            self.xmax = x
            self.ymax = y + len(mot)-1
        if definition == '' or categorie == '':     # Si la définition ou la catégorie ne sont pas fournies, recherche dans le dictionnaire
            if mot in dico.keys():
                (self.definition, self.categorie) = dico[mot]
            else:
                self.categorie = None
                self.definition = None
        
    def __str__(self):
        """
        Return : str : Description du mot avec ses propriétés.
        """
        return(f"Le mot {self.mot} se définit comme {self.definition} de catégorie {self.categorie}. Propriétés: coordonnées {self.xmin,self.ymin}, orientation {self.orientation}, taille {self.taille} et numéro {self.numero}")


# data = 'DEM.jsonl'
# dico = {}        
# with jsonlines.open(data) as reader:
#       for row in reader:
#           dico[row['M']] = (row['SENS'], row['DOM']['nom'])
# mot1 = Mot('Bonjour', dico)
# print(mot1)
# mot2 = MotPositionne('bonjour', dico, 1, 1, 'V', 0)
# print(mot2)