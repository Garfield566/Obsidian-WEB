---
nom: "Theoreme de Thales"
qid: Q11197
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Mplwp_log2e10.svg
---

# Logarithme

> [!Infobox]
> **Logarithme**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Mplwp_log2e10.svg|300]]
> - **Contraire** : exponentielle de base a
> - **Approximé par** : CORDIC
> - **Découvert(e) ou inventé(e) par** : John Napier

En mathématiques, plus généralement en science, le logarithme (du grec, logos: rapport et arithmos: nombre) d'un nombre donné répond à la question « À quelle puissance faut-il élever un certain nombre fixé, appelé la base du logarithme, pour obtenir le nombre donné? », dans les cas où une telle puissance existe. Par exemple, la réponse à « À quelle puissance faut-il élever 10 pour obtenir 1000? » est 3: le logarithme de base dix de 1000 est 3 car 103 = 10×10×10 = 1000.
Plus généralement, le logarithme de base 

 $b$

 d'un nombre réel strictement positif 

 $x$

, noté logb x, est la puissance à laquelle il faut élever la base 

 $b$

 (nombre réel strictement positif différent de 1) pour obtenir ce nombre, ce qui se résume à la définition 

 $b^{\log _{b}x}=x$

. Par exemple, 

 $\log _{10}1000=3$

. Ainsi, une fonction logarithme est la fonction réciproque d'une exponentiation.
John Napier a développé les logarithmes au début du XVIIe siècle. L'utilité du logarithme pour le calcul vient du fait que la fonction logarithme transforme un produit en somme: 

 $\log _{b}(x\cdot y)=\log _{b}x+\log _{b}y\,$

. Pendant trois siècles, la table de logarithmes et la règle à calcul, fondée sur une échelle logarithmique, ont servi pour le calcul, jusqu'à leur remplacement, dans le dernier quart du XXe siècle, par des calculatrices électroniques.
Une échelle logarithmique permet de représenter sur un même graphique des nombres dont l'ordre de grandeur est différent. Les sciences appliquées les utilisent fréquemment dans les formules, comme celles qui évaluent la complexité des algorithmes ou des fractales et celles qui dénombrent les nombres premiers. Ils décrivent les intervalles musicaux et selon le modèle de Weber-Fechner s'appliquent généralement en psychophysique.

## Définitions

Il existe plusieurs définitions. La définition choisie dépend des sources.

## Réciproque de l'exponentiation

L'addition, la multiplication, et l'exponentiation sont des opérations arithmétiques communes. L'inverse de l'addition est la soustraction. L'inverse de la multiplication est la division. De façon similaire, le logarithme est l'inverse de l'exponentiation. L'exponentiation pour une base b, consiste à élever à la puissance. Il s'agit de la fonction qui à un nombre 

 $y$

 associe 

 $b^{y}$

. Par exemple, on peut élever la base 10 à la puissance 3, 4, ou encore 0.5:

 $10^{3}=10\times 10\times 10=1000$

 $10^{4}=10\times 10\times 10\times 10=10000$

 $10^{0.5}=\sqrt {10}=3,1622...$

Le logarithme d'un nombre consiste justement à retrouver la puissance à laquelle il fallait élever la base pour l'obtenir.

 $\log _{10}(1000)=3$

 $\log _{10}(10000)=4$

 $\log _{10}(\sqrt {10})=0,5$

Plus précisément, on définit le logarithme de x en base b, soit logb x, comme le nombre 

 $y$

 tel que 

 $b^{y}=x$

. Ainsi, le logarithme en base b est la fonction réciproque de l'exponentiation en base b.

## Approche élémentaire

Toutefois, cette définition présuppose l'aptitude d'élever un nombre à une puissance non entière. Ainsi, dans le plus simple où la puissance est entière, le logarithme est le nombre entier qui compte les répétitions de la base multipliée par elle-même. Par exemple 10 × 10 × 10 = 1000 et le logarithme de 1000 en base 10 est 3. Dans cette opération, multiplier un nombre par la base équivaut à ajouter 1 à son logarithme. Par exemple 1000 × 10 = 10000 et le logarithme de 10 000 est 3 + 1 = 4. Mais le logarithme n'est pas toujours entier, comme 

 $\log _{10}(\sqrt {10})$

