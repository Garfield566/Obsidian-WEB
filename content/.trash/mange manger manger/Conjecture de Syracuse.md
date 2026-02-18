---
nom: "Conjecture de Syracuse"
qid: Q220462
type: conjecture
categorie: conjecture
tags: "#mathematiques/conjecture"
---

# Conjecture de Syracuse

> [!Infobox]
> **Conjecture de Syracuse**
> - **Sexe ou genre** : féminin
> - **Lieu de naissance** : Buje
> - **Lieu de mort** : Ljubljana
> - **Profession** : entomologiste, professeur d'université, zoologiste
> - **Naissance** : 15 avril 1907
> - **Deces** : 10 decembre 1974
> - **Prénom** : Zora
> - **Nom de famille** : Karaman
> - **Langues parlées ou signées** : slovène, allemand, macédonien

La conjecture de Syracuse, encore appelée conjecture de Collatz, conjecture d'Ulam, conjecture tchèque, problème de Kakutani ou problème 3x + 1, est l'hypothèse mathématique selon laquelle la suite de Syracuse de n'importe quel entier strictement positif atteint 1.
Une suite de Syracuse est une suite d'entiers naturels définie de la manière suivante: on part d'un nombre entier strictement positif; s'il est pair, on le divise par 2; s'il est impair, on le multiplie par 3 et l'on ajoute 1. En répétant l'opération, on obtient une suite d'entiers strictement positifs dont chacun ne dépend que de son prédécesseur.
Par exemple, à partir de 14, on construit la suite des nombres: 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1, 4, 2, 1 et ainsi de suite. C'est la suite de Syracuse du nombre 14. Après que le nombre 1 a été atteint, la suite des valeurs 1, 4, 2, 1, 4, 2… se répète indéfiniment en un cycle de longueur 3, appelé cycle trivial.
Si l'on était parti d'un autre entier naturel, en lui appliquant les mêmes règles, on aurait obtenu une suite de nombres différente. A priori, il serait possible que la suite de Syracuse de certaines valeurs de départ n'atteigne jamais la valeur 1, soit qu'elle aboutisse à un cycle différent du cycle trivial, soit qu'elle diverge vers l'infini. Or, on n'a jamais trouvé d'exemple de suite obtenue suivant les règles données qui n'aboutisse pas à 1, puis au cycle trivial.
En dépit de la simplicité de son énoncé, cette conjecture défie depuis de nombreuses années les mathématiciens. Paul Erdős a dit à propos de la conjecture de Syracuse: « les mathématiques ne sont pas encore prêtes pour de tels problèmes. »

## Origines

Dès les années 1930, Lothar Collatz s'intéressait aux itérations dans les nombres entiers, qu'il représentait au moyen de graphes et d'hypergraphes. Il a présenté plusieurs de ces problèmes lors de conférences. En 1952, selon Collatz, il expliqua son problème à son collègue de Hamburg, Helmut Hasse. Ce dernier le diffusa aux États-Unis lors d'une visite à l'université de Syracuse: la suite de Collatz prit alors le nom de « suite de Syracuse ». D'autres mathématiciens affirment avoir joué un rôle dans l'origine de ce problème, comme Bryan Thwaites. Le mathématicien polonais Stanislas Ulam le répand aussi dans le Laboratoire national de Los Alamos. Dans les années 1960, le problème est repris par le mathématicien Shizuo Kakutani qui en parle à l'université Yale et à l'université de Chicago.
Cette conjecture mobilisa tant les mathématiciens durant les années 1960, en pleine guerre froide, qu'une plaisanterie courut selon laquelle ce problème faisait partie d'un complot visant à ralentir la recherche américaine. Mais rien n'est publié à propos de cette conjecture dans la littérature scientifique avant les années 1970.

## Suite de Syracuse

La suite de Syracuse d'un nombre entier N > 0 est définie par récurrence, de la manière suivante:

 $u_{0}=N$

et pour tout entier naturel n: 

 est pair,

 est impair.

 $$u_{n+1}=\begin{cases}{\dfrac {u_{n}{2}}&\mbox{si }u_{n}\mbox{ est pair,}\\3u_{n}+1&\mbox{si }u_{n}\mbox{ est impair.}\end{cases}}$$

## Énoncé de la conjecture

La conjecture affirme que pour tout entier N > 0, il existe un indice n tel que un = 1.

## Vocabulaire

L'observation graphique de la suite pour N = 15 et pour N = 27 montre que la suite peut s'élever assez haut avant de retomber. Les graphiques font penser à la chute chaotique d'un grêlon ou bien à la trajectoire d'une feuille emportée par le vent. De cette observation est né tout un vocabulaire imagé: on parlera du vol de la suite.
On définit alors: 

