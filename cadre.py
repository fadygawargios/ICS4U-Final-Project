import customtkinter as ctk
from common import *
from PIL import Image, ImageTk
import time
from choixmultiple import choixMultiple
from choixtxt import choixTxt

# Frame class for each page of the application
class cadre():
    def __init__(self, _fenetre, bg_color=COULEUR_BG):
        # Set a self variable for the customtkinter frame
        self._cadre = ctk.CTkFrame(_fenetre, fg_color=bg_color, corner_radius=10)
        
        # Create a dictionary to store all font sizes for the changeFont method
        self._dictTaillePolice = {}

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
        self._dictTaillePolice[str(lbl).split(".!")[-1]] = fontSize

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
        self._dictTaillePolice[str(btn).split(".!")[-1]] = fontSize
        
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
            dict=self._dictTaillePolice,
            fontSize=fontSize,
            btnDimensions=dimensions
        )
        
        # Update the dict containing all font sizes with the MultipleChoice elems using the chercheDict method
        newDict = choix.dict
        self._dictTaillePolice.update(newDict)
        
        # Return the choix object
        return choix

    # Method to add a text field
    def addChoixTxt(self, fontSize=15):
        # Create an object from the ChoixTxt class
        txt = choixTxt(self._cadre, fontSize=fontSize, dict=self._dictTaillePolice)
        
        # Add font size to the dict
        newDict = txt.dict
        self._dictTaillePolice.update(newDict)
        
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
                child.configure(font=("Helvetica", self._dictTaillePolice[childNom] + nouvelleTaille * 5))
            except:
                pass

    # Method that returns the ctk frame object
    @property
    def root(self):
        return self._cadre
