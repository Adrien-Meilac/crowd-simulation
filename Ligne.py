## Fichier Ligne.py
## Fourni la gestion des lignes de champ sur le terrain

import numpy as np
from Vect2D import *
import Variables as Var

class ligne :
    def __init__(self, pos1 = vect2D(), pos2 = vect2D(), canvas = "", color = "black") :
        self.pos1 = pos1        # Position du début de la flèche
        self.pos2 = pos2        # Position de la fin de la flèche
        self.canvas = canvas    # Le terrain sur lequel on dessine
        self.color = color      # Couleur de la flèche
        self.id = canvas.create_line(pos1.x, pos1.y, pos2.x, pos2.y, fill = color, arrow = "last") #Représentation graphique
        
    def rafraichir(self) :
        self.canvas.coords(self.id, self.pos1.x, self.pos1.y, self.pos2.x, self.pos2.y)
        return
        
def init_ligne(terrain):
    '''Permet d'afficher les vecteurs sur chaque case pour représenter le champs vectoriel'''
    Var.Tligne=np.array([[ligne(canvas = terrain)] * Var.largeur] * Var.hauteur, ligne)
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.Tligne[y,x] = ligne(canvas = terrain)
    return
    
def cacher_ligne():
    '''Permet de cacher les vecteurs du champs vectoriel'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.Tligne[y,x].pos1 = vect2D()
            Var.Tligne[y,x].pos2 = vect2D()
            Var.Tligne[y,x].rafraichir()
    return