le temps de vol: c'est le plus petit indice n tel que un = 1.
Il est de 17 pour la suite de Syracuse 15 et de 111 pour la suite de Syracuse 27;

le temps de vol en altitude: c'est le plus petit indice n tel que un < u0.
Il est de 11 pour la suite de Syracuse 15 et de 96 pour la suite de Syracuse 27;

l'altitude maximale: c'est la valeur maximale de la suite.
Elle est de 160 pour la suite de Syracuse 15 et de 9 232 pour la suite de Syracuse 27.

## Sous-problèmes

Derrière cette conjecture, se cachent deux autres conjectures, toutes les deux encore irrésolues.

Toute suite de Syracuse est-elle bornée?
Existe-t-il d'autres cycles que le cycle trivial (4,2,1)?
Les réponses OUI à la première question et NON à la seconde sont nécessaires et suffisantes pour démontrer la conjecture.

## Suite compressée

On remarque que, si un est impair dans la formule ci-dessus, un+1 est nécessairement pair et donc le pas suivant de la suite doit être une division par deux. On peut définir une nouvelle version compressée de la suite de Syracuse en combinant ces deux pas de la façon suivante:

 est pair

 est impair.

 $$v_{n+1}=\begin{cases}{\frac {v_{n}{2}}&\mbox{si }v_{n}\mbox{ est pair}\\{\frac {3v_{n}\,+\,1}{2}}&\mbox{si }v_{n}\mbox{ est impair.}\end{cases}}$$

La nouvelle suite est une suite extraite de la version de base, et la conjecture dit que cette suite aboutit toujours au cycle (1,2,1…).

## Approche inverse

On peut aussi partir d'un algorithme inverse:

 $$R(n)={\begin{cases}\{2n\}&\mbox{si }n\equiv 0,1,2,3\mbox{ ou }5\\\{2n,(n-1)/3\}&\mbox{si }n\equiv 4\end{cases}}\pmod {6}.$$

Au lieu de prouver que la suite directe, partant de n'importe quel entier naturel non nul, mène toujours à 1, on essaye de démontrer que l'algorithme inverse, partant de 1, est capable de générer tous les nombres entiers naturels non nuls.
Il existe aussi une version compressée de l'algorithme inverse:

 $$R(n)={\begin{cases}\{2n\}&\text{si }n\equiv 0\mbox{ ou }1\\\{2n,(2n-1)/3\}&\text{si }n\equiv 2\end{cases}}\pmod {3}.$$

Ces algorithmes inverses peuvent être représentés par des arbres, dont la racine est 1. Si la conjecture est vraie, ces arbres recouvrent tous les entiers naturels non nuls.

## Approche binaire

Les applications répétées de la fonction de Syracuse peuvent être représentées comme une machine abstraite traitant d'un processus binaire. La machine effectuera les trois étapes suivantes sur n'importe quel nombre impair jusqu'à ce qu'il ne reste plus qu'un « 1 »: 

Décaler le nombre en binaire d'un cran à gauche et rajouter « 1 » à l'extrémité droite (donnant 2n + 1);
Additionner le nombre original n (donnant 2n + 1 + n = 3n + 1);
Enlever tous les « 0 » situés à droite (c'est-à-dire diviser par deux jusqu'à ce que le résultat soit impair).

## Exemple

Le nombre de départ choisi est 7. Son écriture en binaire est 111 (car 7 = 22 + 21 + 20) La séquence qui en résulte est la suivante:

## Approche probabiliste

