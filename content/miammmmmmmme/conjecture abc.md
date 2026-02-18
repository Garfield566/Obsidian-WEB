---
nom: "conjecture abc"
qid: Q306393
type: conjecture
categorie: conjecture
tags: "#mathematiques/conjecture"
image: https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Oesterle_Joseph.jpg/330px-Oesterle_Joseph.jpg
---

# Conjecture abc

> [!Infobox]
> **Conjecture abc**
> ![[https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Oesterle_Joseph.jpg/330px-Oesterle_Joseph.jpg|300]]
> - **Découvert(e) ou inventé(e) par** : Joseph Oesterlé, David Masser
> - **Formule décrivant** : entier strictement positif
> - **Date de découverte ou d'invention** : 1985

La conjecture abc ou conjecture d'Oesterlé-Masser est une conjecture en théorie des nombres. Elle a été formulée pour la première fois par Joseph Oesterlé (1988) et David Masser (1985). Elle est formulée en termes de trois nombres entiers positifs, a, b et c (d'où son nom), qui n'ont aucun facteur commun et satisfont à 

 $a+b=c$

. Si d est le produit des facteurs premiers distincts de abc, alors la conjecture affirme à peu près que d ne peut pas être beaucoup plus petit que c. Plus précisément, le rapport 

 $\tfrac {c}{d}$

 peut prendre des valeurs très grandes mais le rapport 

 $\tfrac {c}{d^{1+\varepsilon }}$

 est lui borné pour tout 

 $\varepsilon >0$

Dorian Goldfeld l'a qualifié en 2006 de « problème non résolu le plus important en analyse diophantienne » car, si elle était vérifiée, la conjecture permettrait de démontrer aisément le théorème de Fermat-Wiles dans un sens asymptotique, entre autres.
Des démonstrations diverses de cette conjecture ont été revendiquées, mais à ce jour aucune n'est acceptée par la communauté mathématique.

## Triplets (a, b, c)

Un problème classique en arithmétique est de trouver des triplets (a, b, c) de nombres entiers strictement positifs, premiers entre eux, avec a + b = c où les nombres sont des puissances de nombres entiers (voir le dernier théorème de Fermat).
Par exemple:

 $$2^{5}+7^{2}=3^{4},\qquad 13^{2}+7^{3}=2^{9},\qquad 2^{7}+17^{3}=71^{2},\qquad 3^{5}+11^{4}=122^{2}.$$

Tidjman et Zagier conjecturent que l'équation 

 $x^{p}+y^{q}=z^{r}$

 n'a aucune solution avec des exposants (p, q, r) tous supérieurs à 2 et x, y, z des entiers strictement positifs et premiers entre eux.
Un autre problème arithmétique est d'écrire les entiers comme différence de deux puissances (d'exposants supérieurs à 1) de nombres entiers (voir la conjecture de Pillai, le théorème de Catalan et la conjecture de Fermat-Catalan).
Par exemple:

 $$1=3^{2}-2^{3},\qquad 2=3^{3}-5^{2},\qquad 3=2^{7}-5^{3},\qquad 4=5^{3}-11^{2},\qquad 5=2^{5}-3^{3}.$$

Plus généralement, on s'intéresse à des triplets (a, b, c) de nombres entiers non nuls (éventuellement négatifs), premiers entre eux, avec a + b = c, où les nombres ont des facteurs premiers petits par rapport aux trois nombres.

## Radical et qualité d'un triplet

Soit (a, b, c) un triplet de nombres entiers (non nuls) tel que c = a + b. Le produit des facteurs premiers de abc est appelé le radical de abc.
On définit la qualité d'un triplet (a, b, c) de nombres positifs (avec c = a + b) par:

 $$q(a,b,c)={\frac {\log(c)}{\log(\operatorname {rad} (abc))}}$$

## Un premier exemple

$a=1,\quad b=2^{3}=8\quad \text{ et }\quad c=a+b=9=3^{2}.\quad \,$

