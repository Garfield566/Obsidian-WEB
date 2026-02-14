---
nom: "Theoreme fondamental de lanalyse"
qid: Q192760
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Julia_set_(C_=_0.285,_0.01).jpg
---

# Théorème fondamental de l'algèbre

> [!Infobox]
> **Théorème fondamental de l'algèbre**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Julia_set_(C_=_0.285,_0.01).jpg|300]]
> - **Prouvé ou démontré par** : Jean-Robert Argand
> - **Discipline dont c'est l'objet** : algèbre, analyse complexe
> - **Nomme d'apres** : Jean Le Rond d'Alembert, Carl Friedrich Gauss
> - **Partie de** : liste de théorèmes

En mathématiques, le théorème fondamental de l'algèbre, aussi appelé théorème de d'Alembert-Gauss et théorème de d'Alembert, indique que tout polynôme non constant, à coefficients complexes, admet au moins une racine. En conséquence, tout polynôme à coefficients entiers, rationnels ou encore réels admet au moins une racine complexe, car ces nombres sont aussi des complexes. Une fois ce résultat établi, il devient simple de montrer que sur 

 $\mathbb {C}$

, le corps des nombres complexes, tout polynôme 

 $P$

 est scindé, c'est-à-dire constant ou produit de polynômes de degré 1.
Le temps a rendu l'expression de théorème fondamental de l'algèbre un peu paradoxale. Il n'existe en effet aucune démonstration purement algébrique de ce théorème. Il est nécessaire de faire usage de résultats topologiques ou analytiques pour sa démonstration. L'expression provient d'une époque où l'algèbre s'identifiait essentiellement avec la théorie des équations, c'est-à-dire la résolution des équations polynomiales. Les frontières de l'algèbre ont maintenant changé mais le nom du théorème est resté.
Les conséquences du théorème sont nombreuses; en algèbre linéaire ce résultat est essentiel pour la réduction d'endomorphisme; en analyse, il intervient dans la décomposition en éléments simples des fonctions rationnelles utilisée pour trouver une primitive. On les retrouve aussi en théorie algébrique des nombres, dans un résultat basique indiquant que toute extension algébrique du corps des rationnels peut être considérée comme un sous-corps de celui des complexes.

L'histoire du théorème indique l'importance du résultat aux yeux des mathématiciens du XVIIIe siècle. Les plus grands noms, comme ceux de d'Alembert, Euler, Lagrange ou Gauss se sont attelés à sa démonstration, avec des fortunes diverses. La variété et la richesse des méthodes conçues dans ce but fut un moteur puissant pour l'évolution de la recherche en mathématiques et particulièrement pour une meilleure compréhension des nombres complexes.

## Énoncés

Le théorème fondamental de l'algèbre admet plusieurs énoncés équivalents.

Par exemple, 

 $1+\mathrm {i}$

 est une racine du polynôme 

 $X^{4}+4$

. Sous cette forme, le théorème affirme l'existence d'une racine du polynôme 

 $P(X)$

 mais n'explique pas comment trouver explicitement cette racine. Cet énoncé existentiel décrit plus une propriété du corps des nombres complexes. Un corps est dit algébriquement clos si tout polynôme de degré strictement positif et à coefficients dans ce corps admet au moins une racine dans ce corps. Le théorème se reformule donc ainsi:

(i) Le corps 

 $\mathbb {C}$

 est algébriquement clos.
Ce résultat se reformule aussi en termes de factorisation des polynômes à coefficients complexes:

(ii) Tout polynôme à coefficients complexes est scindé.
Ces résultats indiquent qu'un polynôme à coefficients complexes de degré 

 $n$

, que l'on peut écrire 

 $a_{n}X^{n}+\ldots +a_{1}X+a_{0}$

 s'écrit aussi 

 $a_{n}(X-\alpha _{1})\ldots (X-\alpha _{n})$

. Ici, la famille 

 $(\alpha _{k})$

, pour 

 $k$

 variant de 1 à 

 $n$

, est celle des racines. Certains nombres 

 $\alpha _{k}$

 peuvent être égaux; on parle alors de racines multiples.
Le théorème fondamental de l'algèbre équivaut à chacun des énoncés suivants:

(iii) Tout polynôme non constant à coefficients réels admet au moins une racine complexe.

