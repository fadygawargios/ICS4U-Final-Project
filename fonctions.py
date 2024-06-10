# Importations de bibliothèques tierces
from deep_translator import GoogleTranslator
from pycountry import pycountry
from random import randint
from CTkTable import *
from tkinter import messagebox

# Importations de l'application locale
from common import *

def fichierVersNom(file):
    # *Notez que les fichiers sont nommés avec le code du pays et l'extension .jpg (par exemple, ca.jpg pour le Canada)

    # Supprimez l'extension du nom de fichier
    code = file.split(".jpg", 1)[0]
    # Trouvez les informations du pays en anglais en utilisant le code
    infoPaysEn = pycountry.countries.get(alpha_2=code)
    # Obtenez uniquement le nom parmi toutes les informations disponibles
    nomPaysEn = str(dict(infoPaysEn)["name"])
    # Traduisez le nom du pays en français pour l'utilisateur
    nomPaysfr = GoogleTranslator(source='auto', target='fr').translate(nomPaysEn)
    # Supprimez les informations inutiles du nom
    nomPaysfr = nomPaysfr.split(",", 1)[0]
    nomPaysfr = nomPaysfr.split("(", 1)[0]

    # Retournez le nom en français
    return nomPaysfr

# Fonction qui crée des options, un sous-ensemble aléatoire d'une liste passée
def obtenirOptions(list):
    # Définir la longueur de la liste - 1 pour la génération de nombres aléatoires
    longueur = len(list) - 1
    
    # Définir les listes pour contenir les options et leurs noms de fichiers respectifs
    options = []
    optionsNomFichiers = []

    # Définir une liste pour contenir les nombres aléatoires afin d'éviter les doublons
    nombreAleatoires = []

    # Création de 3 options :
    optionsAChercher = 3
    while optionsAChercher != 0:
        # Générer un nombre aléatoire entre 0 et la longueur de la liste
        nombreAleatoire = randint(0, longueur)
        
        # Si le nombre n'a pas encore été vu
        if nombreAleatoire not in nombreAleatoires:
            # Ajouter le nombre aléatoire vu à la liste
            nombreAleatoires.append(nombreAleatoire)

            # Trouver un nom de fichier aléatoire (qui correspond à l'index des nombres_aléatoires)
            fichierAleatoire = list[nombreAleatoire]

            # Transformer le nom de fichier en nom de pays
            nomPays = fichierVersNom(fichierAleatoire)

            # Ajouter le nom du pays aux options et les noms de fichiers correspondants à optionsNomFichiers
            options.append(nomPays)
            optionsNomFichiers.append(fichierAleatoire)
            
            # Une option de moins à chercher
            optionsAChercher -= 1

    # Retournez les options, leurs noms de fichiers, et un entier aléatoire comme index de la bonne réponse dans la liste des options
    return options, optionsNomFichiers, randint(0, len(options) - 1)

# Fonction pour sauvegarder les scores dans un fichier
def sauvegardeFichier(nom, année, points):
    # Créer une liste avec les informations du joueur
    info = [nom, année, points]      
    # Initialiser les listes pour stocker les données et les indices à supprimer
    data = []
    removeIndices = []
    append = True

    # Vérifier si le fichier classement.txt existe
    if os.path.isfile("classement.txt"):
        # Convertir les données en liste de listes
        with open("classement.txt", "r", encoding="utf-8") as file:
            # Diviser les données en liste
            strData = file.readlines()
            for entry in strData:
                data.append(eval(entry))
        
        file.close()

        # Supprimer les doublons
        for i in range(len(data)):
            # Si le nom et l'année correspondent
            if nom == data[i][0] and année == data[i][1]:
                # Si les nouveaux points sont supérieurs ou égaux, marquer pour suppression
                if points >= data[i][2]:
                    removeIndices.append(i)
                    print(f"{data[i]} est à supprimer.")
                else:
                    append = False

        # Supprimer les entrées marquées
        if len(removeIndices) != 0:
            removeIndices.sort(reverse=True)
            for index in removeIndices:
                data.pop(index)
    
    # Ajouter les nouvelles informations si elles doivent être ajoutées
    if append:  
        data.append(info)

    # Trier les données par points décroissants
    dataTriée = sorted(data, reverse=True, key=lambda x: int(x[2]))
      
    # Écrire les données triées dans le fichier
    with open("classement.txt", "w", encoding="utf-8") as file:
        for elem in dataTriée:
            file.write(f"{elem}\n")

    file.close()

# Fonction pour charger les scores depuis un fichier  
def chargeFichier():
    # Initialiser la liste pour stocker les données
    data = []
    # Vérifier si le fichier classement.txt existe
    if os.path.isfile("classement.txt"):
        with open("classement.txt", "r", encoding="utf-8") as rankings:
            lines = rankings.readlines()

            # Vérifier s'il y a plus d'une ligne dans le fichier
            if len(lines) > 1:
                for entry in lines:
                    # Ajouter chaque entrée non vide à la liste des données
                    if entry.strip():
                        data.append(eval(entry))
            else:
                # Ajouter la seule ligne présente à la liste des données
                data.append(eval(lines[0]))

    # Retourner les données chargées
    return data
    
# Fonction pour afficher un message de bienvenue
def msgSalut(nomFourni):
    messagebox.showinfo(title="Bienvenu!!", message=f"Salut {nomFourni}")


