#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe des tortues"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None
from acteur import Acteur
from turtle import Shape

# 12x12 pixels!
corps = ((-6, -2), (-6, 2), (-5, 3), (-5, 4), (-4, 5), (-3, 5),
        (-2, 6), (2, 6), (3, 5), (4, 5), (5, 4), (5, 3),
        (4, 3), (3, 2), (1, 2), (0, 1), (-1, 1), (-2, 0),
        (-1, -1), (0, -1), (1, -2), (3, -2), (4, -3), (5, -3),
        (5, -4), (4, -5), (3, -5), (2, -6), (-2, -6), (-3, -5),
        (-4, -5), (-5, -4), (-5, -3))


class TMen(Acteur):
    """Classe qui gère les tortues du joueur et de ses adversaires"""
    def __init__(self, fen, color, nom, taille):
        """Initialise correctement la tortue"""
        super().__init__(fen)
        self.deplacer((3, 3))  # enlever après
        pacman = Shape('polygon', corps)
        self.right(90)

        self.taille = taille/25
        self.nom = nom
        fen.register_shape('j'+self.nom, pacman)
        self.color(color)
        self.orienter('est')
        self.shapesize(self.taille, self.taille)
        self.shape('j'+self.nom)

    def orienter(self, direction):
        """Change l'orientation du regard"""
        self.orientation = direction
        if direction == 'est':
            self.setheading(-90)
        elif direction == 'sud':
            self.setheading(0)
        elif direction == 'nord':
            self.setheading(180)
        elif direction == 'ouest':
            self.setheading(90)
