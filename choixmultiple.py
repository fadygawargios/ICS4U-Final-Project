import customtkinter as ctk
from common import *

# Class for multiple choices
class choixMultiple():
    def __init__(self, cadre, options, btnTxt, action, dict, fontSize, btnDimensions):
        # Constructor: 
        
        # Set the self variables of the params
        self._cadre = cadre

        # New dict in the context of the object
        self._dictTaillePolice = dict

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
            self._dictTaillePolice[str(option).split(".!")[-1]] = fontSize

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
        self._dictTaillePolice[str(btnReturn).split(".!")[-1]] = fontSize

        # Pack the button below the options
        btnReturn.pack(pady=10)

    # Method that returns the value of the chosen element
    def réponse(self):
        return self.choix.get()

    # Method that returns the new dict to merge with the old one
    @property
    def dict(self):
        return self._dictTaillePolice
