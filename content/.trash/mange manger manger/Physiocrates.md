---
nom: "Physiocrates"
qid: Q190109
type: ecole_economique
categorie: ecole_economique
tags: "#economie/ecole"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Anillo_cíclico.png
---

# Corps commutatif

> [!Infobox]
> **Corps commutatif**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Anillo_cíclico.png|300]]
> - **Discipline dont c'est l'objet** : théorie des corps, théorie des catégories, algèbre générale

En mathématiques, un corps commutatif (parfois simplement appelé corps, voir plus bas, également champ algébrique ou simplement champ) est une des structures algébriques fondamentales de l'algèbre générale. C'est un ensemble muni de deux opérations binaires rendant possibles les additions, soustractions, multiplications et divisions. Plus précisément, un corps commutatif est un anneau commutatif dans lequel l'ensemble des éléments non nuls est un groupe commutatif pour la multiplication.
Selon la définition choisie d'un corps qui diffère selon les auteurs (la commutativité de la multiplication n'est pas toujours imposée), soit les corps commutatifs sont des cas particuliers de corps (dans le cas où la commutativité n'est pas imposée), soit la dénomination corps commutatif est un pléonasme qui désigne simplement un corps (dans le cas où elle l'est). On renvoie à l'article corps (mathématiques) pour plus de détails.
Des exemples élémentaires de corps commutatifs sont le corps des nombres rationnels noté 

 $\mathbb {Q}$

 $\mathbf {Q}$

), le corps des nombres réels noté 

 $\mathbb {\mathbb {R} }$

 $\mathbf {R}$

), le corps des nombres complexes noté 

 $\mathbb {C}$

 $\mathbf {C}$

) et le corps ℤ/pℤ des classes de congruences modulo p où p est un nombre premier, noté alors également 

 $\mathbb {F} _{p}$

 $\mathbf {F} _{p}$

La théorie des corps commutatifs est le cadre historique de la théorie de Galois, une méthode d'étude qui s'applique en particulier aux corps commutatifs et aux extensions de corps, en relation avec la théorie des groupes, mais s'étend aussi à d'autres domaines, par exemple l'étude des équations différentielles (théorie de Galois différentielle), ou des revêtements.

## Fragments d'histoire

