"""
Created on Sat Jun  1 18:30:18 2024

@author: letou
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from Controleur import Controleur
from FenetreGrille import FenetreGrille


class FenetreDefinitions(tk.Tk):
    def __init__(self, app, grille_complete, taille, nb_vie, nb_aide, cat):
        self.app = app
        super().__init__()

        self.taille = taille
        self.nb_vie = nb_vie
        self.nb_aide = nb_aide
        self.categorie = cat
        self.messagebox_open = False
        self.reponse = False
        
        # Création de la grille vide et de la fenêtre de la grille
        self.grille_complete = grille_complete
        self.controleur = Controleur(self.grille_complete)
        self.grille = self.controleur.creer_grille_vide()
        self.fGrille = FenetreGrille(self, self.grille_complete, self.grille, self.controleur)
        
        self.creer_interface()
        

    def creer_interface(self):
        self.title("Définitions des Mots")
        self.font_name = 'Calibri'
        self.font_size = 12
        self.font_style = font.Font(family=self.font_name, size=self.font_size)

        # Configurer la fenêtre pour qu'elle occupe une grande partie de l'écran
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()
        self.largeur = int(largeur_ecran * 0.4)
        self.hauteur = int(hauteur_ecran * 0.5)
        x_offset = int(largeur_ecran * 0.01)
        y_offset = int((hauteur_ecran - self.hauteur) / 2)
        
        self.geometry(f"{self.largeur}x{self.hauteur}+{x_offset}+{y_offset}")

        # Configuration de la grille pour rendre la mise en page flexible
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Ligne de la zone de texte déroulante

        # Titre et règles du jeu
        self.infos = tk.Frame(self)
        self.infos.grid(row=0, column=0, columnspan=3, sticky='ew')

        text_gauche = "VIES : " + str(self.nb_vie)
        self.info_gauche = tk.Label(self.infos, text=text_gauche, anchor='w')
        self.info_gauche.pack(side='left', fill='x', expand=True)

        text_droite = "AIDES : " + str(self.nb_aide)
        self.info_droite = tk.Label(self.infos, text=text_droite, anchor='e')
        self.info_droite.pack(side='right', fill='x', expand=True)

        # Zone de texte déroulante pour les définitions
        self.definition = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=(self.font_name, self.font_size))
        self.definition.grid(row=1, column=0, columnspan=3, sticky='nsew')

        # Zone de saisie du mot à trouver       
        self.text = tk.StringVar()
        self.saisie = tk.Entry(self, textvariable=self.text)
        self.saisie.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Bouton pour valider le mot
        self.bouton_valider = tk.Button(self, text="Valider")
        self.bouton_valider.bind('<Button-1>', self.valider_mot)
        self.bind('<Return>', self.valider_mot)
        self.bouton_valider.grid(row=2, column=2, padx=5, pady=5)

        # Bouton pour relancer une nouvelle partie
        self.bouton_relancer = tk.Button(self, text="Retour au menu", command=self.afficher_menu)
        self.bouton_relancer.grid(row=3, column=2, padx=5, pady=5)

        # Bouton pour obtenir de l'aide
        self.bouton_aide = tk.Button(self, text="Aide", command=self.aide)
        self.bouton_aide.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Afficher les définitions
        self.afficher_definitions()



    def quitter(self):
        """
        Ferme la fenêtre.
        """
        self.destroy()

    def aide(self):
        """
        Fournit une aide pour remplir la grille, en plaçant une lettre correctement.
        """

         
        (self.grille, self.nb_aide) = self.controleur.aide(self.grille, self.nb_aide) # Appel de la méthode aide du contrôleur pour obtenir une aide

        # Mise à jour de l'affichage en fonction du nombre d'aides disponibles
        if self.nb_aide > 1 :
            self.info_droite.config(text=f"AIDES : {self.nb_aide}")
        elif self.nb_aide == 1:
            self.info_droite.config(text=f"AIDE : {self.nb_aide}")
        else:
            self.info_droite.config(text="Plus d'aide disponible !") # Si plus aucune aide n'est disponible, configure le bouton d'aide pour afficher la réponse
            self.bouton_aide.config(text="Afficher la réponse", command=self.afficher_reponse)
        self.fGrille.afficher_grille() # Affichage de la grille mise à jour
    
    def afficher_reponse(self):
        self.show_messagebox()
        if self.reponse:
            self.grille = self.grille_complete.grille
            self.fGrille.actualiser(self.grille)
            self.nb_vie = 0
            text = 'Vous avez abandonné...'
            self.fin_partie(text)
            self.info_gauche.config(text="VIES : Plus besoin")


    def valider_mot(self, event):
        mot = self.saisie.get()
        fin = False
        (mot_final, test) = self.controleur.execute_choix(mot)
        if test:
            self.controleur.devoiler_mot(self.grille, mot_final)
        else:
            self.nb_vie -= 1
            if self.nb_vie > 1:
                self.info_gauche.config(text=f"VIES : {self.nb_vie}")
            elif self.nb_vie ==1:
                self.info_gauche.config(text=f"VIE : {self.nb_vie}")
            elif self.nb_vie == 0:
                self.fin_partie('Vous êtes mort, dommage')
                self.info_gauche.config(text ="VIES = 0 (triste)" )
                self.info_droite.config(text ="AIDES : Plus besoin" )
                fin = True
        if not fin: 
            self.saisie.delete(0, tk.END)
            self.fGrille.afficher_grille()
            if self.grille == self.grille_complete.grille:
                text = 'Youpi, vous avez gagné!!!'
                self.fin_partie(text)
    
    def fin_partie(self, text):
        self.definition.config(state='normal')
        self.definition.delete('1.0', tk.END)
        (nombre_espaces, nombre_saut_ligne) = self.controleur.centrer_text(text, self.font_style, self.definition)
        for i in range(nombre_saut_ligne):
            self.definition.insert(tk.END, '\n')
        self.definition.insert(tk.END, ' ' *nombre_espaces + text)
        self.fGrille.actualiser(self.grille_complete.grille)
        self.bouton_valider.destroy()
        self.bouton_aide.destroy()
        self.saisie.destroy()
        self.bouton_quitter = tk.Button(self, text = 'Quitter', command = self.app.quitter, height=2, width=20)
        self.bouton_quitter.grid(row=2, column=0)
        self.bouton_relancer.config(height=2, width=20)
        self.bouton_relancer.grid(row=2, column=2)
        self.bouton_def = tk.Button(self, text = 'Afficher les définitions', command = self.afficher_definitions, width = 57)
        self.bouton_def.grid(row=3, column=0, columnspan=4)
        self.definition.config(state='disabled')
               

    def afficher_definitions(self):
        self.definition.config(state='normal')
        self.definition.delete('1.0', tk.END)
        les_mots = self.grille_complete.mots
        les_mots_triees = self.controleur.trier_mots(les_mots)
        for (orientation, liste) in les_mots_triees.items():
            text = "Mots " + orientation.upper() + "\n"
            self.definition.insert(tk.END, text)
            for mot in liste :
                numero = str(mot.numero)
                definition = str(mot.definition)
                text = numero + " : " + definition 
                if mot.categorie != self.grille_complete.ma_categorie:
                    text += '    Catégorie : ' + str(mot.categorie)
                text += '\n'
                self.definition.insert(tk.END, text)
            self.definition.insert(tk.END, '\n')
        self.definition.config(state='disabled')
        

    def show_messagebox(self):
        if not self.messagebox_open:
            self.messagebox_open = True
            self.reponse = messagebox.askyesno("Confirmation", "Voulez-vous vraiment afficher les réponses ?")
            self.messagebox_open = False
        
    
    def afficher_menu(self):
        self.app.show_menu()
    
        

if __name__ == "__main__":
    app = FenetreDefinitions(10, 10, 10, 'all')
    app.mainloop()
