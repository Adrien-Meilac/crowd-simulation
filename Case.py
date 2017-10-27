## Fichier Case.py
## Permet la gestion des options sur les cases dans le terrain

import numpy as np
from math import floor
from Vect2D import *
import Variables as Var

class case :
    def __init__(self, pos = vect2D(), dim = 0, type = 0, score = 0, canvas = "", color = "ivory", explore = False, grille = False):
        self.pos = pos          # Position de la case
        self.dim = dim          # Dimension de la case en pixels
        self.type = type        # Type de la case
        self.score = score      # Distance du plus court chemin à la sortie
        self.canvas = canvas    # Le Canevas sur lequel on dessine
        self.color = color      # Couleur de la case
        self.explore = explore  # Boleen qui indique si la case a ete ou non parcourue
        self.grille = grille    # Affiche les bords ou non pour la grille
        self.id = canvas.create_rectangle(0, 0, dim, dim, fill = color, outline = color) # representation graphique de la case
        self.canvas.move(self.id, pos.x * dim, pos.y * dim) #Positionnement de la case
    
    def rafraichir(self):
        '''raffraichit la couleur d'une case'''
        if self.type == -1 :
            self.color = "black"
        elif self.type == 1 :
            self.color = "green"
        elif self.type == -2 :
            self.color = "red"
        else :
            self.color = "ivory"
        if self.grille :
            if self.color == "black" :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "ivory")
            else :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "black")
        else :
            self.canvas.itemconfig(self.id, fill = self.color, outline = self.color)
        return
    
    def degrade(self, fg, bg, maxd):
        '''Change la couleur en faisant un dégradé entre fg et bg selon la distance du plus court chemin et de la distance maximum'''
        def blend(i,fg,bg):
            ''' interpolation linéaire de la couleur'''
            return (floor((1 - i) * fg[0] + i * bg[0]), int((1 - i) * fg[1] + i * bg[1]), int((1 - i) * fg[2] + i * bg[2]))
        col = blend(self.score / maxd, fg, bg)
        if(self.grille):
            if col[0] > 255 or col[1] > 255 or col[2] > 255 :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "black")
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "black")
        else :
            if col[0] > 255 or col[1] > 255 or col[2] > 255 :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "#%02x%02x%02x" % bg)
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "#%02x%02x%02x" % col)
        return
    
def init_case(terrain):
    '''Initialisation des cases'''
    Var.TCase = np.array([[case(canvas = terrain)] * Var.largeur] * Var.hauteur, case)
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            pos = vect2D(x, y)
            c = case(pos, Var.dimCase, 0, -1, terrain, "ivory", False)
            Var.TCase[y, x] = c
    return
