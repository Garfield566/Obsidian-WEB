---
nom: "Theoreme des nombres premiers"
qid: Q190026
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/EulerPhi.svg
---

# Indicatrice d'Euler

> [!Infobox]
> **Indicatrice d'Euler**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/EulerPhi.svg|300]]
> - **Découvert(e) ou inventé(e) par** : Leonhard Euler
> - **Nomme d'apres** : Leonhard Euler
> - **Discipline dont c'est l'objet** : arithmétique modulaire

En mathématiques, l'indicatrice d'Euler est une fonction arithmétique de la théorie des nombres, qui à tout entier naturel n non nul associe le nombre d'entiers compris entre 1 et n (inclus) et premiers avec n.
Elle intervient en mathématiques pures, à la fois en théorie des groupes, en théorie algébrique des nombres et en théorie analytique des nombres.
En mathématiques appliquées, à travers l'arithmétique modulaire, elle joue un rôle important en théorie de l'information et plus particulièrement en cryptologie.
L'indicatrice d'Euler est aussi appelée indicateur d'Euler, fonction phi d'Euler ou simplement fonction phi, car la lettre 

 $\varphi$

 ϕ

 $\phi$

) est communément utilisée pour la désigner.
Elle porte le nom du mathématicien suisse Leonhard Euler, qui fut le premier à l'étudier.

## Histoire et notation

Leonhard Euler a le premier étudié cette fonction dans les années 1750, mais tout d'abord sans lui donner de nom. Ce n'est qu'en 1784, dans un article où il reprend l'étude de cette fonction, qu'il utilise pour la dénoter la lettre grecque π, sans parenthèses autour de l'argument: denotet character πD multitudinem istam numerorum ipso D minorum, et qui cum eo nullum habeant divisorem communem. C'est finalement en 1801 que Carl Friedrich Gauss introduit la lettre grecque ϕ, dans les Disquisitiones arithmeticae (art. 38), toujours sans user de parenthèses autour de l'argument; il écrit ainsi ϕA pour ce qui est noté maintenant ϕ(A). De nos jours, on emploie la lettre grecque phi minuscule en italique ϕ ou φ.
En 1879, J. J. Sylvester invente le terme de totient pour désigner cette fonction, de sorte qu'elle est généralement désignée sous le terme de « Euler's totient function » dans les écrits anglophones. Le terme totient est employé pour la fonction totient de Jordan, qui est une généralisation de l'indicatrice d'Euler.

## Définition et exemples

L'indicatrice d'Euler est la fonction φ, de l'ensemble ℕ* des entiers strictement positifs dans lui-même, définie par:

 ∗

 ⟶

 ∗

 ⟼

 ∗

 ⩽
 $${\begin{array}{ccccl}\varphi &:&\mathbb {N} ^{*}&\longrightarrow &\mathbb {N} ^{*}\\&&n&\longmapsto &\mathrm {card} (\{m\in \mathbb {N} ^{*}~|~m\leqslant n~\text{et}~m~\mathrm {premier~avec} ~n\}).\end{array}}$$

Par exemple:

