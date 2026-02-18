---
nom: "Plan Marshall"
qid: Q193657
type: politique_economique
categorie: politique_economique
tags: "#economie/politique"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Convex_polygon_illustration1.svg
---

# Ensemble convexe

> [!Infobox]
> **Ensemble convexe**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Convex_polygon_illustration1.svg|300]]
> - **Partie de** : espace affine, liste de types d'ensembles
> - **Discipline dont c'est l'objet** : géométrie convexe

Un objet géométrique est dit convexe lorsque, chaque fois qu'on y prend deux points A et B, le segment [A, B] qui les joint y est entièrement contenu. Ainsi un cube plein, un disque ou une boule sont convexes, mais un objet creux ou bosselé ne l'est pas.

## Définition

On suppose travailler dans un contexte où le segment [x, y] reliant deux points quelconques x et y a un sens (par exemple dans un espace affine sur ℝ — en particulier dans un espace affine sur ℂ — ou dans un espace hyperbolique).

Sauf précision explicite, tout ce qui suit concerne le seul contexte des convexes dans des espaces affines (ou vectoriels), pour lesquels la notion de segment est défini comme ci-dessus.
On appellera dimension d'un convexe non vide C la dimension du sous-espace affine engendré par C.

## Exemples

Les demi-espaces ouverts ou fermés délimités par un hyperplan d'un ℝ-espace vectoriel — ou plus généralement: affine — sont convexes.
Les sous-ensembles convexes de l'espace ℝ des nombres réels sont les intervalles de ℝ.
Dans un espace affine, tout sous-espace affine est convexe; c'est en particulier le cas des sous-espaces vectoriels d'un espace vectoriel.
Le translaté d'un convexe est un convexe.
Dans un espace vectoriel normé réel, toute boule (ouverte ou fermée) est convexe. En effet, d'après la remarque précédente, il suffit de le prouver pour une boule de centre 

 $0$

: pour 

 $t\in [0,1]\text{ et }x,y\in B(0,R),||tx+(1-t)y||\leq R$

. Cela justifie a posteriori le fait d'appeler inégalité de convexité l'axiome d'inégalité triangulaire des espaces vectoriels normés.
 $P_{1},...,P_{n}$

 des points d'un espace vectoriel réel V. Soit E l'ensemble de toutes les combinaisons linéaires 

 $t_{1}P_{1}+...+t_{n}P_{n}$

 ⩽

 $0\leqslant t_{i}$

 pour tout 

 $i$

 $t_{1}+...+t_{n}=1.$

. L'ensemble E est convexe.

## Intersections de convexes

