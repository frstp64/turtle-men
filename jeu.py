#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe de jeu"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None

import tkinter as tk
import turtle
import math
from collections import OrderedDict
from labyrinthe import Labyrinthe
from chrono import Chrono
from monstre import Monstre
from joueurhumain import JoueurHumain
from joueuria import JoueurIA
from tmen import TMen


class Jeu():
    """Constitue une partie du jeu"""
    def __init__(self, infopartie, lienreseau, monpseudo, mode, taille):
        """Initialise tous les paramètres pour le bon démarrage du jeu"""
        self.lienreseau = lienreseau  # conservation du lien avec le serveur
        self.carte = infopartie['params'][0]
        self.vitesse = infopartie['params'][1]
        self.tempsbonus = infopartie['params'][2]
        self.nombremonstres = infopartie['params'][3]
        self.tortues = infopartie['tortues']

        self.monpseudo = monpseudo
        self.mode = mode
        self.taille = taille
        self.info = None

        # initialisation des chronomètres
        self.netchrono = Chrono()  # empêche l'envoi trop rapide de paquets
        self.joueurchrono = Chrono()  # pour les mouvements
        self.pilulechrono = Chrono()  # pour le temps bonus

        # initialisation de la fenêtre de jeu
        self.window = tk.Tk()
        self.window.title('Turtle-Men')

        # mise en forme des scores
        self.scores = OrderedDict()  # dictionnaire ordonné des scores
        self.scores[monpseudo] = [0]  # score du joueur en premier
        rang = 0
        for joueurs in infopartie['tortues']:
            self.scores[joueurs] = [0]
            self.scores[joueurs].append(tk.StringVar(value='{:<10}:{:>10}'
                                        .format(joueurs,
                                                self.scores[joueurs][0])))
        for index in range(len(self.scores)):
            tk.Label(self.window,
                     textvariable=list(
                         self.scores.items())[index][1][1]).grid(row=index,
                                                                 column=0)
            rang += 1

        ## ajouter des trucs de fenêtre içi ##

        #détermine les dimensions de la carte

        largeurcarte = max(len(i) for i in self.carte)
        hauteurcarte = len(self.carte)

                                # taille de la fenêtre
        self.canvas = tk.Canvas(self.window,
                                width=self.taille*largeurcarte,
                                height=self.taille*hauteurcarte)
        self.canvas.grid(row=0, column=1, rowspan=rang)
        self.fen = turtle.TurtleScreen(self.canvas)  # "dessiner" içi
        self.labyrinthe = Labyrinthe(self.fen, self.carte,
                                     self.taille)

        # initialisation des monstres

        self.monstres = dict()

        posmonstres = self.labyrinthe.posDebut('M')

        if self.nombremonstres > 0:
            self.monstres['Blinky'] = [posmonstres, 'nord',
                                       True, False,
                                       Monstre(self.fen, 'red',
                                               'B', self.taille)]
        if self.nombremonstres > 1:
            self.monstres['Pinky'] = [posmonstres, 'nord',
                                      True, False,
                                      Monstre(self.fen, 'pink',
                                              'P', self.taille)]
        if self.nombremonstres > 2:
            self.monstres['Inky'] = [posmonstres, 'nord',
                                     True, False,
                                     Monstre(self.fen, 'cyan',
                                             'I', self.taille)]
        if self.nombremonstres > 3:
            self.monstres['Clyde'] = [posmonstres, 'nord',
                                      True, False,
                                      Monstre(self.fen, 'orange',
                                              'C', self.taille)]

        # initialisation des autres joueurs

        posjoueurs = self.labyrinthe.posDebut('T')

        for nom in self.tortues:
            if nom != self.monpseudo:
                self.tortues[nom].append(TMen(self.fen, 'red',
                                         nom, self.taille))  # instances
                self.tortues[nom][0] = posjoueurs[:]

        # initialisation du joueur principal

        if self.mode == 'manuel':
            self.joueur = JoueurHumain(self.fen, 'yellow',
                                       self.monpseudo, self.taille)
            self.fen.onkeypress(self.joueur.toucheLeft, 'Left')
            self.fen.onkeypress(self.joueur.toucheRight, 'Right')
            self.fen.onkeypress(self.joueur.toucheUp, 'Up')
            self.fen.onkeypress(self.joueur.toucheDown, 'Down')
            self.fen.listen()

        else:
            self.joueur = JoueurIA(self.fen, "yellow", self.monpseudo,
                                   self.taille, self.monstres)
        self.joueur.pos = posjoueurs[:]

        self.joueur.pos = posjoueurs[:]

        self.joueurchrono.reset()  # démarrage du chrono joueur
        self.mvtprec = 'est'  # pour les virages
        self.joueur.pencolor('white')

        self.fen.ontimer(self.go, 1)  # démarrage de la boucle principale
        self.fen.mainloop()

    def go(self):
        """Fonction qui remplit la boucle principale, ne doit pas bloquer"""

        # mise à jour des données
        if self.netchrono.get() > 0.020:  # on peut communiquer
            self.info = self.lienreseau.rapporter(self.joueur.getStatus())
            self.netchrono.reset()

            if self.info is not None:

                # données des monstres
                for monstre in self.info['monstres'].keys():
                    self.monstres[monstre][0] =\
                        self.info['monstres'][monstre][0]
                    self.monstres[monstre][1] =\
                        self.info['monstres'][monstre][1]
                    self.monstres[monstre][2] =\
                        self.info['monstres'][monstre][2]
                    self.monstres[monstre][3] =\
                        self.info['monstres'][monstre][3]

                # données des tortues
                for tortue in self.info['tortues'].keys():
                    if tortue != self.monpseudo:
                        self.tortues[tortue][0] =\
                            self.info['tortues'][tortue][0]
                        self.tortues[tortue][1] =\
                            self.info['tortues'][tortue][1]
                        self.tortues[tortue][2] =\
                            self.info['tortues'][tortue][2]
                        self.tortues[tortue][3] =\
                            self.info['tortues'][tortue][3]

                # mise à jour des scores
                if not self.info['gagnant']:
                    for joueur in self.info['scores'].keys():
                        self.scores[joueur][0] = self.info['scores'][joueur]
                        self.scores[joueur][1].set('{:<10}:{:>10}'
                                                   .format(joueur,
                                                           self.scores[
                                                               joueur][0]))
                else:
                    for joueur in self.info['scores'].keys():
                        if joueur == self.info['gagnant']:
                            self.scores[joueur][1].set('{:<10}:{:>10}'
                                                       .format(joueur,
                                                               'gagnant'))
                        else:
                            self.scores[joueur][1].set('{:<10}:{:>10}'
                                                       .format(joueur,
                                                               'perdant'))

        # mise à jour des monstres
        for monstre in self.monstres.keys():
            self.monstres[monstre][-1].deplacer(self.monstres[monstre][0])
            self.monstres[monstre][-1].orienter(self.monstres[monstre][1])

        # mise à jour des autres tortues
        for joueur in self.tortues.keys():
            if joueur != self.monpseudo:
                self.tortues[joueur][-1].deplacer(self.tortues[joueur][0])
                self.tortues[joueur][-1].orienter(self.tortues[joueur][1])

        # mouvement du joueur
        deltat = self.joueurchrono.get()
        self.joueurchrono.reset()
        case = tuple(math.floor(i) for i in self.joueur.pos)
        diffcase = tuple(i-j for i, j in zip(case, self.joueur.pos))
        normediffcase = (diffcase[0]**2 + diffcase[1]**2)**(0.5)
        distance = self.vitesse*deltat

        if not self.joueur.vie:
            distance = 0

        if self.mvtprec == 'est':
            mvtactuel = (1, 0)
        elif self.mvtprec == 'ouest':
            mvtactuel = (-1, 0)
        elif self.mvtprec == 'nord':
            mvtactuel = (0, -1)
        elif self.mvtprec == 'sud':
            mvtactuel = (0, 1)
        else:
            mvtactuel = (0, 0)

        if self.mode != 'manuel':
            self.joueur.deterDirection()
            self.joueur.posprec = self.joueur.pos

        if self.joueur.bougervers == 'est':
            mvtvoulu = (1, 0)
        elif self.joueur.bougervers == 'ouest':
            mvtvoulu = (-1, 0)
        elif self.joueur.bougervers == 'nord':
            mvtvoulu = (0, -1)
        elif self.joueur.bougervers == 'sud':
            mvtvoulu = (0, 1)
        else:
            mvtvoulu = (0, 0)

        if mvtactuel == mvtvoulu:  # même direction
            pass
        elif mvtactuel == tuple(-i for i in mvtvoulu):  # direction inverse
            self.mvtprec = self.joueur.bougervers
            mvtactuel = mvtvoulu
        else:  # virage
            produitscalaire = abs(sum(i*j for i, j in
                                      zip(diffcase, mvtactuel)))
            if produitscalaire <= distance and not\
               self.labyrinthe.blocExiste(math.floor(self.joueur.pos[1] +
                                                     mvtvoulu[1]),
                                          math.floor(self.joueur.pos[0] +
                                                     mvtvoulu[0])):
                distance -= normediffcase  # perte de distance partielle
                self.mvtprec = self.joueur.bougervers
                mvtactuel = mvtvoulu
            else:
                pass  # on continue dans la même direction

        posvoulue = (self.joueur.pos[0]+distance*mvtactuel[0],
                     self.joueur.pos[1]+distance*mvtactuel[1])
        if not self.labyrinthe.blocExiste(math.floor(posvoulue[1] +
                                          mvtactuel[1]/2+0.5),
                                          math.floor(posvoulue[0] +
                                                     mvtactuel[0]/2+0.5)):
            self.joueur.pos = posvoulue
        else:
            if self.mvtprec == 'est':
                posx = math.floor(posvoulue[0])
            elif self.mvtprec == 'ouest':
                posx = math.ceil(posvoulue[0])
            else:
                posx = posvoulue[0]
            if self.mvtprec == 'nord':
                posy = math.ceil(posvoulue[1])
            elif self.mvtprec == 'sud':
                posy = math.floor(posvoulue[1])
            else:
                posy = posvoulue[1]

            self.joueur.pos = (posx, posy)

        self.joueur.deplacer(self.joueur.pos)
        self.joueur.orienter(self.mvtprec)

        # gestion des nourritures
        casesoccupe = list()
        macase = tuple(math.floor(i+0.5) for i in self.joueur.pos)
        casesoccupe.append(macase)
        for joueur in self.tortues.keys():
            if joueur != self.monpseudo:
                casesoccupe.append(tuple(math.floor(i+0.5) for i in
                                   self.tortues[joueur][-1].pos))

        for posjoueur in casesoccupe:
            if self.labyrinthe.bouffeExiste(posjoueur):
                self.labyrinthe.detruireBouffe(posjoueur)

        # gestion des pilules
        for posjoueur in casesoccupe:
            if self.labyrinthe.piluleExiste(posjoueur):
                self.labyrinthe.detruirePilule(posjoueur)
                if posjoueur == macase:  # c'est nous, avec la pilule
                    self.joueur.energie = True
                    self.joueur.color('lightgreen')
                    self.pilulechrono.reset()
        # autres tortues
        for joueur in self.tortues.keys():
            if joueur != self.monpseudo:
                if self.tortues[joueur][3]:
                    self.tortues[joueur][-1].color('green')
                else:
                    self.tortues[joueur][-1].color('red')

        # collisions avec les monstres
        caseoccupe = []  # on réinitialise
        for monstre in self.monstres.keys():
            posmonstre = self.monstres[monstre][-1].pos
            if self.monstres[monstre][2]:  # monstre en vie
                caseoccupe.append(tuple(math.floor(i+0.5) for i in
                                  self.monstres[monstre][-1].pos))

        for joueur in self.tortues.keys():
            if joueur != self.monpseudo:
                if not self.tortues[joueur][2]:
                    self.tortues[joueur][-1].hideturtle()

        # si les monstres meurent
        for monstre in self.monstres.keys():
            if self.monstres[monstre][2]:
                self.monstres[monstre][-1].showturtle()
            else:
                self.monstres[monstre][-1].hideturtle()

        if macase in caseoccupe and not self.joueur.energie:
            self.joueur.vie = False
            self.joueur.hideturtle()

        if self.pilulechrono.get() >= self.tempsbonus:  # temps bonus dépassé
            self.joueur.energie = False
            self.joueur.color('yellow')

        self.fen.update()
        self.fen.ontimer(self.go, 0)
