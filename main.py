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


# Crée la fenetre principale basé sur la classe app() dans fonctions.py
fenetre = app()
fenetre.ajusteDimensions()

# Fonction qui fixe l'objectif en fonction de la difficulté et démarre le jeu
def commenceJeu():
  if difficulté.réponse() == "Facile":
    objectif = 5
  elif difficulté.réponse() == "Moyenne":
    objectif = 10
  else:
    # TODO: ADD COMMENTS
    objectif = None
  
  # Initialise les variables qui comptent les points et les erreurs commises
  points = 0
  erreurs = 0

  # Change de page au le cadre contenant le jeu
  cadreDifficultés.switchPage(cadreJeu, int(size.réponse()))

  # Commence le jeu
  jeu(points, objectif, erreurs)
  
# _____________PAGE #5_____________

# Crée le cadre qui contiendra toutes les questions et tous les points
cadreJeu = fenetre.créeCadre()

# Fonction principale du jeu qui formule et pose les questions
def jeu(points, objectif, erreurs):

  # Efface la cadre pour une nouvelle question après 2 secondes
  # Donne le temps à l'utilisateur de consulter les commentaires
  cadreJeu.efface(wait=2)

  # Cas de base en récursivité : lorsque l'objectif de point affiche l'écran de fin
  if points == objectif:
    pageFin(erreurs)

  # Cherche les options de la question ainsi que le nom de fichier et l'index de la bonne réponse dans la liste des options
  options, optionFichier, indexBonneRéponse = obtenirOptions(LISTE_DRAPEAUX)

  # Formule la question
  question = f"QUESTION #{points + 1}: À quelle pays appartient ce drapeaux?"
  
  # Obtient le chemin de l'image de la bonne réponse
  cheminImage = os.path.join(CHEMIN_DRAPEAUX, optionFichier[indexBonneRéponse])
  
  # Affiche la question et l'image avec les méthodes addStr et openImage
  cadreJeu.addStr(txt=question)
  cadreJeu.openImage(chemin=cheminImage)

  # Ajoute les options possibles sous forme de boutons radio et d'un bouton de soumission
  choixQuestion = cadreJeu.addChoixMultiple(
    options=options,
    btnTxt="Soumettre!",
    action=lambda: retroaction(points, choixQuestion.réponse(), options[indexBonneRéponse], objectif, erreurs)
)

  # Affiche le nombre de points
  cadreJeu.addStr(f"Points: {points}")

  # Modifie la taille de la police à la taille choisie pour tous les éléments ci-dessus
  cadreJeu.changePolice(int(size.réponse()))

# Fonction qui donne une commentaire et changes le points avant d'appeler le jeu() pour la prochaine question
def retroaction(points, réponse, bonneRéponse, objectif, erreurs):

  # Vérification des réponses, si bonne:
  if réponse == bonneRéponse:
    
    # Commentaire correspondant: Bravo
    cadreJeu.addStr(
        txt="BRAVO!!",
        fontSize=25 * int(size.réponse()),
        style={"fg": "white", "bg": "green"}
    )
    
    # Met à jour la fenêtre pour afficher les commentaires
    root.update()

    # Points de mise à jour: +1
    points += 1

  # Si mal:
  else:
  
    
    # Afficher la bonne réponse
    cadreJeu.addStr(
        txt=f"La bonne réponse était {bonneRéponse}.",
        fontSize=25 * int(size.réponse()),
        style={"fg": "white", "bg": "red"}
    )
    
    # TODO: ADD COMMENTS
    if objectif == None:
      pageFin(points=points)
      return


    # Met à jour la fenêtre pour afficher les commentaires
    root.update()

    # Augmente le nombre d'erreurs commises
    erreurs += 1

    # Si les points ne sont pas à 0, enlevez-en un
    if points != 0:
      points -= 1
  
  # Appelle à nouveau la fonction de jeu avec de nouvelles valeurs de points et d'erreurs
  jeu(points, objectif, erreurs)

# Fonction appelée pour terminer le jeu
def pageFin(erreurs=None, points=None):
  # _____________PAGE #6_____________
  
  # Crée la page finale du jeu
  cadreFin = fenetre.créeCadre()
  
  # Félicitations en fonction du nom s'il est présent
  if nom.réponse() != "":
    cadreFin.addStr(txt=f"Bravo {nom.réponse()}!!", fontSize=25, style=STYLE_TITRE)
  else:
    cadreFin.addStr(txt=f"Bravo!", fontSize=25, style=STYLE_TITRE)

  # Affiche le nombre d'erreurs commises
  # TODO: ADD COMMENTS
  if erreurs != None:
    cadreFin.addStr(txt=f"Vous avez faite {erreurs} erreurs!!")
  
  if points != None:
    cadreFin.addStr(txt=f"Vous avez eu {points} point")

  # Ajoute un bouton pour fermer la fenêtre et quitter
  cadreFin.addBtn(txt="Quitter", action=root.destroy)

  cadreFin.addBtn(txt="Voir Classement")

  # Changez de page pour voir ce cadre avec la bonne taille de police
  cadreJeu.switchPage(cadreFin, int(size.réponse()))

