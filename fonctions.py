# Standard Library Imports
import time
import customtkinter as ctk

# Third-party Library Imports
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
from pycountry import pycountry
from random import randint

# Local Application Imports
from common import *

# Main class describing the single window application
class app():
    def __init__(self):
        # Constructor:
        
        # Create the main window
        self._root = ctk.CTk()

        # Add a title to the window
        self._root.title("Jeux Éducatifs!")

        # Center elements in grid management
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        # Make the application full screen
        self._root.state('zoomed')
        
        # Apply background color
        self._root.configure(fg_color=COULEUR_BG)

        # TODO: ADD COMMENTS
        self._largeur = self._root.winfo_screenwidth()
        self._hauteur = self._root.winfo_screenheight()
        self._root.geometry(f"{self._largeur}x{self._hauteur}")

        self._root.after(0, lambda:self._root.state('zoomed'))


    # Method that returns the original ctk window
    @property
    def root(self):
      return self._root
  
    @property
    def largeur(self):
      return self._largeur
    
    @property
    def hauteur(self):
      return self._hauteur


    # Method that creates a new frame via the frame class
    def créeCadre(self, bg_color=COULEUR_BG):
        
        # Create a frame object with a standard background color
        nouveauCadre = cadre(self._root, bg_color)

        # Return the frame object
        return nouveauCadre

    # Method to close the application
    def destroy(self):
        self._root.destroy()

# Frame class for each page of the application
class cadre(app):
    def __init__(self, _fenetre, bg_color=COULEUR_BG):
        # Set a self variable for the customtkinter frame
        self._cadre = ctk.CTkFrame(_fenetre, fg_color=bg_color, corner_radius=10)
        
        # Create a dictionary to store all font sizes for the changeFont method
        self.dictTaillePolice = {}

    # Method that packs/opens a page
    def ouvre(self):
        self._cadre.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

    # Method that closes a page
    def ferme(self):
        self._cadre.pack_forget()

    # Method that switches between two pages and updates the font size
    def switchPage(self, newPage, fontScale=1):
        self.ferme()
        newPage.ouvre()
        newPage.changePolice(fontScale)

    # Method that opens an image
    def openImage(self, chemin, width=300, height=200):
        # Find the image through the path
        image = Image.open(chemin)

        size = list(image.size)
        size = size[0] // 5, size[1] // 5

        # Change the dimensions of the image based on the parameter
        image = image.resize(tuple(size))

        # Create a customtkinter image object
        imageObj = ImageTk.PhotoImage(image)

        # Place the image in the label and place it on the screen on the page on which the method was called
        lblImage = ctk.CTkLabel(self._cadre, image=imageObj, text="", fg_color=COULEUR_BG)
        lblImage.pack(pady=10)

        # Store the image object once the method execution is complete
        lblImage.image = imageObj

    # Method that clears the page
    def efface(self, wait=0):
        # Wait for a certain time based on the parameter
        time.sleep(wait)

        # For each child (lbl, btn, etc.) on the page
        for child in self._cadre.winfo_children():
            # Clear it
            child.destroy()

    # Method that adds text to the screen
    def addStr(self, txt, fontSize=15, style=STYLE_TXT):
        # Create a label and style it based on the parameters
        lbl = ctk.CTkLabel(self._cadre, text=txt, font=("Helvetica", fontSize), **style)
        
        # Store the font size in a dict to be modified later,
        # the key corresponds to the name of the lbl shortcut, ex: !frame2.lblEx -> lblEx
        self.dictTaillePolice[str(lbl).split(".!")[-1]] = fontSize

        # Pack lbl on the screen
        lbl.pack(pady=10)

    # Method that adds a button
    def addBtn(self, txt, fontSize=15, dimensions=[75, 1], position=[ctk.TOP, ctk.N], action=None, style=STYLE_BTN):
        # Create a styled ctk button element
        btn = ctk.CTkButton(
            self._cadre,
            text=txt,
            font=("Helvetica", fontSize),
            width=dimensions[0],
            height=dimensions[1],
            command=action,
            **style
        )
        # Store its font size in the dict
        self.dictTaillePolice[str(btn).split(".!")[-1]] = fontSize
        
        # Pack it with the possibility of placing it on a side or in a corner
        btn.pack(side=position[0], anchor=position[1], pady=10)

    # Method that adds multiple choices with radio buttons
    def addChoixMultiple(self, options, btnTxt, action, dimensions=[15, 1], fontSize=15):
        # Create a MultipleChoice object based on the options and btn
        choix = choixMultiple(
            self._cadre,
            options=options,
            btnTxt=btnTxt,
            action=action,
            dict=self.dictTaillePolice,
            fontSize=fontSize,
            btnDimensions=dimensions
        )
        
        # Update the dict containing all font sizes with the MultipleChoice elems using the chercheDict method
        newDict = choix.chercheDict()
        self.dictTaillePolice.update(newDict)
        
        # Return the choix object
        return choix

    # Method to add a text field
    def addChoixTxt(self, fontSize=15):
        # Create an object from the ChoixTxt class
        txt = choixTxt(self._cadre, fontSize=fontSize, dict=self.dictTaillePolice)
        
        # Add font size to the dict
        newDict = txt.chercheDict()
        self.dictTaillePolice.update(newDict)
        
        # Return the object
        return txt

    # Method that changes the font size
    def changePolice(self, nouvelleTaille):
        # Get all widgets on the frame
        childWidgets = self._cadre.winfo_children()
        
        # For each:
        for child in childWidgets:
            # Establish the name: corresponds to the key of the dict
            childNom = str(child).split(".!")[-1]
            
            # Try to configure new size
            try:
                child.configure(font=("Helvetica", self.dictTaillePolice[childNom] + nouvelleTaille * 5))
            except:
                pass

    # Method that returns the ctk frame object
    @property
    def root(self):
        return self._cadre

