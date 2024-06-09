import os

# Color Constants
COULEUR_BG = "#fefae0"
COULEUR_TXT = "#283618"
COULEUR_BTN_BG = "#dda15e"
COULEUR_BTN_TXT = "#fefae0"
COULEUR_BTN_HOVER = "#bc883e"

# Define Global Font Size
taillePolice = 12

# Define Repetitive Styles
STYLE_BTN = {
    "fg_color": COULEUR_BTN_BG, 
    "hover_color": COULEUR_BTN_HOVER,
    "text_color": COULEUR_BTN_TXT
}
STYLE_TXT = {
    "fg_color": COULEUR_BG, 
    "text_color": COULEUR_TXT
}
STYLE_TITRE = {**STYLE_TXT, "wraplength": 500, "padx": 50, "pady": 75}

# Define Path Constants
CHEMIN_DRAPEAUX = "./images/Drapeaux/"

# Get the list of all flags
LISTE_DRAPEAUX = os.listdir(CHEMIN_DRAPEAUX)


