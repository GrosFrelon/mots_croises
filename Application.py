# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:48:49 2024

@author: letou
"""
import tkinter as tk
from FenetreMenu import FenetreMenu
from FenetreDefinitions import FenetreDefinitions
import subprocess
import sys

# Installer json lines avec la commande : pip install jsonlines

class Application():
    
    def __init__(self, root):
        self.root = root
        self.root.title("Application")
        self.hauteur =1
        self.largeur =1
        x_offset=0
        y_offset = 0
        self.root.geometry(f"{self.largeur}x{self.hauteur}+{x_offset}+{y_offset}")
        
        self.fMenu = FenetreMenu(self)
        self.Menu = True
        self.Def = False
        
    def show_menu(self):
        """
        Affiche le menu principal.
        Détruit la fenêtre de définition actuelle, s'il y en a une, et affiche la fenêtre du menu principal.
        """
        self.fDef.destroy()
        self.Def = False
        self.fMenu = FenetreMenu(self)
        self. Menu = True
        
    def show_def(self,  grille_complete, taille, nb_vie, nb_aide, cat):
        """
        Affiche la fenêtre des définitions.
        Args:
            grille_complete (list): La grille complète des mots.
            taille (int): La taille de la grille.
            nb_vie (int): Le nombre de vies restantes.
            nb_aide (int): Le nombre d'aides restantes.
            cat (str): La catégorie des mots.

        Détruit la fenêtre du menu principal et affiche la fenêtre des définitions avec les paramètres fournis.
        """
        self.fMenu.destroy()
        self.Menu = False
        self.fDef = FenetreDefinitions(app, grille_complete, taille, nb_vie, nb_aide, cat)
        self.Def = True
    
    def quitter(self):
        """
        Quitte l'application.
        Détruit toutes les fenêtres ouvertes et ferme l'application.
        """
        if self.Def:
            self.fDef.destroy()
        if self.Menu:
            self.fMenu.destroy()
        self.root.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
    