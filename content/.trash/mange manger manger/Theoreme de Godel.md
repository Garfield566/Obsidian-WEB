---
nom: "Theoreme de Godel"
qid: Q190391
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/CLTBinomConvergence.svg
---

# Théorème central limite

> [!Infobox]
> **Théorème central limite**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/CLTBinomConvergence.svg|300]]
> - **Nom court** : CLT
> - **Discipline dont c'est l'objet** : théorie des probabilités
> - **Partie de** : liste de théorèmes

Le théorème central limite (aussi appelé théorème limite central, théorème de la limite centrale ou théorème de la limite centrée) établit la convergence en loi de la somme d'une suite de variables aléatoires, d'espérance et de variance finies, vers la loi normale. Intuitivement, ce résultat affirme qu'une somme de variables aléatoires indépendantes et identiquement distribuées tend (le plus souvent) vers une variable aléatoire gaussienne.
Ce théorème et ses généralisations offrent une explication de l'omniprésence de la loi normale dans la nature: de nombreux phénomènes macroscopiques sont dus à l'addition d'un grand nombre de petites perturbations aléatoires.

## Histoire de la démonstration

La première démonstration de ce théorème, publiée en 1809, est due à Pierre-Simon de Laplace, mais le cas particulier où les variables suivent la loi de Bernoulli de paramètre p = 0,5 était connu depuis les travaux de De Moivre, en 1733.

## À propos de la dénomination de ce théorème

La dénomination « théorème central limite » fait référence à un document scientifique écrit par George Pólya en 1920, intitulé Über den zentralen Grenzwertsatz der Wahrscheinlichkeitsrechnung und das Momentenproblem (Sur le théorème [ayant rapport à la notion de] limite central du calcul probabiliste et le problème des moments). Historiquement, et conformément à la traduction du titre, c'est donc bien le théorème qui est central, d'où l'appellation « théorème central limite ». 
Cependant, dans la littérature mathématique française, on peut trouver d'autres dénominations, comme « théorème limite central », « théorème de la limite centrale » ou « théorème de la limite centrée ». Une justification avancée par certains auteurs est que l'adjectif « central » s'applique au centre de la distribution, par opposition à sa queue.

## Illustrations

Ce théorème est évident si n variables aléatoires suivent une loi normale d'espérance μ: en effet leur somme suit une loi normale de paramètre nμ. Dans le cas de variables ne suivant pas une loi normale, le théorème peut sembler étonnant au premier abord.

## Pile ou face

Donnons d'abord une illustration avec le jeu de pile ou face, illustration ne nécessitant pas de connaissance particulière en statistiques, mais uniquement en dénombrement.
Considérons le jeu de pile ou face et mettons des valeurs sur les faces de la pièce, par exemple 0 pour pile et 1 pour face; on s'intéresse à la somme de n tirages. La pièce est équilibrée, chaque face a une chance sur deux d'être tirée. Si l'on fait un seul tirage, nous avons donc le tirage n°1 (et aucun autre), et son résultat peut être 0 ou 1; nous faisons la somme d'une seule valeur.

Nous avons donc n = 2 possibilités pour la valeur de la somme, apparaissant avec les fréquences suivantes:

Avec deux tirages, chaque tirage peut donner 0 ou 1, ce qui donne le tableau suivant:

nous avons n = 4 possibilités, soit le tableau des fréquences.

Et ainsi de suite:

Graphiquement, on constate que plus le nombre de tirages augmente, plus la courbe de fréquence se rapproche d'une courbe en cloche symétrique, caractéristique de la densité de probabilité de la loi normale.

## Dé à six faces

On obtient un résultat similaire en jetant plusieurs dés à six faces (d6) et en faisant la somme des nombres apparus sur leurs faces supérieures, mais le dénombrement est plus fastidieux (il y a six valeurs par dé).

## Cas avec des lois différentes

Dans toutes les situations ci-dessus, on a des lois uniformes; et pourtant, la somme d'un grand nombre d'événements tend graphiquement vers une courbe en cloche symétrique. Et cela reste vrai même lorsque les lois sont différentes (cas des dés polyédriques non réguliers).

En effet, on ne s'intéresse pas au tirage en lui-même, mais à la somme du tirage. De ce point de vue, plusieurs tirages sont équivalents, donc une valeur de somme peut être obtenue par plusieurs tirages; par exemple, pour deux dés à six faces (2d6), on peut obtenir 7 par 1+6, 2+5, 3+4, 4+3, 5+2 et 6+1, il y a six tirages équivalents. Or, il y a toujours plus de combinaisons permettant d'obtenir une valeur moyenne qu'une valeur extrême, ce qui donne la courbe en cloche.

