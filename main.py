#-------------------------------------------------------------------------------
#  Nom: Fady Gawargios
#  Titre: Jeux Éducatif
#  Description: Une interface graphique python pour deviner le jeu de drapeau 
#  qui rassemble également des informations utilisateur de base et stocke 
# les scores dans un fichier txt (classement.txt)
#--------------------------------------------------------------------------------

# Importation des bibliothèques (third-parrty)
import os
import tkinter as tk
from tkinter import messagebox

# Importation des fonctions et des classes personnalisées
from common import *
from fonctions import obtenirOptions, sauvegardeFichier, chargeFichier, msgSalut
from app import app

# Crée la fenêtre principale basée sur la classe app() dans fonctions.py
fenetre = app()

# Fonction qui fixe l'objectif en fonction de la difficulté et démarre le jeu
def commenceJeu():
    # Vérifie la difficulté choisie et fixe l'objectif
    if difficulté.réponse == "Facile":
        objectif = 5
    elif difficulté.réponse == "Moyenne":
        objectif = 10
    else:
        objectif = None

    # Initialisation des points et des erreurs
    points = 0
    erreurs = 0

    # Passe à la page du jeu avec la difficulté choisie
    cadreDifficultés.switchPage(cadreJeu, int(size.réponse))
    # Appel de la fonction principale du jeu
    jeu(points, objectif, erreurs)

# _____________PAGE #5_____________

# Création du cadre pour le jeu
cadreJeu = fenetre.créeCadre()

# Fonction principale du jeu, affiche les questions et gère les réponses
def jeu(points, objectif, erreurs):
    # Efface le cadre du jeu avant de continuer
    cadreJeu.efface(wait=2)

    # Vérifie si l'objectif de points est atteint
    if points == objectif:
        pageFin(erreurs)

    # Obtient les options de réponse et l'image de drapeau à afficher
    options, optionFichier, indexBonneRéponse = obtenirOptions(LISTE_DRAPEAUX)
    question = f"QUESTION #{points + 1}: À quel pays appartient ce drapeau?"
    cheminImage = os.path.join(CHEMIN_DRAPEAUX, optionFichier[indexBonneRéponse])
    
    # Ajoute la question et l'image au cadre du jeu
    cadreJeu.addStr(txt=question)
    cadreJeu.openImage(chemin=cheminImage)

    # Ajoute les choix multiples pour la réponse
    choixQuestion = cadreJeu.addChoixMultiple(
        options=options,
        btnTxt="Soumettre!",
        action=lambda: retroaction(points, choixQuestion.réponse, options[indexBonneRéponse], objectif, erreurs)
    )

    # Affiche le nombre de points actuels
    cadreJeu.addStr(f"Points: {points}")
    cadreJeu.changePolice(int(size.réponse))

# Fonction qui gère la rétroaction après une réponse
def retroaction(points, réponse, bonneRéponse, objectif, erreurs):
    # Vérifie si la réponse est correcte
    if réponse == bonneRéponse:
        # Affiche un message de félicitations en vert
        cadreJeu.addStr(
            txt="BRAVO!",
            fontSize=25 * int(size.réponse),
            style={"fg_color": "green", "bg_color": "white"}
        )
        root.update()
        # Augmente le nombre de points
        points += 1
    else:
        # Affiche la bonne réponse en rouge
        cadreJeu.addStr(
            txt=f"La bonne réponse \n était {bonneRéponse}.",
            fontSize=25 * int(size.réponse),
            style={"fg_color": "red", "bg_color": "white"}
        )
        
        # Si aucun objectif n'est fixé, enregistre les points et passe à la page de fin
        if objectif == None:
            root.update()
            cadreJeu.efface(wait=2)
            sauvegardeFichier(nom.réponse, année.réponse, points)
            pageFin(points=points)

        root.update()

        # Augmente le nombre d'erreurs
        erreurs += 1
        # Réduit le nombre de points en cas de mauvaise réponse
        if points != 0:
            points -= 1

    # Continue le jeu avec les points et erreurs mis à jour
    jeu(points, objectif, erreurs)

# Fonction qui affiche la page de fin avec les résultats
def pageFin(erreurs=None, points=None):
    # Création du cadre pour la page de fin
    cadreFin = fenetre.créeCadre()
    
    # Affiche un message de félicitations avec le nom de l'utilisateur si fourni
    if nom.réponse != "":
        cadreFin.addStr(txt=f"Bravo {nom.réponse}!!", fontSize=25, style=STYLE_TITRE)
    else:
        cadreFin.addStr(txt=f"Bravo!", fontSize=25, style=STYLE_TITRE)

    # Affiche le nombre d'erreurs si disponible
    if erreurs != None:
        cadreFin.addStr(txt=f"Vous avez fait {erreurs} erreurs!!")
    
    # Affiche le nombre de points si disponible
    if points != None:
        cadreFin.addStr(txt=f"Vous avez eu {points} points.")
    
    # Ajoute des boutons pour quitter ou voir le classement
    cadreFin.addBtn(txt="Quitter", action=root.destroy)
    cadreFin.addBtn(txt="Voir Classement",
        action=lambda: (cadreFin.switchPage(cadreClassement, int(size.réponse)), cadreClassement.chargeClassement(chargeFichier(), int(size.réponse))))

    # Passe à la page de fin
    cadreJeu.switchPage(cadreFin, int(size.réponse))

