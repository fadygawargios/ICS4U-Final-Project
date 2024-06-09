# Importations de bibliothèques standard
import time
import tkinter as tk

# Importations de bibliothèques third-party
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
from pycountry import pycountry
from random import randint

# Importations d'applications locales
from common import *

# Classe principale qui décrit la seule fenêtre composant l'application
class app():
  def __init__(self):
    # Constructor:
    
    # Crée la fenêtre principale
    self.fenetre = tk.Tk()

    # Ajoute un titre à la fenêtre
    self.fenetre.title("Jeux Éducatifs!")

    # Met les elems au centre dans la gestion grid 
    self.fenetre.rowconfigure(0, weight=1)
    self.fenetre.columnconfigure(0, weight=1)

    # Met l'application en mode plein écran
    self.fenetre.state('zoomed')  
  
  # Méthode qui renvoie la fenêtre tk d'origine
  def chercheFen(self):
    return self.fenetre
  
  # Méthode qui maximise les dimensions de la fenêtre
  def ajusteDimensions(self):
    
    # Obtient les dimensions de la fenêtre
    largeurFenetre = self.fenetre.winfo_screenwidth()
    hauteurFenetre = self.fenetre.winfo_screenheight()

    # Rend la fenêtre en plein écran
    self.fenetre.geometry(f"{largeurFenetre}x{hauteurFenetre}")
  
  # Méthode qui crée un nouveau frame via la classe cadre
  def créeCadre(self, bg=COULEUR_BG):
    
    # Crée un objet cadre avec une couleur d'arrière-plan standard
    nouveauCadre = cadre(self.fenetre, bg)

    # Retour l'objet cadre
    return nouveauCadre
  
  # Méthode pour fermer l'application
  def destroy(self):
    self.fenetre.destroy()