## Énoncé

$X_{1},X_{2},\dots,X_{n},\dots$

 une suite de variables aléatoires réelles définies sur le même espace de probabilité, indépendantes et identiquement distribuées suivant la même loi 

 $D$

. Supposons que l'espérance 

 $\mu$

 et l'écart-type 

 $\sigma$

 $D$

 existent et soient finis avec 

 $\sigma \neq 0$

Considérons la somme

 $S_{n}=X_{1}+X_{2}+\dots +X_{n}$

Alors

l'espérance de 

 $S_{n}$

 $n\mu$

son écart-type vaut 

 $\sigma \sqrt {n}$

De plus, quand 

 $n$

 est assez grand, la loi normale 

 $\mathcal {N}(n\mu,n\sigma ^{2})$

 est une bonne approximation de la loi de 

 $S_{n}$

Afin de formuler mathématiquement cette approximation, nous allons poser

 ¯

 $$\overline {X}_{n}=\frac {S_{n}{n}}={\frac {X_{1}+X_{2}+...+X_{n}}{n}}$$

 ¯

 $$Z_{n}={\frac {S_{n}-n\mu }\sigma {\sqrt {n}}}=\sqrt {n}\frac {{\overline {X}_{n}-\mu }{\sigma }}$$

de sorte que l'espérance et l'écart-type de Zn valent respectivement 0 et 1: la variable est ainsi dite centrée et réduite.
Le théorème central limite énonce alors que la suite de variables aléatoires 

 $Z_{1},Z_{2},\dots,Z_{n},\dots$

 converge en loi vers une variable aléatoire 

 $Z$

, définie sur le même espace probabilisé, et de loi normale centrée réduite 

 $\mathcal {N}(0,1)$

 lorsque n tend vers l'infini. 
Cela signifie que si 

 $\Phi$

 est la fonction de répartition de 

 $\mathcal {N}(0,1)$

, alors pour tout réel 

 $z$

 ¯

 $$\lim _{n\to \infty }\mathbb {P} (Z_{n}\leq z)=\lim _{n\to \infty }\mathbb {P} \left(\frac {{\overline {X}_{n}-\mu }{\sigma /\sqrt {n}}}\leq z\right)=\Phi (z)$$

## Démonstration du théorème central limite

Pour un théorème d'une telle importance en statistiques et en probabilité appliquée, il existe une démonstration particulièrement simple utilisant les fonctions caractéristiques. Cette démonstration ressemble à celle d'une des lois des grands nombres.

## Développement limité des variables centrées réduites

Pour une variable aléatoire 

 $Y$

 d'espérance 0 et de variance 1. Comme 

 $Y\in L^{2}(\Omega,\mathcal {F},\mathbb {P} ),$

 sa fonction caractéristique est de classe 

 $C^{2}$

 et par propriété de la fonction caractéristique 

 $\varphi _{Y}^{(k)}(0)=\mathrm {i} ^{k}\mathbb {E} [Y^{k}]$

donc on a 

 $\varphi _{Y}'(0)=i\mathbb {E} [Y]=0$

 $\varphi ''_{Y}(0)=-\mathbb {E} [Y^{2}]=-\text{Var}(Y)=-1.$

Ainsi, 

 $\varphi _{Y}$

 admet un développement limité au voisinage de 0 de la forme 

 $$\varphi _{Y}(t)=1-\frac {t^{2}{2}}+o(t^{2}),\quad t\to 0$$

## Calcul de la fonction caractéristique de la variable Zn

Or, si on prend les 

 $Y_{i}$

 comme les variables centrées réduites des 

 $X_{1},X_{2},\ldots,X_{n}$

 c'est-à-dire: 

 $${\frac {X_{i}-\mu }{\sigma }}$$

, on a simplement:

 ¯

 $$Z_{n}=\frac {{\overline {X}_{n}-\mu }{\sigma /\sqrt {n}}}=\sum _{i=1}^{n}\frac {Y_{i}\sqrt {n}}$$

