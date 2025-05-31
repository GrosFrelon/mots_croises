# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:52:12 2024

@author: letou
"""

import jsonlines  #pip install jsonlines
from Mot import Mot
from MotPositionne import MotPositionne
import random

class Grille:
    
    def __init__(self, taille = 10, categorie = 'all'):
        self.ma_categorie = categorie
        self.taille = taille
        self.fichier = 'DEM.jsonl'
        self.iteration = 20000   #nombre de mots d'une catégorie testé avant de prendre toutes les catégories
        
        self.points_possibles = {'H':[], 'V':[]}  # {'H' : [(x1,y1), (x2,y2)], 'V' : [(x3,y3)], (x4,y4)}
        #représente les positions (x,y) où l'on peut ajouter un mot d'orientation vertical 'V' ou horizontal 'H'
        self.mots = []  # liste des mots positionnes 
        self.les_categories = []  # liste des catégories 
        self.creer_les_categories()
        self.grille = []  # la grille finale, liste 2D avec grille[x][y] pour la case de coordonnée (x,y)
        self.creer_grille_vide()
        self.donnees = {}  #{'mot' : 'définition', 'catégorie'}
        self.importer_donnees()
        self.dico = {}    #{1 : 'sport' : [mot1, mot2], 'sociologie' : [mot3], 2 : 'sport' : [mot4], ...}
        self.créer_dico()
        
        self.remplir_grille()
      
    def creer_les_categories(self):
        """
        Crée une liste des catégories à partir du fichier de données JSONL.
        Parcourt le fichier JSONL et ajoute chaque catégorie rencontrée à la liste `les_categories`.
        """ 
        with jsonlines.open(self.fichier) as reader: 
            for row in reader:
                categorie = row['DOM']['nom']
                if categorie not in self.les_categories:
                    self.les_categories.append(categorie)
    
    def créer_dico(self):
        """
        Crée un dictionnaire de mots à partir du fichier de données JSONL.
        Parcourt le fichier JSONL et crée un dictionnaire contenant les mots triés par longueur et par catégorie.
        """
        # {3 : [{'mot' : 'ane', définition : 'sorte de cheval', type : 'animal'}, ...], 2 : {'je' : }
        with jsonlines.open(self.fichier) as reader: 
            for row in reader:
                if ' ' not in row['M']:  #des mots sans espaces
                    mot = Mot(row['M'], self.donnees, row['SENS'], row['DOM']['nom'])
                    nb_lettre = len(row['M'])
                    categorie = mot.categorie
                    if row.get('no',1) == 1:  #si le mot est bien le sens premier
                        if 't' not in row['DOM']['code'] and 'v' not in row['DOM']['code']: #si ce n'est pas un mot litéraire ou de vieux français
                            if nb_lettre in self.dico.keys():
                                if categorie in self.dico[nb_lettre].keys():
                                    self.dico[nb_lettre][categorie].append(mot)
                                else :
                                    self.dico[nb_lettre][categorie] = [mot]
                            else:
                                self.dico[nb_lettre] = {categorie : [mot]}
            

    def importer_donnees(self):      
        with jsonlines.open(self.fichier) as reader:
             for row in reader:
                 self.donnees[row['M']] = (row['SENS'], row['DOM']['nom'])
    
    def remplir_grille(self):
        '''
        Fonction qui englobe les autres fonctions afin de créer la grille
        '''
        
        orientation = "H"
        if random.random()<0.5:
            orientation = 'V'
        points_positionnes = self.positionner_premier_mot(orientation) #ajoute le premier mot
        self.points_possibles[self.autre_orientation(orientation)].extend(points_positionnes) #ajoute les positions du mot dans les cases possibles
        i = 1
        #tant qu'il y a des points possibles 
        while (len(self.points_possibles['H']) != 0 or len(self.points_possibles['V']) != 0):
            (position, orientation) = self.donne_point() #on prend un point au hasard
            les_cases = self.cases_possibles(position, orientation)  #on donne les cases ou l'on pourrait mettre un mot
            ((x_max, y_max), (xfixe, yfixe)) =  self.tri_cases(position, les_cases, orientation) #on trie ces posisitions pour qu'elles soient viables
            if len(les_cases) != 0:  #si il reste des position posibles pour le point
                (mot_choisi, (xmot,ymot))=self.trouver_mot(les_cases, orientation, (xfixe,yfixe), (x_max, y_max))  #on trouve un mot
                self.ajouter_mot(mot_choisi, xmot, ymot, les_cases, orientation, position, i) #on l'ajoute à la grille, à la liste des mots et à la liste des points possibles
                self.actualiser_points_possible((xfixe,yfixe), orientation)  #on actualise les points possibles pour l'ancien mot, ou est ce que je ne peux plus mettre
                self.actualiser_points_possible((xfixe,yfixe), self.autre_orientation(orientation))  #pareil pour le nouveau mot
                i+=1
            elif len(les_cases) == 0 and len(self.points_possibles) != 0: #Si il y a aucunes cases de viables 
                self.points_possibles[orientation].remove(position)
            
    def positionner_premier_mot(self, orientation):
        '''
        Positionne un premier mot sur la grille aléatoirement
        Parameters
        ----------
        orientation : String
            'V' : Vertical, 'H' : Horizontal
        Returns
        -------
        Points_positionnes : List de doublet
            les doublet (x,y) des lettres positionnes du mot
        '''
        test = False
        i=0
        while not test:
            categorie = self.ma_categorie
            if i>self.iteration:
               categorie='all' 
            taille = random.randint(4,self.taille)
            cat = self.donner_categorie(taille, categorie)
            if cat:
                mot = self.dico[taille][cat][random.randint(0, len(self.dico[taille][cat])-1)] 
                x = random.randint(0,self.taille-1)
                y = random.randint(0,self.taille-1)
                if orientation == 'V':
                    if x + mot.taille <= self.taille:
                        test = True
                if orientation == 'H':
                    if y + mot.taille <= self.taille:
                        test = True
            i+=1
        points_positionnes = []
        if orientation == 'V':
            i = x
            for lettre in mot.mot:
                self.grille[i][y] = lettre
                points_positionnes.append((i,y))
                i+=1 
        if orientation == 'H':
            i = y
            for lettre in mot.mot:
                self.grille[x][i] = lettre
                points_positionnes.append((x,i))
                i+=1 
        self.mots.append(MotPositionne(mot.mot, self.donnees, x, y, orientation, 0))
        return(points_positionnes)
    
    def autre_orientation(self,orientation):
        if orientation == 'V':
            r = 'H'
        elif orientation == 'H':
            r = 'V'
        return(r)
    
    def cases_possibles(self, position, direction):
        '''
        Parameters
        ----------
        possition : (x,y) de l'intersection
        orientation : 'H', 'V'
        Returns
        -------
        les_cases = [(x1,y1), (x2,y2), ...] les positions possibles pour mettre des mots
        Ce sont toutes les coordonées disponible pour mettre un mot avant de rencontrer un obstacle
        Par exemple si le mot à mettre est vertical, on enregistre toutes les position au dessus
        de la case position jusqu'à rencontrer un mot, pareil en dessous.
        
        Fonction principalement créée par Chat GPT (90%)
        '''
        grid = self.grille
        (start_row, start_col) = position
        cells_with_no_neighbors = []
        num_rows = len(grid)
        num_cols = len(grid[0])

        # Définir les pas pour la direction choisie
        if direction == 'H':  # Horizontal
            dr, dc = 0, 1
        elif direction == 'V':  # Vertical
            dr, dc = 1, 0
        else:
            raise ValueError("Direction non valide. Utilisez 'H' pour horizontal ou 'V' pour vertical.")

        # Vérifier les voisins de la case initiale
        if direction == 'V':
            for dr_voisin in [-1, 1]:
                r = start_row + dr_voisin
                c = start_col
                if 0 <= r < num_rows and 0 <= c < num_cols and grid[r][c] != 0:
                    has_neighbors = True
                    break
            else:
                if grid[start_row][start_col] != 0:
                    cells_with_no_neighbors.append((start_row, start_col))
        elif direction == 'H':
            for dc_voisin in [-1, 1]:
                r = start_row 
                c = start_col + dc_voisin
                if 0 <= r < num_rows and 0 <= c < num_cols and grid[r][c] != 0:
                    has_neighbors = True
                    break
            else:
                if grid[start_row][start_col] != 0:
                    cells_with_no_neighbors.append((start_row, start_col))

        # Parcourir la grille à partir de la case initiale dans les deux sens dans la direction spécifiée
        for step in [-1, 1]:  # Pour explorer dans les deux sens
            row, col = start_row, start_col
            distance = 0
            while 0 <= row < num_rows and 0 <= col < num_cols:
                if (row != start_row or col != start_col) and grid[row][col] == 0:
                    has_neighbors = False

                    # Vérifier tous les voisins
                    for dr_neighbor, dc_neighbor in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        r = row + dr_neighbor
                        c = col + dc_neighbor
                        if 0 <= r < num_rows and 0 <= c < num_cols and grid[r][c] != 0:
                            if not (r == start_row and c == start_col):  # Vérifier si ce n'est pas la case initiale
                                has_neighbors = True
                                break

                    if not has_neighbors:
                        cells_with_no_neighbors.append((row, col))
                    else:
                        break  # Arrêter d'explorer dans cette direction si une case avec un voisin est rencontrée

                distance += 1
                row, col = start_row + distance * step * dr, start_col + distance * step * dc

        return cells_with_no_neighbors
                    
    
    def donne_point(self):
        '''
        Donne un point aléatoire dans la liste de tous les points possibles, avec son orientaion
        Returns
        -------
        ((x,y), orientation)
        '''
        orientation = ''
        if len(self.points_possibles['H']) != 0:
            indice = random.randint(0, len(self.points_possibles['H'])-1)
            point = self.points_possibles['H'][indice]
            orientation = 'H'
        elif len(self.points_possibles['V']) != 0:
            indice = random.randint(0, len(self.points_possibles['V'])-1)
            point = self.points_possibles['V'][indice]
            orientation = 'V'
        else:
            point = None
            orientation = None
        return(point, orientation)
    
    def tri_cases(self, position, les_cases, orientation):
        '''
        Trie la liste cases afin qu'il ne reste que les cases viable pour positionner la première lettre
        Le mot posisionnée aura la place de faire 4 ou plus lettres
        On vérifie aussi que sa première lettre ne sera pas possionnée en dessous de l'intersection'
        
        Parameters
        ----------
        possition : (x,y)
        les_cases
        
        Returns
        -------
        position :(x,y) coordonées da la case de croissement entre les 2 mots
        (x_max, y_max) : coordonées de la case de la dernière lettre du mot possible
        
        '''
        (xfixe, yfixe) = position
        (x_max, y_max) = (xfixe, yfixe)
        for (x,y) in les_cases:
            if x>x_max:
                x_max = x
            if y>y_max:
                y_max = y
        if orientation == 'V':
            x_min = x_max - 3 #pour avoir des mots d'au moins 4 lettres
            if x_min>xfixe:  #pour que la première lettre du futur mot soit de toute façon au dessus du mot
                x_min = xfixe
            for i in range(len(les_cases)-1,-1,-1):
                (x,y) = les_cases[i]
                if x > x_min:
                    les_cases.pop(i)  #on enlève les cases non viables
        elif orientation == 'H':
            y_min = y_max - 3
            if y_min>yfixe:
                y_min = yfixe
            for i in range(len(les_cases)-1,-1,-1):
                (x,y) = les_cases[i]
                if y > y_min:
                    les_cases.pop(i)
        return((x_max, y_max), position)
   
    def trouver_mot(self, les_cases, orientation, position, position_max):
        '''
        Parameters
        ----------
        les_cases_triées
        orientation du mot
        position (x, y) de l'intersection entre les mots
        position (xmax, ymax) de la dernière lettre
        
        Returns
        -------
        mot : TYPE Mot
        position : (x,y)
        '''
        trouve = False
        (xfixe, yfixe) = position
        (xmax, ymax) = position_max
        i=0
        while not trouve:
                (x,y) = random.choice(les_cases)
                i+=1
                categorie = self.ma_categorie
                if i > self.iteration:
                    categorie = 'all'
                (mot, trouve) = self.chercher_mot(orientation, categorie, (xmax, ymax), (xfixe,yfixe), (x,y))
        return(mot, (x,y))
    
    def chercher_mot(self, orientation, categorie, coord_max, coord_fixe, coord_mot):
        '''
        Fonction qui cherche un mot adapté à la lettre à l'intetersection, qui respecte les critères
        de taille et de la catégorie.
        
        '''
        (xfixe,yfixe) = coord_fixe
        (x,y) = coord_mot
        (xmax, ymax) = coord_max
        trouve = False
        mot_choisi = ''
        if orientation == 'V':
            indice_intersection = xfixe-x
            taille_max = xmax-x+1  #la taille maximal possible du mot pour un x aléatoire dans les cases
            taille_min = xfixe-x+1 if xfixe-x+1 > 3 else 4  #la taille minimal pour relier la première lettre du mot et l'intersection avec le mot déjà en place de coordonnées (xfixe, yfixe) 
        elif orientation =='H':
            indice_intersection = yfixe-y
            taille_max = ymax-y+1
            taille_min = yfixe-y+1 if yfixe-y+1 > 3 else 4
        
        if taille_max>=4:  #on fixe une taille min, il faut que le mot soit suffisamment long
            taille_possibles = list(range(taille_min,taille_max+1))
            taille_choisi = random.choice(taille_possibles)  #une taille aléatoire
            cat_choisi = self.donner_categorie(taille_choisi, categorie)  # la catégorie
            if cat_choisi:
                indice = random.randint(0,len(self.dico[taille_choisi][cat_choisi])-1) 
                mot_choisi = self.dico[taille_choisi][cat_choisi][indice]  #un mot aléatoire à partir de la catégorie et de la taille
                if self.grille[xfixe][yfixe] == mot_choisi.mot[indice_intersection] :  #si ils ont la même lettre à l'intersection
                    mot_deja_mis = False
                    for mots in self.mots:
                         if mot_choisi.mot == mots.mot: #si ce mot est déjà utilisé dans la grille
                             mot_deja_mis = True
                    if not mot_deja_mis:
                        trouve = True
        return(mot_choisi, trouve)
    
    
    def donner_categorie(self, taille, categorie_souhaite):
        '''
        Fonction qui retourne n'importe quelle catégorie si 'all' est séléctionné
        Elle retourne la catégorie souhaité si il existe un mot de la taille souhaité de cette catégorie
        None sinon
        '''
        categorie = None
        if categorie_souhaite == 'all':
            cat_possible = list(self.dico[taille].keys()) # toutes les catégories associées à une taille
            categorie = random.choice(cat_possible)
        elif categorie_souhaite in self.les_categories:
            if self.dico[taille].get(categorie_souhaite, 0) != 0:  #si il y a la catégorie pour une taille donnée
                categorie = categorie_souhaite
        return(categorie)
        
        
    
    def ajouter_mot(self, mot_choisi, xmot, ymot, les_cases, orientation, position, indice):
        '''
        Ajoute les lettre du mot dans la grille, dans la liste les_mots, comme type MotPositionne
        et ses coordonnées dans les points possibles
        Parameters
        ----------
        orientation : string ('V' ou 'H')
        mot : Mot
        position : (x,y)
        Returns
        ---------
        mot : MotPositionne
        '''
        if mot_choisi is not None:
            mot = MotPositionne(mot_choisi.mot, self.donnees, xmot, ymot, orientation, indice)
            self.mots.append(mot)
            for i in range(mot.taille):
                self.grille[xmot][ymot] = mot.mot[i]
                self.points_possibles[self.autre_orientation(orientation)].append((xmot,ymot))
                if orientation =='V':
                    xmot+=1
                elif orientation == 'H':
                    ymot+=1
            
        
    def actualiser_points_possible(self, point, orientation):
        '''
        Supprime les points anciennement possible
        Parameters
        ----------
        point : (x,y) lettre à partir duquel on a ajouté le mot
        orientation
        '''
        (xp,yp) = point
        indices = []
        if orientation == 'V':
            for i in range(len(self.points_possibles['V'])-1):
                (x,y) = self.points_possibles['V'][i]
                if x==xp and (y==yp or y==yp+1 or y==yp-1):  #on supprime le point utilisé et les points voisins pour ne pas avoir 2 mots cote à cote
                    indices.append(i)
            indices_inverse = indices[::-1]  #pour ne pas décaler les indices, on supprime d'abord les mots avec les indices les plus grand
            for i in indices_inverse:
                self.points_possibles['V'].pop(i)
        if orientation == 'H':
            for i in range(len(self.points_possibles['H'])-1):
                (x,y) = self.points_possibles['H'][i]
                if y==yp and (x==xp or x==xp+1 or x==xp-1): 
                    indices.append(i)
            indices_inverse = indices[::-1]
            for i in indices_inverse:
                self.points_possibles['H'].pop(i)
        
    
    def afficher_grille(self):
        ''' 
        permet d'afficher la grille proprement dans la console
        '''
        
        temp_grid = [[0] * len(self.grille) for _ in range(len(self.grille))]
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if self.grille[i][j] == 0:
                    temp_grid[i][j] = ' '
                else:
                    temp_grid[i][j] = self.grille[i][j]
            print(temp_grid[i])

            
    def creer_grille_vide(self): 
        ''' 
        créer la grille vide à partir de la taille
        '''
        nombre_case = self.taille
        for j in range (nombre_case):
                self.grille.append([0]*nombre_case)

if __name__ == "__main__":
    grille = Grille(10, 'chimie')
    grille.afficher_grille()
    print(grille.points_possibles)
    for mot in grille.mots:    
        print(mot)
    
           

           
         