Les nombres premiers qui divisent abc sont 2 et 3.
Le radical du triplet (1; 8; 9) est le produit des diviseurs premiers de abc: 

 $\operatorname {rad} (1\times 8\times 9)=2\times 3=6$

On remarque que, dans notre exemple, le radical est plus petit que c, le plus grand des nombres a, b, c: 

 $\operatorname {rad} (abc)<c$

Les triplets (a, b, c) de nombres positifs, premiers entre eux, avec a + b = c, tels que 

 $\operatorname {rad} (abc)<c$

, sont rares. Par exemple, il n'y en a que six parmi les triplets de nombres inférieurs à 100.
Dans notre exemple la qualité du triplet vaut environ 1,2263:

 $$q(1,8,9)=\frac {\log(9)}{\log(6)}\approx {}1{,}2263$$

La qualité du triplet (1; 8; 9) est la puissance à laquelle il faut élever le radical pour obtenir c.
On a: 

 $c=a+b\approx \operatorname {rad} (abc)^{1{,}2263}$

Les triplets dont le radical est inférieur à c sont ceux qui ont une qualité supérieure à 1.

## Deuxième exemple

$a=3,\quad b=5^{3}=125\quad \text{ et }\quad c=2^{7}=128.\;$

Le radical du triplet (3; 125; 128) est: 

 $\operatorname {rad} (3\times 125\times 128)=2\times 3\times 5=30$

, qui est beaucoup plus petit que c.
La qualité du triplet est environ 1,4266: 

 $$q(3,125,128)=\frac {\log(128)}{\log(30)}\approx {}1{,}4266$$

On a: 

 $c=a+b\approx \operatorname {rad} (abc)^{1{,}4266}$

On voit que la qualité du triplet (a, b, c) est encore inférieure à 2. C'est le cas de tous les triplets de nombres premiers entre eux (a, b, c) dont la qualité a été calculée.
La conjecture abc énonce que les triplets de nombres (positifs et premiers entre eux) pour lesquels 

 ϵ

 $c=a+b>\operatorname {rad} (abc)^{1+\epsilon }$

 n'existent qu'en nombre fini quel que soit le nombre 

 ϵ
 $\epsilon >0$

 fixé.

## Énoncé de la conjecture

Quel que soit 

 $\varepsilon >0$

, il existe une constante 

 $K_{\varepsilon }$

 telle que, pour tout triplet 

 $(a,b,c)$

 d'entiers relatifs (non nuls) premiers entre eux vérifiant 

 $a+b=c$

, on ait:

 $$\max(|a|,|b|,|c|)\leq \operatorname {K} _{\varepsilon }(\operatorname {rad} (abc))^{1+\varepsilon }$$

où 

 $\operatorname {rad} (n)$

 est le radical de n, c'est-à-dire le produit des nombres premiers divisant n.

## Formulations équivalentes

Une deuxième formulation utilise les logarithmes. En prenant le logarithme dans la première formulation, on obtient:

 ϵ
 $$\max(\log |a|,\log |b|,\log |c|)\leq \log \operatorname {K} _{\varepsilon }+(1+\epsilon )\log \operatorname {rad} (abc)$$

On peut formuler la conjecture en faisant intervenir la notion de qualité q(a, b, c) d'un triplet (a; b; c), définie par 

 $$q(a,b,c)={\frac {\log |c|}{\log(\operatorname {rad} (abc))}}$$

Avec cette notation, la conjecture suppose que pour tout ε > 0, il n'existe qu'un nombre fini de triplets (a; b; c) d'entiers positifs et premiers entre eux tels que: a + b = c et q(a, b, c) > 1 + ε.
Une autre forme de la conjecture affirme que pour tout ε > 0, il n'existe qu'un nombre fini de triplets (a; b; c) d'entiers positifs et premiers entre eux tels que: a + b = c et

 $c>(\operatorname {rad} (abc))^{1+\varepsilon }.$

