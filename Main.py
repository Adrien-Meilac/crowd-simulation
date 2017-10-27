from tkinter import *
import os
import time
import Variables as Var
from Case import*
from Texte import*
from Ligne import*
from Individu import*
from Moteur import*
from Evenement import*

cwd = os.getcwd() #Chemin absolu du fichier Main.py

#Fenêtre
tk = Tk()
tk.title(Var.titre)
tk.iconbitmap(cwd+"\icon.ico")
tk.resizable(0, 0)
#tk.wm_attributes("-topmost", 1)

#Panneau de délimitation gloable
p = PanedWindow(tk, orient=HORIZONTAL)
p.pack()

#Panneau de délimitation à gauche
p1 = PanedWindow(p, orient=VERTICAL)
p1.pack(side = LEFT, fill=Y)

#Panneau de délimitation à droite
p2 = PanedWindow(p, orient=HORIZONTAL)
p2.pack(side = RIGHT, fill=Y)

##Menu
menubar = Menu(tk)
    
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau", command=lambda : (nouveau(terrain), reset_temps()))
menu1.add_command(label="Enregistrer sous...", command=enregistrer_sous)
menu1.add_command(label="Charger", command= lambda : (charger(terrain),reset_temps()))
menu1.add_separator()
menu1.add_command(label="Quitter", command=tk.destroy)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label= "Remplir de mur", command = remplir_mur)
menubar.add_cascade(label="Éditer", menu=menu2)
    
menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label= "Normal", command = lambda : change_mode(1))
menu3.add_command(label= "Champ de potentiel", command = lambda : change_mode(2))
menu3.add_command(label= "Distance", command = lambda : change_mode(3))
menu3.add_command(label= "Ligne de champ", command = lambda : change_mode(4))
menu3.add_separator()
menu3.add_command(label= "Grille", command = affiche_grille)
menubar.add_cascade(label="Affichage", menu=menu3)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="Manuel", command = lambda : os.startfile("..\Memoire.pdf"))
menu4.add_command(label="A propos", command=info)
menubar.add_cascade(label="Aide", menu=menu4)


tk.config(menu=menubar)

##Boite à outils (p1)
Label(p1, text = "Boite à outils").pack(side = TOP)
Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Pinceau
Label(p1, text = "Pinceau").pack()

# liste de sélection
liste = Listbox(p1, height=4)
liste.insert(1, "Mur")
liste.insert(2, "Sortie")
liste.insert(3, "Individu")
liste.insert(4, "Effacer")

liste.pack(fill=X)

#Taille du pinceau
Label(p1, text = "Taille du pinceau").pack()
taille_pinceau = Scale(p1,from_=1, to=10, orient=HORIZONTAL)
taille_pinceau.pack(fill=X)

#Type de pinceau
Label(p1, text = "Forme du pinceau").pack()
bouton_typePinceau = Button(p1, text = "Croix", command = lambda : change_typePinceau(bouton_typePinceau))
bouton_typePinceau.pack(fill=X)

Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Bouton pour recalculer le champ de potentiel
bouton_recalcule = Button(p1, text = "Recalculer le champ", command = lambda : recalcule(label_dMaxCase))
bouton_recalcule.pack(fill=X)

#Boutons relatifs aux individus
Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

Label(p1, text = "Individus").pack()

#Bouton pour lancer une simulation automatique
bouton_simulation = Button(p1, text = "Démarrer la simulation", command = lambda : (recalcule(label_dMaxCase), place_indiv(terrain, nb_indiv), reset_temps()))
bouton_simulation.pack(fill=X)

#Détermine le nombre d'individu à placer entre 0 et 200
nb_indiv_defaut = IntVar(p1)
nb_indiv_defaut.set(Var.NIndiv)
nb_indiv = Spinbox(p1, from_=0, to=200, textvariable=nb_indiv_defaut, justify='center')
nb_indiv.pack(fill=X)

#Supprime tous les individus du terrain
bouton_indiv2 = Button(p1, text = "Supprimer", command = lambda : (supprime_indiv(terrain),reset_temps()))
bouton_indiv2.pack(fill=X)

#Met en pause le mouvement des individus
bouton_pause = Button(p1, text = "Pause", command = lambda : change_pause(bouton_pause))
bouton_pause.pack(fill=X)

##Statistiques
Label(p2, text = "Statistiques").pack(side = TOP)
Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Case la plus éloignée
Label(p2, text = "Distance du point\n le plus éloigné\n d'une sortie :").pack()
label_dMaxCase = Label(p2, text = "∞")
label_dMaxCase.pack()

Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Nombre d'individus encore sur le terrain
Label(p2, text = "Nombre\n d'individus :").pack()
label_nbIndiv = Label(p2, text = str(len(Var.LIndiv)))
label_nbIndiv.pack()

Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Le chronomètre qui mesure le temps que met la dernière personne à sortir
Label(p2, text = "Temps écoulé :").pack()
label_temps = Label(p2, text = "00:00")
label_temps.pack()

bouton_temps = Button(p2, text = "Réinitialiser\n le chrono", command = reset_temps)
bouton_temps.pack(fill=X)

Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)


##Le terrain
terrain = Canvas(p, width=Var.largeur*Var.dimCase,height=Var.hauteur*Var.dimCase, bd=0, highlightthickness=0, background="grey")
terrain.pack(side=RIGHT)

tk.update()

#Evenements relatif au terrain
terrain.bind("<Button-1>", lambda event : clic_gauche(event, taille_pinceau, terrain))
terrain.bind("<Button-3>", clic_droit)
terrain.bind("<B1-Motion>", lambda event : deplacement_clic_gauche(event, taille_pinceau))
terrain.bind("<B3-Motion>", deplacement_clic_droit)
terrain.bind("<ButtonRelease-1>", reset_clic) 

#Evenements relatif a la liste de selection
liste.bind("<<ListboxSelect>>", selection)

##Fonction de mise à jour
def update():
    if not(Var.pause) :
        bouge_indiv()
        sortir_indiv(terrain)
        stat_nbIndiv(label_nbIndiv)
        
        if(len(Var.LIndiv) !=0) :
            Var.tps += Var.TpsRaffraichissement/1000
            tpsStr = time.strftime("%M:%S", time.gmtime(Var.tps))
            label_temps.config(text = tpsStr)
    tk.update_idletasks()
    tk.after(Var.TpsRaffraichissement, update)

##Initialisation
init_case(terrain)
init_ligne(terrain)
init_texte(terrain)
tk.after(Var.TpsRaffraichissement, update)
tk.mainloop()
