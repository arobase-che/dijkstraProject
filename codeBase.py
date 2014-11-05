# -*- coding: utf8 -*-
'''
Created on 1 sept. 2014

@author: team
'''

# --------------------------------------------------------------------------------------------
#      IMPORT
# --------------------------------------------------------------------------------------------

from tkinter import *       # pour affichage de la carte

import math                     # focntion trigo pour conversion en coordonnées cartésienne
import sys
# --------------------------------------------------------------------------------------------
#      STRUCTURES DE DONNEES
# --------------------------------------------------------------------------------------------

# definition des arcs ; tuple (dest, dist, insecurité)
# definition des succ : liste d'arcs
# definition coordonnées des noeuds : liste (long, lat, X,Y)
# definition noeud : tuple (ind, coord, succ)
# definition graphe : liste noeuds




# --------------------------------------------------------------------------------------------
#      VARIABLES GLOBALES
#       dimension fenetre et cercle
# --------------------------------------------------------------------------------------------
# fenetre

winWidth =1000     # largeur de la fenetre
winHeight = 700     # hauteur de la fenetre : recalculée en focntion de la taille du graphe
MaxHeight =600     # hauteur maximale de la fenetre
border = 20             # taille en px des bords

# decalration ratio mise a l'echelle

ratio= 1.0                  # rapport taille graphe / taille fenetre
ratioWidth = 1.0      #  rapport largeur graphe/ largeur de la fenetre
ratioHeight =1.0      #  rapport hauteur du graphe hauteur de la fenetre



#  cercle

rayon = 1              # rayon pour dessin des points
""" mettre 10 pour les graphes de tests
et mettre 1 pour les vrai graphes paris et berlin
"""



# longitude  et latitude min et max

# seront reccalculées à patir de la lecture du fichier

minLat = sys.maxsize
maxLat = 0
minLong = sys.maxsize
maxLong = 0
zoom = 1
origineX = 0
origineY = 0


# --------------------------------------------------------------------------------------------
#      FONCTIONS ANNEXES
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------
#   Calcul de la distance entre deux points
#   entrée : point - coordonnée long et lat en radian
#   sortie : distance entre les deux points en metre
# --------------------------------------------------------------------------

def distanceLongLat(pointA, pointB):
    longA = pointA[0]
    longB =pointB[0]
    latA = pointA[1]
    latB=pointB[1]

    deltaLong = longB - longA

    # distance angulaire en radian
    S_AB = math.acos(math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(deltaLong))

    # distance en metre= distance angulaire * rayon terre
    return (S_AB* 6378000)



# ---------------------------------------------------------------
#       fonction de dessin du graphe
# ---------------------------------------------------------------

#   dessin d'un cercle
#   entrée : coordonnée x, y (en px), rayon, couleur

def cercle(can,x,y,r,coul):
    can.create_oval(x-r, y-r, x+r, y+r, outline = coul, fill = coul)



#
#
def getXY( cX, cY) :
  return ((int(cX*ratio)+border)-origineX)*zoom+origineX, (winHeight - (int(cY*ratio)+ border)-origineY)*zoom+origineY

#   dessin d'un noeud
#   entrée : noeud, couleur

okK = False
def dessinNoeud(canvas,noeud, couleur):
    global okK
    # recupere les coord du neourd (long, lat)
    coord = noeud[1]
    if not okK :
      print(ratio, border, origineX, zoom, origineY)
      okK = True
    long = ((int(coord[2]*ratio)+border)-origineX)*zoom+origineX
    lat = (winHeight - (int(coord[3]*ratio)+ border)-origineY)*zoom+origineY

    cercle(canvas,long, lat, rayon,couleur)
    #canvas.create_text(long, lat, text = str(noeud[0])) 



#   dessin d'un graphe
#   entrée : graphe, couleur

def dessinGraphe(canvas,graphe, couleur) :
    for noeud in graphe :
        dessinNoeud(canvas,noeud, couleur)


# dessin d'un chemin
# entrée : chemin, couleur

def dessinChemin(canvas,chemin, couleur) :
    for indNoeud in chemin :
        dessinNoeud(canvas,grapheParis[indNoeud], couleur)


# ---------------------------------------------------------------
#  calcul pour mise à l'echelle graphe / fenetre
#  calcule aussi les coordonnées cartesienne des points
# ---------------------------------------------------------------

def miseEchelle(graphe):
    # minimum lat, long
    global minLat
    global maxLat
    global minLong
    global maxLong
    global winWidth
    global winHeight
    global ratio



    # calcul des min en long et lat
    for noeud in graphe:
        coord = noeud[1]
        longval = coord[0]
        lat = coord[1]
        minLat = min(lat, minLat)
        minLong = min(longval, minLong)
        maxLat = max(lat,maxLat)
        maxLong = max(longval, maxLong)


    # calcule de l'absisse - distance a un point de coordonnees(min long , meme lat)

    for noeud in graphe:
        coord = noeud[1]
        pointA = (coord[0], coord[1])
        pointB=(minLong, coord[1])
        x = distanceLongLat(pointA, pointB)
        coord[2] = x


    # calcule de l'ordonnee - distance a un point de coordonnees (meme long , min lat)

    for noeud in graphe:
        coord = noeud[1]
        pointA = (coord[0], coord[1])
        pointB=(coord[0], minLat)
        y = distanceLongLat(pointA, pointB)
        coord[3] = y


    # verification abscisse min max, ordonnee min max

    minX =  sys.maxsize
    minY = sys.maxsize
    maxX = 1
    maxY = 1

    for noeud in graphe:
        coord = noeud[1]
        x = coord[2]
        y = coord[3]
        minX= min(x, minX)
        minY = min(y, minY)
        maxX = max(x,maxX)
        maxY = max(y, maxY)


    # calcul des ratio

    ratio = (winWidth - 2*border) / (maxX )
    winHeight = int ( ratio *  (maxY)) + 2* border
    winHeight = min (winHeight, MaxHeight)
    ratio = min (ratio, (winHeight - 2*border) / (maxY))

#def tracerArc(canvas, graphe, couleur):                                               
#  for noeud in graphe :
#    for arcs in noeud[2]:
#      canvas.create_line(int(noeud[1][2]*ratio)+border, winHeight - int(noeud[1][3]*ratio)-border,int(graphe[arcs[0]][1][2]*ratio)+border, winHeight - int(graphe[arcs[0]][1][3]*ratio)-border, fill='black')

