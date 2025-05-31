# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:30:18 2024

@author: letou
"""
import tkinter as tk

class FenetreGrille(tk.Toplevel):
    def __init__(self, master, grille_complete, grille, controleur):
        
        super().__init__(master)
        self.grille_complete = grille_complete
        self.grille = grille
        self.controleur = controleur
        
        self.title("La grille")

        self.taille = int(self.winfo_screenheight()*0.9)   # Taille de la fenêtre carrée
        self.n = int(self.taille/len(self.grille))  # Taille d'une case de la grille
        
        # Détermination de la taille de la police en fonction de la taille de la grille
        self.font_size_numero = 120//len(self.grille)
        self.font_size = 240//len(self.grille)
        
         # Création du canevas pour afficher la grille
        self.canvas = tk.Canvas(self, width=self.taille, height=self.taille)
        self.canvas.pack()
        self.placement()
        self.afficher_grille()
    
    def placement(self):
        """
        Place la fenêtre de grille au centre de l'écran et 
        calcul la taille de la fenêtre en fonction de la taille de la grille complète.
        """

        # Calcul de la largeur et de la hauteur de la fenêtre en fonction de la taille de la grille complète
        self.largeur = self.n*(self.grille_complete.taille)
        self.hauteur = self.n*(self.grille_complete.taille)

        # Récupération des dimensions de l'écran
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()

        # Calcul des décalages pour centrer la fenêtre sur l'écran
        x_offset=largeur_ecran - self.largeur
        y_offset=0

        # Définition de la géométrie de la fenêtre pour la centrer sur l'écran
        self.geometry(f"{self.largeur}x{self.hauteur}+{x_offset}+{y_offset}")
        
        
    def afficher_numero(self):
        """
        Affiche les numéros des mots dans la grille.
        """
        
        les_mots = self.grille_complete.mots # Récupération de la liste des mots de la grille complète
        position_prise = [] # Liste pour garder une trace des positions déjà prises par les mots
        for mot in les_mots:
              decalage = self.n/6 # Calcul du décalage pour positionner le numéro à l'intérieur de la case
              (pos_x, pos_y) = self.controleur.position(position_prise, mot, self.n, decalage) # Calcul de la position (pos_x, pos_y) pour le numéro du mot
              texte = str(mot.numero)  # Conversion du numéro du mot en texte
              self.canvas.create_text(pos_x, pos_y, text=texte, fill = 'black', font=("Helvetica", self.font_size_numero)) # Création du texte du numéro à sa position sur le canevas
    
    def afficher_grille(self):
        """
        Affiche la grille sur le canevas.

        La méthode parcourt chaque élément de la grille et crée un rectangle correspondant sur le  canevas,
        avec la couleur appropriée en fonction de la valeur de la grille.
        Les éléments de la grille sont représentés comme suit :
        - 0 : un rectangle noir
        - 1 : un rectangle blanc
        - Autres valeurs : un rectangle blanc avec le texte en majuscules correspondant au contenu de la case.

         Returns:
            None
        """
        for i in range(len(self.grille_complete.grille)):
            for j in range(len(self.grille_complete.grille[0])):
                decalage= self.n/2 # Décalage pour le positionnement
                pos_x = j*self.n + decalage # Position en x du rectangle
                pos_y = i*self.n + decalage # Position en y du rectangle
                if self.grille_complete.grille[i][j] == 0: # Si la case de la grille complète est noire
                    self.canvas.create_rectangle(j * self.n, i * self.n, (j + 1) * self.n, (i + 1) * self.n, fill="black") # Création d'un rectangle noir
                else: 
                    if self.grille[i][j] == 0: # Si la case de la grille ne contient pas de lettres
                        self.canvas.create_rectangle(j * self.n, i * self.n, (j + 1) * self.n, (i + 1) * self.n, fill="black") # Création d'un rectangle noir
                    elif self.grille[i][j] == 1: # Si la case de la grille contient une lettre 
                        self.canvas.create_rectangle(j * self.n, i * self.n, (j + 1) * self.n, (i + 1) * self.n, fill="white") # Création d'un rectangle blanc
                    else: # Si la case de la grille contient autre chose qu'un simple 0 ou 1
                        self.canvas.create_rectangle(j * self.n, i * self.n, (j + 1) * self.n, (i + 1) * self.n, fill="white") # Création d'un rectangle blanc
                        texte = self.grille[i][j].upper() # Convertir le contenu de la case en majuscules
                        self.canvas.create_text(pos_x, pos_y, text=texte, fill="black", font=("Helvetica", self.font_size)) # Création du texte dans le canevas
        self.afficher_numero()
    
    def actualiser(self, grille):
        self.grille = grille
        self.afficher_grille()