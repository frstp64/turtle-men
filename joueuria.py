#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contient la classe de l'intelligence artificielle"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None

from tmen import TMen
import math
import random


class JoueurIA(TMen):
    """Classe qui détermine le mouvement que le joueur devrait faire"""
    def __init__(self, fen, color, nom, taille, monstres):
        """initialisation"""
        super().__init__(fen, color, nom, taille)
        self.bougervers = 'est'
        self.monstres = monstres
        self.posprec = (0, 0)  # position précédente

    def deterDirection(self):
        """Détermine la direction à prendre selon l'état du jeu"""
        casedanger = []
        for monstre in self.monstres.keys():
            casemonstrex = math.floor(self.monstres[monstre][0][0])
            casemonstrey = math.floor(self.monstres[monstre][0][1])
            casedanger.append((casemonstrex, casemonstrey))

        macase = tuple(math.floor(i) for i in self.pos)
        casesdevant = list()
        # on regarde les 4 cases cases devant nous (T inversé)
        if self.bougervers == 'est':
            casesdevant.append((macase[0]+1, macase[1]))
            casesdevant.append((macase[0]+2, macase[1]))
            casesdevant.append((macase[0]+1, macase[1]+1))
            casesdevant.append((macase[0]+1, macase[1]-1))
        elif self.bougervers == 'ouest':
            casesdevant.append((macase[0]-1, macase[1]))
            casesdevant.append((macase[0]-2, macase[1]))
            casesdevant.append((macase[0]-1, macase[1]+1))
            casesdevant.append((macase[0]-1, macase[1]-1))
        elif self.bougervers == 'nord':
            casesdevant.append((macase[0], macase[1]-1))
            casesdevant.append((macase[0], macase[1]-2))
            casesdevant.append((macase[0]+1, macase[1]-1))
            casesdevant.append((macase[0]-1, macase[1]-1))
        elif self.bougervers == 'sud':
            casesdevant.append((macase[0], macase[1]+1))
            casesdevant.append((macase[0], macase[1]+2))
            casesdevant.append((macase[0]+1, macase[1]+1))
            casesdevant.append((macase[0]-1, macase[1]+1))

        if self.posprec != self.pos:  # pas bloqué
            for case in casesdevant:
                if case in casedanger and not self.energie:  # inverser
                    if self.bougervers == 'est':
                        self.bougervers = 'ouest'
                    elif self.bougervers == 'ouest':
                        self.bougervers = 'est'
                    elif self.bougervers == 'nord':
                        self.bougervers = 'sud'
                    elif self.bougervers == 'sud':
                        self.bougervers = 'nord'
                    break  # pour éviter de foncer dans deux monstres
                # sinon on continue

        else:  # bloqué par un mur
            if self.bougervers in ('nord', 'sud'):
                self.bougervers = random.choice(('ouest', 'est'))
            else:
                self.bougervers = random.choice(('nord', 'sud'))