# Fonction qui affiche un message d'avertissement si le nom n'est pas fourni
def avertissement():
    # Vérifie si le nom est fourni
    nomFourni = nom.réponse
    if nomFourni == "":
        # Affiche une boîte de dialogue d'erreur
        messagebox.showerror(
            title="Avertissement",
            message="Vous ne pouvez plus progresser sans nom."
        )
        # Revient à la page d'information
        cadreInfo.switchPage(cadreInfo, int(size.réponse))
    else:
        # Affiche un message de salut et passe à la page de choix des difficultés
        msgSalut(nomFourni)
        cadreInfo.switchPage(cadreDifficultés)

# _____________PAGE #1_____________

# Création du cadre pour la page d'accueil
cadreAccueil = fenetre.créeCadre()
cadreAccueil.ouvre()

# Ajoute un message de bienvenue à la page d'accueil
cadreAccueil.addStr("Bienvenue aux jeux éducatifs!!", fontSize=50, style=STYLE_TITRE)
cadreAccueil.addBtn(
    "Commencer!",
    action=lambda: (cadreAccueil.switchPage(cadreInfo, int(size.réponse))),
    style=STYLE_BTN
)

# Ajoute un bouton pour voir le classement
cadreAccueil.addBtn(
    "Voir Classement",
    action=lambda: (cadreAccueil.switchPage(cadreClassement, int(size.réponse)), cadreClassement.chargeClassement(chargeFichier(), int(size.réponse))),
    style=STYLE_BTN
)

# Ajoute un bouton pour accéder aux paramètres
cadreAccueil.addBtn(
    txt="Params",
    dimensions=[15, 1],
    position=[tk.LEFT, tk.SW],
    action=lambda: (cadreAccueil.switchPage(cadreParamétres, int(size.réponse)))
)

# _____________PAGE #2_____________

# Création du cadre pour la page des paramètres
cadreParamétres = fenetre.créeCadre()
# Ajoute une option pour choisir la taille de la police
cadreParamétres.addStr(txt="CHOISISSEZ LA TAILLE DE LA POLICE: ")
size = cadreParamétres.addChoixMultiple(
    options=["1", "2", "3"],
    btnTxt="Retour",
    dimensions=[15, 1],
    action=lambda: (cadreParamétres.switchPage(cadreAccueil, int(size.réponse)))
)

# _____________PAGE #3_____________

# Création du cadre pour la page d'information
cadreInfo = fenetre.créeCadre()
# Ajoute des instructions pour l'utilisateur
cadreInfo.addStr(txt="POUR COMMENCER", fontSize=35, style=STYLE_TXT)
cadreInfo.addStr(txt="Tapez votre noms ci-dessous:")
nom = cadreInfo.addChoixTxt()
cadreInfo.addStr(txt="Choisissez votre année d'étude ci-dessous:")
année = cadreInfo.addChoixMultiple(
    options=["1-2 année", "3-4 année", "+4 année"],
    btnTxt="Jouer",
    action=avertissement
)

# Ajoute un bouton pour revenir à la page d'accueil
cadreInfo.addBtn(
    "Retour",
    dimensions=[15, 1],  
    position=[tk.LEFT, tk.SW], 
    action=lambda: (cadreInfo.switchPage(cadreAccueil, int(size.réponse))),
    style=STYLE_BTN
)

# _____________PAGE #4_____________

# Création du cadre pour la page de choix des difficultés
cadreDifficultés = fenetre.créeCadre()
objectif = 0
# Ajoute des options pour choisir la difficulté du jeu
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

# _____________PAGE #6_____________

# Création du cadre pour la page de classement
cadreClassement = fenetre.créeCadre()
cadreClassement.addStr(txt="CLASSEMENT", fontSize=35, style=STYLE_TXT)

# Ajoute un bouton pour revenir à la page d'accueil depuis le classement
cadreClassement.addBtn(
    "Retour",
    dimensions=[15, 1],  
    position=[tk.LEFT, tk.SW], 
    action=lambda: (cadreClassement.switchPage(cadreAccueil, int(size.réponse)))
)

root = fenetre.root
root.mainloop()