# Fonction qui avertit l'utilisateur si le champ de nom est vide
def avertissement():
  nomFourni = nom.réponse()
  
  # Si aucun nom n'a été fourni
  if nomFourni == "":
    
    # Une boîte pop-up informe
    rép = messagebox.askquestion(
        title="Avertissement",
        message="Êtes-vous sûr de vouloir continuer sans nom !?"
    )

    # Si oui, saluez-le en tant qu'utilisateur anonyme
    if rép == "yes":
      msgSalut("Utulisateur Anonyme")

    # Si non, ne fais rien
    elif rép == "no":
      return
  
  # Si le nom a été fourni, saluez-le
  else:
   msgSalut(nomFourni)

# Fonctions qui accueillent l'utilisateur
def msgSalut(nomFourni):
  
  # Boîte pop up pour saluer l'utilisateur par son nom.
  messagebox.showinfo(title="Bienvenu!!", message=f"Salut {nomFourni}")
  
  # Passe à la page suivante
  cadreInfo.switchPage(cadreDifficultés)


# _____________PAGE #1_____________

# Crée un cadre pour la page d'accueil et l'ouvre
cadreAccueil = fenetre.créeCadre()

# Ouvre le cadre nouvellement créé
cadreAccueil.ouvre()

# addStr est une méthode de cadre qui ajoute du texte stylisé à l'écran
cadreAccueil.addStr("Bienvenue aux jeux éducatifs!!", fontSize=50, style=STYLE_TITRE)

# De même, addBtn ajoute un bouton. Action qui décrit ce que fera le bouton, 
# ici il passera à la page suivante avec la méthode switchPage
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

# Un bouton pour accéder à la page 2, la page des paramètres
cadreAccueil.addBtn(
    "Paramétres",
    dimensions=[15, 1],  # Specify dimensions on a separate line
    position=[tk.LEFT, tk.SW],  # Specify position on a separate line
    action=lambda: (cadreAccueil.switchPage(cadreParamétres, int(size.réponse()))),
    style=STYLE_BTN
)

# _____________PAGE #2_____________

# Crée un cadre pour la page des paramètres
cadreParamétres = fenetre.créeCadre()

# Ajoute un titre à la page
cadreParamétres.addStr(txt="CHOISISSEZ LA TAILLE DE LA POLICE: ")

# Ajoute une série de boutons radio (la liste des options) avec un bouton
# Ici c'est pour choisir la taille de la police
size = cadreParamétres.addChoixMultiple(
    options=["1", "2", "3"],
    btnTxt="Retour",
    dimensions=[15, 1],
    action=lambda: (cadreParamétres.switchPage(cadreAccueil, int(size.réponse())))
)

# _____________PAGE #3_____________

# Crée la page qui collectera les informations sur l'utilisateur
cadreInfo = fenetre.créeCadre()

cadreInfo.addStr(txt="POUR COMMENCER", fontSize=35, style=STYLE_TXT)
cadreInfo.addStr(txt="Tapez votre noms ci-dessous:")

# Ajoute une zone de texte pour obtenir le nom de l'utilisateur
nom = cadreInfo.addChoixTxt()

cadreInfo.addStr(txt="Choissisais votre année d'étude ci-dessous:")

# Ajoute une liste de boutons radio pour sélectionner l'année 
# (actuellement sans importance car il n'y a qu'un seul jeu)
année = cadreInfo.addChoixMultiple(
    options=["1-2 année", "3-4 année", "+4 année"],
    btnTxt="Jouer",
    action=avertissement
)

# Ajoute un bouton au cas où l'utilisateur souhaite revenir à la page avant
cadreInfo.addBtn(
    "Retour",
    dimensions=[15, 1],  
    position=[tk.LEFT, tk.SW], 
    action=lambda: (cadreInfo.switchPage(cadreAccueil, int(size.réponse()))),
    style=STYLE_BTN
)


# _____________PAGE #4_____________

# Crée le cadre pour choisir la difficulté
cadreDifficultés = fenetre.créeCadre()

# Initialiser la variable objectif du point à 0
objectif = 0

# Explique les options à l'utilisateur
cadreDifficultés.addStr("Veuillez choisir une difficulté: ", fontSize=35)

cadreDifficultés.addStr(
    txt="En mode facile, il vous faudra 5 points pour gagner, en mode moyen, 10 points et en mode compétition,"

)

cadreDifficultés.addStr(
  txt="vous devrez obtenir autant de bonnes réponses que possible,\n votre meilleur score sera ensuite enregistré dans un classement."
)

# Ajoute les boutons pour choisir la difficulté
difficulté = cadreDifficultés.addChoixMultiple(
    options=["Facile", "Moyenne", "Mode Compétition"],
    btnTxt="Continuer",
    action=commenceJeu
)

# TODO: ADD COMMENTS
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


# TODO: ADD COMMENTS
def chargeClassement(frame, data):
  # Create the table widget
  table = Table(frame.chercheCad(), columns=["chinese", "dog", "apple"], font_size=10, col_width=100, headings_bold=True)

  # Set table headers
  for row in data:
    table.insert_row(tuple(row))

  table.pack()


"""
  # Set table data cells
  for row_index, row_data in enumerate(data[1:]):
    for col_index, cell_value in enumerate(row_data):
        table.insert_row(row_index+1, col_index, cell_value)

"""

# Exécute la boucle tkinter en fonction de la fenêtre d'origine, 
# et non de la classe que j'ai créée (c'est ce que chercheFen obtient)
root = fenetre.chercheFen()
root.mainloop()