φ(8) = 4 car parmi les nombres de 1 à 8, seuls les quatre nombres 1, 3, 5 et 7 sont premiers avec 8;
φ(12) = 4 car parmi les nombres de 1 à 12, seuls les quatre nombres 1, 5, 7 et 11 sont premiers avec 12;
un entier p > 1 est premier si et seulement si tous les nombres de 1 à p – 1 sont premiers avec p, c.-à-d. si et seulement si φ(p) = p – 1;
φ(1) = 1 car 1 est premier avec lui-même (c'est le seul entier naturel qui vérifie cette propriété, si bien que pour tout entier n > 1, on peut remplacer non seulement m ∈ ℕ* par m ∈ ℕ mais m ≤ n par m < n, dans la définition ci-dessus de φ(n)).
On trouvera ci-dessous les 99 premières valeurs de la fonction φ (suite  A000010 de l'OEIS).

## Calcul

La valeur de l'indicatrice d'Euler s'obtient à partir de la décomposition en facteurs premiers de n:

 $$\rm {si}\quad n=\prod _{i=1}^{r}p_{i}^{k_{i}}\quad \rm {alors}\quad \varphi (n)=\prod _{i=1}^{r}(p_{i}-1)p_{i}^{k_{i}-1}=n\prod _{i=1}^{r}{\left(1-\frac {1}{p_{i}}\right)}$$

où chaque pi désigne un nombre premier et ki un entier strictement positif: on peut le déduire du théorème précédent ou, plus élémentairement, du principe d'inclusion-exclusion.
Par exemple, pour les nombres sans facteurs carré 

 $$n=\prod _{i=1}^{r}p_{i}$$

, comme les primorielles, on obtient 

 $$\quad \varphi (n)=\prod _{i=1}^{r}(p_{i}-1)$$

## Algorithme de calcul

En 2025, on ne connaît pas d'algorithme efficace pour calculer l'indicatrice d'Euler d'un entier n donné. L'expression ci‐dessus requiert de calculer les facteurs premiers de n, ce qui est réputé difficile: les meilleurs algorithmes de factorisation connus ont une complexité sous‐exponentielle.
Le problème du calcul de l'indicatrice d'Euler est plus général que le problème RSA car il permet de résoudre facilement ce dernier. Par conséquent, la connaissance d'un algorithme de calcul efficace casserait la sécurité du système cryptographique RSA.

## Transformée de Fourier

L'indicatrice d'Euler est la transformée de Fourier discrète du PGCD, évaluée en 1.
 $$\mathcal {F}\{\mathbf {x} \}[m]=\sum \limits _{k=1}^{n}x_{k}\cdot \mathrm {e} ^{-2\mathrm {i} \pi \frac {mk}{n}}$$

où xk = PGCD(k,n) pour k ∈ {1,..., n}. Alors

 $$\varphi (n)=\mathcal {F}\{\mathbf {x} \}=\sum \limits _{k=1}^{n}\mathrm {PGCD} (k,n)\mathrm {e} ^{-2\mathrm {i} \pi \frac {k}{n}}.$$

La partie réelle de la formule est

 $$\varphi (n)=\sum \limits _{k=1}^{n}\mathrm {PGCD} (k,n)\cos \left(\frac {2\pi k}{n}\right).$$

Par exemple, en utilisant 

 $\cos \tfrac {\pi }{5}=\tfrac {{\sqrt {5}+1}{4}}$

 $\cos \tfrac {2\pi }{5}=\tfrac {{\sqrt {5}-1}{4}}$

 $${\begin{array}{rcl}\varphi (10)&=&\mathrm {PGCD} (1,10)\cos \tfrac {2\pi }{10}+\mathrm {PGCD} (2,10)\cos \tfrac {4\pi }{10}+\mathrm {PGCD} (3,10)\cos \tfrac {6\pi }{10}+\cdots +\mathrm {PGCD} (10,10)\cos \tfrac {20\pi }{10}\\&=&1\cdot (\tfrac {{\sqrt {5}+1}{4}})+2\cdot (\tfrac {{\sqrt {5}-1}{4}})+1\cdot (-\tfrac {{\sqrt {5}-1}{4}})+2\cdot (-\tfrac {{\sqrt {5}+1}{4}})+5\cdot (-1)\\&&+\ 2\cdot (-\tfrac {{\sqrt {5}+1}{4}})+1\cdot (-\tfrac {{\sqrt {5}-1}{4}})+2\cdot (\tfrac {{\sqrt {5}-1}{4}})+1\cdot (\tfrac {{\sqrt {5}+1}{4}})+10\cdot (1)\\&=&4.\end{array}}$$

Contrairement au produit d'Euler et la formule de la somme des diviseurs, Celle-ci ne requiert pas de connaître les facteurs de n. Cependant, elle implique le calcul du PGCD de n et de tous les entiers positifs inférieurs à n, ce qui suffit par ailleurs à donner la factorisation.

## Arithmétique modulaire

L'indicatrice d'Euler est une fonction essentielle de l'arithmétique modulaire; elle est à la base de résultats fondamentaux, à la fois en mathématiques pures et appliquées.

Si a divise b alors φ(a) divise φ(b).

Si n a q diviseurs premiers impairs distincts, φ(n) est divisible par 2q.
Ces deux propriétés peuvent se déduire du calcul explicite de φ.

Pour tout entier n > 2, φ(n) est pair et la somme de tous les entiers positifs inférieurs et premiers à n est égale à n φ(n)/2.
En effet, m ↦ n – m est une bijection entre les entiers premiers à n compris entre 0 (ou 1) et n/2 et ceux compris entre n/2 et n, et n/2 peut être entier mais pas premier à n.

Dans le groupe (ℤ/nℤ, +), les éléments d'ordre d (un diviseur de n) sont les générateurs du sous-groupe engendré par n/d. Si les éléments de ℤ/nℤ sont partitionnés selon leurs ordres, on obtient donc:

 ∗

 $$\forall n\in \mathbb {N} ^{*}\quad n=\sum _{d|n}\varphi (d)$$

La formule d'inversion de Möbius donne alors:

 ∗

 $$\forall n\in \mathbb {N} ^{*}\quad \varphi (n)=\sum _{d|n}\mu (d)\frac {n}{d}$$

,où μ désigne la fonction de Möbius.

## Applications

La cryptologie utilise cette fonction. Le chiffrement RSA se fonde sur la propriété suivante (théorème d'Euler):

Une autre branche de la théorie de l'information utilise l'indicatrice: la théorie des codes. C'est le cas des codes correcteurs, et particulièrement des codes cycliques. Ce type de code se construit à l'aide d'un polynôme cyclotomique, orLe degré du n-ième polynôme cyclotomique Φn est égal à φ(n).

## Fonctions génératrices

Les deux formules φ = μ ✻ Id et φ ✻ 1 = Id, présentées ci-dessus, où ✻ désigne la convolution de Dirichlet, permettent de calculer respectivement les fonctions génératrices de Dirichlet et de Lambert.

Comme la série de Dirichlet génératrice de μ est 1/ζ(s) — où ζ est la fonction zêta de Riemann — et celle de Id est ζ(s – 1), on en déduit celle de φ (qui converge pour Re(s) > 2):

 $$\sum _{n=1}^{\infty }\frac {\varphi (n)}{n^{s}}=\frac {\zeta (s-1)}{\zeta (s)}.$$

La série de Lambert associée à φ (qui converge pour |q| < 1) est

 $$\sum _{n=1}^{\infty }\frac {\varphi (n)q^{n}{1-q^{n}}}=\sum _{m=1}^{\infty }mq^{m}=\frac {q}{(1-q)^{2}}.$$

## Moyenne asymptotique

Arnold Walfisz a établi

 $$\sum _{n\leq x}\varphi (n)=\frac {3}{\pi ^{2}}x^{2}+O\left(x(\log x)^{2/3}(\log \log x)^{4/3}\right)\ \ (x\rightarrow \infty )$$

(où O est le grand O de Landau), en exploitant entre autres des estimations de sommes d'exponentielles dues à I. M. Vinogradov et à N. M. Korobov. À ce jour, c'est toujours la meilleure estimation de ce type démontrée.

## Divisibilité des valeurs de phi par un entier quelconque

La propriété qui suit, qui fait partie du « folklore » (c'est-à-dire apparemment dont aucune preuve spécifique n'a été publiée: voir l'introduction de cet article dans laquelle elle est citée comme étant « connue depuis longtemps ») a des conséquences importantes. Par exemple elle exclut la distribution uniforme des valeurs de 

 $\varphi (n)$

 dans les progressions arithmétiques modulo 

 $q$

 pour n'importe quel entier 

 $q>1$

Pour chaque entier positif 

 $q$

, la relation 

 $q|\varphi (n)$

 est vérifiée pour presque tout 

 $n$

, c'est-à-dire à l'exception de 

 $o(x)$

 valeurs de 

 $n\leq x$

 lorsque 

 $x\rightarrow \infty$

Cette propriété est une conséquence élémentaire du fait que la somme des réciproques des premiers congrus à 1 modulo 

 $q$

 diverge, qui lui-même est un corollaire de la preuve du Théorème de la progression arithmétique.

## Croissance de la fonction

Asymptotiquement, on a

 ⩽
 $n^{1-\varepsilon }0\,$

 $n>N(\varepsilon )\,$

L'égalité à la borne supérieure est satisfaite chaque fois que n est un nombre premier. Et si on considère la relation

 premier

 $$\frac {\varphi (n)}{n}=\prod _{p|n,\ p\text{ premier}}(1-p^{-1})\,$$

on peut constater que les valeurs les plus petites de 

 $$\frac {\varphi (n)}{n}$$

 correspondent aux n primoriels, c'est-à-dire ceux qui sont le produit d'un segment initial de la suite de tous les nombres premiers. À partir du troisième théorème de Mertens et des inégalités de Tchebychev on peut montrer que l'estimation ci-dessus peut être remplacée par

 ⩽
 $$\frac {{\rm {e}^{-\gamma }n}{\ln \ln n}}(1+o(1))<\varphi (n)\leqslant n-1\$$

(où o est le petit o de Landau et 

 $\gamma$

 est la constante d'Euler-Mascheroni), et que la minoration est optimale.

## Autres formules impliquant la fonction φ d'Euler

$\forall n>0,\ \forall a>1\quad n|\varphi (a^{n}-1)$

car l'ordre multiplicatif de a modulo an – 1 vaut n.

 $$\varphi (mn)=\varphi (m)\varphi (n)\frac {d}{\varphi (d)}\text{ pour }d=\rm {pgcd}(m,n),$$

en particulier:

 est pair

 est impair

 $$\varphi (2m)={\begin{cases}2\varphi (m)&\text{ si }m\text{ est pair}\\\varphi (m)&\text{ si }m\text{ est impair}\end{cases}}$$

 $\forall k\geq 1\quad \varphi (n^{k})=n^{k-1}\varphi (n).$

 ∣
 $$\sum _{d\mid n}{\frac {\mu ^{2}(d)}{\varphi (d)}}=\frac {n}{\varphi (n)}.$$

 $$\forall n>1\quad \sum _{1\leq k\leq n \atop \rm {pgcd}(k,n)=1}k=\frac {1}{2}n\varphi (n).$$

 ⌊

 ⌋

 $$\sum _{k=1}^{n}\varphi (k)=\frac {1}{2}\left(1+\sum _{k=1}^{n}\mu (k)\left\lfloor \frac {n}{k}\right\rfloor ^{2}\right).$$

En 1965, P. Kesava Menon a démontré

 $$\sum _{\stackrel {1\leq k\leq n}{\rm {pgcd}}(k,n)=1}\rm {pgcd}(k-1,n)=\varphi (n)d(n)$$

où d est la fonction nombre de diviseurs

 ⌊

 ⌋

 $$\sum _{k=1}^{n}\frac {\varphi (k)}{k}=\sum _{k=1}^{n}\frac {\mu (k)}{k}\left\lfloor \frac {n}{k}\right\rfloor =\frac {6}{\pi ^{2}}n+O\left((\log n)^{2/3}(\log \log n)^{4/3}\right)$$

 $$\sum _{k=1}^{n}\frac {k}{\varphi (k)}=\frac {315~\zeta (3)}{2\pi ^{4}}n-\frac {\log n}{2}+O\left((\log n)^{2/3}\right)$$

 premier

 $$\sum _{k=1}^{n}\frac {1}{\varphi (k)}=\frac {315~\zeta (3)}{2\pi ^{4}}\left(\log n+\gamma -\sum _{p\text{ premier}}{\frac {\log p}{p^{2}-p+1}}\right)+O\left(\frac {(\log n)^{2/3}{n}}\right)$$

 (γ est la constante d'Euler).

 $$\forall m>1\quad \sum _{1\leq k\leq n \atop \rm {pgcd}(k,m)=1}1=n\frac {\varphi (m)}{m}+O\left(2^{\omega (m)}\right)$$

où ω(m) est le nombre de diviseurs premiers de m distincts

## Inégalités

Voici quelques inégalités impliquant la fonction φ:

 $$\varphi (n)>\frac {n}{{\rm {e}^{\gamma }\;\log \log n+\frac {3}{\log \log n}}}$$

 pour n > 2,

 ⩾

 $$\varphi (n)\geqslant \sqrt {\frac {n}{2}}$$

 pour n > 0
 ⩾

 $\varphi (n)\geqslant \sqrt {n}$

 pour n > 6.
On a déjà remarqué que pour n premier, φ(n) = n – 1. Pour un nombre composé n, nous avons

 ⩽
 $\varphi (n)\leqslant n-\sqrt {n}.$

Par conséquent, pour tout n > 1:

 $$01.$$

## Conjectures

Les résultats ci-dessous ne sont encore que des conjectures à l'heure actuelle:

 $n$

 est premier si (et seulement si) 

 $n\equiv 1\bmod {\varphi }(n)$

 (c'est le problème de Lehmer, énoncé par Derrick Lehmer)

 $\forall {n>0}\quad \exists {m\neq n}\quad \varphi (n)=\varphi (m)$

 (c'est la « conjecture de Carmichael » que Robert Daniel Carmichael, en 1907, a énoncée et cru démontrer, mais qui reste toujours un problème ouvert).

## Nombres remarquables

À partir de la fonction indicatrice d'Euler et de fonctions proches, diverses familles de nombres remarquables peuvent être définies.

## Fonction indicatrice

Un nombre totient est un nombre entier appartenant à l'image de la fonction indicatrice d'Euler: c'est-à-dire un entier m pour lequel il existe au moins un n pour lequel φ(n) = m. La valence ou multiplicité d'un nombre totient m est le nombre de solutions à cette équation.
Un nombre nontotient est un entier naturel qui n'est pas un nombre totient. Tout nombre entier impair supérieur à 1 est trivialement un nontotient. Il existe également une infinité de nontotients pairs, et chaque entier positif a un multiple qui est un nontotient pair.
Un nombre hautement totient est un entier totient dont la multiplicité est supérieure à celle de n'importe quel entier positif inférieur à lui.

## Fonction cototient

La fonction cototient est définie à partir de l'indicatrice d'Euler, comme Id - φ: elle associe à tout entier naturel n non nul le nombre n – φ(n). Ce nombre représente le nombre d'entiers compris entre 1 et n (inclus) et qui ne sont pas premiers avec n (de manière équivalente, qui ont avec n au moins un facteur premier commun). À partir de la fonction cototient, sont définies de manière équivalente les nombres cototients, noncototients et hautement cototients.
Un nombre cototient est un nombre entier appartenant à l'image de la fonction cototient: c'est-à-dire un entier m pour lequel il existe au moins un n pour lequel n – φ(n) = m. La valence ou multiplicité d'un nombre cototient m est le nombre de solutions à cette équation.
Un nombre noncototient est un entier naturel qui n'est pas un nombre cototient, c'est-à-dire un entier m n'admettant pas d'antécédent par la fonction cototient. De manière équivalente, exprimé algébriquement, ce sont les entiers m tels que l'équation n – φ(n) = m ne possède pas de solution.
Un nombre hautement cototient est un entier cototient dont la multiplicité est supérieure à celle de n'importe quel entier positif inférieur à lui. De manière équivalente, exprimé algébriquement, ce sont les entiers m tels que l'équation n – φ(n) = m possède plus de solution que chacune des équations n – φ(n) = k pour tout 1 < k < m.