Soit ( 

 $t\in \mathbb {R}$

 ), et pour tout (

 ∗

 $n\in \mathbb {N} ^{*}$

 ), comme (

 $X_{1},\ldots,X_{n}$

) sont mutuellement indépendantes et identiquement distribuées, on a:

 $${\begin{aligned}\varphi _{Z_{n}}(t)&=\mathbb {E} \left[\exp \left(itZ_{n}\right)\right]\\&=\mathbb {E} \left[\exp \left(it\sum _{i=1}^{n}\frac {Y_{i}\sqrt {n}}\right)\right]\\&=\mathbb {E} \left[\prod _{i=1}^{n}\exp \left(\frac {it}{\sqrt {n}}Y_{i}\right)\right]\\&=\prod _{i=1}^{n}\mathbb {E} \left[\exp \left(\frac {it}{\sqrt {n}}Y_{i}\right)\right]\\&=\prod _{i=1}^{n}\varphi _{Y_{i}}\left(\frac {t}{\sqrt {n}}\right)\\&=\left(\varphi _{Y_{1}}\left(\frac {t}{\sqrt {n}}\right)\right)^{n}\end{aligned}}$$

## Convergence et identification

Donc la fonction caractéristique de 

 $Z_{n}$

 ⟶

 $$\left[\varphi _{Y}\left(\frac {t}{\sqrt {n}}\right)\right]^{n}=\left[1-\frac {t^{2}{2n}}+o\left(\frac {t^{2}{n}}\right)\right]^{n}\longrightarrow \mathrm {e} ^{-t^{2}/2}$$

 lorsque 

 $n\to \infty$

Mais cette limite est la fonction caractéristique de la loi normale centrée réduite 

 $\mathcal {N}(0,1)$

, d'où l'on déduit le théorème central limite grâce au théorème de convergence de Lévy, qui affirme que la convergence simple des fonctions caractéristiques implique la convergence en loi.

## Convergence vers la limite

La convergence de la fonction de répartition de Zn est uniforme, en vertu du deuxième théorème de Dini. Si le moment centré d'ordre 3, 

 $\mathrm {E} [(\mathrm {X} -\mu )^{3}]$

 existe et est fini, alors la vitesse de convergence est au moins d'ordre 

 $1/\sqrt {n}$

 (voir le théorème de Berry-Esseen).
Images d'une loi lissées par sommation qui montrent la distribution de la loi originale et trois sommations successives (obtenues par convolution):

Dans les applications pratiques, ce théorème permet en particulier de remplacer une somme de variables aléatoires en nombre assez grand mais fini par une approximation normale, généralement plus facile à manipuler. Il est donc intéressant de voir comment la somme s'approche de la limite. Les termes utilisés sont expliqués dans l'article Variable aléatoire.
Une somme de variables continues est une variable continue dont on peut comparer la densité de probabilité à celle de la limite normale.

Avec une somme de variables discrètes, il est parfois commode de définir une pseudo-densité de probabilité mais l'outil le plus efficace est la fonction de probabilité représentée par un diagramme en bâtons. On peut constater graphiquement une certaine cohérence entre les deux diagrammes, difficile à interpréter. Dans ce cas, il est plus efficace de comparer les fonctions de répartition.
D'autre part, l'approximation normale est particulièrement efficace au voisinage des valeurs centrales. Certains disent même qu'en matière de convergence vers la loi normale, l'infini commence souvent à six.
La précision se dégrade à mesure qu'on s'éloigne de ces valeurs centrales. C'est particulièrement vrai pour une somme de variables positives par nature: la loi normale fait toujours apparaître des valeurs négatives avec des probabilités faibles mais non nulles. Même si c'est moins choquant, cela reste vrai en toutes circonstances: alors que toute grandeur physique est nécessairement bornée, la loi normale qui couvre un intervalle infini n'est qu'une approximation utile.
Enfin, pour un nombre donné de termes de la somme, l'approximation normale est d'autant meilleure que la distribution est plus symétrique.

## Application à la statistique mathématique

Ce théorème de probabilités possède une interprétation en statistique mathématique. Cette dernière associe une loi de probabilité à une population. Chaque élément extrait de la population est donc considéré comme une variable aléatoire et, en réunissant un nombre n de ces variables supposées indépendantes, on obtient un échantillon. La somme de ces variables aléatoires divisée par n donne une nouvelle variable nommée la moyenne empirique. Celle-ci, une fois réduite, tend vers une variable normale réduite lorsque n tend vers l'infini.

## Densités de probabilité

