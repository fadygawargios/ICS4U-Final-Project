import customtkinter as ctk
from common import *
from cadre import cadre

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