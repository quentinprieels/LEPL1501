# LEPL1501
Modélisation de la grue du groupe 11.57 dans le cadre du cours Projet LEPL1501 du premier quadrimestre 2020 en ingénieur Civil.
Dans le cadre de ce projet, il faut concevoir une grue flottante permettant de construire une éolienne en mer.
Cette grue a d'abord été modélisée sur un logiciel de développement 3D appelé *[Fusion 360](https://www.autodesk.com/products/fusion-360/overview)*.
![La grue sur Fusion360](img/allCrane.png)
Le programme python ci-dessus a pour but de modéliser mathématiquement le comportement de cette grue.

## Données à entrer

Cette section est consacrée aux variables à rentrer pour les calculs. Le choix des différentes variables se fait dans le
fichier ```variables.py```.

- les coordonnées en x, y et z et leurs angles avec l'horizontale des différentes pièces de la grue :
    - grappin
    - contrepoids
    - les sections / bras de la grue :
        - section 1
        - section 2
        - section 3
        - section 4
    - la pièce déplacée

- les masses des différentes pièces de la grue
- les différentes constantes :
    - gravité
    - inertie
    - coefficient d'amortissement

## Données sorties par le programme 


Cette section est consacrée aux données sorties par le programme. Les graphiques sont créées en 2 phases :
- ```main.py``` : création des variables utilisées et applications de calculs
- ```graphs.py``` : création des graphiques

Les graphiques sont :
- L'angle en fonction du temps
- La vitesse angulaire en fonction du temps
- L'accélération en fonction du temps
- Le diagramme de phase
- Les coordonnées du centre de gravité et de poussée du système en fonction du temps
- Les différentes énergies du système en fonction du temps

<img src="https://raw.githubusercontent.com/quentinprieels/LEPL1501/master/img/motionCrane.png" width="18%"></img> 
<img src="https://raw.githubusercontent.com/quentinprieels/LEPL1501/master/img/centerGravity_centerThrust.png" width="18%"></img> 
<img src="https://raw.githubusercontent.com/quentinprieels/LEPL1501/master/img/omegaAndTheta.png" width="18%"></img> 
<img src="https://raw.githubusercontent.com/quentinprieels/LEPL1501/master/img/phaseDiagram.png" width="18%"></img> 
<img src="https://raw.githubusercontent.com/quentinprieels/LEPL1501/master/img/energy.png" width="18%"></img> 


## Conclusion

### Evolution :
Le programme à connu deux phases :
- Une première avec des équations approximative ne prenant pas en compte l'inertie de la barge ([voir le projet](https://github.com/Nimbelungen/projet1-1157)).
- Puis une évolution prenant en compte tous les paramètres possibles.

### Temps : 
Les différents programmeurs ont mis plusieurs jours pour en arriver là, le programme fonctionne bien.

### Modèle de grue utilisé :
Le modèle utilisé pour la grue est un bras mécanique géant.
