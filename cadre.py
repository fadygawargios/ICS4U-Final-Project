import customtkinter as ctk
from PIL import Image, ImageTk
import time
from choixmultiple import choixMultiple
from choixtxt import choixTxt
from CTkTable import *
from common import *

# Classe de cadre pour chaque page de l'application
class cadre():
    def __init__(self, _fenetre, bg_color=COULEUR_BG):
        # Définir une variable self pour le cadre customtkinter
        self._cadre = ctk.CTkFrame(_fenetre, fg_color=bg_color, corner_radius=10)
        
        # Créer un dictionnaire pour stocker toutes les tailles de police pour la méthode changeFont
        self._dictTaillePolice = {}

    # Méthode qui affiche/ouvre une page
    def ouvre(self):
        self._cadre.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

    # Méthode qui ferme une page
    def ferme(self):
        self._cadre.pack_forget()

    # Méthode qui bascule entre deux pages et met à jour la taille de la police
    def switchPage(self, newPage, fontScale=1):
        self.ferme()  # Fermer la page actuelle
        newPage.ouvre()  # Ouvrir la nouvelle page
        newPage.changePolice(fontScale)  # Changer la taille de la police de la nouvelle page

    # Méthode qui ouvre une image
    def openImage(self, chemin, width=300, height=200):
        # Trouver l'image via le chemin
        image = Image.open(chemin)

        # Ajuster la taille de l'image
        size = list(image.size)
        size = size[0] // 5, size[1] // 5

        # Changer les dimensions de l'image selon les paramètres
        image = image.resize(tuple(size))

        # Créer un objet image customtkinter
        imageObj = ImageTk.PhotoImage(image)

        # Placer l'image dans le label et l'afficher à l'écran sur la page où la méthode a été appelée
        lblImage = ctk.CTkLabel(self._cadre, image=imageObj, text="", fg_color=COULEUR_BG)
        lblImage.pack(pady=10)

        # Stocker l'objet image une fois l'exécution de la méthode terminée
        lblImage.image = imageObj

    # Méthode qui efface la page
    def efface(self, wait=0):
        # Attendre un certain temps selon le paramètre
        time.sleep(wait)

        # Pour chaque enfant (lbl, btn, etc.) sur la page
        for child in self._cadre.winfo_children():
            # Le détruire
            child.destroy()

    # Méthode qui ajoute du texte à l'écran
    def addStr(self, txt, fontSize=15, style=STYLE_TXT):
        # Créer un label et le styliser selon les paramètres
        lbl = ctk.CTkLabel(self._cadre, text=txt, font=("Helvetica", fontSize), **style)
        
        # Stocker la taille de la police dans un dictionnaire pour la modifier plus tard,
        # la clé correspond au nom du raccourci du label, ex: !frame2.lblEx -> lblEx
        self._dictTaillePolice[str(lbl).split(".!")[-1]] = fontSize

        # Afficher le label à l'écran
        lbl.pack(pady=10)

    # Méthode qui ajoute un bouton
    def addBtn(self, txt, fontSize=15, dimensions=[750, 3], position=[ctk.TOP, ctk.N], action=None, style=STYLE_BTN):

        # Créer un élément bouton ctk stylisé
        btn = ctk.CTkButton(
            self._cadre,
            text=txt,
            font=("Helvetica", fontSize),
            width=dimensions[0],
            height=dimensions[1],
            command=action,
            **style
        )

        # Stocker sa taille de police dans le dictionnaire
        self._dictTaillePolice[str(btn).split(".!")[-1]] = fontSize
        
        # L'afficher avec la possibilité de le placer sur un côté ou dans un coin
        btn.pack(side=position[0], anchor=position[1], pady=10)

    # Méthode qui ajoute des choix multiples avec des boutons radio
    def addChoixMultiple(self, options, btnTxt, action, dimensions=[15, 1], fontSize=15):
        # Créer un objet MultipleChoice basé sur les options et le bouton
        choix = choixMultiple(
            self._cadre,
            options=options,
            btnTxt=btnTxt,
            action=action,
            dict=self._dictTaillePolice,
            fontSize=fontSize,
            btnDimensions=dimensions
        )
        
        # Mettre à jour le dictionnaire contenant toutes les tailles de police avec les éléments de MultipleChoice en utilisant la méthode chercheDict
        newDict = choix.dict
        self._dictTaillePolice.update(newDict)
        
        # Retourner l'objet choix
        return choix

    # Méthode pour ajouter un champ de texte (user input)
    def addChoixTxt(self, fontSize=15):
        # Créer un objet de la classe ChoixTxt
        txt = choixTxt(self._cadre, fontSize=fontSize, dict=self._dictTaillePolice)
        
        # Ajouter la taille de police au dictionnaire
        newDict = txt.dict
        self._dictTaillePolice.update(newDict)
        
        # Retourner l'objet
        return txt

    # Méthode qui change la taille de la police
    def changePolice(self, nouvelleTaille):
        # Obtenir tous les widgets sur le cadre
        childWidgets = self._cadre.winfo_children()
        
        # Pour chaque widget :
        for child in childWidgets:
            # Établir le nom : correspond à la clé du dictionnaire
            childNom = str(child).split(".!")[-1]
            
            # Essayer de configurer la nouvelle taille
            try:
                child.configure(font=("Helvetica", self._dictTaillePolice[childNom] + nouvelleTaille * 5))
            except:
                pass
            
    # Méthode qui charge le classement et affiche une table
    def chargeClassement(self, data, fontScale=1):
        # Compteur pour suivre le nombre de widgets
        count = 1
        # Pour chaque widget sur le cadre
        for widget in self._cadre.winfo_children():
            # Détruire les widgets au-delà des deux premiers
            if count > 2:
                widget.destroy()
            count += 1

        # Si les données ne sont pas vides
        if data != []:
            # En-têtes pour la table
            headers = ["Classement", "Nom", "Année", "Meilleur Score"]
            
            # Ajouter les en-têtes aux données
            data.insert(0, headers)

            # Ajouter les rangs aux données
            for rankIndex in range(len(data)):
                if rankIndex != 0:
                    data[rankIndex].insert(0, f"#{rankIndex}")
            
            # SOURCE: https://github.com/Akascape/CTkTable
            # Créer une table avec les données fournies et les styles
            table = CTkTable(master=self._cadre, 
                             row=len(data), 
                             column=len(data[0]), 
                             values=data, 
                             font=("Helvetica", 15 * fontScale),
                             width=250 * fontScale)  

            # Afficher la table pour qu'elle s'étende et remplisse l'espace
            table.pack(padx=20, pady=20)
        else:
            # Ajouter un message si aucune donnée n'est présente
            self.addStr("Aucun info à classer.")

    # Méthode qui retourne l'objet cadre ctk
    @property
    def root(self):
        return self._cadre