# Class cadre pour chaque page de l'application
class cadre(app):
  def __init__(self, fenetre, bg=COULEUR_BG):

    # Définit une variable self pour le cadre tkinter
    self.cadre = tk.Frame(fenetre, bg=bg)

    # Crée un dictionnaire qui stockera toutes les 
    # tailles de police pour la méthode changePolice
    self.dictTaillePolice = {}

  # Méthode qui pack/ouvre une page
  def ouvre(self):
    self.cadre.pack(fill=tk.BOTH, expand=True)

  # Méthode qui ferme une page
  def ferme(self):
    self.cadre.pack_forget()

  # Méthode qui switch entre deux pages et mets à jour de la taille de la police
  def switchPage(self, newPage, fontScale=1):
    self.ferme()
    newPage.ouvre()
    newPage.changePolice(fontScale)
  
  # Méthode qui ouvre une image
  def openImage(self, chemin, dimensions=[200, 150]):
    
    # Cherche l'image à travers le chemin
    image = Image.open(chemin)

    # Modifie les dimensions de l'image en fonction du paramètre
    image = image.resize((dimensions[0], dimensions[1]))

    # Crée un objet image tkinter
    imageObj = ImageTk.PhotoImage(image)

    # Place l'image dans l'étiquette et la place à l'écran 
    # dans la page sur laquelle la méthode a été appelée
    lblImage = tk.Label(self.cadre, image=imageObj)
    lblImage.pack()

    # Stocke l'objet image une fois l'exécution de la méthode terminée
    # Source: https://youtube.com/watch?v=4MKO0knAAKo&t=374s
    lblImage.image = imageObj

  # Méthode qui efface la page
  def efface(self, wait=0):

    # Attend un certain temps en fonction du paramètre
    time.sleep(wait)
    
    # Pour chaque enfant (lbl, btn, etc) sur la page
    for child in self.cadre.winfo_children():
      # Efface le
      child.destroy()
  
  # Méthode qui ajoute du texte à l'écran
  def addStr(self, txt, fontSize=15, style=STYLE_TXT):

    # Crée une étiquette et la stylise en fonction des paramètres
    lbl = tk.Label(self.cadre, text=txt, font=("Times", fontSize), **style)
    
    # Stocke la taille de la police dans un dict pour être modifié plus tard, 
    # le key correspond au nom du lbl raccourci, ex: !frame2.lblEx -> lblEx
    self.dictTaillePolice[str(lbl).split(".!")[-1]] = fontSize

    # Pack lbl à l'écran
    lbl.pack()

  # Méthode qui ajoute un bouton
  def addBtn(self, txt, fontSize=15, dimensions=[75, 1], position=[tk.TOP, tk.N], action=None, style=STYLE_BTN):

    # Crée un élément de bouton tk stylisé
    btn = tk.Button(
        self.cadre,
        text=txt,
        font=("Times", fontSize),
        width=dimensions[0],
        height=dimensions[1],
        command=action,
        **style
    )
    # Stocke sa taille de police dans le dict
    self.dictTaillePolice[str(btn).split(".!")[-1]] = fontSize
    
    # Le pack avec la possibilité de le placer sur un côté ou dans un coin
    btn.pack(side=position[0], anchor=position[1])
  
  # Méthode qui ajoute des choix multiples avec des boutons radio
  def addChoixMultiple(self, options, btnTxt, action, dimensions=[15, 1], fontSize=15):

    # Crée un objet du class ChoixMultiple basée sur les options et btn
    choix = choixMultiple(
    self.cadre,
    options=options,
    btnTxt=btnTxt,
    action=action,
    dict=self.dictTaillePolice,
    fontSize=fontSize,
    btnDimensions=dimensions
)
    
    # Met à jour le dict contenant toutes les taillePolice avec les elems du choixMultiple
    # à l'aide du méthode chercheDict()
    newDict = choix.chercheDict()
    self.dictTaillePolice.update(newDict)
    
    # Retourne l'objet choix
    return choix
  
  # Méthode pour ajouter un champ de texte
  def addChoixTxt(self, fontSize=15):
    
    # Crée un objet à partir de la classe ChoixTxt
    txt = choixTxt(self.cadre, fontSize=fontSize, dict=self.dictTaillePolice)
    
    # Ajoute taillePolice au dict
    newDict = txt.chercheDict()
    self.dictTaillePolice.update(newDict)
    
    # Retourne l'objet
    return txt
  
  # Méthode qui change la taille de la police
  def changePolice(self, nouvelleTaille):
    # Obtient tous les widgets sur le cadre
    childWidgets = self.cadre.winfo_children()
    
    # Pour chacun:
    for child in childWidgets:
      # Établit le nom: correspond au key du dict
      childNom = str(child).split(".!")[-1]
      
      # Essai de configurer nouvelle taille
      try:
        child.configure(font=("Times", self.dictTaillePolice[childNom] + nouvelleTaille * 5))
      except:
        pass
  
  # Méthode qui renvoie l'objet frame tk
  def chercheCad(self):
    return self.cadre
  
# Class pour les choix multiples
class choixMultiple(cadre):
  def __init__(self, cadre, options, btnTxt, action, dict, fontSize, btnDimensions):
    # Constructor: 
    
    # Définit les variables self des params
    self.options = options
    self.cadre = cadre

    # Nouveau dict dans le contexte de l'objet
    self.dictTaillePolice = dict

    # Garantit un choix au début
    self.choix = tk.StringVar()
    self.choix.set(options[0])

    # Pour chaque option:
    for option in options:
      # Crée un bouton radio stylisée
      option = tk.Radiobutton(cadre, text=option,
        variable=self.choix,
        value=option,
        font = ("Times", fontSize),
        **STYLE_TXT)
      
      # Ajoute au dict suivant le même standard pour nommer les keys
      self.dictTaillePolice[str(option).split(".!")[-1]] = fontSize

      # Pack l'option/bouton radio crée
      option.pack()

    # Bouton standard pour sortir/soumettre
    btnReturn = tk.Button(
        cadre,
        text=btnTxt,
        width=btnDimensions[0],
        height=btnDimensions[1],
        command=action,
        font=("Times", fontSize),
        **STYLE_BTN
    )

    # Ajoute au dict
    self.dictTaillePolice[str(btnReturn).split(".!")[-1]] = fontSize

    # Pack le bouton en dessous des optiions
    btnReturn.pack()

  # Méthode qui renvoie la valeur de l'élément choisi
  def réponse(self):
    return self.choix.get()
  
  # Méthode qui renvoie le nouveau dict à fusionner avec l'ancien
  def chercheDict(self):
    return self.dictTaillePolice

