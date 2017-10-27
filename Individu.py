## Fichier Individu.py
## Creation et suppression d'individus, gestion des interactions avec leur environnement

from Vect2D import *
from math import floor
import numpy as np
import random as rd
import Variables as Var

class individu:
    def __init__(self, pos, dpos, vmoy, r, canvas, color):
        self.pos = pos          # Position de chaque individu
        self.dpos = dpos        # Vitesse de chaque individu
        self.r = r              # Rayon de chaque individu
        self.vmoy = vmoy        # Vitesse moyenne d'un individu
        self.canvas = canvas    # Le Canevas sur lequel on dessine
        self.color = color      # Couleur de chaque individu
        self.id = canvas.create_oval(-1 * r, -1 * r, r, r, fill = color, outline = color) #Représentation graphique
        self.canvas.move(self.id, pos.x, pos.y) #On le place à sa position
    
    def bouge(self):
        '''deplace un individu de dpos'''
        self.canvas.move(self.id, self.dpos.x, self.dpos.y)
        self.pos += self.dpos
        return
     
# Fonction de gestion du nombre d'individu
def init_indiv(terrain):
    supprime_indiv(terrain)
    for i in range(Var.NIndiv):
        # Afin d'éviter que des individus se retrouve a moitie dans un mur on genere sur un intervalle ou chacun d'eux est pleinement dans une case
        while 1 :
            x = rd.uniform(Var.rIndiv, (Var.largeur - 1) * Var.dimCase - Var.rIndiv)
            y = rd.uniform(Var.rIndiv, (Var.hauteur - 1) * Var.dimCase - Var.rIndiv)
            if Var.TCase[floor(y / Var.dimCase), floor(x / Var.dimCase)].type >= 0 :
                break
        pose_indiv(x, y, terrain)
    return
    
def pose_indiv(x, y, terrain):
    '''Pose un inidividu sur le terrain en (x,y)'''
    pos = vect2D(x, y)
    dpos = vect2D(0, 0)
    indiv=individu(pos, dpos, rd.uniform(Var.vminIndiv, Var.vmaxIndiv), Var.rIndiv, terrain,"red")
    Var.LIndiv.append(indiv)
    return

def supprime_indiv(terrain):
    '''supprime tous les individus du terrain'''
    for i in Var.LIndiv :
        terrain.delete(i.id)
    Var.LIndiv = []
    return
    
def sortir_indiv(terrain):
    '''Permet de supprimer un individu lorsqu'il a atteint la sortie'''
    for individu in Var.LIndiv :
        x = floor(individu.pos.x / Var.dimCase)
        y = floor(individu.pos.y / Var.dimCase)
        if Var.TCase[y, x].type == 1 :
            terrain.delete(individu.id)
            Var.LIndiv.remove(individu)
    return 
    
# Fonction de gestion des collisions avec les murs, les bords et les autres individus
def touche_indiv(individu1, individu2):
    '''Test si deux individus se touchent'''
    return (individu1.pos - individu2.pos).norme() <= individu1.r + individu2.r

def rebond_indiv(individu1, individu2): 
    '''Lorsqu'il y a collision entre deux individu, calcule les vitesses de chacun après le choc'''
    if p_scal(individu1.dpos, individu2.dpos) < 0 : #Vérifie si les individus ne s'éloignent pas déjà
        return
    
    n = individu1.pos - individu2.pos
    n1 = projection(individu1.dpos, n)
    n2 = projection(individu2.dpos, n)
    
    t1 = individu1.dpos - n1
    t2 = individu2.dpos - n2
    #On conserve les composantes tangentielles et on échange les composantes normales
    individu1.dpos = (t1 + n2)
    individu2.dpos = (t2 + n1)
    
    return
    
def rebond_mur(individu):
    '''Lorsqu'un individu touche un mur, on le fait rebondir en inversant sa vitesse selon les axes de chocs'''
    pos = individu.pos
    r = individu.r
    c = Var.TCase[floor(pos.y / Var.dimCase), floor(pos.x / Var.dimCase)]
    if c.type == -1 :
        if pos.x -r < c.pos.x or pos.x + r > c.pos.x + Var.dimCase :
            individu.dpos.x *= -1
        if pos.y -r < c.pos.y or pos.y + r > c.pos.y + Var.dimCase :
            individu.dpos.y *= -1
    return
    
def rebond_bord(individu):
    '''Lorsqu'un individu touche un mur, on le fait rebondir en inversant sa vitesse selon les axes de chocs'''
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > Var.largeur*Var.dimCase:
        individu.dpos.x *= -1
    if pos.y - r < 0 or pos.y + r > Var.hauteur*Var.dimCase :
        individu.dpos.y *= -1
    return

# Programme de gestion des mouvements
def bouge_indiv():
    '''Gestion du mouvement des individus en fonction de l'environnement de chacun'''
    for i, individu1 in enumerate(Var.LIndiv) :
        x = floor(individu1.pos.x / Var.dimCase)
        y = floor(individu1.pos.y / Var.dimCase)
        individu1.dpos = individu1.dpos.normalise() * np.random.normal(individu1.vmoy, 0.2)
        individu1.dpos += Var.Tdirection[y,x]
        for individu2 in Var.LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1, individu2)
        rebond_bord(individu1)
        rebond_mur(individu1)
        individu1.bouge()
    return
