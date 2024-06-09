#-------------------------------------------------------------------------------
#  Nom: Fady Gawargios
#  Titre: Jeux Éducatif
#  Description: Une interface graphique python pour deviner le jeu de drapeau 
#  qui rassemble également des informations utilisateur de base.
#--------------------------------------------------------------------------------

from tkinter import messagebox
import tkinter as tk
from common import *
from fonctions import app, obtenirOptions
from tktable import Table
from customtkinter import * 
from PIL import Image, ImageTk
import os

# Crée la fenetre principale basé sur la classe app() dans fonctions.py
fenetre = app()

# Fonction qui fixe l'objectif en fonction de la difficulté et démarre le jeu
def commenceJeu():
    if difficulté.réponse() == "Facile":
        objectif = 5
    elif difficulté.réponse() == "Moyenne":
        objectif = 10
    else:
        objectif = None

    points = 0
    erreurs = 0
    cadreDifficultés.switchPage(cadreJeu, int(size.réponse()))
    jeu(points, objectif, erreurs)

# _____________PAGE #5_____________

cadreJeu = fenetre.créeCadre()

# TODO: ADD COMENTS + MAKE SURE NO ONE FLAG IS SHOWN TWICE
def jeu(points, objectif, erreurs):
    cadreJeu.efface(wait=2)

    if points == objectif:
        pageFin(erreurs)

    options, optionFichier, indexBonneRéponse = obtenirOptions(LISTE_DRAPEAUX)
    question = f"QUESTION #{points + 1}: À quelle pays appartient ce drapeaux?"
    cheminImage = os.path.join(CHEMIN_DRAPEAUX, optionFichier[indexBonneRéponse])
    

    cadreJeu.addStr(txt=question)
    cadreJeu.openImage(chemin=cheminImage)

    choixQuestion = cadreJeu.addChoixMultiple(
        options=options,
        btnTxt="Soumettre!",
        action=lambda: retroaction(points, choixQuestion.réponse(), options[indexBonneRéponse], objectif, erreurs)
    )

    cadreJeu.addStr(f"Points: {points}")
    cadreJeu.changePolice(int(size.réponse()))

def retroaction(points, réponse, bonneRéponse, objectif, erreurs):
    if réponse == bonneRéponse:
        cadreJeu.addStr(
            txt="BRAVO!",
            fontSize=25 * int(size.réponse()),
            style={"fg_color": "green", "bg_color": "white"}
        )
        root.update()
        points += 1
    else:
        cadreJeu.addStr(
            txt=f"La bonne réponse \n était {bonneRéponse}.",
            fontSize=25 * int(size.réponse()),
            style={"fg_color": "red", "bg_color": "white"}
        )
        
        if objectif == None:
            root.update()
            cadreJeu.efface(wait=2)
            pageFin(points=points)

        root.update()
        
        erreurs += 1
        if points != 0:
            points -= 1

    jeu(points, objectif, erreurs)

def pageFin(erreurs=None, points=None):
    cadreFin = fenetre.créeCadre()
    if nom.réponse() != "":
        cadreFin.addStr(txt=f"Bravo {nom.réponse()}!!", fontSize=25, style=STYLE_TITRE)
    else:
        cadreFin.addStr(txt=f"Bravo!", fontSize=25, style=STYLE_TITRE)

    if erreurs != None:
        cadreFin.addStr(txt=f"Vous avez fait {erreurs} erreurs!!")
    
    if points != None:
        cadreFin.addStr(txt=f"Vous avez eu {points} points.")
    
    cadreFin.addBtn(txt="Quitter", action=root.destroy)
    cadreFin.addBtn(txt="Voir Classement",
        action=lambda: (cadreFin.switchPage(cadreClassement, int(size.réponse())), chargeClassement(cadreClassement, data)),
        style=STYLE_BTN)

    cadreJeu.switchPage(cadreFin, int(size.réponse()))

def avertissement():
    nomFourni = nom.réponse()
    if nomFourni == "":
        rép = messagebox.askquestion(
            title="Avertissement",
            message="Êtes-vous sûr de vouloir continuer sans nom !?"
        )
        if rép == "yes":
            msgSalut("Utilisateur Anonyme")
        elif rép == "no":
            return
    else:
        msgSalut(nomFourni)

