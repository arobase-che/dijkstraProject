""" Fait par Hédy et Miguel le 24 septembre """ 

from codeBase import *
import codeBase 
import math
import os
import time

prefixFile = "paris_mod_"

noeudDebut = 1
noeudFin   = 100

flecheActive = False
showBestNode = True
showUsedNode = True
showBestArrow= False
showArrow    = True
showValueArc = False

colorNode      = 'red'
colorBestNode  = 'blue'
colorUsedNode  = 'yellow'
colorBestArrow = 'magenta' 
colorArrow     = 'black'
colorBG        = 'white'

maxDistance = 0
maxSecurite = 0
nbNoeud     = 0

enableScale  = False
enableAstart = True

zoom = False

def distanceManhattan( XY1, XY2 ):
  return math.sqrt((XY1[0]-XY2[0])**2+(XY1[1]-XY2[1])**2)
def getEstimation( graphe, noeud, arc, scale) :
  global maxDistance, maxSecurite
  distance = arc[1]
  insecurite = arc[2]
  if enableScale :
    return distance / maxDistance * scale + insecurite / maxSecurite * (1-scale)
  else:
    if enableAstart :
      X1 = getXY(graphe[arc[0]][1][2],graphe[arc[0]][1][3])
      X2 = getXY(graphe[noeudFin][1][2],graphe[noeudFin][1][3])
      print(arc[0],((X2[0]-X1[0])*(X2[0]-X1[0])+(X2[1]-X1[1])*(X2[1]-X1[1])))
      return distance + distanceLongLat((graphe[arc[0]][1][0], graphe[arc[0]][1][1]), (graphe[noeudFin][1][0], graphe[noeudFin][1][1])) #distanceManhattan(X1, X2)
    else:
      return distance

def tracerArc(canvas, graphe):
  for noeud in graphe :
    for arcs in noeud[2]:
      canvas.create_line(int(noeud[1][2]*codeBase.ratio)+codeBase.border, codeBase.winHeight - int(noeud[1][3]*codeBase.ratio)-codeBase.border, int(graphe[arcs[0]][1][2]*codeBase.ratio)+codeBase.border, codeBase.winHeight - int(graphe[arcs[0]][1][3]*codeBase.ratio)-codeBase.border, fill=colorArrow)
      if showValueArc :
        canvas.create_text( ( int(noeud[1][2]*codeBase.ratio)+codeBase.border + int(graphe[arcs[0]][1][2]*codeBase.ratio)+codeBase.border) /2
                       ,  ( codeBase.winHeight - int(noeud[1][3]*codeBase.ratio)-codeBase.border + codeBase.winHeight - int(graphe[arcs[0]][1][3]*codeBase.ratio)-codeBase.border ) /2 - 10
                       ,  text = str(arcs[1])) 

def minDist(aParc, dist) :
  if aParc == []:
    return -1
  minNoeud = aParc[0]
  for noeud in aParc[1:]:
    if dist[noeud][0] < dist[minNoeud][0] :
      minNoeud = noeud
  return minNoeud

def getAbsolutDistance( graphe, noeudA, noeudB ):
  return math.sqrt(graphe[noeudA][1][0]*graphe[noeudB][1][0]+graphe[noeudA][1][1]*graphe[noeudB][1][1])

def dijkstra(graphe, debut, fin, scale):
   # Distance contient les distances minimales calculées à partir de debut et le dernier élement permettant d'acceder à celui-ci
   #       (Distance, Noeud précedent le plus proche)
  dist = [(-1,-1)]*len(graphe)

  dist[debut] = (0,debut)
  if enableAstart : 
    dist[debut] = (distanceManhattan((graphe[debut][1][2], graphe[debut][1][3]), (graphe[fin][1][2], graphe[fin][1][3])), debut)
  aParc = [debut]
  proche = debut
  while aParc != [] and proche != fin :

    for arc in graphe[proche][2]:
      if dist[arc[0]][0] == -1 :
        dist[arc[0]] = (dist[proche][0]+getEstimation(graphe, proche, arc, scale) ,proche)
        #dist[arc[0]] = (dist[proche][0]+(getEstimation(arc[1], arc[2], scale)),proche)
        aParc.append(arc[0])
      else:
        if dist[arc[0]][0] > dist[proche][0]+getEstimation(graphe, proche, arc, scale) :
          dist[arc[0]] = (dist[proche][0]+getEstimation(graphe, proche, arc, scale),proche)

    aParc.remove(proche)
    proche = minDist(aParc,dist)

  return dist

def calChemin(dist, debut, fin):
  chemin = []
  distanceTotal = 0
  insecuriteTotal = 0
  enCour = fin
  while enCour != debut :
    chemin.append(enCour)
    #for arc in graphe[dist[enCour][1]][2]:
      #if arc[0] == enCour :
        #distanceTotal += arc[1]
        #insecuriteTotal += arc[2]
    enCour = dist[enCour][1]

  chemin.append(noeudDebut)
  chemin.reverse()
  for i,noeud in enumerate(chemin[:-1]):
    arcInteressants = [ arc for arc in graphe[noeud][2] if arc[0] == chemin[i+1]]
    if len(arcInteressants) != 1 :
      print("J'ai trouvé une couille !")
    distanceTotal += arcInteressants[0][1]
    insecuriteTotal += arcInteressants[0][2]
    #print("J'ajoute " + str(arcInteressants[0][1]) + " a " + str(distanceTotal-arcInteressants[0][1]) + " = " + str(distanceTotal))

  return (chemin, distanceTotal, insecuriteTotal)
  
