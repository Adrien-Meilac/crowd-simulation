## Fichier Variables.py
## Ce fichier contient toutes les variables globales qui font fonctionner le code

import numpy as np
from Vect2D import *

# Variable de la fenêtre
titre = "Simulateur de mouvement de foule"  # titre du l'interface graphique
largeur = 50                                # largeur du terrain en nombre de cases
hauteur = 30                                # hauteur du terrain en nombre de cases
dimCase = 20                                # Taille d'une case en pixels

# Variables concernant les individus
LIndiv = []                                 # Liste des individus sur le terrain
NIndiv = 100                                # Nombre d'individu à créer au début de la simulation
rIndiv = 3                                  # Rayon de chaque individu
vminIndiv = 0.5                             # Vitesse minimale d'un individu
vmaxIndiv = 2                               # Vitesse maximale d'un individu

# Variables concernant le terrain :
LSortie = []    # Liste des sorties sous la forme [x,y]

#Variables relatif à la selection des cases que l'on va parcourir
    # x = abscisse, y = ordonnée, (0,0) représente la case en haut à gauche
    # Par défaut, si aucune case n'est selectionnée, on pointe vers la case (-1,-1)
xPointeur = -1                              # abscisse du curseur en case
yPointeur = -1                              # ordonnée du curseur en case
nvCase = True                               # boleen qui renvoit true lorsqu'une case est sélectionnée
typeCase = 0                                # type de la case (-1 = infranchissable, 0 = case normale, 1 = sortie)
placeIndiv = False                          # Sur une case, true si on peut placer un individu

# Variables globale du stockage des donnees
    # Attention, pour demander la case à la colonne x et ligne y, il faut écrire TCase[y,x]
TCase = np.array([])                        # Stocke les cases sous forme de tableau 
Tdirection = np.array([[vect2D()] * largeur] * hauteur, vect2D)  # Stocke le vecteur direction de chacune des cases dans un tableau
Tligne = np.array([])                       # Stocke les lignes de champ sous forme de tableau
Ttexte = np.array([])                       # Stocke les distances minimum de chaque case à la sortie sous forme de tableau

# Variable de gestion des paramètres dans l'interface
grilleTerrain = False                       # Boleen qui permet d'afficher une grille sur le terrain
typePinceau = False                         # Boleen qui permet de selectionner le type de pinceau (0 = Croix, 1 = Carre) 
mode = 1                                    # Permet de selectionner un mode d'affichage (1 = normal, 2 = champ de potentiel, 3 = distance, 4 = lignes de champ)

# Gestion du temps
TpsRaffraichissement = 30                   # Temps de raffraichissement en ms
tps = 0                                     # Temps de référence pour le chrono
pause = False                               # Boleen pour mettre en pause le mouvement des individus

#Statistique
dMaxCase = -1                               # Distance maximale d'une case d'une sortie
