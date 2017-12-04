#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe de labyrinthe"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None
import turtle


def lget(liste, *index, default=' '):
    """Accède un élément de liste, renvoie default si mauvais index
       similaire à la méthode get d'un dictionnaire, récursion possible"""
    try:
        if len(index) > 1:
            return lget(liste[index[0]], *index[1:], default=default)
        else:
            return liste[index[0]]
    except IndexError:  # index incorrect
        return default


class Labyrinthe():
    """Classe qui gère le labyrinthe: carte, grains, pilules"""
    def __init__(self, canvas, carte, taillebloc):
        self.canvas = canvas  # instance sur laquelle il faut dessiner
        self.carte = carte  # la carte à dessiner
        self.taillebloc = taillebloc  # taille individuelle des blocs
        self.pilules = dict()  # dictionnaire des pilules
        self.bouffes = dict()  # dictionnaire des bouffes

        self.canvas.setworldcoordinates(0, len(self.carte),
                                        max(len(i) for i in self.carte), 0)
        self.canvas.bgcolor("black")

        # création de la tortue qui va dessiner tout
        self.cartographe = turtle.RawTurtle(self.canvas)
        self.cartographe.penup()
        self.cartographe.color('blue')
        self.cartographe.pensize(self.taillebloc/5)
        if self.taillebloc/5 < 1:
            self.cartographe.pensize(1)  # dans le cas d'une petite taille
        self.cartographe.hideturtle()  # ne pas cacher pour debug
        self.canvas.tracer(0)
        self.afficherLabyrinthe()
        self.afficherBouffes()
        self.afficherPilules()
        self.canvas.update()

    def posDebut(self, char):
        """Retourne la position de départ"""
        for indexy, ligne in enumerate(self.carte):
            for indexx, caractere in enumerate(ligne):
                if caractere.upper() == char.upper():
                    return (indexx, indexy)

    def blocExiste(self, *position):
        """Retourne True si un bloc se trouve à une position (y, x)"""
        return lget(self.carte, *position) == 'X'

    def dessinerLigne(self, xa, ya, xb, yb):
        """ Dessine une ligne"""
        self.cartographe.goto(xa, ya)
        self.cartographe.pendown()
        self.cartographe.goto(xb, yb)
        self.cartographe.penup()

    def dessinerCoin(self, x, y, delta, location):
        """ Dessine un coin rond"""
        if location == 'hd':  # haut droit
            self.cartographe.goto(x+1-delta, y)
            self.cartographe.setheading(0)
        if location == 'bd':  # bas droit
            self.cartographe.goto(x+1, y+1-delta)
            self.cartographe.setheading(90)
        if location == 'bg':  # bas gauche
            self.cartographe.goto(x+delta, y+1)
            self.cartographe.setheading(180)
        if location == 'hg':  # haut gauche
            self.cartographe.goto(x, y+delta)
            self.cartographe.setheading(270)

        self.cartographe.pendown()
        self.cartographe.circle(delta, extent=90)
        self.cartographe.penup()

    def afficherLabyrinthe(self):
        """Affiche la carte (généralement une bonne idée)"""
        #delta = 2 ** 0.5 - 1
        delta = 0.2
        for indexligne, ligne in enumerate(self.carte):
            for indexbloc, bloc in enumerate(ligne):
                # 4 cotés
                if bloc == 'X':
                    # côté haut
                    if lget(self.carte, indexligne-1, indexbloc) != 'X':  # ^
                        self.dessinerLigne(indexbloc+delta, indexligne,
                                           indexbloc+1-delta, indexligne)
                    # coin haut droit
                    if lget(self.carte, indexligne-1, indexbloc+1) != 'X':
                        if lget(self.carte, indexligne-1, indexbloc) != 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc+1) != 'X':
                            self.dessinerCoin(indexbloc, indexligne,
                                              delta, 'hd')
                        elif lget(self.carte, indexligne-1, indexbloc) != 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc+1) == 'X':
                            self.dessinerLigne(indexbloc+1-delta, indexligne,
                                               indexbloc+1, indexligne)
                        elif lget(self.carte, indexligne-1, indexbloc) == 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc+1) != 'X':
                            self.dessinerLigne(indexbloc+1, indexligne,
                                               indexbloc+1, indexligne+delta)
                    # côté droit
                    if lget(self.carte, indexligne, indexbloc+1) != 'X':  # >
                        self.dessinerLigne(indexbloc+1, indexligne+delta,
                                           indexbloc+1, indexligne+1-delta)
                    # coin bas droit
                    if lget(self.carte, indexligne+1, indexbloc+1) != 'X':
                        if lget(self.carte, indexligne+1, indexbloc) != 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc+1) != 'X':
                            self.dessinerCoin(indexbloc, indexligne,
                                              delta, 'bd')
                        elif lget(self.carte, indexligne, indexbloc+1) != 'X'\
                                and lget(self.carte,
                                         indexligne+1, indexbloc) == 'X':
                            self.dessinerLigne(indexbloc+1, indexligne+1-delta,
                                               indexbloc+1, indexligne+1)
                        elif lget(self.carte, indexligne, indexbloc+1) == 'X'\
                                and lget(self.carte,
                                         indexligne+1, indexbloc) != 'X':
                            self.dessinerLigne(indexbloc+1, indexligne+1,
                                               indexbloc+1-delta, indexligne+1)
                    # côté bas
                    if lget(self.carte, indexligne+1, indexbloc) != 'X':  # v
                        self.dessinerLigne(indexbloc+1-delta, indexligne+1,
                                           indexbloc+delta, indexligne+1)
                    # coin bas gauche
                    if lget(self.carte, indexligne+1, indexbloc-1) != 'X':
                        if lget(self.carte, indexligne+1, indexbloc) != 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc-1) != 'X':
                            self.dessinerCoin(indexbloc, indexligne,
                                              delta, 'bg')
                        elif lget(self.carte, indexligne, indexbloc-1) == 'X'\
                                and lget(self.carte,
                                         indexligne+1, indexbloc) != 'X':
                            self.dessinerLigne(indexbloc+delta, indexligne+1,
                                               indexbloc, indexligne+1)
                        elif lget(self.carte, indexligne, indexbloc-1) != 'X'\
                                and lget(self.carte,
                                         indexligne+1, indexbloc) == 'X':
                            self.dessinerLigne(indexbloc, indexligne+1,
                                               indexbloc, indexligne+1-delta)
                    # côté gauche
                    if lget(self.carte, indexligne, indexbloc-1) != 'X':  # <
                        self.dessinerLigne(indexbloc, indexligne+1-delta,
                                           indexbloc, indexligne+delta)
                    # coin haut gauche
                    if lget(self.carte, indexligne-1, indexbloc-1) != 'X':
                        if lget(self.carte, indexligne-1, indexbloc) != 'X'\
                                and lget(self.carte,
                                         indexligne, indexbloc-1) != 'X':
                            self.dessinerCoin(indexbloc, indexligne,
                                              delta, 'hg')
                        elif lget(self.carte, indexligne, indexbloc-1) != 'X'\
                                and lget(self.carte,
                                         indexligne-1, indexbloc) == 'X':
                            self.dessinerLigne(indexbloc, indexligne+delta,
                                               indexbloc, indexligne)
                        elif lget(self.carte, indexligne, indexbloc-1) == 'X'\
                                and lget(self.carte,
                                         indexligne-1, indexbloc) != 'X':
                            self.dessinerLigne(indexbloc, indexligne,
                                               indexbloc+delta, indexligne)

                elif bloc != 'X':
                    # coin haut droit
                    if lget(self.carte, indexligne-1, indexbloc) == 'X' and\
                       lget(self.carte, indexligne, indexbloc+1) == 'X':
                        self.dessinerCoin(indexbloc, indexligne, delta, 'hd')
                    # coin bas droit
                    if lget(self.carte, indexligne, indexbloc+1) == 'X' and\
                       lget(self.carte, indexligne+1, indexbloc) == 'X':
                        self.dessinerCoin(indexbloc, indexligne, delta, 'bd')
                    # coin bas gauche
                    if lget(self.carte, indexligne+1, indexbloc) == 'X' and\
                       lget(self.carte, indexligne, indexbloc-1) == 'X':
                        self.dessinerCoin(indexbloc, indexligne, delta, 'bg')
                    # coin haut gauche
                    if lget(self.carte, indexligne, indexbloc-1) == 'X' and\
                       lget(self.carte, indexligne-1, indexbloc) == 'X':
                        self.dessinerCoin(indexbloc, indexligne, delta, 'hg')

    def afficherBouffes(self):
        """Affiche initialement la nourriture"""
        self.cartographe.shape('circle')
        self.cartographe.color('yellow')
        if self.taillebloc/5 < 1:
            taillepoint = 1
        else:
            taillepoint = self.taillebloc/5
        self.cartographe.shapesize(taillepoint/25, taillepoint/25)

        for indexligne, ligne in enumerate(self.carte):
            for indexbloc, bloc in enumerate(ligne):
                if bloc == '.':
                    self.bouffes[(indexbloc, indexligne)] = True
                    self.cartographe.goto(indexbloc+0.5, indexligne+0.5)
                    self.cartographe.pendown()
                    self.bouffes[(indexbloc, indexligne)] =\
                        self.cartographe.stamp()
                    self.cartographe.penup()

    def bouffeExiste(self, position):
        """Retourne True si il y a un grain dans la position donnée"""
        return position in self.bouffes

    def detruireBouffe(self, position):
        """Enlève un grain de nourriture si ce dernier se fait engloutir"""
        self.cartographe.clearstamp(self.bouffes[position])
        del self.bouffes[position]

    def afficherPilules(self):
        """Affiche initialement les pilules"""
        self.cartographe.shape('circle')
        self.cartographe.color('red')
        if self.taillebloc/3 < 2:
            taillepoint = 2
        else:
            taillepoint = self.taillebloc/3
        self.cartographe.shapesize(taillepoint/10, taillepoint/10)

        for indexligne, ligne in enumerate(self.carte):
            for indexbloc, bloc in enumerate(ligne):
                if bloc == 'O':
                    self.bouffes[(indexbloc, indexligne)] = True
                    self.cartographe.goto(indexbloc+0.5, indexligne+0.5)
                    self.cartographe.pendown()
                    self.pilules[(indexbloc, indexligne)] =\
                        self.cartographe.stamp()
                    self.cartographe.penup()

    def piluleExiste(self, position):
        """Retourne True si il y a une pilule dans la position donnée"""
        return position in self.pilules

    def detruirePilule(self, position):
        """enlève une pilule si elle est mangée"""
        self.cartographe.clearstamp(self.pilules[position])
        del self.pilules[position]
