import customtkinter as ctk
from common import *

# Classe pour les choix multiples
class choixMultiple():
    def __init__(self, cadre, options, btnTxt, action, dict, fontSize, btnDimensions):
        # Constructeur : 
        
        # Définir les variables self des paramètres
        self._cadre = cadre

        # Nouveau dict dans le contexte de l'objet
        self._dictTaillePolice = dict

        # Assurer un choix au début
        self.choix = ctk.StringVar()
        self.choix.set(options[0])

        # Pour chaque option :
        for option in options:
            # Créer un bouton radio stylisé
            option = ctk.CTkRadioButton(cadre, text=option,
                variable=self.choix,
                value=option,
                font=("Helvetica", fontSize),
                fg_color=COULEUR_BTN_HOVER, 
                hover_color=COULEUR_BTN_HOVER,
                text_color=COULEUR_TXT
                )
            
            # Ajouter au dict en suivant la même norme pour nommer les clés
            self._dictTaillePolice[str(option).split(".!")[-1]] = fontSize

            # Ajouter l'option/le bouton radio créé
            option.pack(pady=5)

        # Bouton standard pour quitter/soumettre
        btnReturn = ctk.CTkButton(
            cadre,
            text=btnTxt,
            width=btnDimensions[0],
            height=btnDimensions[1],
            command=action,
            font=("Helvetica", fontSize),
            **STYLE_BTN
        )

        # Ajouter au dict
        self._dictTaillePolice[str(btnReturn).split(".!")[-1]] = fontSize

        # Ajouter le bouton sous les options
        btnReturn.pack(pady=10)

    # Méthode qui retourne la valeur de l'élément choisi
    @property
    def réponse(self):
        return self.choix.get()

    # Méthode qui retourne le nouveau dict à fusionner avec l'ancien
    @property
    def dict(self):
        return self._dictTaillePolice