La théorie des corps (commutatifs) se développe tout au long du XIXe siècle, en parallèle et de façon intimement liée avec la théorie des groupes, la théorie des anneaux et l'algèbre linéaire. Jusqu'à cette époque, l'algèbre s'identifie à la théorie des équations polynomiales et de leur résolution. C'est dans ce contexte qu'apparaissent les premières notions de théorie des corps, avec les travaux de Niels Abel et ceux d'Évariste Galois, même si la structure n'est pas identifiée explicitement. Galois est le premier à parler d'adjonction (pour des éléments algébriques) et démontre le théorème de l'élément primitif.
Avec la naissance de l'étude des nombres algébriques, motivée par des problèmes de nature arithmétique, il est devenu nécessaire de préciser explicitement la structure de corps, en parallèle avec les notions d'entier algébrique, et d'anneau. C'est dans ce contexte que la structure de corps est introduite indépendamment (et de façons assez différentes) par Richard Dedekind et Leopold Kronecker. Le vocabulaire actuel vient de Dedekind, qui définit un corps (Körper en allemand, c'est la raison pour laquelle un corps quelconque est souvent nommé K) comme un sous-ensemble de nombres réels ou complexes stable par addition, soustraction, multiplication et division.
Par ailleurs, Gauss avait étudié les congruences sur les entiers dans ses Disquisitiones arithmeticae, parues en 1801, et étudié en détail le cas premier, ce qui revient implicitement à l'étude des corps finis premiers. En 1830, s'inspirant de Gauss, Galois avait étendu cette étude aux corps finis quelconques, les éléments de ceux-ci étant vus comme des expressions polynomiales finies traitées comme des nombres (le calcul se faisant modulo un polynôme irréductible). E. H. Moore montre en 1893 qu'un corps commutatif fini, qu'il voit comme un ensemble de symboles de cardinal fini s, muni des quatre opérations « sujettes aux identités ordinaires de l'algèbre abstraite » peut se définir à la façon de Galois.
La même année, Heinrich Weber donne la première véritable axiomatisation des corps (commutatifs), dans un article dont le but est de donner une présentation générale de la théorie de Galois. L'axiomatisation des théories mathématiques en est encore à ses balbutiements et Weber oublie (mais bien sûr utilise) l'associativité de la multiplication.
En 1910, Ernst Steinitz établit la théorie axiomatique des corps, dans un mémoire fondateur de l'algèbre moderne.

## Définition et exemples

Un corps commutatif est un ensemble 

 $K$

 muni de deux lois internes notées en général 

 $+$

 $\times$

 vérifiant les conditions suivantes:

 $\left(K,+\right)$

 forme un groupe abélien (on dit aussi: groupe commutatif), dont l'élément neutre est noté 

 $0$

 ∖
 $(K\setminus \{0\},\times )$

 forme un groupe abélien, dont l'élément neutre est 

 $1$

la multiplication est distributive par rapport à l'addition (à gauche comme à droite) c'est-à-dire que

 $$\forall (a,b,c)\in K^{3}\quad a\times (b+c)=a\times b+a\times c\quad \hbox{et}\quad (b+c)\times a=b\times a+c\times a$$

On parle alors du corps commutatif 

 $(K,+,\times )$

Exemples de corps commutatifs:

l'ensemble 

 $(\mathbb {Q},+,\times )$

 des nombres rationnels;
l'ensemble 

 $(\mathbb {R},+,\times )$

 des nombres réels;
l'ensemble 

 $(\mathbb {C},+,\times )$

 des complexes;
l'ensemble 

 $\left(\mathbb {Z} /p\mathbb {Z},+,\times \right)$

 des entiers modulo un nombre premier p. Ou 

 $\mathbb {Z} /p\mathbb {Z}$

 représente l'anneau ℤ/pℤ.
Un sous-corps d'un corps commutatif 

 $K$

 est une partie 

 $L$

 $K$

, stable par 

 $+$

 $\times$

, telle que 

 $L$

 munie des lois induites soit un corps.

## Caractéristique et corps premier

$1_{K}$

 l'unité du corps 

 $K$

. S'il existe un entier naturel 

 $n$

 non nul tel que 

 ⏟

 $n\cdot 1_{K}=\underbrace {1_{K}+1_{K}+\cdots } _{n\text{ fois }}$

 est nul, on appelle caractéristique du corps 

 $K$

 le plus petit entier positif non nul vérifiant cette propriété. S'il n'existe pas d'entier non nul vérifiant cette propriété, on dit que le corps 

 $K$

 est de caractéristique nulle.
Par exemple, le corps 

 $\mathbb {R}$

 est de caractéristique nulle alors que le corps 

 $\mathbb {Z} /p\mathbb {Z}$

 est de caractéristique 

 $p$

. Si elle est non nulle, la caractéristique d'un corps est nécessairement un nombre premier. En effet si tel n'était pas le cas une factorisation de ce nombre fournirait des diviseurs non nuls de 

 $0$

, or un corps est un anneau intègre.
Un corps est dit premier s'il n'a pas de sous-corps autre que lui-même. Un corps premier infini est isomorphe au corps 

 $\mathbb {Q}$

 des nombres rationnels. Un corps premier fini est isomorphe au corps 

 $\mathbb {Z} /p\mathbb {Z}$

 pour un certain nombre premier 

 $p$

Plus généralement, tout corps 

 $K$

 contient un corps premier, qui est le plus petit de ses sous-corps, et que l'on appelle corps premier de 

 $K$

, ou sous-corps premier de 

 $K$

. Le sous-corps premier de 

 $K$

 contient nécessairement 

 $1_{K}$

, donc ses multiples entiers 

 $\mathbb {Z} \cdot 1_{K}$

. Si la caractéristique est nulle c'est donc un corps isomorphe à 

 $\mathbb {Q}$

 (le corps des fractions de 

 $\mathbb {Z}$

); si la caractéristique est un nombre premier 

 $p$

, c'est un corps isomorphe à 

 $\mathbb {Z} /p\mathbb {Z}$

, et on identifie habituellement ce sous-corps premier soit à 

 $\mathbb {Q}$

 soit à 

 $\mathbb {Z} /p\mathbb {Z}$

## Corps finis

Ce sont les corps dont le nombre d'éléments est fini. Le théorème de Wedderburn montre qu'ils sont nécessairement commutatifs. On démontre aussi que le nombre d'éléments d'un tel corps est toujours une puissance d'un nombre premier. Il est en fait possible de dresser la liste de tous les corps finis, à isomorphisme près.
Le plus petit corps fini est celui des booléens, dont voici les tables d'addition (correspondant au « ou exclusif ») et de multiplication (correspondant au « et »):

Les exemples les plus élémentaires de corps finis sont les corps de congruences modulo un nombre premier comme dans le cas ci-dessus, mais il en existe une infinité d'autres: à isomorphisme près, un par puissance de nombre premier.

## Corps et anneau

L'ensemble 

 $(\mathbb {Z},+,\times )$

 n'est pas un corps car la plupart des éléments non nuls de 

 $\mathbb {Z}$

 ne sont pas inversibles: par exemple, il n'existe pas d'entier relatif 

 $n$

 tel que 

 $2n=1$

 $2$

 n'est pas inversible.
Un anneau commutatif est un ensemble A qui, comme 

 $\mathbb {Z}$

, est muni de deux lois 

 $+$

 $\times$

 vérifiant les axiomes suivants:

 $(A,+)$

 forme un groupe abélien dont l'élément neutre est noté 

 $0$

 ∖
 $(A\setminus \{0\},\times )$

 forme un monoïde commutatif;
la multiplication est distributive par rapport à l'addition (à gauche comme à droite).
Un anneau commutatif A est intègre s'il vérifie:

 $\forall (a,b)\in A^{2},\quad ab=0\Rightarrow (a=0\hbox{ ou }b=0)$

Tout corps commutatif est un anneau intègre et tout anneau intègre fini est un corps. Le théorème suivant règle le cas des anneaux infinis:

si un anneau commutatif A est intègre, on peut le plonger dans son corps des fractions, qui est le plus petit corps contenant l'anneau.

Exemple: 

 $\mathbb {Q}$

 est le corps des fractions de 

 $\mathbb {Z}$

Un anneau commutatif A est un corps si et seulement s'il est simple, c.-à-d. non nul et sans idéaux non triviaux.
Un anneau commutatif non nul A est un corps si et seulement si tout A-module est libre.

## Corps et espace vectoriel

Partant du corps 

 $\mathbb {R}$

, il est naturel de s'intéresser à 

 $\mathbb {R} ^{n}$

, ensemble des n-uplets de réels. On est amené à le munir d'une addition et d'une multiplication par un réel. La structure ainsi définie (une addition interne munissant l'ensemble d'une structure de groupe et une multiplication externe possédant des propriétés de distributivité et d'associativité) est appelée espace vectoriel sur 

 $\mathbb {R}$

. Il est alors naturel de définir ce que pourrait être un espace vectoriel sur un corps commutatif K quelconque.

## Corps et équation algébrique

L'étude des polynômes à coefficients dans un corps commutatif et la recherche de leurs racines ont développé considérablement la notion de corps. Si 

 $f$

 est un polynôme de degré 

 $n$

 sur un corps commutatif 

 $K$

, l'équation 

 $f(x)=0$

 est une équation algébrique dans 

 $K$

. Si, de plus, 

 $f$

 est un polynôme irréductible, l'équation est dite irréductible. Lorsque 

 ⩾
 $n\geqslant 2$

, trouver les solutions d'une telle équation demande de se placer dans un corps plus grand que 

 $K$

, une extension de corps. 
Par exemple, l'équation 

 $x^{2}-2=0$

 est irréductible dans 

 $\mathbb {Q}$

 mais possède des racines dans 

 $\mathbb {R}$

 ou mieux dans 

 $\mathbb {Q} \left[\sqrt {2}\right]$

. L'équation 

 $x^{2}+1=0$

 ne possède pas de solution dans 

 $\mathbb {R}$

 mais en possède dans 

 $\mathbb {C}$

 ou mieux dans 

 $\mathbb {Q} \left[i\right]$

Un corps de rupture d'un polynôme est, par exemple, un corps minimal contenant 

 $K$

 et une racine de 

 $f$

Le corps de décomposition de 

 $f$

 est le plus petit corps contenant 

 $K$

 ainsi que toutes les racines de 

 $f$

L'étude des corps de décomposition d'un polynôme et du groupe de permutations de ses racines forme la branche des mathématiques que l'on appelle la théorie de Galois.

## Propriétés

$(K,+,\times )$

 un corps commutatif. Alors tout polynôme de degré 

 ⩾
 $n\geqslant 0$

 admet au plus 

 $n$

 zéros (ou racines) dans 

 $K$

 $(K,+,\times )$

 un corps commutatif. Alors tout sous-groupe fini de 

 ∗

 $\left(K^{*},\times \right)$

 est un groupe cyclique.

Ces résultats restent vrais si l'on remplace le corps par un anneau commutatif intègre quelconque (comme on peut voir en plongeant un tel anneau dans son corps des fractions).

## Autres domaines d'étude

On retrouve la théorie des corps dans l'étude de certaines fonctions comme les fonctions rationnelles ou les fonctions elliptiques.

## Structures additionnelles

Corps valué
Corps ordonné