## Le cas ε = 0

On ne peut pas enlever l'hypothèse 

 $\varepsilon >0$

 dans la formulation de la conjecture. En effet, si on prend:

 $a_{n}=3^{2^{n}},\quad b_{n}=-1,\quad \text{ et }\quad c_{n}=3^{2^{n}}-1$

 $a_{n},b_{n},\text{ et }c_{n}$

 sont premiers entre eux et on a 

 $a_{n}+b_{n}=c_{n}$

. De plus, si n > 0, 

 $2^{n+2}$

 divise 

 $c_{n}$

, donc:

 $$\operatorname {rad} (|a_{n}b_{n}c_{n}|)\leq 3\times 2\times {|c_{n}| \over 2^{n+2}}\frac {2^{n+1}{3}}\operatorname {rad} (|a_{n}b_{n}c_{n}|)>2^{n-1}\operatorname {rad} (|a_{n}b_{n}c_{n}|)$$

Le rapport 

 $${\frac {\max(|a_{n}|,|b_{n}|,|c_{n}|)}{\operatorname {rad} (|a_{n}b_{n}c_{n}|)}}>2^{n-1}$$

 prend des valeurs arbitrairement grandes.

## Exemple

Pour n = 2, 

 $3^{2^{2}}=81,\quad \text{ et }\quad 3^{2^{2}}-1=80=2^{4}\times 5$

le triplet (1; 80; 81) a pour radical: 

 $\operatorname {rad} (1\times 80\times 81)=2\times 3\times 5=30$

 $\max(|a|,|b|,|c|)=2{,}7\operatorname {rad} (abc)>2\operatorname {rad} (abc)$

La qualité du triplet (1; 80; 81) est environ 1,2920: 

 $$q(1,80,81)=\frac {\log(81)}{\log(30)}\approx {}1{,}2920$$

