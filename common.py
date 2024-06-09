import os

# définit les constantes de couleur
COULEUR_BG = "#fefae0"
COULEUR_TXT ="#283618"
COULEUR_BTN = "#dda15e"

# définit la taille globale du txt modifiée dans les paramètres
taillePolice = 10

# définit les styles répétitifs
STYLE_BTN = {"fg": COULEUR_TXT, "bg": COULEUR_BTN}
STYLE_TXT = {"fg": COULEUR_TXT, "bg": COULEUR_BG}
STYLE_TITRE = {**STYLE_TXT, "wraplength": 500, "padx": 50, "pady": 75}

# Définit les constantes de chemin
CHEMIN_DRAPEAUX = "./images/Drapeaux/"

# Obtient la liste de tous les cartes
LISTE_DRAPEAUX = os.listdir(CHEMIN_DRAPEAUX)


