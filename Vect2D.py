## Fichier Vect2D.py
## Ce fichier contient une classe éponyme et des méthodes permettant d'effectuer les opérations de bases sur des vecteurs à deux dimensions.

from math import *

class vect2D:
    '''Fourni des vecteurs à deux dimensions'''
    def __init__(self, x = 0, y = 0):
        '''constructeur d'un vecteur'''
        self.x = x
        self.y = y
        
    # Addition
    def __iadd__(self, vecteur):
        '''Gestion de +='''
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x += vecteur.x
        nVecteur.y += vecteur.y
        return nVecteur
    def __add__(self, vecteur):
        '''Gestion de l'addition de deux vecteurs'''
        nVecteur = self
        nVecteur += vecteur
        return nVecteur
    def __isub__(self, vecteur):
        '''Gestion de -='''
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x -= vecteur.x
        nVecteur.y -= vecteur.y
        return nVecteur
    def __sub__(self, vecteur):
        '''Gestion de la soustraction de deux vecteurs'''
        nVecteur = self
        nVecteur -= vecteur
        return nVecteur
        
    # Multiplication
    def __imul__(self, scalaire):
        '''Gestion de la multiplication d'un vecteur par un scalaire via l'operateur *='''
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x *= scalaire
        nVecteur.y *= scalaire
        return nVecteur
    def __mul__(self, scalaire):
        '''Gestion de la multiplication d'un vecteur par un scalaire'''
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur *= scalaire
        return nVecteur
    def __rmul__(self, scalaire):
        '''Gestion de la multiplication d'un vecteur par un scalaire'''
        return self * scalaire

    # Affichage d'un vecteur
    def __str__(self):
        return "[{},{}]".format(self.x,self.y)
    def __repr__(self):
        return "[{},{}]".format(self.x,self.y)

    # Méthodes
    def norme(self):
        '''Renvoit la norme d'un vecteur'''
        return sqrt(self.x**2 + self.y**2)
        
    def normalise(self):
        '''Renvoit le vecteur normalisé'''
        if self.norme() != 0 :
            return (1 / self.norme()) * self
        return self
        
## Fonctions sur les vecteurs :      
        
def p_scal(vecteur1, vecteur2):
    '''Calcule le produit scalaire de deux vecteurs'''
    return vecteur1.x * vecteur2.x + vecteur1.y * vecteur2.y
    
def projection(vecteur1, vecteur2): 
    '''Calcule la projection du vecteur 1 sur l'axe dirigé par le vecteur 2'''
    return p_scal(vecteur1, vecteur2.normalise()) * vecteur2.normalise()
