# Third-party Library Imports
from deep_translator import GoogleTranslator
from pycountry import pycountry
from random import randint

# Local Application Imports
from common import *

def fichierVersNom(file):
    # *Note that files are named with the country code and the .jpg extension (e.g., ca.jpg for Canada)

    # Remove the extension
    code = file.split(".jpg", 1)[0]
    # Find the country info in English using the code
    infoPaysEn = pycountry.countries.get(alpha_2=code)
    # Get only the name from all the available information
    nomPaysEn = str(dict(infoPaysEn)["name"])
    # Translate the country name to French for the user
    nomPaysfr = GoogleTranslator(source='auto', target='fr').translate(nomPaysEn)
    # Remove unnecessary info from the name
    nomPaysfr = nomPaysfr.split(",", 1)[0]
    nomPaysfr = nomPaysfr.split("(", 1)[0]

    # Return the name in French
    return nomPaysfr

# Function that creates options, a random subset of a passed list
def obtenirOptions(list):
    # Define the length of the list - 1 for random number generation
    longueur = len(list) - 1
    
    # Define lists to contain the options and their respective file names
    options = []
    optionsNomFichiers = []

    # Define a list to contain the random numbers to avoid duplicates
    nombreAleatoires = []

    # Creation of 3 options:
    optionsAChercher = 3
    while optionsAChercher != 0:
        # Generate a random number between 0 and the length of the list
        nombreAleatoire = randint(0, longueur)
        
        # If the number hasn't been seen yet
        if nombreAleatoire not in nombreAleatoires:
            # Add the random number just seen to the list
            nombreAleatoires.append(nombreAleatoire)

            # Find a random file name (which corresponds to the index of random_numbers)
            fichierAleatoire = list[nombreAleatoire]

            # Transform the file name into a country name
            nomPays = fichierVersNom(fichierAleatoire)

            # Add the country name to options and the corresponding file names to optionsNomFichiers
            options.append(nomPays)
            optionsNomFichiers.append(fichierAleatoire)
            
            # One less option to search for
            optionsAChercher -= 1

    # Return the options, their file names, and a random int as the index of the correct answer from the options list
    return options, optionsNomFichiers, randint(0, len(options) - 1)