Il existe des arguments heuristiques et statistiques de nature à motiver la conjecture. Considérons par exemple une itération de la suite de Syracuse compressée sur un nombre v pris aléatoirement dans un intervalle assez grand. Si v est pair, il est multiplié par (1/2), tandis que s'il est impair, il est multiplié par (3/2) environ. Dans les deux cas, on vérifie que la parité du résultat est indépendante de celle de v. Un raisonnement heuristique consiste à supposer que ce raisonnement probabiliste est valable pour n'importe quel terme de la suite compressée. Bien que ce ne soit pas rigoureux (les termes de la suite ne sont pas aléatoires), certaines observations expérimentales tendent à le confirmer. Ainsi, le modèle obtenu en appliquant cette hypothèse prédit convenablement le temps de vol en altitude de la suite. Avec cette heuristique, on peut dire que statistiquement, l'effet de deux opérations consécutives de la suite revient à multiplier le nombre de départ par (3/4), ou encore que l'opération de Syracuse est contractante, en moyenne, dans un rapport approximativement égal à la racine carrée de (3/4) = 0,866…
Ce rapport nettement inférieur à l'unité suggère fortement que les éléments successifs d'une suite de Syracuse ne peuvent très probablement pas croître indéfiniment. Il n'existe aucune preuve rigoureuse de cette affirmation (et même si l'on parvenait à rendre rigoureux cet argument probabiliste, cela ne permettrait pas encore de conclure, un événement de probabilité quasi nulle mais non nulle, n'étant pas pour autant impossible). De plus, l'argument ici esquissé n'exclut nullement l'existence de cycles non triviaux.
Concernant la répartition des nombres qui satisfont à l'hypothèse de Syracuse, par des méthodes élaborées de programmation linéaire on arrive à montrer que, pour x suffisamment grand, le nombre d'entiers inférieurs à x qui satisfont l'hypothèse de Syracuse est au moins xa pour certaine constante a < 1. En 2002, I. Krasikov et J. Lagarias obtinrent a = 0,84.
Terence Tao a annoncé, en 2019, avoir prouvé (rigoureusement, mais par un argument probabiliste) que presque toutes les orbites de Collatz sont bornées par toute fonction qui diverge vers l'infini. En rendant compte de cet article, Quanta Magazine estime que « Tao a obtenu l'un des résultats les plus significatifs sur la conjecture de Collatz depuis des décennies ».

## Approche calculatoire

Une voie d'exploration intéressante consiste en l'étude systématique du comportement de la suite de Syracuse à l'aide d'ordinateurs, pour des nombres de départ de plus en plus grands. On a ainsi vérifié la conjecture pour tout N < 271 ≈ 2,36 × 1021. La grandeur de ce nombre est de nature à renforcer notre croyance en la véracité de la conjecture de Syracuse. Il convient cependant de comprendre qu'aussi loin que l'on poursuive le calcul, il ne peut directement fournir une démonstration de cette conjecture; le calcul pourrait éventuellement, au contraire, rencontrer un contre-exemple, qui démontrerait la fausseté de la conjecture. Cette approche présente aussi l'intérêt de fournir des résultats numériques utilisables par les théoriciens pour compléter leurs démonstrations. Par exemple, en utilisant la borne N < 268. avec un théorèmesur la longueur des cycles de la suite de Syracuse, on peut conclure qu'à part le cycle trivial (1,4,2,1…) il n'existe aucun cycle de longueur inférieure à 186 milliards. La nouvelle borne N < 271 ≈ 2,36 × 1021 permet de montrer 
qu'un cycle non trivial est au moins de longueur 355 504 839 929.
Les résultats numériques permettent de chercher des corrélations entre le nombre de départ N et la durée de vol, ou le record d'altitude. On a ainsi observé que si les records d'altitude pouvaient être très élevés, la durée du vol était en comparaison plus modeste. Une observation sur les nombres déjà étudiés semble indiquer que l'altitude maximale est majorée par φ(N)×N2, où φ(N) pourrait être soit une constante, soit une fonction lentement croissante. Le temps de vol est plus erratique mais semble majoré par un multiple du logarithme de N. Les expériences numériques suggèrent ainsi de nouvelles conjectures auxquelles les théoriciens peuvent s'attaquer.
En revanche, la recherche théorique est seule en mesure d'apporter des lumières concernant l'existence de trajectoires infinies: il a été démontré que l'ensemble des nombres appartenant à une telle trajectoire aurait une densité asymptotique nulle; pour rester dans l'image du vol, on pourrait dire que le grêlon, pour ne pas retomber jusqu'au sol, doit acquérir et maintenir une haute « vitesse de libération ». Si la conjecture est vraie, alors un tel vol infini est impossible.

## Un énoncé indécidable ?