def msgSalut(nomFourni):
    messagebox.showinfo(title="Bienvenu!!", message=f"Salut {nomFourni}")
    cadreInfo.switchPage(cadreDifficultés)

# _____________PAGE #1_____________

cadreAccueil = fenetre.créeCadre()
cadreAccueil.ouvre()

cadreAccueil.addStr("Bienvenue aux jeux éducatifs!!", fontSize=50, style=STYLE_TITRE)
cadreAccueil.addBtn(
    "Commencer!",
    action=lambda: (cadreAccueil.switchPage(cadreInfo, int(size.réponse()))),
    style=STYLE_BTN
)

cadreAccueil.addBtn(
    "Voir Classement",
    action=lambda: (cadreAccueil.switchPage(cadreClassement, int(size.réponse())), chargeClassement(cadreClassement, data)),
    style=STYLE_BTN
)

cadreAccueil.addBtn(
    "Paramétres",
    dimensions=[15, 1],
    position=[tk.LEFT, tk.SW],
    action=lambda: (cadreAccueil.switchPage(cadreParamétres, int(size.réponse()))),
    style=STYLE_BTN
)

# _____________PAGE #2_____________

cadreParamétres = fenetre.créeCadre()
cadreParamétres.addStr(txt="CHOISISSEZ LA TAILLE DE LA POLICE: ")
size = cadreParamétres.addChoixMultiple(
    options=["1", "2", "3"],
    btnTxt="Retour",
    dimensions=[15, 1],
    action=lambda: (cadreParamétres.switchPage(cadreAccueil, int(size.réponse())))
)

# _____________PAGE #3_____________

cadreInfo = fenetre.créeCadre()
cadreInfo.addStr(txt="POUR COMMENCER", fontSize=35, style=STYLE_TXT)
cadreInfo.addStr(txt="Tapez votre noms ci-dessous:")
nom = cadreInfo.addChoixTxt()
cadreInfo.addStr(txt="Choissisais votre année d'étude ci-dessous:")
année = cadreInfo.addChoixMultiple(
    options=["1-2 année", "3-4 année", "+4 année"],
    btnTxt="Jouer",
    action=avertissement
)

cadreInfo.addBtn(
    "Retour",
    dimensions=[15, 1],  
    position=[tk.LEFT, tk.SW], 
    action=lambda: (cadreInfo.switchPage(cadreAccueil, int(size.réponse()))),
    style=STYLE_BTN
)

# _____________PAGE #4_____________

cadreDifficultés = fenetre.créeCadre()
objectif = 0
cadreDifficultés.addStr("Veuillez choisir une difficulté: ", fontSize=35)
cadreDifficultés.addStr(
    txt=("En mode facile, il vous faudra 5 points pour gagner, en mode moyen, 10 points et en mode compétition,\n" +
         " vous devrez obtenir autant de bonnes réponses que possible,\n votre meilleur score sera ensuite enregistré dans un classement.")
)

difficulté = cadreDifficultés.addChoixMultiple(
    options=["Facile", "Moyenne", "Mode Compétition"],
    btnTxt="Continuer",
    action=commenceJeu
)

cadreClassement = fenetre.créeCadre()
cadreClassement.addStr(txt="CLASSEMENT", fontSize=35, style=STYLE_TXT)
data = ["Name", "Age", "City"], ["Alice", 25, "New York"], ["Bob", 30, "London"]

cadreClassement.addBtn(
    "Retour",
    dimensions=[15, 1],  
    position=[tk.LEFT, tk.SW], 
    action=lambda: (cadreClassement.switchPage(cadreAccueil, int(size.réponse()))),
    style=STYLE_BTN
)

def chargeClassement(frame, data):
    table = Table(frame.root, columns=["Name", "Age", "City"], font_size=10, col_width=100, headings_bold=True)
    for row in data:
        table.insert_row(tuple(row))
    table.pack()

root = fenetre.root
root.mainloop()
