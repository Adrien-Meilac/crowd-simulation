## Fichier Texte.py
## Fourni la gestion du texte sur le terrain

import numpy as np
from Vect2D import *
import Variables as Var

class texte :
    '''permet de definir des mots sur le graphique avec une position précise'''
    def __init__(self, pos = vect2D(), mot = "", canvas = "", color = "black"):
        self.pos = pos          # La position du centre du texte sur le terrain
        self.mot = mot          # Texte à afficher
        self.canvas = canvas    # Pointe vers le terrain sur lequel on dessine
        self.color = color      # La couleur du texte
        self.id = canvas.create_text(pos.x, pos.y, text = mot) # Réprésentation graphique
        
    def rafraichir(self):
        self.canvas.coords(self.id, self.pos.x, self.pos.y)
        self.canvas.itemconfig(self.id, text = self.mot)
        return

## Methode de gestion du texte

def init_texte(terrain):
    '''Permet d'afficher sur chaque case du terrain la distance qu'il y a entre elle et la sortie la plus proche'''
    global Ttexte
    Var.Ttexte = np.array([[texte(canvas = terrain)] * Var.largeur] * Var.hauteur, texte)
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.Ttexte[y, x] = texte(vect2D(x, y) * Var.dimCase + vect2D(1, 1) * (Var.dimCase / 2), canvas = terrain)
    return
    
def cacher_texte():
    '''Permet de masquer la distance notée sur chaque case en mettant un mot vide'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.Ttexte[y,x].mot = ""
            Var.Ttexte[y,x].rafraichir()
    return