La densité de probabilité de la somme de plusieurs variables indépendantes s'obtient par convolution de leurs densités (si celles-ci existent). Ainsi on peut interpréter le théorème central limite comme une formulation des propriétés des densités de probabilité soumises à une convolution: sous les conditions établies précédemment, la convoluée d'un certain nombre de densités de probabilité tend vers la densité normale lorsque leur nombre croît indéfiniment.
Comme la fonction caractéristique d'une convolution est le produit des fonctions caractéristiques des variables en cause, le théorème central limite peut se formuler d'une manière différente: sous les conditions précédentes, le produit des fonctions caractéristiques de plusieurs densités de probabilité tend vers la fonction caractéristique de la loi normale lorsque le nombre de variables croît indéfiniment.

## Produits de variables aléatoires

Le théorème central limite nous dit à quoi il faut s'attendre en matière de sommes de variables aléatoires indépendantes; qu'en est-il des produits? Puisque le logarithme d'un produit de nombres strictement positifs est la somme des logarithmes de ces nombres, le logarithme d'un produit de variables aléatoires à valeurs strictement positives tend vers une loi normale. Le produit tend alors lui-même vers une loi log-normale.
Diverses grandeurs physiques dépendent multiplicativement d'un grand nombre de facteurs aléatoires positifs (par exemple des quantités telles que la masse ou la longueur, qui ne peuvent être négatives), de sorte qu'elles sont bien décrites par une loi log-normale.

## Généralisations du théorème central limite

Le théorème central limite admet plusieurs généralisations qui donnent la convergence de sommes de variables aléatoires sous des hypothèses beaucoup plus faibles. Ces généralisations ne nécessitent pas des lois identiques mais font appel à des conditions qui assurent qu'aucune des variables n'exerce une influence significativement plus importante que les autres. Telles sont la condition de Lindeberg et la condition de Lyapounov. D'autres généralisations autorisent même une dépendance « faible ». De plus, une généralisation due à Gnedenko et Kolmogorov énonce que la somme d'un certain nombre de variables aléatoires avec une queue de distribution décroissante selon 

 $|x|^{-\alpha -1}$

 $0<\alpha <2$

 (ayant donc une variance infinie) tend vers une loi de Lévy tronquée symétrique et stable quand le nombre de variables augmente.

## Condition de Liapounov

On peut, au prix d'une formulation un peu moins simple, supprimer l'hypothèse selon laquelle les variables 

 $X_{n}$

 sont de même loi. Les variables 

 $X_{n}$

 restent toutefois indépendantes: soit donc 

 $(X_{n})_{n\geq 1}$

 une suite de variables aléatoires définies sur le même espace de probabilité, indépendantes. Supposons que, pour 

 $n\geq 1$

 $X_{n}$

 ait une espérance finie 

 $\mu _{n}$

 et un écart-type fini 

 $\sigma _{n}$

, et posons

 $$s_{n}^{2}=\sum _{i=1}^{n}\sigma _{i}^{2}$$

 $$Z_{n}=\frac {1}{s_{n}}\ \sum _{i=1}^{n}(X_{i}-\mu _{i})$$

Supposons que pour un certain 

 $\delta >0$

 la condition de Liapounov

 $$\lim _{n\to +\infty }{\frac {1}{s_{n}^{2+\delta }}}\sum _{i=1}^{n}\mathbb {E} \left[|X_{i}-\mu _{i}|^{2+\delta }\right]=0$$

soit satisfaite, alors la somme normalisée des 

 $X_{i}$

 converge vers une loi normale centrée réduite, c'est-à-dire:

 ⟶

 $$Z_{n}\underset {n\to +\infty }{\overset {\mathcal {L}{\longrightarrow }}}\mathcal {N}(0,1)$$

## Condition de Lindeberg

Avec les mêmes définitions et les mêmes notations que précédemment, nous pouvons remplacer la condition de Liapounov par la suivante qui est plus faible.

## Cas des variables dépendantes

Il existe quelques théorèmes qui traitent le cas de sommes de variables aléatoires réelles dépendantes, par exemple le théorème central limite pour les suites m-dépendantes, le théorème central limite pour les martingales et le théorème central limite pour les processus mélangeants.

## Cas des vecteurs aléatoires

Il existe une généralisation à des vecteurs aléatoires indépendants et de même loi, dont les composantes sont de carrés intégrables, la limite étant alors un vecteur gaussien. Une première version de ce théorème central limite vectoriel, due à Pierre-Simon de Laplace, parait en 1812. Parmi les nombreuses conséquences de ce théorème, on compte par exemple la convergence vers la loi du χ², cruciale, par exemple, pour ses applications en statistiques, ou encore la convergence des marches aléatoires vers le mouvement Brownien.
