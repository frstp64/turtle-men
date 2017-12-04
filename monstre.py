#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe des monstres"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None
from turtle import Shape
from acteur import Acteur

# forme original de 14x14 pixels -> [-7, 7],[-7, 7]

fantomeCorps = ((-7, -7), (-7, 0), (-6, 3), (-4, 5),
                (0, 7), (4, 5), (6, 3), (7, 0),
                (7, -7), (5, -5), (3, -7), (2, -7),
                (2, -5), (-2, -5), (-2, -7), (-3, -7),
                (-5, -5))

fantomeOeilG = ((-3, 0), (-4, 1), (-4, 3), (-3, 4),
                (-2, 4), (-1, 3), (-1, 1), (-2, 0))
fantomePupilleG = ((-3, 1), (-3, 2), (-2, 2), (-2, 1))

fantomeOeilD = ((3, 0), (4, 1), (4, 3), (3, 4),
                (2, 4), (1, 3), (1, 1), (2, 0))
fantomePupilleD = ((3, 1), (3, 2), (2, 2), (2, 1))


class Monstre(Acteur):
    """Classe qui contient la description des monstres"""
    def __init__(self, fen, color, nom, taille):
        """Initialise l'instance de monstre"""
        super().__init__(fen)
        self.right(90)
        self.nom = nom
        self.taille = taille/25  # taille du sprite

        fantomee = Shape('compound')
        fantomee.addcomponent(fantomeCorps, color)
        fantomee.addcomponent(fantomeOeilG, 'white')
        fantomee.addcomponent(fantomeOeilD, 'white')
        fantomee.addcomponent
        (tuple((x+1, y) for x, y in fantomePupilleG), 'blue')
        fantomee.addcomponent
        (tuple((x+1, y) for x, y in fantomePupilleD), 'blue')

        fantomeo = Shape('compound')
        fantomeo.addcomponent(fantomeCorps, color)
        fantomeo.addcomponent(fantomeOeilG, 'white')
        fantomeo.addcomponent(fantomeOeilD, 'white')
        fantomeo.addcomponent
        (tuple((x-1, y) for x, y in fantomePupilleG), 'blue')
        fantomeo.addcomponent
        (tuple((x-1, y) for x, y in fantomePupilleD), 'blue')

        fantomen = Shape('compound')
        fantomen.addcomponent(fantomeCorps, color)
        fantomen.addcomponent(fantomeOeilG, 'white')
        fantomen.addcomponent(fantomeOeilD, 'white')
        fantomen.addcomponent
        (tuple((x, y+2) for x, y in fantomePupilleG), 'blue')
        fantomen.addcomponent
        (tuple((x, y+2) for x, y in fantomePupilleD), 'blue')

        fantomes = Shape('compound')
        fantomes.addcomponent(fantomeCorps, color)
        fantomes.addcomponent(fantomeOeilG, 'white')
        fantomes.addcomponent(fantomeOeilD, 'white')
        fantomes.addcomponent
        (tuple((x, y-1) for x, y in fantomePupilleG), 'blue')
        fantomes.addcomponent
        (tuple((x, y-1) for x, y in fantomePupilleD), 'blue')

        fen.register_shape(self.nom+'est', fantomee)
        fen.register_shape(self.nom+'ouest', fantomeo)
        fen.register_shape(self.nom+'nord', fantomen)
        fen.register_shape(self.nom+'sud', fantomes)
        self.orienter('est')
        self.shapesize(self.taille, self.taille)

    def orienter(self, direction):
        """Change l'orientation du regard vers l'est"""
        self.shape(self.nom+direction)