# Class for multiple choices
class choixMultiple(cadre):
    def __init__(self, cadre, options, btnTxt, action, dict, fontSize, btnDimensions):
        # Constructor: 
        
        # Set the self variables of the params
        self.options = options
        self._cadre = cadre

        # New dict in the context of the object
        self.dictTaillePolice = dict

        # Ensure a choice at the beginning
        self.choix = ctk.StringVar()
        self.choix.set(options[0])

        # For each option:
        for option in options:
            # Create a styled radio button
            option = ctk.CTkRadioButton(cadre, text=option,
                variable=self.choix,
                value=option,
                font=("Helvetica", fontSize),
                fg_color=COULEUR_BTN_HOVER, 
                hover_color=COULEUR_BTN_HOVER,
                text_color=COULEUR_TXT
                )
            
            # Add to the dict following the same standard for naming the keys
            self.dictTaillePolice[str(option).split(".!")[-1]] = fontSize

            # Pack the created option/radio button
            option.pack(pady=5)

        # Standard button for exit/submit
        btnReturn = ctk.CTkButton(
            cadre,
            text=btnTxt,
            width=btnDimensions[0],
            height=btnDimensions[1],
            command=action,
            font=("Helvetica", fontSize),
            **STYLE_BTN
        )

        # Add to the dict
        self.dictTaillePolice[str(btnReturn).split(".!")[-1]] = fontSize

        # Pack the button below the options
        btnReturn.pack(pady=10)

    # Method that returns the value of the chosen element
    def réponse(self):
        return self.choix.get()

    # Method that returns the new dict to merge with the old one
    def chercheDict(self):
        return self.dictTaillePolice

# Class for entries
class choixTxt(cadre):
    def __init__(self, cadre, fontSize, dict):
        # Constructor:
        
        # Set the self variables of the params
        self._cadre = cadre
        self.dictTaillePolice = dict
        
        # Create the ctk entry object with a wider width
        self.txtNom = ctk.CTkEntry(self._cadre, width=400, font=("Helvetica", fontSize))
        self.txtNom.pack(pady=10)

        # Add to the new dict
        self.dictTaillePolice[str(self.txtNom).split(".!")[-1]] = fontSize

    # Method that retrieves the info written in the entry
    def réponse(self):
        return self.txtNom.get()

    # Method that retrieves the dict containing the sizes
    def chercheDict(self):
        return self.dictTaillePolice

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
