## Fichier Evenement.py
## Gère les interactions entre le code et l'interface

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import numpy as np
import Variables as Var
from Case import *
from Texte import *
from Ligne import *
from Individu import *
from Moteur import *

# Fonction du Menu
    # Option de Fichier
def nouveau(terrain):
    '''Crée un nouveau terrain'''
    if askyesno("Attention", "Êtes vous sûr de vouloir tout supprimer ?"):
        terrain_vierge(terrain)
    return

def enregistrer_sous():
    '''Enregistre le terrain dans un fichier texte'''
    save = asksaveasfile(mode = 'w', filetypes = [('Fichier Texte (.txt)','.txt')], defaultextension = ".txt")
    if save == "" :
        return
    for x in range(Var.largeur):
        for y in range(Var.hauteur - 1):
            save.write(str(Var.TCase[y,x].type) + " ")
        save.write(str(Var.TCase[Var.hauteur-1,x].type))
        save.write("\n")
    save.close()
    return

def charger(terrain):
    '''Charge le terrain d'un fichier texte'''
    filename = askopenfilename(title = "Ouvrir votre fichier", filetypes = [('Fichier Texte (.txt)', '.txt')])
    if filename == "" :
        return
    terrain_vierge(terrain)
    save = open(filename, "r")
    data = save.readlines()
    for x, line in enumerate(data):
        L = line.split()
        for y,l in enumerate(L):
            if int(l) == 1 :
                Var.LSortie.append([x,y])
            Var.TCase[y,x].type = int(l)
            Var.TCase[y,x].rafraichir()
    save.close()
    return
    
    # Option Éditer
def remplir_mur() :
    '''Rempli le terrain de mur'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.TCase[y,x].type = -1
            Var.TCase[y,x].rafraichir()
    return
  
    
    # Option Affichage
def change_mode(nvmode):
    '''Change le mode d'affichage'''
    Var.mode = nvmode
    rafraichir()
    return
    
def affiche_grille():
    '''Active ou désactive la grille'''
    Var.grilleTerrain = not(Var.grilleTerrain)
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            if(Var.grilleTerrain):
                Var.TCase[y,x].grille = True
            else :
                Var.TCase[y,x].grille = False
    rafraichir()
    return
    
    # Option Aide (Menu4)
def info():
    '''Affiche des infos sur le programme'''
    showinfo("A propos", Var.titre + " par LAM Kevin et MEILAC Adrien")
    return
    
# Panneau latéral gauche
def change_typePinceau(self):
    '''Change le type de pinceau entre Carré ou Croix'''
    if Var.typePinceau :
        self.config(text = "Croix", command =  lambda : change_typePinceau(self))
    else :
        self.config(text = "Carré", command =  lambda : change_typePinceau(self))
    Var.typePinceau=not(Var.typePinceau)
    self.pack(fill=X)
    return
    
def recalcule(label):
    '''Recalcule le chmp de potentiel'''
    recalcule_champ_potentiel()
    stat_dMaxCase(label)
    return
    
## bouton_indiv
def place_indiv(terrain, label):
    '''Place des individus aux hasard sur le terrain et met a jour le nombre d'individus affiché par label'''
    n = label.get()
    if(n == ""):
        Var.NIndiv = 0
    else :
        if(int(n) > 200) :
            Var.NIndiv = 200
        else :
            Var.NIndiv = int(label.get())
    init_indiv(terrain)
    return

## bouton_pause
def change_pause(self):
    '''Active/désactive la pause'''
    Var.pause = not(Var.pause)
    if(Var.pause) :
        self.config(text = "Pause", command =  lambda : change_pause(self), relief = SUNKEN)
    else :
        self.config(text = "Pause", command =  lambda : change_pause(self), relief = RAISED)
    self.pack(fill=X)
    return

## label_temps
def reset_temps() :
    '''Remet le chrono à zéro'''
    Var.tps = 0
    return

##Évènements

##Souris
def coordonnees_pointeur(x,y) :
    '''Détermine quelle case est selectionnée selon les coordonnées du pointeur'''
    if (Var.xPointeur == x // Var.dimCase and Var.yPointeur == y // Var.dimCase) :
        Var.nvCase = False
    else :
        Var.nvCase = True
    Var.xPointeur = x // Var.dimCase
    Var.yPointeur = y // Var.dimCase
    return

def clic_gauche(event, taille_pinceau, terrain):
    coordonnees_pointeur(event.x,event.y)
    if(Var.placeIndiv) :
        pose_indiv(event.x,event.y,terrain)
    else :
        if(Var.typeCase!=1) :
            wavefront(Var.xPointeur,Var.yPointeur, [], [change_case_action], taille_pinceau.get(), Var.typePinceau)
        else :
            creer_sortie(Var.xPointeur,Var.yPointeur)
    return

def deplacement_clic_gauche(event, taille_pinceau) :
    coordonnees_pointeur(event.x,event.y)
    if(Var.placeIndiv == False) :
        if(Var.nvCase) :
            if(Var.typeCase!=1) :
                wavefront(Var.xPointeur,Var.yPointeur, [], [change_case_action], taille_pinceau.get(), Var.typePinceau)
            else :
                creer_sortie(Var.xPointeur,Var.yPointeur)
    return
    
def efface_case(x,y):
    if(Var.TCase[y,x].type == 1) :
        Var.LSortie.remove([C.x,C.y])
    Var.TCase[y,x].score = -1
    Var.TCase[y,x].type = 0
    Var.TCase[y,x].rafraichir()
    
def clic_droit(event):
    coordonnees_pointeur(event.x,event.y)
    efface_case(Var.xPointeur,Var.yPointeur)
    return

def deplacement_clic_droit(event) :
    coordonnees_pointeur(event.x,event.y)
    if(Var.nvCase) :
        efface_case(Var.xPointeur,Var.yPointeur)
    return

def reset_clic(event):
    '''Remet toutes les valeurs de la souris par défaut'''
    Var.xPointeur = -1
    Var.yPointeur = -1
    Var.nvCase = False
    return

## Liste du pinceau

def selection(event):
    '''Selestionne le type de case/individus à appliquer'''
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    Var.placeIndiv = False
    if (value == "Mur") :
        Var.typeCase = -1
    elif (value == "Effacer") :
        Var.typeCase = 0
    elif (value == "Sortie") :
        Var.typeCase = 1
    elif(value == "Individu"):
        Var.placeIndiv = True
    return