C'est pourquoi Jean-Pierre Friedelmeyer (cf. p. 661 dans) présente une progression élémentaire pour définir le logarithme de n'importe quel nombre positif non nul en base 10. On commence par trouver l'entier K tel que 

 ⩽
 $10^{K}\leqslant x<10^{K+1}$

. De là, on a 

 ⩽

 $10^{10K}\leqslant x^{10}<10^{10K+10}$

. Puis il existe un unique chiffre entre 0 et 9 tel que 

 ⩽

 $10^{10K+a}\leqslant x^{10}<10^{10K+a+1}$

. Jusque là, le nombre « K,a » (l'entier K est la partie entière du nombre et a sa partie décimale) est une approximation du logarithme décimal de x à 1/10 près. En répétant le processus à l'infini, on obtient le logarithme en base 10.

## Primitive

Le logarithme peut être défini comme la primitive de la fonction 

 $x\mapsto 1/x$

 qui s'annule en 1:

 $$\ln:t\mapsto \int _{1}^{t}{\frac {\mathrm {d} x}{x}}$$

On obtient alors le logarithme népérien qui est la réciproque de l'exponentiation en base e. Cette définition était donnée dans les classes de lycée en France de 1960 à 2000 (cf. p. 660 dans ).

## Solution d'une équation fonctionnelle

Cauchy dans son Cours d'analyse algébrique (1821) (voir Chapitre V, paragraphe 1, 3e problème, p. 109-111 dans) définit les fonctions logarithmes comme solutions de l'équation fonctionnelle (c'est-à-dire une équation dont l'inconnue est une fonction) suivante:

 $f(xy)=f(x)+f(y)$

où 

 $f$

 est la fonction inconnue. C'est l'approche utilisée en France à partir de 2001 (cf. p. 658 dans), voir infra.

## Logarithmes d'usage courant

Trois fonctions logarithmes sont d'usage courant:

le logarithme népérien (ou naturel) dont la base est le nombre e, est fondamental en analyse mathématique car il est la primitive de la fonction 

 $x\mapsto \tfrac {1}{x}$

 s'annulant en 1 et la fonction réciproque de la fonction exponentielle; il est souvent noté ln sauf en informatique ou en théorie des nombres où log sans autre précision signifie en général logarithme népérien;
le logarithme décimal, dont la base est 10, reste le plus communément utilisé pour les calculs dans le domaine technologique ainsi qu'en chimie pour le calcul de pH;
le logarithme binaire, dont la base est 2, est utile en informatique théorique et pour certains calculs appliqués.
Si la base est évidente d'après le contexte, ou si elle n'a pas d'importance, on peut écrire simplement log x. Cela arrive quand on utilise une notation de Landau, comme 

 $O(\log x)$

## Logarithme népérien

Le logarithme népérien, ou logarithme naturel, est la fonction logarithme dont la dérivée est la fonction inverse définie de 

 ∗

 $\mathbb {R} _{+}^{*}$

 $\mathbb {R}$

 $$x\mapsto \frac {1}{x}$$

La fonction de Neper est par convention notée « ln » ou « log », notation couramment utilisée en théorie des nombres et en informatique.
La base de la fonction logarithme népérien, notée e, est appelée nombre de Neper ou nombre d'Euler.
Une valeur approchée est:

 $\mathrm {e} \approx 2{,}718$

## Logarithme décimal

C'est le logarithme le plus pratique dans les calculs numériques manuels, il est noté log ou log10. La norme ISO 80000-2 indique que log10 devrait être noté lg, mais cette notation est rarement utilisée.
On le retrouve dans la création des échelles logarithmiques, les repères semi-logarithmiques ou log-log, dans la règle à calcul, dans le calcul du pH, dans l'unité du décibel.
Il précise à quelle puissance il faut élever 10 pour retrouver le nombre de départ: l'image d'un nombre par log est l'entier relatif auquel il faut élever 10 pour obtenir l'antécédent. Par exemple:

En base dix:

 $\log _{10}(10)=1\text{ car }10^{1}=10$

 $\log _{10}(100)=2\text{ car }10^{2}=100$

 $\log _{10}(1000)=3\text{ car }10^{3}=1000$

 $\log _{10}(0,01)=-2\text{ car }10^{-2}=0,01$

La valeur du logarithme d'autres nombres que des puissances de 10 demande un calcul approché. Le calcul de log(2) par exemple peut se faire à la main, en remarquant que 210 ≈ 1000 donc 10 log10(2) ≈ 3 donc log10(2) ≈ 0,3.
Pour tout réel strictement positif b différent de 1 et pour tout réel x > 0,

 $$\log _{b}(x)={\frac {\log _{10}(x)}{\log _{10}(b)}}$$

## Logarithme binaire

La norme ISO 80 000 recommande de noter lb le logarithme en base 2.
Le logarithme binaire, d'usage spécialisé dans le calcul des intervalles musicaux à partir d'un rapport de fréquences, pour obtenir des octaves, des demi-tons ou des cents, a trouvé beaucoup plus d'application en informatique. Les ordinateurs travaillant en système binaire, le calcul d'un logarithme en base 2 se fait par l'algorithme le plus précis et le plus efficace.
Un nombre x codé en virgule flottante binaire se décompose en une mantisse m, comprise entre 1 (inclus) et 2 (exclu) et un exposant p, indiquant la puissance de 2 qui multiplie la mantisse pour obtenir le nombre. L'exposant est la partie entière du logarithme binaire, tandis que le logarithme binaire de la mantisse est compris entre 0 (inclus) et 1 (exclu).

 $x=2^{p}\times m\Longrightarrow \textrm {lb}(x)=p+\textrm {lb}(m).$

Ce qui ramène le calcul à celui du logarithme binaire d'un nombre entre 1 (inclus) et 2 (exclu). Si on multiplie ce nombre par lui-même, et que le résultat dépasse 2, c'est que le nombre est supérieur à √2: le chiffre suivant, après la virgule, est un 1, dans le cas contraire, c'est un 0. On continue par itération jusqu'à la précision souhaitée.
Les deux logarithmes précédents se déduisent de celui-ci par:

 $$\ln(x)={\frac {\mathrm {lb} (x)}{\mathrm {lb} (\mathrm {e} )}}\text{ et }\log _{10}(x)={\frac {\mathrm {lb} (x)}{\mathrm {lb} (10)}}$$

## Cologarithme

Le cologarithme d'un nombre est l'opposé du logarithme de ce nombre et le logarithme de son inverse: 

 colog

 $$\operatorname {colog} _{b}x=-\log _{b}x=\log _{b}\frac {1}{x}$$

## Historique

La présentation de correspondances entre suites arithmétiques et suites géométriques avec l'observation qu'une somme dans une suite correspond à un produit dans l'autre est ancienne et on la voit déjà chez Archimède (IIIe siècle av. J.-C.), Chuquet (XVe siècle) et Stifel (début du XVIe siècle) en Europe, al-Samaw'al (XIIe siècle) et Ibn Hamza al-Maghribi (fin du XVIe siècle) dans le monde arabe, mais l'observation est plutôt tournée vers une utilisation algébrique.
Vers la fin du XVIe siècle, le développement de l'astronomie et de la navigation maritime d'une part et les calculs bancaires d'intérêts composés d'autre part poussent les mathématiciens à chercher des méthodes de simplification de calculs et en particulier le remplacement des multiplications par des sommes. L'invention de tables dites logarithmique permettant de faciliter les calculs comportant des produits est l'œuvre de mathématiciens du début du XVIIe siècle: Jost Bürgi, Neper et Briggs, travail poursuivi par Johannes Kepler, Ezechiel de Decker et Adriaan Vlacq.
En 1647, Grégoire de Saint-Vincent, travaillant sur la quadrature de l'hyperbole, définit la fonction primitive de la fonction 

 $x\mapsto \tfrac {1}{x}$

 s'annulant en 1. Huygens remarquera en 1661 que cette fonction se trouve être une fonction logarithme particulière: le logarithme naturel.
La correspondance entre les fonctions exponentielles et logarithmes n'apparaît qu'après le travail de Leibniz sur la notion de fonction, en 1697, et se développe au cours du XVIIIe siècle dans les écrits d'Euler.
La tentative d'application de la fonction logarithmique à la variable complexe date du XVIIIe siècle et donne lieu à une controverse entre Bernoulli et Leibniz résolue par Euler.

## Propriétés des fonctions logarithme

Dans cette section, nous donnons des propriétés d'une fonction logarithme, quelle que soit sa base b.

## Propriétés algébriques

Les fonctions logarithme sont les morphismes continus non constamment nuls de 

 ∗

 $(\mathbb {R} _{+}^{*},\times )$

 $(\mathbb {R},+)$

. Plus précisément, pour tout réel b strictement positif et différent de 1, le logarithme de base b: logb est l'unique fonction continue 

 $f$

 définie sur 

 ∗

 $\mathbb {R} _{+}^{*}$

 vérifiant l'équation fonctionnelle:

 $${\begin{cases}\forall x,y>0,\,f(xy)=f(x)+f(y)\\f(b)=1\end{cases}}$$

Cette définition permet de déduire les propriétés suivantes, pour 

 $x,y>0$

 $\log _{b}(1)=0$

Tout logarithme transforme produit en somme: 

 $\log _{b}(x\cdot y)=\log _{b}x+\log _{b}y\,$

Tout logarithme transforme un quotient en différence: 

 $$\log _{b}\left(\frac {x}{y}\right)=\log _{b}x-\log _{b}y\,$$

Tout logarithme transforme puissance en produit: 

 $\log _{b}(x^{y})=y\log _{b}(x)$

La dernière égalité s'obtient comme suit. On démontre que pour tous les entiers naturels n, on a 

 $\log _{b}(x^{n})=n\log _{b}(x)$

. Puis on l'étend aux entiers relatifs n. Puis on démontre 

 $\log _{b}(x^{r})=r\log _{b}(x)$

 pour tout rationnel r. Enfin, 

 $\log _{b}(x^{y})=y\log _{b}(x)$

 grâce à la continuité, comme tout réel strictement positif x est la limite d'une suite dont le terme général est de la forme brn, où (rn) est une suite de rationnels convergeant vers un réel 

 ℓ

 $\ell$

, on détermine logb(x) comme étant la limite de rn.

## Changement de base

Deux fonctions logarithmes ne diffèrent que d'une constante multiplicative: pour tous réels strictement positifs a et b différents de 1 et pour tout réel x > 0,

 $$\log _{b}(x)={\frac {\log _{a}(x)}{\log _{a}(b)}}$$

Toutes les fonctions logarithmes peuvent donc s'exprimer à l'aide d'une seule, par exemple la fonction logarithme népérien: pour tout réel strictement positif b différent de 1 et pour tout réel x > 0,

 $$\log _{b}(x)=\frac {\ln(x)}{\ln(b)}$$

## Dérivée

La fonction logb est dérivable sur 

 ∗

 $\mathbb {R} _{+}^{*}$

 de dérivée:

 $$\log _{b}'(x)=\frac {1}{x\ln(b)}$$

 qui a même signe que ln(b).
Donc la fonction logb est strictement monotone, croissante quand b est supérieur à 1, décroissante dans le cas contraire.

## Limite

Le logarithme tend vers l'infini quand son argument tend vers l'infini:

 $\log _{b}(x)\xrightarrow {x\rightarrow +\infty } +\infty$

Le théorème des croissances comparées donne:

## Nombre de chiffres avant la virgule

Si b est un entier supérieur ou égal à 2 et x > 0, la représentation propre de x en base b possède n chiffres avant la virgule si et seulement si 

 ⩽
 $b^{n-1}\leqslant x<b^{n}$

, soit 

 ⩽

 $n-1\leqslant \log _{b}x<n$

. Le nombre 

 $n(x)$

 de chiffres dans l'écriture en base 

 $b$

 du nombre 

 $x$

 est donc égal à 

 ⌊

 ⌋

 $\left\lfloor {\log _{b}x}\right\rfloor +1$

. Et lorsque x tend vers l'infini, on a donc 

 ∼
 $\log _{b}x\sim n(x)$

## Fonction réciproque (antilogarithme)

La fonction 

 ∗

 $\log _{b}:\mathbb {R} _{+}^{*}\to \mathbb {R}$

 est la bijection réciproque de la fonction exponentielle de base b, parfois appelée antilogarithme de base b:

 ∗

 $$\operatorname {antilog_{b}}:\mathbb {R} \to \mathbb {R} _{+}^{*},\;x\mapsto b^{x}$$

Autrement dit, les deux façons possibles de combiner (ou composer) les logarithmes et l'élévation à des puissances redonnent le nombre original:

pour tout réel x, prendre la puissance x-ième de b, puis le logarithme en base b de cette puissance, redonne x:

 ∗

 $\forall x\in \mathbb {R} _{+}^{*}\quad \log _{b}(b^{x})=x\log _{b}(b)=x$

inversement, pour tout réel y strictement positif, prendre d'abord le logarithme en base b, puis élever b à sa puissance, redonne y:

 $b^{\log _{b}(y)}=y.$

Les fonctions réciproques sont étroitement liées aux fonctions originales.
Leurs graphes, qui se correspondent lorsqu'on échange les coordonnées x et y (ou par réflexion par rapport à la diagonale x = y), sont montrés à droite dans le cas où b est un réel strictement supérieur à 1: un point (u, t = bu) sur le graphe (rouge) de la fonction antilogarithme x ↦ bx fournit un point (t, u = logb(t)) sur le graphe (bleu) du logarithme et vice versa. Comme b > 1, la fonction logb est croissante et quand x tend vers +∞, logb(x) tend vers +∞, tandis que lorsque x approche zéro, logb(x) tend vers –∞. Dans le cas où le réel b est strictement compris entre 0 et 1, la fonction logb est décroissante et ces limites sont interverties.
En matière de calcul, l'antilog ramène des logarithmes aux valeurs. Soit à évaluer une formule F combinant multiplications, divisions et exponentiations, et soit f la formule définissant le logarithme de F en combinant sommes, différences et produits des (logarithmes) des données. La valeur de F peut s'obtenir comme l'antilog de la valeur de f, ce qui conclut le calcul. On peut ainsi remplacer l'évaluation 

 $F=(x\times y\times z)^{1/3}$

 antilog

 $$F=\operatorname {antilog} _{b}\left({\frac {\log _{b}(x)+\log _{b}(y)+\log _{b}(z)}{3}}\right)$$

## Algorithmes

Il existe plusieurs algorithmes pour calculer le logarithme d'un nombre.

## Généralisations

Le logarithme complexe est la fonction réciproque de l'exponentielle complexe et généralise ainsi la notion de logarithme aux nombres complexes. Le logarithme discret généralise les logarithmes aux groupes cycliques et a des applications en cryptographie à clé publique.

## Applications

Le logarithme apparaît dans plusieurs domaines.

## Informatique

Le logarithme est utilisé pour exprimer la complexité temporelle d'algorithmes. Il apparaît dans la complexité temporelle de plusieurs algorithmes de type diviser pour régner. Par exemple, la recherche dichotomique dans un tableau trié de n éléments s'effectue en temps 

 $O(\log n)$

, le tri fusion qui trie un tableau de n éléments en 

 $O(n\log n)$

 ou la transformation de Fourier rapide en 

 $O(n\log n)$

 d'un signal à n éléments.

## Chimie

Le potentiel hydrogène est 

 $\mathrm {pH} =-\log \,a_{\mathrm {H} }$

 où 

 $a_{\mathrm {H} }$

 est une mesure sans dimension de l'activité des ions hydrogène H+.

## Acoustique

Le niveau sonore se mesure souvent en décibel, qui est une mesure de puissance qui utilise une échelle logarithmique.

## Théorie de l'information

Le logarithme apparaît dans la définition de l'entropie.

## Théorèmes en mathématiques

Le logarithme apparaît dans le théorème des nombres premiers.