La relative faiblesse des résultats obtenus en dépit de l'application acharnée de méthodes mathématiques puissantes a conduit certains chercheurs à se demander si la conjecture de Syracuse est un problème indécidable (avec les axiomes usuels utilisés par les mathématiciens, tels que ZFC). En 1972, John Conway a établi l'indécidabilité algorithmique pour une famille de problèmes qui généralise de manière naturelle le problème 3x+1 (voir l'article sur le langage de programmation exotique FRACTRAN). Ce résultat implique qu'il y a dans la famille considérée des problèmes individuels qui sont indécidables (il est en fait même possible, en théorie sinon en pratique, d'en expliciter un), mais ne résout pas la décidabilité du problème de Syracuse en particulier.

## Extension aux nombres négatifs, aux nombres réels et aux nombres complexes

La même suite compressée étendue aux entiers relatifs fait apparaître de nombreux autres cycles, comme (-5,-7,-5) ou (-17,-25,-37,-55,-41,-61,-91,-17). Le problème de Syracuse peut d'ailleurs être vu comme la restriction aux entiers naturels de la suite 

 $z_{n+1}=f(z_{n})$

 où 

 $f(z)$

 est une fonction réelle ou complexe bien choisie, par exemple la fonction suivante:

 $$f(z)=\frac {1}{2}z\cos ^{2}\left(\frac {\pi }{2}z\right)+(3z+1)\sin ^{2}\left(\frac {\pi }{2}z\right).$$

Ou, dans la version compressée où 

 $3z+1$

 est remplacée par 

 $$\frac {(3z+1)}{2}$$

 $$f(z)=\frac {1}{2}z\cos ^{2}\left(\frac {\pi }{2}z\right)+\frac {(3z+1)}{2}\sin ^{2}\left(\frac {\pi }{2}z\right).$$

Dans l'ensemble des nombres réels, cette fonction a été étudiée par Marc Chamberland. Il montre que la conjecture ne tient pas avec cette fonction pour les nombres réels car il existe une infinité de points fixes. Il a également montré qu'il existe de nombreux autres cycles, et qu'il existe des suites infinies divergentes de réels.
Dans le plan complexe, cette fonction a été étudiée par Letherman, Schleicher et Wood. De nombreux points divergent à l'infini, représentés dans l'illustration ci-contre en jaune ou bleu. La frontière qui sépare ces régions divergentes et celles qui ne divergent pas, ici en noir, forme une courbe fractale. On y retrouve des éléments caractéristiques de l'ensemble de Mandelbrot (ce dernier résultat n'est pas très étonnant en fait, car cet ensemble est universel).

À noter également le prolongement continu décrit dans le roman de Thierry Lefebvre (La conjecture des hirondelles - Saison 3). L'un des personnages établit la formule 

 $$h(x)=\frac {7x+2-(5x+2)\cos(\pi x)}{4}$$

 qui évite de faire le test de parité et permet l'étude d'une fonction continue sur R

## Variantes

Différentes variantes du problème de Collatz ont été étudiées.
L'une d'elles consiste à remplacer le nombre 3 du problème de Collatz par le nombre 5. Elle s'énonce ainsi:

 $u_{0}=N$

et pour tout entier naturel n: 

 est pair,

 est impair.

 $$u_{n+1}=\begin{cases}{\dfrac {u_{n}{2}}&\mbox{si }u_{n}\mbox{ est pair,}\\5u_{n}+1&\mbox{si }u_{n}\mbox{ est impair.}\end{cases}}$$

La forme compressée permet de diminuer le nombre d'étapes, mais a le même comportement

 $u_{0}=N$

et pour tout entier naturel n: 

 est pair,

 est impair.

 $$u_{n+1}=\begin{cases}{\dfrac {u_{n}{2}}&\mbox{si }u_{n}\mbox{ est pair,}\\{\dfrac {5u_{n}+1}{2}}&\mbox{si }u_{n}\mbox{ est impair.}\end{cases}}$$

Selon la valeur initiale N, trois types de suite sont obtenues:

Les suites aboutissant à 1, comme pour celles de la conjecture de Collatz; c'est le cas pour N compris entre 1 et 4.
Les suites aboutissant à une boucle, c'est le cas pour N = 5 ou N = 10;
Les suites qui semblent se poursuivre jusqu'à l'infini (cette divergence n'est pas démontrée); c'est le cas pour N = 7 ou N = 9.
La différence de comportement entre la suite de Collatz en 3x +1 et celle en 5x + 1 n'a pas été démontrée formellement.

## La conjecture de Syracuse dans la culture

La conjecture de Syracuse apparaît dans le roman du même nom, par Antoine Billot, publié en 2008. Le protagoniste, mathématicien renommé en particulier pour avoir démontré la conjecture, est confronté à un jeune étudiant algérien, dont il a tué le grand-père dans le cadre de la guerre d'indépendance de l'Algérie.
La conjecture des hirondelles, roman en trois tomes de Thierry Lefebvre, a été publié à partir de 2021 sur la base de la légende urbaine associant la conjecture de Syracuse à un affrontement pendant la guerre froide. Il met en scène un jeune mathématicien ukrainien chargé de trouver un contre-exemple à la conjecture afin de démontrer la supériorité informatique de l'Union soviétique.
