# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:00:09 2024

@author: letou
"""

import tkinter as tk
from tkinter import ttk, font
import jsonlines
from Grille import Grille

class FenetreMenu(tk.Tk):
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root)
        
        super().__init__()
        self.fichier = 'DEM.jsonl'
        self.les_categories = ['all']
        self.creer_les_categories()
        self.variable_difficulte = {'Bébé' : {'taille_grille': 5, 'nb_vie' : 10, 'nb_aide' : 5},
                            'Débutant': {'taille_grille': 7, 'nb_vie' : 12, 'nb_aide' : 8},
                            'Intermédiaire' : {'taille_grille': 10, 'nb_vie' : 15, 'nb_aide' : 17},
                            'Difficile' : {'taille_grille': 15, 'nb_vie' : 20, 'nb_aide' : 20},
                            'Expert' : {'taille_grille': 20, 'nb_vie' : 30, 'nb_aide' : 30}
                           }
        
        self.title("Le mot croisé ultime - Menu")
        self.creer_widgets()
    
    def creer_widgets(self):
        self.font_name = "Helvetica"
        self.font_size = 16
        self.font_style = font.Font(family=self.font_name, size = self.font_size)
        
        # Titre
        self.label_titre = tk.Label(self, text="Le mot croisé ultime", font=("Helvetica", 24))
        self.label_titre.pack(pady=20)
        
        # Zone centrale pour les règles
        self.frame_regles = tk.Frame(self)
        self.frame_regles.pack(pady=20)
        
        self.label_regles = tk.Label(self.frame_regles, text="Règles du jeu :", font=(self.font_name, self.font_size))
        self.label_regles.pack(anchor="w")
        
        self.texte_regles = tk.Text(self.frame_regles,  wrap="word", height=15, width=75)
        self.texte_regles.pack()
        self.ecrire_regles()
        
        # Rendre la zone de texte en lecture seule
        self.texte_regles.config(state='disabled')
        
        # Frame pour les éléments en bas
        self.frame_bas = tk.Frame(self)
        self.frame_bas.pack(pady=20)
        
        # Menu déroulant pour la difficulté
        self.label_difficulte = tk.Label(self.frame_bas, text="Difficulté:")
        self.label_difficulte.grid(row=0, column=0, padx=5)
        
        self.difficulte = tk.StringVar()
        self.menu_difficulte = ttk.Combobox(self.frame_bas, textvariable=self.difficulte)
        self.menu_difficulte['values'] = list(self.variable_difficulte.keys())
        self.menu_difficulte.grid(row=0, column=1, padx=5)
        self.menu_difficulte.current(0)
        
        # Bouton Start
        self.bouton_start = tk.Button(self.frame_bas, text="Start", font=("Helvetica", 16), width=10, height=2)
        self.bouton_start.grid(row=0, column=2, padx=10, ipadx=10, ipady=5)
        self.bouton_start.bind("<Button-1>", self.jouer)
        
        # Menu déroulant pour la catégorie des mots
        self.label_categorie = tk.Label(self.frame_bas, text="Catégorie:")
        self.label_categorie.grid(row=0, column=3, padx=5)
        
        self.categorie = tk.StringVar()
        self.menu_categorie = ttk.Combobox(self.frame_bas, textvariable=self.categorie)
        self.menu_categorie['values'] = self.les_categories
        self.menu_categorie.grid(row=0, column=4, padx=5)
        self.menu_categorie.current(0)
        
        self.bouton_quitter = tk.Button(self, text = 'Quitter', command = self.app.quitter)
        self.bouton_quitter.pack()
        
        self.update_idletasks()
        self.largeur = self.winfo_reqwidth()
        self.hauteur = self.winfo_reqheight()
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()
        x_offset = (largeur_ecran - self.largeur) // 2
        y_offset = (hauteur_ecran - self.hauteur) // 2
        
        self.geometry(f"{self.largeur}x{self.hauteur}+{x_offset}+{y_offset}")
        
    def jouer(self, event):
        """
        Lance le jeu avec les paramètres sélectionnés par l'utilisateur.

        Cette fonction récupère les paramètres de difficulté et de catégorie sélectionnés
        par l'utilisateur, crée une nouvelle grille de jeu en fonction de ces paramètres,
        et affiche la fenêtre de définition avec les paramètres appropriés.

        Entrée :
        - self : référence à l'instance de la classe
        - event : l'événement déclencheur (ex. clic sur un bouton)

        Sortie : aucune
        """
        diff = self.menu_difficulte.get() # Récupérer la difficulté sélectionnée dans le menu
        cat = self.menu_categorie.get()  # Récupérer la catégorie sélectionnée dans le menu
        
        taille = self.variable_difficulte[diff]['taille_grille']  # Extraire la taille de la grille, le nombre de vies et le nombre d'aides pour la difficulté sélectionnée
        nb_vie = self.variable_difficulte[diff]['nb_vie']
        nb_aide = self.variable_difficulte[diff]['nb_aide']
        grille_complete = Grille(taille, cat) # Créer une nouvelle grille de jeu avec la taille et la catégorie sélectionnées
        
        self.app.show_def(grille_complete, taille, nb_vie, nb_aide, cat) # Afficher la fenêtre de définition avec les paramètres de la grille, le nombre de vies, d'aides et la catégorie
        
        
    def creer_les_categories(self):
        """
        créer des catégories de plus de 1000 mots à partir du dictionnaire. Permet de pouvoir choisir la categorie avec laquelle on veut jouer
        Entree : self : référence à l'instance de la classe
        Sortie : aucune
        """
        categories_nb_occurence = {}  # Initialiser un dictionnaire pour compter le nombre de mots dans chaque catégorie
        with jsonlines.open(self.fichier) as reader: # Ouvrir le fichier contenant les données des mots et leurs catégories
            for row in reader:  
                categorie = row['DOM']['nom'] # Extraire la catégorie de chaque ligne lue
                if categorie not in categories_nb_occurence.keys():# Ajouter ou incrémenter le compteur de la catégorie dans le dictionnaire
                    categories_nb_occurence[categorie]=1
                else:
                    categories_nb_occurence[categorie]+=1
                    
        for (categorie, nb_occurence) in categories_nb_occurence.items(): # Parcourir le dictionnaire des catégories et leurs occurrences
            if nb_occurence > 1000:   #oblige chaque catégorie à avoir un minimum de mot
                self.les_categories.append(categorie)
    
    
    
    def ecrire_regles(self):
        text = "Bienvenue sur votre nouveau jeu de mots croisés !"
        text += "\n"
        text += "Avant d'appuyez sur Start, vous pouvez choisir la catégorie. Il n'est pas assuré que la totalité des mots la respectent mais si ce n'est pas le cas, l'autre catégorie sera précisée. Choisissez aussi la difficulté !"
        text += "\n"
        text += "Appuyez sur Start et c'est parti ! Lisez les définitions et prenez connaissance de la grille !"
        text += "\n"
        text += "Sous la liste de définitions, une case vous permez de rentrer les mots devinés. Appuyez sur valider, ou sur votre touche entrée pour confirmer."
        text += "\n"
        text += "Si le mot est dans la grille : il s'affiche. Sinon, vous perdez une vie."
        text += "\n"
        text += "Vous avez un nombre limité d'indices, qui affichent une lettre de manière aléatoire sur la grille."
        text += "\n"
        text += "Le nombre de vies, d'indices et la taille de la grille dépendent de la difficulté choisie (mais pas la difficulté des mots)."
        text += "\n"
        text += "ATTENTION : Certains mots sont peu courants, vous risquez de perdre fréquemment, à vos risques et périls..."
        self.texte_regles.insert(tk.END, text)

if __name__ == "__main__":
    app = FenetreMenu()
    app.mainloop()
