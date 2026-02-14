---
nom: "Theoreme de Bayes"
qid: Q207264
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://upload.wikimedia.org/wikipedia/commons/f/f3/Pierre_de_Fermat.jpg
---

# Nombre de Fermat

> [!Infobox]
> **Nombre de Fermat**
> ![[https://upload.wikimedia.org/wikipedia/commons/f/f3/Pierre_de_Fermat.jpg|300]]
> - **Nomme d'apres** : Pierre de Fermat
> - **Aspect de** : polygone constructible à la règle et au compas

Un nombre de Fermat est un nombre qui peut s'écrire sous la forme 

 $2^{2^{n}}+1$

, avec 

 $n$

 entier naturel. Le nombre de Fermat de rang 

 $n$

 $2^{2^{n}}+1$

, est noté 

 $F_{n}$

La suite 

 $(F_{n})$

, qui débute par 3, 5, 17, 257, 65537, 4294967297, 18446744073709551617 est répertoriée comme suite A000215 de l'OEIS.
Ces nombres doivent leur nom à Pierre de Fermat, qui émit la conjecture que tous ces nombres étaient premiers. Cette conjecture se révéla fausse, F5 étant composé, de même que tous les suivants jusqu'à F32. On ne sait pas si les nombres à partir de F33 sont premiers ou composés. Ainsi, les seuls nombres de Fermat premiers connus sont au nombre de cinq, à savoir les cinq premiers F0, F1, F2, F3 et F4, qui valent respectivement 3, 5, 17, 257 et 65 537.
Les nombres de Fermat disposent de propriétés intéressantes, en général issues de l'arithmétique modulaire. En particulier, le théorème de Gauss-Wantzel établit un lien entre ces nombres et la construction à la règle et au compas des polygones réguliers: un polygone régulier à 

 $n$

 côtés peut être construit à la règle et au compas si et seulement si 

 $n$

 est une puissance de 2, ou le produit d'une puissance de 2 et de nombres de Fermat premiers distincts.

## Histoire

En 1640, dans une lettre adressée à Bernard Frénicle de Bessy, Pierre de Fermat énonce son petit théorème et commente: « Et cette proposition est généralement vraie en toutes progressions et en tous nombres premiers; de quoi je vous envoierois la démonstration, si je n'appréhendois d'être trop long. » Ce théorème lui permet d'étudier les nombres portant maintenant son nom. Dans cette même lettre, il émet la conjecture que ces nombres sont tous premiers mais reconnaît: « je n'ai pu encore démontrer nécessairement la vérité de cette proposition ». Cette hypothèse le fascine; deux mois plus tard, dans une lettre à Marin Mersenne, il écrit: « Si je puis une fois tenir la raison fondamentale que 3, 5, 17, etc. sont nombres premiers, il me semble que je trouverai de très belles choses en cette matière, car j'ai déjà trouvé des choses merveilleuses dont je vous ferai part. » Il écrit encore à Blaise Pascal: « C'est une propriété de la vérité de laquelle je vous réponds. La démonstration en est très malaisée et je vous avoue que je n'ai pu encore la trouver pleinement ; je ne vous la proposerois pas pour la chercher, si j'en étois venu à bout ». Dans une lettre à Kenelm Digby, non datée mais envoyée par Digby à John Wallis le 16 juin 1658, Fermat donne encore sa conjecture comme non démontrée. Toutefois, dans une lettre de 1659 à Pierre de Carcavi, il s'exprime en des termes qui, selon certains auteurs, impliquent qu'il estime avoir trouvé une démonstration. Si Fermat a soumis cette conjecture à ses principaux correspondants, elle est par contre absente des Arithmétiques de Diophante rééditées en 1670, où son fils retranscrivit les quarante-sept autres conjectures qui furent plus tard prouvées. C'est la seule conjecture erronée de Fermat.
En 1732, le jeune Leonhard Euler, à qui Christian Goldbach avait signalé cette conjecture trois ans auparavant, la réfute: F5 est divisible par 641. Il ne dévoile la construction de sa preuve que quinze ans plus tard. Il y utilise une méthode similaire à celle qui avait permis à Fermat de factoriser les nombres de Mersenne M23 et M37.
Il est probable que les seuls nombres premiers de cette forme soient 3, 5, 17, 257 et 65 537, car Boklan et Conway ont prépublié en mai 2016 une analyse très fine estimant la probabilité d'un autre nombre premier à moins d'un sur un milliard.

## Premières propriétés

La suite des nombres de Fermat peut se définir par récurrence simple:

 ⩾
 $${\begin{cases}F_{0}=3\\F_{n}\ =\ (F_{n-1}-1)^{2}+1,&\text{pour }n\geqslant 1\end{cases}}$$

ou par récurrence double:

 ⩾
 $${\begin{cases}F_{0}=3,F_{1}=5\\F_{n}=F_{n-1}^{2}-2(F_{n-2}-1)^{2},&\text{pour }n\geqslant 2\end{cases}}$$

ou par récurrence forte:

 ⩾
 $${\begin{cases}F_{0}=3\\F_{n}\ =\ \prod _{i=0}^{n-1}F_{i}\ +\ 2,&\text{pour }n\geqslant 1\end{cases}}$$

ou encore:

 ⩾
 $${\begin{cases}F_{0}=3,F_{1}=5\\F_{n}=F_{n-1}+2^{2^{n-1}}\prod _{i=0}^{n-2}F_{i},&\text{pour }n\geqslant 2\end{cases}}$$

On en déduit le théorème de Goldbach affirmant que:

Deux nombres de Fermat distincts sont premiers entre eux.
 $D(n,b)$

 le nombre de chiffres utilisés pour écrire 

 $F_{n}$

 en base 

 $b$

 ⌊

 ⌋

 ⌊

 ⌋
 $$D(n,b)=\left\lfloor \log _{b}\left(2^{2^\overset {n}{}}+1\right)+1\right\rfloor \approx \lfloor 2^{n}\,\log _{b}2+1\rfloor,$$

où les crochets désignent la fonction partie entière et 

 $\log _{b}$

 le logarithme de base 

 $b$

La suite 

 $(D(n,10))$

, qui débute par 1, 1, 2, 3, 5, 10, 20, 39, 78, 155 est répertoriée comme suite A057755 de l'OEIS.
Tous les nombres de Fermat à partir de 

 $F_{2}=17$

 se terminent par le chiffre 7 en écriture décimale.
Les nombres de Fermat premiers ne sont pas des nombres brésiliens alors que les nombres de Fermat composés sont tous des nombres brésiliens.

## Nombre de Fermat et primalité

La raison historique de l'étude des nombres de Fermat est la recherche de nombres premiers. Fermat connaissait déjà la proposition suivante:

Soit k un entier strictement positif; si le nombre 2k + 1 est premier, alors k est une puissance de 2.

Fermat a conjecturé (erronément, comme on l'a vu) que la réciproque était vraie; il a montré que les cinq nombres

 $F_{0}=2^{1}+1=3$

 $F_{1}=2^{2}+1=5$

 $F_{2}=2^{4}+1=17$

 $F_{3}=2^{8}+1=257$

 $F_{4}=2^{16}+1=65\,537$

 sont premiers. Actuellement, on ne connaît que cinq nombres de Fermat premiers, ceux cités ci-dessus.
On ignore encore s'il en existe d'autres, mais on sait que les nombres de Fermat Fn, pour n entre 5 et 32, sont tous composés; F33 est le plus petit nombre de Fermat dont on ne sait pas s'il est premier ou composé.
En 2013, le plus grand nombre de Fermat dont on savait qu'il est composé était: F2 747 497; l'un de ses diviseurs est le nombre premier de Proth 57×22 747 499 + 1.

## Factorisation des nombres de Fermat composés

Euler démontre le théorème:

Tout facteur premier d'un nombre de Fermat Fn est de la forme k.2n+1 + 1, où k est un entier.
(Lucas a même démontré plus tard que tout facteur premier d'un nombre de Fermat Fn est de la forme k.2n+2 + 1.)
Ceci lui permet de trouver rapidement:

 $F_{5}=2^{32}+1=4\,294\,967\,297=641\times 6\,700\,417$

 (semi-premier).

 $(641=10\times 2^{5+1}+1=5\times 2^{5+2}+1)$

Le cas général est un problème difficile du fait de la taille des entiers Fn, même pour des valeurs relativement faibles de n. En 2020, le plus grand nombre de Fermat dont on connaisse la factorisation complète est F11, dont le plus grand des cinq diviseurs premiers a 564 chiffres décimaux (la factorisation complète de Fn, pour n inférieur à 10, est, elle aussi, entièrement connue). En ce qui concerne F12, on sait qu'il est composé; mais c'est, en 2020, le plus petit nombre de Fermat dont on ne connaisse pas la factorisation complète. Quant à F20, c'est, en 2020, le plus petit nombre de Fermat composé dont on ne connaisse aucun diviseur premier.

## Série des inverses des nombres de Fermat

La série des inverses des nombres de Fermat est convergente et sa somme 

 $$\sum _{n=0}^{\infty }\frac {1}{2^{2^{n}+1}}\approx 0{,}596$$

 est irrationnelle et même transcendante. Ces résultats viennent de ce que cette somme est trop bien approchée par des rationnels.

## Produit de nombres de Fermat consécutifs et application à l'infinitude des nombres premiers

Une itération de l'identité remarquable 

 $a^{2}-b^{2}=(a-b)(a+b)$

 donne 

 $a^{2^{n}}-b^{2^{n}}=(a-b)(a+b)(a^{2}+b^{2})\cdots (a^{2^{n-1}}+b^{2^{n-1}})$

. On en déduit que 

 $2^{2^{n}}-1$

 ⩾
 $$\prod _{k=0}^{n-1}(2^{2^{k}}+1)\text{ pour }n\geqslant 1$$

 et que 

 $$F_{n}-2=\prod _{k=0}^{n-1}F_{k}$$

Ceci permet la démonstration suivante de l'infinitude des nombres premiers, démonstration se trouvant en deuxième position (après la démonstration d'Euclide) dans le livre des raisonnements divins. En effet, la relation précédente montre que deux nombres de Fermat distincts sont premiers entre eux. Choisir un diviseur premier de chacun d'entre eux fournit alors une suite infinie de nombres premiers.

## Polygone régulier

Gauss et Wantzel ont établi un lien entre ces nombres et la construction à la règle et au compas des polygones réguliers: un polygone régulier à n côtés est constructible si et seulement si n est le produit d'une puissance de 2 (éventuellement égale à 20 = 1) et d'un nombre fini (éventuellement nul) de nombres de Fermat premiers distincts.
Par exemple, le pentagone régulier est constructible à la règle et au compas puisque 5 est un nombre de Fermat premier; de même, un polygone à 340 côtés est constructible à la règle et au compas puisque 340 = 22.F1.F2.

## Généralisations

Il est possible de généraliser une partie des résultats obtenus pour les nombres de Fermat.
Pour que 

 $a^{n}\!+1$

 soit premier, a doit nécessairement être pair et n doit être une puissance de deux.
On appelle couramment « nombres de Fermat généralisés » les nombres de la forme 

 $a^{2^{n}}\!\!+1$

 (avec a ≥ 2), mais Hans Riesel a donné aussi ce nom aux nombres de la forme 

 $a^{2^{n}}\!\!+b^{2^{n}}$

. Le plus grand nombre premier de la forme 

 $a^{2^{n}}\!\!+1$

 connu en 2017 est 

 $24\,518^{2^{18}}\!\!+1$

, un nombre de plus d'un million de chiffres.