. (On a: 

 $\max(|a|,|b|,|c|)\approx \operatorname {rad} (abc)^{1{,}2920}$

## Le triplet (1 ; 4 374 ; 4 375)

Un exemple de triplet ayant une qualité élevée est:

 $a=1,\quad b=2\times 3^{7}=4\;374\quad \text{ et }\quad c=5^{4}\times 7=4\;375.$

 Son radical est: 

 $\operatorname {rad} (abc)=2\times 3\times 5\times 7=210$

La qualité du triplet (a; b; c) est environ 1,5679: 

 $$q(a,b,c)=\frac {\log(4\;375)}{\log(210)}\approx {}1{,}5679$$

On a: 

 $c=a+b\approx \operatorname {rad} (abc)^{1{,}5679}$

## Le triplet de Reyssat

Éric Reyssat (de) a découvert le triplet qui a la plus grande qualité connue:

 $$a=2,\quad b=3^{10}\times 109=6\;436\;341\quad \text{ et }\quad c=23^{5}=6\;436\;343.$$

Son radical est: 

 $\operatorname {rad} (abc)=2\times 3\times 109\times 23=15\;042$

La qualité du triplet (a; b; c) est environ 1,6299: 

 $$q(a,b,c)={\frac {\log(23^{5})}{\log(15\;042)}}\approx {}1{,}6299$$

On a: 

 $c=a+b\approx \operatorname {rad} (abc)^{1{,}6299}$

## Analogie avec les polynômes : le théorème de Mason-Stothers

L'idée de la conjecture abc s'est formée par analogie avec les polynômes. Un théorème abc est en effet disponible pour les polynômes sur un corps algébriquement clos de caractéristique nulle.
L'analogue pour les polynômes (en) a été démontré par Wilson Stothers (en) en 1981, et de manière élémentaire par Richard Mason (nl) en 1984. Il se formule ainsi:

Pour tous les polynômes 

 $a(t),b(t),c(t)$

 premiers entre eux vérifiant 

 $a+b=c$

, on a 

 $\max(\deg\{a,b,c\})\leq n_{0}(abc)-1$

où 

 $n_{0}(abc)$

 est le nombre de racines distinctes de abc.
Ce théorème permet de démontrer de manière aisée le théorème de Fermat pour les polynômes: l'équation

 $X(t)^{n}+Y(t)^{n}=Z(t)^{n}$

où 

 $X(t),Y(t),Z(t)$

 sont des polynômes non constants, n'a pas de solutions si 

 $n\geq 3$

La tentation est alors grande de trouver un analogue pour les entiers, car il permettrait de démontrer tout aussi facilement le théorème de Fermat dans un sens asymptotique.

## Le théorème de Fermat asymptotique

En supposant la conjecture abc, on peut démontrer une version asymptotique du théorème de Fermat, dans le sens où on montre qu'il existe N tel que pour tout 

 $n\geq N$

 $x^{n}+y^{n}=z^{n}$

 n'a plus de solutions entières (strictement positives). Ce N dépendrait cependant explicitement de la constante 

 $K_{\varepsilon }$

 donnée par la conjecture abc.
En prenant un 

 ϵ

 $\epsilon$

 strictement positif quelconque, on suppose que x, y et z sont des entiers tous non nuls tels que 

 $x^{n}+y^{n}=z^{n}$

. Quitte à les réorganiser, on les suppose tous positifs et, quitte à les diviser par leur PGCD à la puissance n, on suppose qu'ils sont premiers entre eux. On a donc d'après la conjecture abc:

 ϵ

 $$\max(|x|^{n},|y|^{n},|z|^{n})=z^{n}\leq \operatorname {K} _{\epsilon }\operatorname {rad} ((xyz)^{n})^{1+\varepsilon }$$

 $\operatorname {rad} ((xyz)^{n})=\operatorname {rad} (xyz)$

. Ceci donne, compte tenu de 

 $\operatorname {rad} (xyz)\leq xyz\leq z^{3}$

 $z^{n}\leq \operatorname {K} _{\varepsilon }z^{3(1+\varepsilon )}$

donc en supposant 

 $z\geq 2$

, on obtient:

 $$n\leq 3(1+\varepsilon )+{\frac {\ln(\operatorname {K} _{\varepsilon })}{\ln(2)}}$$

 ϵ
 $\epsilon =1$

, on a 

 $$n\leq 6+{\frac {\ln(\operatorname {K} _{1})}{\ln(2)}}$$

ce qui fournit un majorant de n dépendant explicitement de 

 $\operatorname {K} _{1}$

## Autres conséquences

La conjecture abc permettrait de prouver d'autres théorèmes importants en théorie des nombres, parmi lesquels:

le théorème de Roth;
le théorème de Baker;
le théorème de Bombieri-Vinogradov;
le théorème de Faltings précédemment nommé conjecture de Mordell;
la conjecture de Pillai;
la conjecture de Szpiro.
La conjecture d'Erdős-Woods s'en déduirait également, à un ensemble fini près de contre-exemples.

## Démonstrations revendiquées

Lucien Szpiro a proposé une démonstration en 2007 mais elle a été rapidement décelée comme incorrecte. La conjecture qui porte son nom sous une forme modifiée est équivalente à la conjecture abc.
En août 2012, le mathématicien japonais Shinichi Mochizuki a publié un article sur sa page personnelle où il annonce avoir démontré cette conjecture. Mais cette démonstration n'a pas été validée par les autres spécialistes de la question. Peter Scholze et Jacob Stix ont publiquement déclaré que, en septembre 2018, cette démonstration n'était en l'état pas recevable. Néanmoins, en avril 2020, sa démonstration est acceptée pour publication dans Publications of the Research Institute for Mathematical Sciences, journal publié par l'Institut de recherches pour les sciences mathématiques dont Mochizuki est l'éditeur en chef.
ABC@home est un projet de calcul réparti utilisant BOINC afin de démontrer la conjecture abc en trouvant tous les triplets (a, b, c) jusqu'à 1018, voire plus.