L'intersection de deux convexes (et même d'une famille quelconque de convexes) est elle-même convexe (et ce très généralement, dès lors qu'on peut définir la convexité).

## Stabilité par barycentres à coefficients positifs

La définition de la convexité repose, après le choix de deux points quelconques x et y, sur la considération des points du segment [x, y], autrement dit des barycentres à coefficients positifs de ces deux points. En utilisant le théorème d'associativité des barycentres, on peut étendre aux barycentres à coefficients positifs d'un nombre quelconque de points:

## Enveloppe convexe

Étant donné une partie quelconque A de l'espace ambiant E (espace affine ou contexte plus général), il existe au moins un sous-ensemble convexe de E contenant A, à savoir E lui-même; ceci autorise à considérer l'intersection de tous les sous-ensembles convexes de E contenant A. On l'appelle l'enveloppe convexe de A et on la note co(A) ou Conv(A).
On vérifie aussitôt que co(A) est donc le plus petit sous-ensemble convexe de E contenant A, au sens de l'inclusion sur P(E).
Si x et y sont deux points de E, co({x, y}) est le segment [x, y].

## Le théorème de la projection

À condition de travailler dans un espace euclidien (ou plus généralement dans un espace de Hilbert), on dispose d'un résultat remarquable: étant donné un convexe fermé non vide, pour tout point x de l'espace, il existe un et un seul point p(x) du convexe à distance minimale de x. Ce résultat est accompagné de diverses informations complémentaires, notamment le caractère obtus de l'angle 

 $\widehat {xp(x)m}$

 pour tout point m du convexe, ou le caractère 1-lipschitzien de l'application p.

## Séparation des convexes et structure de la frontière

Une technique utile est celle de la « séparation » de deux convexes. Elle consiste, étant donné deux convexes sans point commun d'un même espace, à découper cet espace en deux par un hyperplan (donc un plan, si la dimension est 3) qui laisse les convexes de part et d'autre de ce mur de séparation. Les démonstrations de la possibilité d'un tel découpage sont multiples, permettant d'obtenir des énoncés plus ou moins généraux; certaines utilisent le théorème de Hahn-Banach, outil d'analyse fonctionnelle particulièrement pertinent pour l'étude en dimension infinie.
Cette méthode permet tout particulièrement de justifier de l'existence en chaque point de la frontière d'un convexe d'un « hyperplan d'appui »: un hyperplan passant par ce point et laissant le convexe tout entier dans l'un des deux demi-espaces qu'il borde. Ce résultat est à son tour fondamental pour étudier plus en détail la structure de la frontière des convexes (divisions en faces, arêtes, etc.) et particulièrement des polyèdres convexes. On est ainsi amenés à distinguer diverses catégories de points (points extrémaux, sommets) qui joueront un rôle central dans les problèmes d'optimisation sur le convexe, par exemple en optimisation linéaire.

## Fonctions convexes associées à un ensemble convexe

L'étude des ensembles convexes peut bénéficier des résultats d'analyse qui concernent les fonctions convexes. Plusieurs telles fonctions peuvent en effet être associées à un convexe non vide C.

La plus simple est sa fonction indicatrice, variante de la fonction caractéristique adaptée à la convexité: c'est la fonction qui prend la valeur 0 sur C, et la valeur +∞ en dehors;
Lorsque l'espace ambiant est un espace vectoriel de dimension finie, muni d'une structure euclidienne, on peut ensuite considérer la fonction conjuguée de la précédente, qu'on appelle alors la fonction d'appui de C;
Enfin, relativement à chacun des points de C, on peut définir la jauge du convexe, qui est reliée de façon très parlante à sa géométrie et utile notamment dans certaines preuves des théorèmes de séparation des convexes.

## Propriétés topologiques

Dans cette section, on suppose l'espace ambiant muni d'une topologie compatible avec sa structure géométrique (c'est toujours le cas dans les espaces de dimension finie; si on est dans un espace vectoriel de dimension infinie cela revient à exiger qu'il s'agisse d'un espace vectoriel topologique).

## Adhérence, intérieur, frontière

Les opérateurs d'adhérence et d'intérieur préservent la convexité. En outre, lorsque le convexe considéré n'est pas d'intérieur vide (et on peut facilement se ramener à ce cas en le considérant comme partie de son enveloppe affine et non de l'espace global), le convexe, son intérieur et son adhérence ont tous trois la même frontière.
On peut montrer très facilement qu'un convexe compact est l'enveloppe convexe de sa frontière (hors le cas dégénéré de la dimension 0).

## Connexité

Une partie convexe d'un espace affine réel (ou complexe) est connexe par arcs, car tout segment reliant deux points constitue un chemin entre ces deux points. En particulier, elle est donc connexe.
Cependant, une partie convexe d'un espace quelconque n'est pas forcément connexe. Un contre-exemple est donné par l'intervalle fermé des nombres rationnels compris entre 0 et 1: c'est un ensemble convexe de ℚ qui est totalement discontinu.

## Enveloppe convexe-fermée d'un ensemble

Si A est une partie quelconque de l'espace on désigne par enveloppe convexe-fermée de A, et l'on note co(A), l'adhérence co(A) de son enveloppe convexe.
On vérifie aisément que co(A) est aussi l'intersection des convexes fermés contenant A (« plus petit » convexe fermé contenant A), et que A a même enveloppe convexe-fermée que co(A) et A.
La forme géométrique du théorème de Hahn-Banach permet de montrer que dans un espace localement convexe, co(A) est l'intersection des demi-espaces fermés contenant A, ce qui prouve que tout convexe fermé est faiblement fermé.
Dans un espace de Banach — ou plus généralement de Fréchet — l'enveloppe convexe-fermée d'un compact est compacte.

## Description à homéomorphisme près en dimension finie

Pour r > 0, on notera Bd une boule fermée de centre 0 et de rayon r dans un espace vectoriel séparé de dimension finie d (pour n'importe quelle norme — toutes sont équivalentes).
Les compacts convexes disposent d'une structure simple:

Plus généralement, les convexes fermés d'une dimension finie d donnée sont homéomorphes à l'un ou l'autre d'un nombre limité (d + 2) de modèles simples:

Pour lire ce théorème sur un exemple instructif, celui de la dimension 3, les convexes fermés de dimension 3 sont homéomorphes à un des cinq modèles suivants: ℝ3 tout entier, la région délimitée par deux plans parallèles, un cylindre, une boule dans ℝ3 ou un demi-espace.
Les intérieurs relatifs de tous les modèles énumérés au théorème précédent sont homéomorphes entre eux, c'est-à-dire homéomorphes à ℝd. L'homéomorphisme donné par le théorème précédent échangeant les intérieurs relatifs, on peut donc en conclure que tous les ouverts convexes de dimension d sont homéomorphes entre eux (ce qui, en réalité, était une étape de la preuve). On peut en fait obtenir mieux, à savoir un difféomorphisme.

Il ne faut pas espérer une classification aussi simple des convexes sans condition topologique: qu'on songe que toute partie de ℝ2 contenant le disque unité ouvert et incluse dans le disque unité fermé est convexe.

## Ensembles convexes et géométrie combinatoire

Les ensembles convexes jouent un rôle central en géométrie combinatoire, ne serait-ce que parce que, face à un nombre fini de points d'un espace affine, l'opération géométrique la plus évidente qu'on puisse leur appliquer est d'examiner leur enveloppe convexe: ce qu'on appelle un polytope.

## Polytopes

L'objet de base de la géométrie combinatoire convexe, c'est le polytope, qu'on peut définir comme enveloppe convexe d'un nombre fini de points.
Pour ne citer ici que l'exemple sans doute le plus fameux de résultat de géométrie combinatoire, en dimension 3, les nombres de sommets, d'arêtes et de faces d'un polytope sont liés par la formule d'Euler (voir à ce sujet l'article Caractéristique d'Euler):

 $S-A+F=2.$

## Les théorèmes de Radon, Helly et Carathéodory

Considérons un ensemble 

 $A=\{a_{1},\dots,a_{d+2}\}$

 de d + 2 points dans un espace affine de dimension d.
Le théorème de Radon affirme que:

Pour énoncer de façon parallèle les théorèmes de Helly et Carathéodory, on va introduire une notation: pour chaque indice i variant entre 1 et d + 2, notons

 $$\Delta _{i}=\mathrm {Conv} \left(a_{1},\dots,a_{i-1},a_{i+1},\ldots,a_{d+2}\right)$$

 l'enveloppe convexe des points de A autres que le point ai. En dimension 2, chaque Δi serait un triangle (et il y en aurait quatre); en dimension 3 on aurait affaire à une collection de cinq tétraèdres, et ainsi de suite.
Les deux énoncés suivants sont des cas particuliers des énoncés les plus courants des théorèmes de Helly et Carathéodory, mais qui en contiennent essentiellement toute l'information: on reconstitue facilement les énoncés généraux à partir des versions fournies ci-dessous.

Ces théorèmes sont étroitement liés: la démonstration la plus courante de Helly est fondée sur Radon, tandis qu'on prouve facilement Carathéodory indépendamment, mais il est aussi possible par exemple de déduire Helly de Carathéodory ou le contraire.
D'innombrables variantes les précisent ou les généralisent.
