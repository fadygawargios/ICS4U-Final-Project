import customtkinter as ctk
from common import *

# Class for entries
class choixTxt():
    def __init__(self, cadre, fontSize, dict):
        # Constructor:
        
        # Set the self variables of the params
        self._cadre = cadre
        self._dictTaillePolice = dict
        
        # Create the ctk entry object with a wider width
        self.txtNom = ctk.CTkEntry(self._cadre, width=400, font=("Helvetica", fontSize))
        self.txtNom.pack(pady=10)

        # Add to the new dict
        self._dictTaillePolice[str(self.txtNom).split(".!")[-1]] = fontSize

    # Method that retrieves the info written in the entry
    def réponse(self):
        return self.txtNom.get()

    # Method that retrieves the dict containing the sizes
    @property
    def dict(self):
        return self._dictTaillePolice