# Class pour les entry
class choixTxt(cadre):
  def __init__(self, cadre, fontSize, dict):
    # Constructor:
    
    # Définit les variables self des params
    self.cadre = cadre
    self.dictTaillePolice = dict
    
    # Crée l'objet entrée de tk
    self.txtNom = tk.Entry(self.cadre, width=30, font=("Times", fontSize), bd=2)
    self.txtNom.pack()

    # Ajoute au nouveau dict
    self.dictTaillePolice[str(self.txtNom).split(".!")[-1]] = fontSize

  # Méthode qui cherche l'info écrit dans l'entry
  def réponse(self):
    return self.txtNom.get()
  
  # M/thode qui cherche le dict contenant les tailles
  def chercheDict(self):
    return self.dictTaillePolice

def fichierVersNom(file):
  # *Sachez que les fichiers sont nommés avec le code du pays et l'extension .jpg (ex: ca.jpg pour Canada)

  # Enleve l'extension
  code = file.split(".jpg", 1)[0]
  # Cherche l'info du pays en anglais avec le code
  infoPaysEn = pycountry.countries.get(alpha_2=code)
  # Sort seulement le nom de tout l'information disponible
  nomPaysEn = str(dict(infoPaysEn)["name"])
  # Traduit le nom du pays en francais pour l'utulisateur
  nomPaysfr = GoogleTranslator(source='auto', target='fr').translate(nomPaysEn)
  # Enleve des info inutile du nom
  nomPaysfr = nomPaysfr.split(",", 1)[0]
  nomPaysfr = nomPaysfr.split("(", 1)[0]

  # Retourne le nom en francais
  return nomPaysfr


# Fonction qui crée des options, un sous-liste aléatoire d'une liste passée
def obtenirOptions(list):

  # Définit la longeur de la liste - 1 pour la génération de nombres aléatoires
  longueur = len(list) - 1
  
  # Définit les listes pour contenir les options et les noms de ffichiers respectifs
  options = []
  optionsNomFichiers = []

  # Définit une liste pour contenir les nombres aléatoires pour éviter les doublons
  nombreAleatoires = []

  # Creation de 3 options:
  optionsAChercher = 3
  while optionsAChercher != 0:

    # Génére un nombre aléatoire entre 0 et la longeur de la liste
    nombreAleatoire = randint(0, longueur)
    
    # Si le nombre n'a pas était vu encore
    if nombreAleatoire not in nombreAleatoires:
      
      # Ajoute le nombre_aléatoire qu'on vient de voir dans la liste
      nombreAleatoires.append(nombreAleatoire)

      # Trouve le nom d'un fichier aléatoire (ce qui correspond à l'index de nombres_aléatoires) 
      fichierAleatoire = list[nombreAleatoire]

      # Transforme le nom du ficher en nom de pays
      nomPays = fichierVersNom(fichierAleatoire)

      # Ajoute le nom du pays dans options et le noms du fichier correspondantes dans optionsNomFichiers
      options.append(nomPays)

      optionsNomFichiers.append(fichierAleatoire)
      
      # Un moins d'options qui reste à chercher
      optionsAChercher -= 1

  # Retourne les options, leurs nom de fichiers et une int aléatoire comme index de la bonne réponse du liste options
  return options, optionsNomFichiers, randint(0, len(options) - 1)

