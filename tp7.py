#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""interface ligne de commande principale de jeu"""
__auteur__ = "frstp64", "lpass2"
__date__ = "2014-12-03"
__coequipiers__ = None

import argparse
from clientreseau import *
from jeu import *


def analyseCarte(objetfichier):
    """Lis le fichier et renvoie une liste de chaines de caractères"""
    contenu = objetfichier.readlines()
    #enlever les caractères de fin de ligne ('\n' et '\n)
    for indice, chaine in enumerate(contenu):
        contenu[indice] = chaine.strip('\r\n')
    objetfichier.close()
    return contenu

###DÉBUT GESTION ARGUMENTS###

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Interface ligne de commande \
    pour Turtle-Men", conflict_handler="resolve")
    parser.add_argument("action", choices=['lister', 'créer', 'joindre'],
                        help="Action à effectuer")

    #arguments nécessaires à lister
    #(il n'y en a pas)

    #arguments nécessaires à créer
    parser.add_argument("-f", "--fichier", type=open,
                        help="nom du fichier")
    parser.add_argument("-t", "--tortues", default="1", type=int,
                        help=
                        "le nombre de tortues pour la partie, 1 par défaut")
    parser.add_argument("-n", "--monstres", default="4", type=int,
                        choices=range(5),
                        help="le nombre de monstres, 4 par défaut")
    parser.add_argument("-v", "--vitesse", default="3", type=int,
                        help="la vitesse en cases par seconde, 3 par défaut")
    parser.add_argument("-d", "--pilule", default="10", type=int,
                        help="la durée des pilules en secondes, 10 par défaut")

    #arguments nécessaires à joindre et créer
    parser.add_argument("-p", "--pseudo", help="le pseudonyme du joueur")

    #arguments nécessaire à joindre
    parser.add_argument("-c", "--createur", help="le pseudonyme du créateur")

    #optionnels généraux
    parser.add_argument("-m", "--mode", default="manuel",
                        choices=['manuel', 'auto'],
                        help=
                        "mode de commande de tortue, manuel par défaut")
    parser.add_argument(
        "-s", "--size", default="25", type=int,  # cases carrées
        help="Peut prendre une taille de bloc, 25 par défaut")

    args = parser.parse_args()

    #vérifier si certaines variables respectent des conditions
    if args.tortues < 1:
        raise ValueError('Nombre incorrect de tortues!')
    if args.vitesse <= 0:
        raise ValueError('La vitesse doit être supérieure à 0!')
    if args.pilule < 0:
        raise ValueError('La durée de la pilule doit être >= 0!')

    #méthode très brute pour rendre certaines options obligatoires
    if args.action in ('joindre', 'créer'):
        parser.add_argument("--pseudo", "-p", required=True,
                            help="le pseudonyme du joueur, nécessaire pour \
    joindre une partie")
        if args.action == 'créer':
            parser.add_argument("--fichier", "-f", type=open,
                                required=True, help="nom du fichier")
        if args.action == 'joindre':
            parser.add_argument("--createur", "-c", required=True,
                                help="le pseudonyme du créateur")
        args = parser.parse_args()

    ### FIN DE LA GESTION DES ARGUMENTS ###

    #lister les parties, ne requiert pas de pseudonyme, ce dernier est fictif
    if args.action == 'lister':
        parties = ClientReseau('loremipsumdolorsitamet',
                               'python.gel.ulaval.ca', 31415).lister()
        print('{:*^60}'.format("Parties en attente de joueurs"))
        print('{:^30}{:^30}'.format('Créateur', 'Nombre de places libres'))
        for pseudonyme in parties:
            print('{:<30}{:>30}'.format(pseudonyme, parties[pseudonyme]))
        print()

    #joindre une partie
    elif args.action in ('joindre', 'créer'):
        lienreseau = ClientReseau(args.pseudo, 'python.gel.ulaval.ca', 31415)
        #créer une partie requiert seulement l'envoi d'info en plus
        if args.action == 'créer':
            infopartie = lienreseau.creer(args.tortues,
                                          (analyseCarte(args.fichier),
                                           args.vitesse,
                                           args.pilule, args.monstres))
        else:
            infopartie = lienreseau.joindre(args.createur)

        #lancement de la partie
        try:
            partie = Jeu(infopartie, lienreseau, args.pseudo,
                         args.mode, args.size)
        except:
            pass
