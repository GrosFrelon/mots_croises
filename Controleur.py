# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:44:05 2024

@author: Brico
"""
import random
from Grille import Grille
from Mot import Mot
from MotPositionne import MotPositionne

class Controleur:
    
    _slots_=['grille']
    
    def __init__(self, grille_remplie):
       self.grille_remplie = grille_remplie
       self.mots = grille_remplie.mots
       self.mots_places = [] #liste des mots déjà trouvé par l'utilisateur 
       
    
    def centrer_text(self, text, font_style, zone):

        largeur_text = font_style.measure(text)
        
        largeur_zone = zone.winfo_width()
        hauteur_zone = zone.winfo_height()
        
        largeur_caractere = font_style.measure(" ")
        hauteur_caractere = font_style.metrics("linespace") 
        
        nombre_pixels_largeur = (largeur_zone - largeur_text) // 2
        nombre_espaces = nombre_pixels_largeur//largeur_caractere
        
        nombre_pixel_hauteur = hauteur_zone/2
        nombre_saut_ligne = int(nombre_pixel_hauteur//hauteur_caractere)
        
        return(nombre_espaces, nombre_saut_ligne)
        
      
    def trier_mots(self, les_mots):
        """
        Trie les mots en fonction de leur orientation.
        Args:
            les_mots (list): Liste des objets MotPositionne à trier.
        Returns:
            dict: Dictionnaire contenant deux listes de mots triés, une pour les mots verticaux et une pour les mots horizontaux.
        """
        dico = {'verticaux': [],
                'horizontaux': []}
        for mot_positionne in les_mots:
            if mot_positionne.orientation == 'V':
                dico['verticaux'].append(mot_positionne)
            elif mot_positionne.orientation == 'H':
                dico['horizontaux'].append(mot_positionne)
        return(dico)
    
    def position(self, l, mot, n, decalage):
        """
        Détermine la position d'un mot sur la grille.
        Args:
            l (list): Liste des coordonnées des mots déjà placés sur la grille.
            mot (MotPositionne): Objet MotPositionne à placer sur la grille.
            n (int): Taille d'une case de la grille.
            decalage (int): Valeur de décalage entre les mots sur la grille.
        Returns:
            tuple: Coordonnées (pos_x, pos_y) du coin supérieur gauche du mot sur la grille.
        """
        pos_x = mot.ymin*n + decalage # Calcul de la position x du coin supérieur gauche du mot
        pos_y = mot.xmin*n + decalage
        if (mot.xmin, mot.ymin) in l: # Vérifie si les coordonnées du coin supérieur gauche du mot sont déjà occupées
            if mot.orientation == 'V':
                pos_y += n - 2*decalage # Décalage vertical pour éviter la superposition de mots
            else:
                pos_x += n - 2*decalage
        l.append((mot.xmin, mot.ymin))
        return(pos_x, pos_y)
       
       
    def execute_choix(self, mot) : 
        '''
        Cette fonction prend le mot rentré par le joueur en entrée et vérifie s'il existe dans la liste des mots valides. 
        Si le mot  est validé, il est ajouté à la liste des mots placés et la fonction retourne le mot et un indicateur de succès. 
        Sinon, elle ne retourne que False. 

        Args:
            mot (str): Le mot à vérifier.

        Returns:
            tuple: Un tuple contenant le mot validé et un booléen indiquant si l'opération a réussi.
                (mot_final (str), test (bool))
        '''
        test = False
        mot_final = ""
        mot = mot.lower()#tout en minuscule
        for mot_valide in self.mots:
            if mot_valide.mot == mot : #vérifie que le mot est bien dans la grille à trouver
                if mot not in self.mots_places : #vérifie que le mot n'est pas déjà placé
                    test = True
                    mot_final = mot_valide
                    self.mots_places.append(mot_final) 
        return(mot_final, test)
        
        
    
    def aide(self, grille, nb_aide):
        '''

        Cette fonction ajoute des lettres à la grille pour aider le joueur. 
        Si la grille est déjà complète ou si le nombre d'aides est épuisé, elle affiche un message correspondant.

        Args:
            grille (list): La grille actuelle du jeu.
            nb_aide (int): Le nombre d'aides restantes.

        Returns:
            tuple: Un tuple contenant la grille mise à jour et le nombre d'aides restantes.
                (grille (list), nb_aide (int))
        '''
        test = False
        # Vérifie si des mots restent à placer, si la grille n'est pas déjà remplie et s'il reste des aides disponibles
        if len(self.mots) != len(self.mots_places) and grille != self.grille_remplie.grille and nb_aide != 0:
            while not test:
                mot_aleatoire = random.choice(self.mots)
                if mot_aleatoire not in self.mots_places : # Vérifie si le mot dont proviendra l'aide sélectionné n'a pas déjà été placé
                # Liste des lignes et des colonnes possibles pour le mot
                    x_possible = list(range(mot_aleatoire.xmin, mot_aleatoire.xmax+1))
                    y_possible = list(range(mot_aleatoire.ymin, mot_aleatoire.ymax+1))
                    ligne_aleatoire = x_possible[random.randint(0, len(x_possible)-1)]
                    colonne_aleatoire = y_possible[random.randint(0, len(y_possible)-1)]
                    #ligne_aleatoire = random.randint(0, len(self.grille_remplie.grille)-1)
                    #colonne_aleatoire = random.randint(0, len(self.grille_remplie.grille[0])-1)
                    cas = grille[ligne_aleatoire][colonne_aleatoire]    #Vérifie si la case choisie est vide
                    if cas ==1:
                        grille[ligne_aleatoire][colonne_aleatoire]=self.grille_remplie.grille[ligne_aleatoire][colonne_aleatoire]
                        test = True
                        nb_aide = nb_aide - 1
        else:
            if grille == self.grille_remplie.grille:
                print('je peux pas aider, deja gagné')
            elif nb_aide==0:
                print("tu n'as plus d'aide, débrouille toi")
        return(grille, nb_aide)
                    
        
    
    def creer_grille_vide(self):
        '''
        La fonction retourne une grille remplie de 1 ou 0. 
        S'il y a un 1 c'est qu'une lettre doit être trouver, 
        tandis que le 0 correspond à une case noir.
    
        Returns :
            nouvelle_grille : liste de liste
        '''

        taille = self.grille_remplie.taille
        nouvelle_grille = [[0 for _ in range(taille)] for _ in range(taille)] #création d'une nouvelle grille vide
        for i in range(taille):
            for j in range(taille):
                if self.grille_remplie.grille[i][j] != 0 : #s'il n'y a pas de 0 dans la grille
                    nouvelle_grille[i][j] = 1 #c'est qu'il y a une lettre, donc on place un 1
                else:
                    nouvelle_grille[i][j] = 0 #sinon, c'est qu'il s'agit d'une case noir, on place donc un 0
        
        return nouvelle_grille

    # grille = Grille()
    # grille.remplir_grille()
    # grille.afficher_grille()
    # grille_vide = creer_grille_vide(grille)

    # Afficher la nouvelle grille
    # for ligne in grille_vide :
    #     print(ligne)

    def devoiler_mot(self,grille, mot):
        '''
    
        Cette fonction dévoile un mot entier sur la grille. 
    
        Args:
            grille (list): La grille actuelle du jeu sous forme de liste de listes.
            mot (Mot): Un objet représentant le mot à dévoiler, contenant ses coordonnées de départ, 
                       sa taille, son orientation, et le mot lui-même.
    
        Returns:
            None
        '''
        xmot = mot.xmin
        ymot = mot.ymin
        orientation = mot.orientation
        for i in range(mot.taille):
            grille[xmot][ymot] = mot.mot[i]
            if orientation =='V':
                xmot+=1
            elif orientation == 'H':
                ymot+=1  
        
        