def tracerChemin(canvas, graphe, dist, debut, fin):
  enCour = fin
  while enCour != debut :
    if showBestArrow :
      canvas.create_line(int(graphe[dist[enCour][1]][1][2]*codeBase.ratio)+codeBase.border, codeBase.winHeight - int(graphe[dist[enCour][1]][1][3]*codeBase.ratio)-codeBase.border, int(graphe[enCour][1][2]*codeBase.ratio)+codeBase.border, codeBase.winHeight - int(graphe[enCour][1][3]*codeBase.ratio)-codeBase.border, fill=colorBestArrow, arrow=LAST)
    if showBestNode :
      dessinNoeud(canvas,graphe[enCour],colorBestNode)
    enCour = dist[enCour][1]

def tracerNoeudsActifs(canvas, graphe, dist):
  for i,x in enumerate(dist) :
    if x != (-1,-1) :
      dessinNoeud(canvas,graphe[i],colorUsedNode)
  


graphe = []

def getNode( nodeStr ) :
  nodeList = nodeStr.split('\t')
  #       ( "Identifiant" , "Corde au nez" , "List Sucesseurs (Arcs)" )
  
  return (int(nodeList[0]), [float(nodeList[1])*math.pi/180, float(nodeList[2])*math.pi/180,0,0], [] )

def getArc( arcStr ) :
  arcStr = arcStr.split('\t')
  #      ( "Origine"    , "Destination" , "Distance" , "Insecurité")
  return (int(arcStr[0]), int(arcStr[1]), float(arcStr[2]), float(arcStr[3]))



def calDistance( dist ) :
  if len(dist) <= 1 :
    return (0,0)
  else:
    print(dist[0])
    for arc in graphe[dist[0][1]][2]:
      if arc[0] == dist[1][1]:
        return calDistance(dist[1:]) + (arc[1],arc[2])
    print("Erreur dans le parcourt")
    return (-100000,-1000000)
   


def startDijkstra(can,inputDebut,inputFin, scale):
    global noeudDebut
    global noeudFin
    can.delete(ALL)
    print("Calcule de dijkstra")
    try :
      noeudDebut = int(inputDebut.get())
    except:
      print("Veuillez entrez un entrer")

    try :
      noeudFin   = int(inputFin.get())
    except:
      print("Veuillez entrez un entrer")

    tU1, tP1 = time.time(),time.clock()
    print(scale.get())
    dist = dijkstra(graphe, noeudDebut, noeudFin, float(100-scale.get())/100)

    tP2,tU2 = time.clock(),time.time()
    print(tP2-tP1, "s / ", tU2-tU1, "s")

    chemin, distanceTotal, insecuriteTotal = calChemin(dist, noeudDebut, noeudFin)
    print(chemin)
    print(len(chemin))
    print( "Indice entre ", noeudDebut, " et ", noeudFin, " : ", dist[noeudFin][0])
    print( "Distance entre ", noeudDebut, " et ", noeudFin, " : ", distanceTotal)
    print( "Insecurite entre ", noeudDebut, " et ", noeudFin, " : ", insecuriteTotal)

    print("Dessin des noeuds et Arcs")
    dessinGraphe(can,graphe, colorNode)
    if showUsedNode :
      tracerNoeudsActifs(can, graphe, dist)
    if showArrow :
      tracerArc(can, graphe)
    tracerChemin(can, graphe, dist, noeudDebut, noeudFin)






def bouclePrincipaleGUI( ) :
  print("Mise à l'echelle")
  if zoom :
    miseEchelle([graphe[i] for i,k in enumerate(dist) if k != (-1,-1)])
  else:
    miseEchelle(graphe)
  #print(graphe) 



  print("Initialisation de Tkinter")

  fen = Tk()
  buttonQuit=Button(fen, text="quitter", command=fen.destroy) # Bouton qui détruit la fenêtre
  can = Canvas(fen, width = winWidth, height = winHeight, bg =colorBG)

  inputDebut = Entry(fen,width=7)
  inputFin = Entry(fen,width=7)
  scale=Scale(fen,orient=VERTICAL) # Bouton qui lance la recherche
  buttonStart=Button(fen, text="Lancer", command=(lambda : startDijkstra(can,inputDebut,inputFin, scale))) # Bouton qui lance la recherche
  inputDebut.place(x=20,y=20)
  inputFin.place(x=20,y=60)
  buttonStart.place( x=20, y=100)
  scale.place(x=20, y=180)
  buttonQuit.place(x=20, y=140)        # insère le bouton dans la fenêtre


  can.place(x=100)
  can.delete(ALL)

  print("Main loop")
  fen.mainloop()


  
print("Lecture des Noeuds")
with open( prefixFile + "noeuds.csv",'r') as fichier:
  for line in fichier:
    line = line.rstrip('\n')
    graphe.append( getNode(line) )
    nbNoeud+=1


print("Lecture des Arcs")
with open( prefixFile + "arcs.csv",'r') as fichier:
  for line in fichier:
    line = line.rstrip('\n')
    arc = getArc( line )
    if( arc[2] > maxDistance ) :
      maxDistance = arc[2]
    if( arc[3] > maxSecurite ) :
      maxSecurite = arc[3]
    graphe[arc[0]][2].append( (arc[1], arc[2], arc[3] ) )

print("Il y a " + str(nbNoeud))
print("La distance maximum est " + str(maxDistance))
print("La sécurite maximum est " + str(maxSecurite))

bouclePrincipaleGUI()

