#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe du joueur humain"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None
from tmen import TMen


class JoueurHumain(TMen):
    """Classe qui gère les mouvements du joueur humain"""

    def __init__(self, fen, color, nom, taille):
        """initialisation"""
        super().__init__(fen, color, nom, taille)
        self.bougervers = 'est'
        self.position = [0, 0]

    def toucheLeft(self):
        """Si le joueur veut aller à gauche"""
        self.fen.onkeypress(None, 'Left')
        self.bougervers = 'ouest'
        self.fen.onkeypress(self.toucheLeft, 'Left')

    def toucheRight(self):
        """Si le joueur veut aller à droite"""
        self.fen.onkeypress(None, 'Right')
        self.bougervers = 'est'
        self.fen.onkeypress(self.toucheRight, 'Right')

    def toucheUp(self):
        """Si le joueur veut aller vers le haut"""
        self.fen.onkeypress(None, 'Up')
        self.bougervers = 'nord'
        self.fen.onkeypress(self.toucheUp, 'Up')

    def toucheDown(self):
        """Si le joueur veut aller vers le bas"""
        self.fen.onkeypress(None, 'Down')
        self.bougervers = 'sud'
        self.fen.onkeypress(self.toucheDown, 'Down')
