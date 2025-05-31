# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:41:44 2024

@author: letou
"""
import jsonlines

data = 'DEM.jsonl' # Nom du fichier de données JSONL
dico = {} # Dictionnaire pour stocker les données du fichier JSONL
with jsonlines.open(data) as reader: # Lecture du fichier JSONL et remplissage du dictionnaire
     for row in reader:
         dico[row['M']] = (row['SENS'], row['DOM']['nom'])
         
class Mot:
    
    def __init__(self, mot, dico, definition = '', categorie = ''):
        self.mot = mot
        self.taille = len(mot)
        if definition == '' or categorie == '':    #recherche dans la base de donnée si on lui donne pas en entrée
            if mot in dico.keys():
                (self.definition, self.categorie) = dico[mot]
            else:
                self.categorie = None
                self.definition = None
        else:
            self.categorie = categorie
            self.definition = definition
        
    def __str__(self):
        """
        Return : str : Description du mot avec sa définition et sa catégorie.
        """
        return(f"{self.mot} se définit comme {self.definition} et appartient à la catégorie {self.categorie}")

# mot = Mot('bonjour',dico)
# mot1 = Mot('bonjour', dico)
# mot = Mot('bonjour',dico)
# print(mot)
# mot1 = Mot('bonjour', dico, 'yo', 'salutaion')
# print(mot1)

#va plus vite car calcul le dico qu'une seule fois