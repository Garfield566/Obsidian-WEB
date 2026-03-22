---
title: "Résumé de cours : Généralités sur les espaces vectoriels"
source: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=mathsup/cours/ev.html"
author:
  - "[[Fred Bayart]]"
published:
created: 2026-03-22
description: "Ressources de mathématiques"
tags:
  - "clippings"
image:
---
désigne le corps ou .

Structure d'espace vectoriel

On appelle espace vectoriel sur (ou -espace vectoriel) un ensemble muni de deux lois:

- une loi interne, notée , telle que soit un groupe commutatif. L'élément nul est noté .
- une loi externe, notée , qui est une application de dans vérifiant:
	1. .
		2. .
		3. .
		4. .

Les éléments de sont appelés des vecteurs et les éléments de sont appelés des scalaires.

Exemples: , , sont des espaces vectoriels. Si est un ensemble, l'ensemble des fonctions de dans est lui aussi un espace vectoriel. En particulier, l'ensemble des suites à valeurs réelles (resp. à valeurs complexes) est un -espace vectoriel (resp. un -espace vectoriel).

Proposition: Soit des -espaces vectoriels. Alors le produit cartésien , muni de l'addition et de la multiplication externe est un -espace vectoriel.

Famille de vecteurs

Dans cette partie, désigne un espace vectoriel sur .

Une combinaison linéaire de la famille finie de vecteurs de est un vecteur s'écrivant où les sont des éléments de . Une combinaison linéaire d'une famille quelconque est un vecteur s'écrivant où tous les , sauf un nombre fini, sont nuls.

Une famille finie de vecteurs est libre si, pour tout choix de ,

Une famille quelconque de vecteurs est libre si toute sous-famille finie extraite est libre.

Une famille qui n'est pas libre est une famille liée.

Exemple: Soit une famille de avec . Alors est une famille libre.

Une famille est génératrice de si tout vecteur de est combinaison linéaire des .

Propriétés des familles libres et génératrices: Soit et deux familles de vecteurs de avec .

- si est libre, alors est libre;
- si est génératrice, alors est génératrice.
- si est une famille génératrice, et si est combinaison linéaire des vecteurs de , alors est une famille génératrice.
- si est une famille libre, et si n'est pas combinaison linéaire des vecteurs de , alors est libre.

Sous-espaces vectoriels

Dans cette partie, désigne un espace vectoriel sur .

Une partie de est un sous-espace vectoriel de si est non-vide et si est stable par et . Dans ce cas, est lui-même un espace vectoriel.

Caractérisation des sous-espaces vectoriels: Une partie de est un sous-espace vectoriel de si et seulement si les 3 propriétés suivantes sont vérifiées:

1. ;
2. Pour tout , ;
3. Pour tout et tout , .

Exemples:

- est un sous-espace vectoriel de ;
- dans , toute droite vectorielle (passant par l'origine) est un sous-espace vectoriel de ;
- dans , toute droite vectorielle (passant par l'origine), tout plan vectoriel est un sous-espace vectoriel de ;
- pour , l'ensemble des polynômes de degré au plus est un sous-espace de ;
- l'ensemble des matrices symétriques d'ordre est un sous-espace vectoriel de .

Proposition: L'ensemble des solutions d'un système linéaire homogène de équations à inconnues est un sous-espace vectoriel de .

Proposition: L'intersection de deux sous-espaces vectoriels est un sous-espace vectoriel.

Proposition et définition: Si est une partie de , il existe un sous-espace vectoriel de contenant qui est le plus petit possible (pour l'inclusion). On l'appelle le sous-espace engendré par et on le note . Si , alors est l'ensemble des combinaisons linéaires des vecteurs :

En particulier, on a les propriétés suivantes:

- si , alors ;
- si est un sous-espace vectoriel contenant , alors ;
- l'espace est inchangé si on ajoute à un des vecteurs une combinaison linéaire des autres vecteurs;
- ;
- si est combinaison linéaire de , alors .

Proposition: Soit une famille de vecteurs de et un sous-espace vectoriel de . Alors

Somme de sous-espaces vectoriels

Soit et deux sous-espaces vectoriels de . On appelle somme de et l'espace vectoriel noté défini par Deux sous-espaces et sont en somme directe si la décomposition de tout vecteur de comme somme d'un vecteur de et d'un vecteur de est unique. On note alors .

Proposition: Deux sous-espaces et sont en somme directe si et seulement si .

On dit que et sont supplémentaires dans s'ils sont en somme directe et si .

Plus généralement, on définit la somme de sous-espaces vectoriels de par C'est un sous-espace vectoriel de . La somme est directe si la décomposition de tout vecteur de sous la forme avec est unique. Ceci revient à dire que si avec , alors .

![](https://www.bibmath.net/ressources/images/danger.png) Si , on ne peut pas caractériser le fait que sont en somme directe en vérifiant que si .

Applications linéaires

Une application est appelée une application linéaire si, pour tous et tous , on a On note l'ensemble des applications linéaires de dans , et si . Une application linéaire de dans s'appelle aussi un endomorphisme de .

Exemples:

- L'application , , est linéaire et s'appelle l'application identité de .
- Pour , l'application , , est une application linéaire et s'appelle l'homothétie de rapport .

Toute combinaison linéaire d'applications linéaires est linéaire. La composée d'applications linéaires est linéaire. On note souvent au lieu de , et pour .

Proposition: est un anneau.

On dit qu'une application linéaire est un isomorphisme si elle est bijective. La fonction réciproque d'un isomorphisme est elle-même une application linéaire.

Un endomorphisme qui est aussi un isomorphisme s'appelle un automorphisme de . L'ensemble des automorphismes de est noté . est un groupe.

L'image directe d'un sous-espace vectoriel de par une application linéaire est un sous-espace vectoriel de . L'image réciproque d'un sous-espace vectoriel de par une application linéaire est un sous-espace vectoriel de .

On appelle noyau de l'application linéaire le sous-espace vectoriel de

Théorème: est injective si et seulement si .

On appelle image de l'application linéaire le sous-espace vectoriel de

Proposition: Si est une famille génératrice de , alors .

Projections et symétries

Soit et deux sous-espaces supplémentaires de . On appelle projection (ou projecteur) sur parallèlement à l'application linéaire définie sur par où se décompose uniquement en avec et . On a alors et .

Caractérisation des projections: Un endomorphisme est une projection si et seulement si . L'application est alors la projection sur parallèlement à .

Soit et deux sous-espaces supplémentaires de . On appelle symétrie par rapport à parallèlement à l'application linéaire définie sur par où se décompose uniquement en avec et . On a alors et .

Caractérisation des symétries: Un endomorphisme est une symétrie si et seulement si . L'application est alors la symétrie par rapport à parallèlement à .