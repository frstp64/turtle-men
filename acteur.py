#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe qui décrit la notion d'acteur"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None
from turtle import RawTurtle


class Acteur(RawTurtle):
    """Classe décrivant l'objet d'acteur"""
    def __init__(self, fen):
        """Initialise une instance d'acteur"""
        super().__init__(fen)
        self.fen = fen
        self.penup()
        self.orientation = 'est'
        self.vie = True
        self.energie = False
        self.pos = (0, 0)

    def deplacer(self, pos):
        """Déplace l'acteur"""
        x, y = pos
        self.pos = pos
        self.goto(x+0.5, y+0.5)

    def getStatus(self):
        """Permet de recevoir l'état de l'acteur sous forme de tuple"""
        return (self.pos, self.orientation, self.vie, self.energie)