(iv) Les polynômes irréductibles à coefficients réels sont exactement les polynômes de degré 1, et les polynômes de degré 2 à discriminant strictement négatif (s'écrivant 

 $aX^{2}+bX+c$

, avec 

 $a$

 non nul et 

 $b^{2}-4ac<0$

(v) Tout polynôme non constant à coefficients réels s'écrit comme un produit de polynômes à coefficients réels de degrés 1 ou 2.

## Analyse

Il apparaît parfois nécessaire de calculer une primitive d'une fonction rationnelle, c'est-à-dire d'une fonction quotient de deux fonctions polynôme. On peut considérer la fonction 

 $f$

 définie par:

 $$f(x)={\frac {5x^{2}-3x-11}{x^{3}-2x^{2}-5x+6}}.$$

Un corollaire du théorème fondamental indique que le dénominateur se factorise en éléments du premier degré; ici on trouve:

 $x^{3}-2x^{2}-5x+6=(x-1)(x+2)(x-3).$

Une décomposition en éléments simples de la fonction montre l'existence de trois valeurs 

 $a,b$

 $c$

 telles que:

 $$f(x)=\frac {a}{x-1}+\frac {b}{x+2}+\frac {c}{x-3}.$$

Un rapide calcul montre que 

 $a=\dfrac {3}{2},b=1$

 $c=\dfrac {5}{2}$

; le calcul de la primitive devient alors aisément réalisable.

## Algèbre linéaire

La réduction d'endomorphisme fait appel aux polynômes. On peut choisir comme cas particulier un endomorphisme autoadjoint 

 $a$

 d'un espace euclidien 

 $E$

 pour illustrer l'usage du théorème. Sa matrice dans une base orthonormale est donc symétrique et toutes ses valeurs propres sont réelles. Le polynôme caractéristique de 

 $a$

 admet, d'après le théorème fondamental de l'algèbre, une racine 

 $\lambda$

. Il s'agit d'une valeur propre de 

 $a$

. En remarquant que l'espace orthogonal 

 $F$

 à l'espace propre de valeur propre 

 $\lambda$

 est stable par 

 $a$

 on comprend que l'endomorphisme est diagonalisable. En effet, il suffit d'appliquer maintenant la même réduction à la restriction de 

 $a$

 à 

 $F$

, qui est aussi autoadjointe. Pas à pas l'endomorphisme 

 $a$

 est ainsi diagonalisé.
Cet exemple est choisi parmi de nombreux autres. La diagonalisation d'un endomorphisme apparaît souvent comme la conséquence de l'existence d'une racine du polynôme caractéristique ou minimal.

## Arithmétique

L'un des objets de la théorie algébrique des nombres traditionnelle est l'étude des corps de nombres, c'est-à-dire des extensions finies du corps 

 $\mathbb {Q}$

 des rationnels. Tous ces corps sont algébriques sur 

 $\mathbb {Q}$

 donc se plongent dans sa clôture algébrique, le corps 

 ¯

 ${\overline {\mathbb {Q} }}$

 des nombres algébriques. D'après le théorème fondamental de l'algèbre, 

 ¯

 ${\overline {\mathbb {Q} }}$

 se plonge lui-même dans 

 $\mathbb {C}$

## Démonstration directe

La démonstration présentée ici détaille celle de Cauchy.
On considère un polynôme de degré 

 $n>0$

 à coefficients complexes, 

 $P(X)=a_{0}+a_{1}X+\ldots +a_{n}X^{n}$

Dans un premier temps, l'existence d'un minimum global pour la fonction qui à 

 $z$

 associe le module de 

 $P(z)$

 est établie. Pour cela, on remarque que si le module de 

 $z$

 est suffisamment grand, le module de 

 $P(z)$

 l'est aussi et donc l'ensemble des 

 $z$

 pour lesquels 

 $|P(z)|$

 n´est pas trop grand est nécessairement borné. Ensuite, on utilise le fait que tout fermé borné de ℂ est compact et qu'une fonction continue d'un compact dans ℝ a une image elle-même compacte, donc fermée et bornée, ce qui implique que la fonction atteint sa borne inférieure, en un certain point 

 $z_{0}$

Enfin, on raisonne par l'absurde: on suppose que l'image de 

 $z_{0}$

 $P$

 est non nulle. On trouve, par le développement de Taylor du polynôme autour de 

 $z_{0}$

, une « direction » 

 $c$

 (un nombre complexe non nul) telle que la fonction de 

 $\mathbb {R}$

 $\mathbb {R}$

 qui à 

 $t$

 associe le module de 

 $P(z_{0}+tc)$

 soit, pour tout 

 $t>0$

 assez petit, strictement inférieure à sa valeur en 

 $0$

. Cette contradiction permet de conclure.

Cette preuve repose donc essentiellement sur le fait que 

 $\mathbb {R}$

 possède la propriété de la borne supérieure.

## Par le théorème de Liouville

Une preuve très concise repose sur le théorème de Liouville en analyse complexe. À cet effet, on considère un polynôme 

 $P$

 à coefficients complexes, de degré au moins égal à 

 $1$

. On suppose qu'il n'a aucune racine: dès lors, la fonction rationnelle 

 $\dfrac {1}{P}$

 est entière et bornée (car elle tend vers 

 $0$

 à l'infini, d'après la démonstration précédente); du théorème de Liouville, on déduit qu'elle est constante, ce qui contredit l'hypothèse sur le degré, et prouve ainsi par l'absurde l'existence d'au moins une racine de 

 $P$

## Par le théorème de Rouché

Une autre démonstration concise s'appuie sur le théorème de Rouché en analyse complexe. On considère le polynôme 

 $p$

 à valeurs dans 

 $\mathbb {C}$

 défini par:

 $p(z)=a_{0}+\cdots +a_{n}z^{n}$

en supposant que le coefficient 

 $a_{n}$

 est non nul. Il suffit ensuite de comparer ce polynôme à 

 $a_{n}z^{n}$

 sur un cercle suffisamment grand pour en déduire, en appliquant le théorème de Rouché, que 

 $p$

 possède autant de zéros (avec multiplicités) que 

 $a_{n}z^{n}$

, c'est-à-dire 

 $n$

## Par le théorème de Cauchy

Une troisième preuve concise se base sur le théorème intégral de Cauchy en analyse complexe.
Par l'absurde, on suppose que pour tout 

 $z\in \mathbb {C}$

 $P(z)\neq 0$

 et on considère la fonction suivante 

 {\textstyle z\mapsto {\frac {P'(z)}{P(z)}}}

 qui est holomorphe sur 

 $\mathbb {C}$

. Par le théorème intégral de Cauchy, on a

 ∗

 $\forall \rho \in \mathbb {R} _{+}^{*}$

 $$\int _{|z|=\rho }\frac {P'(z)}{P(z)}\mathrm {d} z=0.$$

Or en effectuant la division polynomiale de 

 $$\frac {P'(z)}{P(z)}$$

, on obtient après inversion de la somme et de l'intégrale sur la série absolument convergente que

 $$\lim \limits _{\rho \rightarrow +\infty }\int _{|z|=\rho }\frac {P'(z)}{P(z)}\mathrm {d} z=2\pi i\operatorname {deg} P\neq 0.$$

Il y a donc une contradiction et le polynôme 

 $P$

 a au moins une racine.

## Par le théorème d'inversion locale

Puisque 

 $P$

 est continu et que 

 $$\lim \limits _{|z|\rightarrow +\infty }|P(z)|=+\infty$$

, l'application 

 $P$

 est propre donc son image 

 $\mathrm {Im} (P)$

 est fermée, donc 

 ∖

 $\mathbb {C} \setminus \mathrm {Im} (P)$

 est ouvert. Par ailleurs, d'après le théorème d'inversion locale, 

 ∣

 $P(\{z\in \mathbb {C} \mid P'(z)\neq 0\})$

 est ouvert; son intersection avec l'ensemble 

 ∖
 ∣

 $R:=\mathbb {C} \setminus P(\{z\in \mathbb {C} \mid P'(z)=0\})$

 des valeurs qui sont soit non atteintes par 

 $P$

, soit atteintes mais non critiques, est donc un ouvert de 

 $R$

, complémentaire dans 

 $R$

 de l'ouvert précédent.
Or (puisque 

 $P'$

 n'a qu'un nombre fini de racines) 

 $R$

 est cofini donc connexe. L'un de ses deux ouverts est donc vide. Ce ne peut pas être le second, car il est égal à 

 ∖
 ∣

 $\mathrm {Im} (P)\setminus P(\{z\in \mathbb {C} \mid P'(z)=0\})$

Par conséquent, 

 ∖

 ∅

 $\mathbb {C} \setminus \mathrm {Im} (P)\neq \emptyset$

, ce qui implique 

 $\mathrm {Im} (P)=\mathbb {C}$

. On a donc 

 $0\in \mathrm {Im} (P)$

 et donc il existe un nombre 

 $z\in \mathbb {C}$

 tel que 

 $P(z)=0$

## Homotopie

Une homotopie entre deux lacets est une déformation continue permettant de passer du premier lacet au deuxième. L'article détaillé montre que si 

 $P$

 est un polynôme de degré 

 $n$

 et si 

 $\rho$

 est un nombre réel suffisamment grand, le lacet 

 $\alpha$

 défini sur le cercle unité par:

 $$\forall t\in [0,1]\quad \alpha (t)={\frac {P(\rho \exp(2\pi \mathrm {i} t))}{|P(\rho \exp(2\pi \mathrm {i} t))|}}$$

 $n$

 fois le tour du cercle. Si le polynôme 

 $P$

 n'avait pas de racine, ce lacet serait homotope à un point. Cette contradiction est la base de la démonstration proposée dans l'article détaillé.

## Corps réel clos

Il n'existe pas de démonstration purement algébrique du « théorème fondamental de l'algèbre » car, à un endroit ou à un autre, des considérations de continuité interviennent nécessairement. Ce point n'a été complètement clarifié qu'en 1927, par Emil Artin et Otto Schreier, avec la théorie des corps ordonnables et des corps réels clos. Ces auteurs ont abouti au théorème d'algèbre suivant, « attribué » par Nicolas Bourbaki à Euler et Lagrange:

On dit alors que 

 $K$

 est un « corps ordonné maximal », ou encore un « corps réel clos ».

Pour le corps 

 $\mathbb {R}$

, les conditions (1.a) et (1.b) sont satisfaites, d'après deux théorèmes d'analyse se déduisant du théorème des valeurs intermédiaires. Par suite, le corps 

 $\mathbb {C}$

 des complexes, obtenu en lui adjoignant 

 $i=\sqrt {-1}$

, est algébriquement clos.

Remarques
La démonstration ci-dessus est une réécriture moderne de celle conçue par Lagrange. Il s'agit d'une ingénieuse combinatoire, que Laplace fut le premier à utiliser pour mettre au point la stratégie d'Euler. Une démonstration plus courte fait appel à la théorie de Galois (voir ci-dessous).
Tout corps réel clos 

 $K$

 vérifie les mêmes propriétés du premier ordre que 

 $\mathbb {R}$

. En particulier, les seuls polynômes irréductibles de 

 $K[X]$

 sont les polynômes du premier degré et les polynômes du second degré ayant un discriminant strictement inférieur à 

 $0$

 $K$

 vérifie la propriété des valeurs intermédiaires pour les polynômes de 

 $K[X]$

. En revanche, ℝ est le seul corps totalement ordonné possédant la propriété (du second ordre) de la borne supérieure, qui fonde la « preuve directe ».

## Les origines

À l'époque de François Viète (1540 - 1603), le calcul littéral vient d'être découvert par ce mathématicien ainsi que les relations entre coefficients et racines. Il remarque aussi qu'il est toujours possible de construire une équation ayant exactement 

 $n$

 racines données. En 1608, Peter Roth prétend que le nombre de racines d'une équation polynomiale est borné par son degré. Par « racine », il n'entendait pas forcément des racines de la forme 

 $a+ib$

. Un premier énoncé correct est donné par Albert Girard (1595 - 1632), qui, en 1629, dans son traité intitulé Inventions nouvelles en l'algèbre, annonce que:

« Toutes les équations d'algèbre reçoivent autant de solutions que la dénomination de la plus haute quantité le démontre. »

Cette idée est reprise dans la Géométrie de René Descartes (1596-1650), qui utilise pour la première fois le terme imaginaire, pour qualifier des racines: «... quelquefois seulement imaginaires c'est-à-dire que l'on peut toujours en imaginer autant que j'ai dit en chaque équation, mais qu'il n'y a quelquefois aucune quantité qui corresponde à celle qu'on imagine... ». Albert Girard les appelait, pour sa part, des inexplicables. Leur compréhension est encore insuffisante pour donner un sens à l'idée d'une démonstration. Un nombre imaginaire est ici un nombre fictif, qui, pour les polynômes de degrés supérieurs, joueraient le même rôle que le symbole 

 $\sqrt {-1}$

 formalisé par Bombelli pour les équations de petit degré.
À cette époque et pendant plus d'un siècle, ce type de propos n'est pas sujet à démonstration, et prouver une définition, ou encore pire une imagination, n'a pas le moindre sens.

## L'émergence des nombres complexes

Il faut plus d'un siècle pour passer des nombres imaginaires, fictifs ou impossibles de Girard et Descartes, aux nombres complexes que nous connaissons, c'est-à-dire de la forme 

 $a+ib$

, où 

 $a$

 $b$

 sont des nombres réels. Petit à petit, les nombres complexes sont apprivoisés par les mathématiciens. À l'aide d'un développement en série, Gottfried Wilhelm Leibniz (1646 - 1716) donne un sens univoque à l'égalité de Bombelli:

 ${\sqrt[{3}]{2+\sqrt {-121}}}+{\sqrt[{3}]{2-\sqrt {-121}}}=4.$

L'usage de l'unité imaginaire 

 $i$

 devient de plus en plus fréquent, et cela dans des contextes bien différents de celui de la théorie des équations. Le mathématicien Abraham de Moivre démontre la formule qui porte son nom et éclaire la relation entre la trigonométrie et les nombres complexes. Enfin, la célèbre formule d'Euler 

 $e^{i\pi }+1=0$

, publiée en 1748, achève de convaincre les plus sceptiques.
En 1746, Jean le Rond d'Alembert exprime le besoin de démontrer le théorème fondamental de l'algèbre. Sa motivation n'est en rien algébrique, il souhaite démontrer l'existence d'une décomposition en éléments simples de n'importe quelle fonction rationnelle, afin d'en obtenir des primitives. Si le monde mathématique admet immédiatement le bien-fondé de la nécessité d'une démonstration, l'approche de D'Alembert ne séduit pas. Son procédé se fonde sur des convergences de suites et de familles de courbes, une approche purement analytique. Elle est de plus incomplète, et suppose sans preuve qu'une fonction continue sur un compact et à valeurs réelles atteint son minimum. Elle suppose aussi démontré un résultat sur la convergence de séries, maintenant connu sous le nom de théorème de Puiseux. Les grands noms de son époque souhaitent une démonstration algébrique, de même nature que le théorème.
La preuve de D'Alembert fut révisée par Argand en 1814. Ce dernier remplaça le théorème de Puiseux par une simple inégalité, connue aujourd'hui sous le nom d'inégalité d'Argand. Mais la preuve reste incomplète jusqu'au milieu du XIXe siècle.

## Les preuves d'Euler et de Lagrange

Deux tentatives de preuves sont l'œuvre de Leonhard Euler (1707 - 1783) et de Joseph-Louis Lagrange (1736 - 1813). Elles se suivent et celle plus tardive de Lagrange vise à combler certaines lacunes laissées par Euler.
Les démonstrations utilisent le fait que si le degré n d'un polynôme à coefficients réels est impair, il est « évident » que le polynôme admet une racine réelle, car si une grandeur est suffisamment grande, l'image par le polynôme de cette grandeur et de son opposé sont de signes opposés. Il faudra attendre les travaux de Bernard Bolzano de 1816 pour obtenir une démonstration du théorème des valeurs intermédiaires rigoureuse et pour que ce résultat ne soit plus une « évidence ».
 $n$

 n'est plus impair mais de la forme 

 $2^{p}q$

 $q$

 impair, l'objectif d'Euler et Lagrange est de montrer, par récurrence sur 

 $p$

 (cf. ci-dessus, § Corps réel clos), que toutes les racines imaginaires, au sens de Girard ou Descartes, sont complexes au sens où elles sont combinaisons linéaires à coefficients réels de 

 $1$

 et de 

 $i$

. La démonstration d'Euler est rigoureuse pour le degré 

 $4$

, mais à peine esquissée dans le cas général, celle de Lagrange se fonde sur des fonctions rationnelles invariantes par ce que l'on appelle maintenant un groupe de permutations des racines. D'autres tentatives de même nature sont l'œuvre de Foncenex et de Laplace.

## Gauss et la rigueur

Carl Friedrich Gauss écrit sa thèse de doctorat sur le sujet en 1799. Il reproche une démarche peu rigoureuse de la part de ses prédécesseurs, à l'exception de d'Alembert qui utilise un raisonnement analytique de nature différente (mais ayant aussi des lacunes). Ils supposent tous l'existence de 

 $n$

 racines et montrent que ces racines sont des nombres complexes. Le sens à donner à ces 

 $n$

 racines laisse Gauss perplexe, il s'exprime ainsi: « L'hypothèse de base de la démonstration, l'axiome est que toute équation possède effectivement 

 $n$

 racines possibles ou impossibles. Si l'on entend par possibles réels et par impossibles, complexes, cet axiome est inadmissible puisque c'est justement ce qu'il s'agit de démontrer. Mais si l'on entend par possibles les quantités réelles et complexes et par impossibles tout ce qui manque pour qu'on ait exactement 

 $n$

 racines, cet axiome est acceptable. Impossible signifie alors quantité qui n'existe pas dans tout le domaine des grandeurs. » La faiblesse, c'est que, si elles n'existent pas, et cela dans tout le domaine des grandeurs, est-il raisonnable de calculer dessus comme le font Euler et Lagrange?
La première preuve de Gauss, présentée en 1799 et fondée sur le canevas de d'Alembert, reste encore incomplète. À l'époque, l'existence d'un minimum atteint par une fonction continue définie sur un compact n'est pas démontrée. En 1814, un amateur suisse du nom de Jean-Robert Argand présente une preuve à la fois solide et simple, fondée sur le canevas de d'Alembert. La preuve de Cauchy dans son Cours d'analyse est inspirée, indirectement au moins, de celle d'Argand.
Selon Remmert, cette première preuve de Gauss est une belle preuve géométrique, mais reste encore incomplète. Les zéros sont interprétés comme les intersections des deux courbes algébriques réelles 

 $\mathrm {Re} (P)=0$

 $\mathrm {Im} (P)=0$

. En l'infini, ces courbes ont 

 $2n$

 branches qui s'alternent (partie facile de la preuve). Malheureusement, en déduire l'existence de 

 $n$

 points d'intersections comptées avec multiplicité n'est pas une application directe du théorème des valeurs intermédiaires. Elle ne sera donnée qu'en 1920, par Ostrowski.
La deuxième preuve de Gauss, en 1815, fait appel à la démarche d'Euler et de Lagrange. Cette fois-ci, il remplace les racines par des indéterminées, ce qui aboutit à une preuve rigoureuse, mais plus tardive que celle d'Argand. Les deux seules hypothèses que fait Gauss sont (i) toute équation algébrique de degré impair a une racine réelle; (ii) toute équation quadratique à coefficients complexes a deux racines complexes.
La troisième preuve de Gauss date de 1816. Il s'agit en réalité d'un résultat sur la localisation des zéros des fonctions polynomiales, dont la généralisation (en 1862) aux fonctions holomorphes est le théorème de Rouché.
La quatrième preuve de Gauss date de 1849. Il s'agit d'une variante de la première preuve, où Gauss envisage cette fois des polynômes à coefficients complexes.

## La théorie de Galois

L'histoire finit par combler la lacune de la démonstration de Lagrange. Évariste Galois (1811 - 1832) réutilise les idées de Lagrange sous un angle plus novateur et qui préfigure l'algèbre moderne. Ces idées, reprises par Ernst Kummer et Leopold Kronecker, débouchent sur l'existence d'un corps contenant toutes les racines du polynôme, et cela indépendamment de toute construction sur les nombres complexes. Ce corps est appelé corps de décomposition, son usage permet la reprise des idées de Lagrange, de manière tout à fait rigoureuse.
Remmert attribue cette réactualisation de la preuve de Lagrange à Adolf Kneser. Une version moderne due à Artin, utilisant la théorie de Galois et le premier théorème de Sylow, redémontre que les seules extensions finies de ℝ sont 

 $\mathbb {R}$

 $\mathbb {C}$

## Démonstrations itératives et effectivité

Même complétée et corrigée, la démonstration de D'Alembert et d'Argand n'est pas constructive: elle utilise le fait que le module d'un polynôme atteint son minimum, sans préciser en quel point. Il serait pourtant souhaitable de pouvoir approcher les racines des polynômes, par exemple en disposant d'une démonstration qui explicite une manière d'exhiber une racine, ou une suite de nombres complexes qui converge vers une racine. Des théorèmes de localisation sur les zéros des fonctions holomorphes peuvent être déduits du théorème des résidus dû à Cauchy, mais ne sont pas réellement effectifs: il est difficile d'implémenter un algorithme d'approximation fondé sur ceux-ci (et ils sont inutilisables en pratique sans ordinateurs puissants); on trouvera une analyse plus précise de ces méthodes dans cette section de l'article Hypothèse de Riemann, car ce sont les seules utilisables pour localiser les zéros de la fonction 

 $\zeta$

Selon Remmert, la première tentative significative fut proposée par Weierstrass en 1859. Bien que la méthode proposée ne fonctionne pas bien, l'idée est intéressante: il s'agit d'itérer la fonction

 $x\mapsto x-P(x)$

Ceci donne lieu à une suite qui, si elle converge, converge vers un zéro de 

 $P$

. Cette idée est exploitée pour montrer le théorème du point fixe pour les fonctions contractantes par exemple. Cependant, la convergence n'est, ici, pas automatique: l'ensemble des valeurs de 

 $x$

 pour lesquelles la suite itérée est bornée n'est pas 

 $\mathbb {C}$

 en général; même en se limitant à un domaine borné, il arrive fréquemment que la suite diverge pour presque tout point de départ; ceux pour lesquels elle reste bornée forment d'ailleurs une des « fractales » les plus connues: l'ensemble de Julia (rempli) associé à 

 $P$

, et qui est souvent une poussière de Cantor, de dimension de Hausdorff nulle; c'est par exemple le cas du polynôme 

 $P(X)=-X^{2}+X-1$

D'un point de vue pratique, une autre suite convergeant plus souvent est donnée par la méthode de Muller; elle demande à chaque étape le calcul d'une racine carrée (complexe).
Si les racines du polynôme 

 $P$

 étudié sont simples (ce qui est une condition générique), la méthode de Newton peut être appliquée. Elle consiste à itérer la fonction

 $x\mapsto x-\dfrac {P(x)}{P'(x)},$

qui à 

 $x$

 associe le point où s'annule la fonction affine tangente à 

 $P$

 $x$

. Encore une fois, si cette suite converge, sa limite est un zéro de 

 $P$

 et, cette fois, la convergence est assurée si la valeur initiale est choisie suffisamment proche d'une racine de 

 $P$

Une importante correction a été apportée par Morris Hirsch et Stephen Smale en 1979. Elle consiste à itérer la fonction

 $$x\mapsto x-\min(1,H(x))\frac {P(x)}{P'(x)},$$

où la fonction 

 $H$

 est définie en fonction du polynôme 

 $P$

 par la formule

 $$H(x)=C(|x|)\frac {|P'(x)|^{2}{|P(x)|\max |a_{i}|}}.$$

 $a_{i}$

 sont les coefficients de 

 $P$

 $C$

 est une fonction rationnelle d'une variable réelle. Hirsch et Smale démontrèrent que la suite obtenue 

 $z_{k}$

 converge toujours vers un zéro du polynôme 

 $P$

, quelle que soit la valeur initiale 

 $z_{0}$

Weierstrass propose également en 1891 une méthode itérative, connue actuellement sous le nom de méthode de Durand-Kerner (en), plus puissante qui converge (dans de bonnes conditions) non pas vers une seule racine mais vers l'ensemble des 

 $n$

 racines simples 

 $(\zeta _{j})$

 $$z_{k}^{(i+1)}=z_{k}^{(i)}-{\frac {P(z_{k}^{(i)})}{a_{n}\,\prod _{j\not =k}(z_{k}^{(i)}-z_{j}^{(i)})}}$$

 qui est proche de l'itération de

 $$z_{k}^{(i+1)}=z_{k}^{(i)}-{\frac {P(z_{k}^{(i)})}{a_{n}\,\prod _{j\not =k}(z_{k}^{(i)}-\zeta _{j})}}$$

 qui a pour point fixe les racines.
