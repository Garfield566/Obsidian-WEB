---
nom: "conjecture de Goldbach"
qid: Q485520
type: conjecture
categorie: conjecture
tags: "#mathematiques/conjecture"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Goldbach_partitions_of_the_even_integers_from_4_to_50_rev4b.svg
---

# Conjecture de Goldbach

> [!Infobox]
> **Conjecture de Goldbach**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Goldbach_partitions_of_the_even_integers_from_4_to_50_rev4b.svg|300]]
> - **Nomme d'apres** : Christian Goldbach
> - **Généralisation de** : conjecture faible de Goldbach, théorème de Chen

La conjecture de Goldbach est l'assertion mathématique qui s'énonce comme suit:

Tout nombre entier pair supérieur à 3 peut s'écrire comme une somme de deux nombres premiers.
Formulée en 1742 par Christian Goldbach, c'est l'un des plus vieux problèmes non résolus de la théorie des nombres et des mathématiques. Il partage avec l'hypothèse de Riemann et la conjecture des nombres premiers jumeaux le numéro 8 des problèmes de Hilbert, énoncés par celui-ci en 1900.
La figure ci-contre montre les solutions de l'équation 2N = p + q représentées par des ronds, où 2N est un nombre pair entre 4 et 50, et p et q sont deux nombres premiers: les nombres 2N sont représentés par les lignes horizontales et les nombres premiers p et q sont représentés par les lignes inclinées rouges et bleues. La conjecture de Goldbach correspond au fait qu'aussi loin qu'on prolonge la figure vers le bas, toute ligne horizontale grise contiendra au moins un rond:

La conjecture de Goldbach est un cas particulier d'une conjecture liée à l'hypothèse H de Schinzel.

## Origine

Le 7 juin 1742, le mathématicien prussien Christian Goldbach écrit au mathématicien suisse Leonhard Euler une lettre à la fin de laquelle il propose la conjecture suivante:

Tout nombre strictement supérieur à 2 peut être écrit comme une somme de trois nombres premiers.
(Goldbach admettait 1 comme nombre premier; la conjecture moderne exclut 1, et remplace donc 2 par 5.)
Dans sa réponse datée du 30 juin 1742, Euler rappelle à Goldbach que cet énoncé découle d'un énoncé antérieur que Goldbach lui avait déjà communiqué:

Tout nombre pair peut être écrit comme somme de deux nombres premiers.
(Comme précédemment, « nombre » est à prendre au sens « entier strictement supérieur à 0 » et la conjecture moderne remplace 0 par 2.)
Selon une version plus faible de la conjecture, tout nombre impair supérieur ou égal à 9 est somme de trois nombres premiers impairs.

## Justification heuristique

La majorité des mathématiciens pense que la conjecture de Goldbach est vraie, en se basant surtout sur des considérations statistiques axées sur la répartition des nombres premiers: plus le nombre est grand, plus il y a de manières disponibles pour le représenter sous forme de somme de deux ou trois autres nombres, et la plus « compatible » devient celle pour laquelle au moins une de ces représentations est constituée entièrement de nombres premiers.
Une version très grossière de l'argument probabiliste heuristique (pour la forme forte de la conjecture de Goldbach) est la suivante. Le théorème des nombres premiers affirme qu'un entier m sélectionné aléatoirement d'une manière brute possède 

 $\tfrac {1}{\ln m}$

 chance d'être premier. Ainsi, si n est un grand entier pair et m, un nombre compris entre 3 et n/2, alors on peut s'attendre à ce que la probabilité que m et n – m soient tous deux premiers soit égale à 

 $\tfrac {1}{\ln m\ln(n-m)}$

. Cet argument heuristique n'est pas rigoureux pour de nombreuses raisons; par exemple, on suppose que les événements que m et n – m soient premiers sont statistiquement indépendants l'un de l'autre. Si l'on poursuit quand même ce raisonnement heuristique, on peut estimer que le nombre total de manières d'écrire un grand nombre entier pair n comme la somme de deux nombres premiers impairs vaut environ

 $$\sum _{m=3}^{n/2}\frac {1}{\ln m}\frac {1}{\ln(n-m)}\approx {\frac {n}{2\ln ^{2}n}}.$$

Puisque cette quantité tend vers l'infini lorsque n augmente, on peut s'attendre à ce que tout entier pair suffisamment grand non seulement possède au moins une représentation sous forme de somme de deux nombres premiers, mais en fait en possède beaucoup.
L'argument heuristique ci-dessus est en fait quelque peu imprécis, car il ignore certaines corrélations entre les probabilités que m et n – m soient premiers. Par exemple, si m est impair alors n – m aussi, et si m est pair alors n – m aussi, or les nombres premiers sont tous impairs à part 2. De même, si n est divisible par 3 et si m est déjà un nombre premier distinct de 3, alors n – m est aussi premier avec 3 donc sa probabilité d'être premier est légèrement supérieure à celle d'un entier quelconque. En poursuivant ce type d'analyse avec plus de soin, Hardy et Littlewood conjecturèrent en 1923 (c'est une partie de la célèbre conjecture des n-uplets premiers de Hardy-Littlewood) que pour tout c ≥ 2, le nombre de représentations d'un grand entier n sous la forme de somme de c premiers 

 $n=p_{1}+\cdots +p_{c}$

 $p_{1}\leq \ldots \leq p_{c}$

 devrait être équivalent à

 $$\left(\prod _{p}{\frac {p\gamma _{c,p}(n)}{(p-1)^{c}}}\right)\int \limits _{2\leq x_{1}\leq \ldots \leq x_{c} \atop x_{1}+\ldots +x_{c}=n}{\frac {\mathrm {d} x_{1}\ldots \mathrm {d} x_{c-1}}{\ln x_{1}\ldots \ln x_{c}}}$$

où le produit porte sur tous les nombres premiers p, et 

 $\gamma _{c,p}(n)$

 est le nombre de solutions de l'équation 

 $n\equiv q_{1}+\cdots +q_{c}\mod p$

 en arithmétique modulaire, soumise aux contraintes 

 $q_{1},\ldots,q_{c}\not \equiv 0\mod p$

. Cette formule asymptotique a été démontrée pour c ≥ 3 à partir du travail de Vinogradov, mais est encore à l'état de conjecture pour c = 2. Dans ce dernier cas, l'expression ci-dessus est nulle lorsque n est impair, et lorsque n est pair elle se simplifie en

 $$2\Pi _{2}\left(\prod \limits _{p|n \atop p\geq 3}\frac {p-1}{p-2}\right)\int _{2}^{n}{\frac {\mathrm {d} x}{\ln ^{2}x}}\approx 2\Pi _{2}\left(\prod \limits _{p|n \atop p\geq 3}\frac {p-1}{p-2}\right){\frac {n}{\ln ^{2}n}},$$

où 

 $\Pi _{2}$

 est la constante des nombres premiers jumeaux

 $$\Pi _{2}=\prod _{p\geq 3}\left(1-\frac {1}{(p-1)^{2}}\right)=0{,}660~161~815~8\ldots.$$

Cette formule asymptotique est quelquefois appelée conjecture étendue de Goldbach. La conjecture forte de Goldbach est en fait très similaire à celle des nombres premiers jumeaux, et les deux conjectures sont présumées de difficultés comparables.

## Théorèmes apparentés

Dans le cadre de recherches en vue de démontrer la conjecture de Goldbach, plusieurs théoriciens des nombres ont abouti à des théorèmes plus faibles que la conjecture. Le tableau suivant présente quelques étapes significatives de ces recherches. La mention f indique les théorèmes en rapport avec la conjecture faible de Goldbach, « tout nombre impair supérieur ou égal à 9 est somme de trois nombres premiers impairs. »:

## Vérifications numériques

En 2014, les vérifications numériques publiées conduisent aux conclusions suivantes:

la conjecture de Goldbach est vérifiée pour tous les entiers pairs jusqu'à 4×1018 (Tomás Oliveira e Silva, Siegfried Herzog et Silvio Pardi);
la conjecture faible de Goldbach est vérifiée pour tous les entiers impairs jusqu'à 8,875×1030 (H. A. Helfgott et David J. Platt).

## Dans la culture

En 2007, Luis Piedrahita et Rodrigo Sopeña produisent le film espagnol La Cellule de Fermat (La Habitación de Fermat) mettant en scène un jeune mathématicien qui affirme faussement avoir démontré la conjecture et un vieux mathématicien qui, lui, l'aurait démontrée.
Le roman Oncle Petros et la Conjecture de Goldbach [détail des éditions], d'Apóstolos Doxiádis, raconte l'histoire fictive d'un mathématicien ayant consacré sa vie professionnelle à la seule conjecture de Goldbach, gaspillant ainsi ses ressources intellectuelles et se mettant lui-même à l'écart de la vie scientifique et de sa famille. Le roman en profite surtout pour fournir un éclairage culturel sur quelques mathématiciens et logiciens du début du siècle (Kurt Gödel, Alan Turing, Srinivasa Ramanujan, Godfrey Harold Hardy…) et les rapports entre leurs différents travaux.
Afin de faire de la publicité pour le livre de Doxiádis, l'éditeur britannique Tony Faber offrit en 2000 un prix d'un million de dollars américains pour une preuve de la conjecture. Le prix ne pouvait être attribué qu'à condition que la preuve soit soumise à publication avant avril 2002. Il n'a jamais été réclamé.
Le roman Le Théorème du Perroquet, de Denis Guedj, met en scène un mathématicien qui, au fond de l'Amazonie, réussit à démontrer la conjecture de Goldbach. Refusant de la livrer à l'humanité, il se suicide en brûlant ses recherches. Mais avant, il la fait apprendre par son perroquet. Des mafieux veulent s'approprier l'oiseau mais ce dernier reste muet. Excédés, ils l'abattent. Le roman se termine dans la forêt où le perroquet, blessé, récite la démonstration aux autres animaux. Elle demeure ainsi inconnue des humains.
Le film Le Théorème de Marguerite (2023) d'Anna Novion présente une normalienne, Marguerite, qui travaille sur la résolution d'un pan de la conjecture de Goldbach.
