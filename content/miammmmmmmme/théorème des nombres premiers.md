---
nom: "théorème des nombres premiers"
qid: Q386292
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/PrimeNumberTheorem.png
---

# Théorème des nombres premiers

> [!Infobox]
> **Théorème des nombres premiers**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/PrimeNumberTheorem.png|300]]
> - **Prouvé ou démontré par** : Jacques Hadamard, Charles-Jean de La Vallée Poussin
> - **Partie de** : liste de théorèmes
> - **Discipline dont c'est l'objet** : théorie analytique des nombres

En mathématiques, et plus précisément en théorie analytique des nombres, le théorème des nombres premiers, démontré indépendamment par Hadamard et La Vallée Poussin en 1896, est un résultat concernant la distribution asymptotique des nombres premiers.

## Énoncés équivalents

Le théorème des nombres premiers équivaut à 

 ∼
 $\pi (x)\ln(\pi (x))\sim x$

 lorsque 

 $x\rightarrow \infty$

 donc au comportement asymptotique suivant pour le n-ième nombre premier 

 $p_{n}$

 ∼
 $p_{n}\sim n\ln(n)$

Il équivaut aussi à

 ∼
 $\theta (x)\sim x\quad (x\rightarrow \infty )$

et à

 ∼
 $\psi (x)\sim x\quad (x\rightarrow \infty )$

puisque chacune des deux fonctions de Tchebychev 

 $$\theta (x):=\sum _{p\in \mathbb {P},~p\leq x}\ln p\quad$$

 ∗

 $$\quad \psi (x):=\sum _{p\in \mathbb {P},~k\in \mathbb {N} ^{*},~p^{k}\leq x}\ln p$$

, où 

 $\mathbb {P}$

 désigne l'ensemble des nombres premiers, est asymptotiquement équivalente à 

 $\pi (x)\ln x$

 lorsque 

 $x\rightarrow \infty$

Le théorème des nombres premiers est également équivalent, en un certain sens, à l'assertion selon laquelle la fonction zêta de Riemann ne s'annule pas sur l'abscisse de partie réelle 1:

 $\forall t\in \mathbb {R} \quad \zeta (1+\mathrm {i} t)\neq 0$

## Approximations asymptotiques

Un approximant de π(x) nettement meilleur que x/ln(x) est la fonction logarithme intégral li(x) ou sa variante, la fonction d'écart logarithmique intégrale Li(x):

 ∼

 ∼

 $\pi (x)\sim \rm {li}(x)\sim \rm {Li}(x)$

où

 $$\rm {li}(x)=\int _{0}^{x}{\frac {\mathrm {d} t}{\ln(t)}}\text{ et }\mathrm {Li} (x)=\mathrm {li} (x)-\mathrm {li} (2)=\int _{2}^{x}{\frac {\mathrm {d} t}{\ln(t)}}.$$

Voir les sections Histoire et Exemples d'estimations numériques ci-dessous pour des estimations de l'erreur de ces approximations.

## Histoire

Le théorème des nombres premiers a été conjecturé dans la marge d'une table de logarithmes par Gauss en 1792 ou 1793 alors qu'il avait seulement 15 ou 16 ans (selon ses propres affirmations ultérieures) et par Adrien-Marie Legendre (ébauche en l'An VI du calendrier républicain, soit 1797-1798, conjecture précise en 1808).
Le Russe Pafnouti Tchebychev a établi en 1851 que si x est assez grand, π(x) est compris entre 0,92129x/ln(x) et 1,10556x/ln(x).
Le théorème a finalement été démontré indépendamment par Hadamard et La Vallée Poussin en 1896 à l'aide de méthodes d'analyse complexe, utilisant en particulier la fonction ζ de Riemann.
En 1899, La Vallée Poussin a affiné son résultat en montrant que (avec la notation O de Landau)

 $$\pi (x)=\rm {li}(x)+O\left(x\exp \left(-\sqrt {\frac {\ln x}{2V}}\right)\right)$$

pour une certaine constante V. Landau (en 1909) puis bien d'autres ont travaillé à réduire la taille admissible de cette constante V, avec une méthode dans laquelle V mesure une propriété extrémale d'une certaine classe de polynômes trigonométriques. On sait que V = 34,5036 convient. Le problème de la détermination avec cette méthode de la valeur V la plus petite possible est connu sous le nom de « Problème extrémal de Landau ». C'est un sujet de recherche intéressant en soi, indépendamment de son application à l'estimation de La Vallée Poussin. Laquelle application est devenue d'ailleurs purement anecdotique depuis qu'on dispose de l'estimation de Vinogradov-Korobov-Richert (voir juste ci-dessous) qui est bien meilleure, et qui implique en particulier qu'on peut remplacer V par un nombre aussi petit qu'on veut dans celle de La Vallée Poussin.
Contrairement à ce que peut laisser penser l'expérimentation numérique, li(x) n'est pas toujours supérieur à π(x). Le mathématicien anglais John Littlewood a démontré, dès 1914, qu'il y a une infinité de x pour lesquels cette inégalité est inversée; plus précisément il a établi l'évaluation asymptotique

 ±

 $$\pi (x)-\rm {li}(x)=\Omega _{\pm }\left(\sqrt {x}\frac {\log \log \log x}{\log \log x}\right)\ (x\rightarrow \infty ).$$

À cause de la relation entre la fonction ζ et la fonction π, l'hypothèse de Riemann a une importance considérable en théorie des nombres: si elle était démontrée, cela produirait de loin une bien meilleure estimation de l'erreur intervenant dans le théorème des nombres premiers.
Helge von Koch en 1901 a montré plus précisément:

L'hypothèse de Riemann implique l'estimation 

 $\pi (x)=\rm {li}(x)+O\left(\sqrt {x}\ln x\right).$

(Cette dernière estimation est en fait équivalente à l'hypothèse de Riemann). On est encore loin d'une évaluation si précise. En revanche, on sait que toute amélioration de la région sans zéro de la fonction ζ améliore de facto le terme d'erreur du théorème des nombres premiers. La meilleure région sans zéro actuellement connue a été obtenue en 1958 par Korobov et Vinogradov.
[Cette région était un peu trop « optimiste » et n'a jamais été rigoureusement établie, ni par Vinogradov, ni par Korobov, ni par personne d'autre. Elle a été finalement remplacée par une région plus petite (mais établie par une preuve) par Hans-Egon Richert en 1967].
La région de Richert implique le résultat suivant:

 $$\pi (x)=\rm {li}(x)+O\left(x\exp \left(-c(\ln x)^{3/5}(\ln \ln x)^{-1/5}\right)\right),$$

où c > 0 est une constante absolue.
En ce qui concerne des majorations explicites, mentionnons les travaux de Rosser et Schoenfeld (en) (1962, 1975, 1976), puis ceux de Dusart (1998). À l'aide d'ordinateurs de plus en plus puissants, ces chercheurs ont pu déterminer de plus en plus de zéros non triviaux de la fonction ζ sur la droite critique. Cette meilleure connaissance implique de bonnes estimations des fonctions usuelles de nombres premiers, avec ou sans l'hypothèse de Riemann. Ainsi Schoenfeld a-t-il pu établir:

si l'hypothèse de Riemann est vraie, alors 

 $$\forall x\geq 2657,\quad |\pi (x)-\rm {li}(x)|-1,\quad \sum _{p<x}p^{\alpha }\sim \frac {x^{\alpha +1}{(\alpha +1)\ln x}}\sim \rm {li}(x^{\alpha +1})$$

Le cas α = 0 de cette équivalence est bien entendu le théorème des nombres premiers; le cas α = 1 a été traité par Edmund Landau en 1909. Le cas α = –1, pour lequel cette équivalence ne s'applique pas, est donné par le deuxième théorème de Mertens: 

 $$\sum _{p<x}\frac {1}{p}=\ln \ln x+M+O(1/\ln x)$$

## Ébauche de la preuve

On commence par écrire l'égalité entre le produit d'Euler et la factorisation de Weierstrass de la fonction zêta:

 $$\zeta (s)=\prod _{p\in \mathbb {P} }\ \frac {1}{1-p^{-s}}={\frac {\mathrm {e} ^{a+bs}}{s-1}}\prod _{\rho \in Z}\left(1-\frac {s}{\rho }\right)\mathrm {e} ^\frac {s}{\rho }$$

avec s de partie réelle strictement supérieure à 1, Z l'ensemble des zéros (triviaux et non triviaux) de zêta et a, b des constantes. On prend ensuite la dérivée logarithmique:

 $$\frac {\zeta '(s)}{\zeta (s)}=-\sum _{p\in \mathbb {P} }\frac {p^{-s}{1-p^{-s}}}\ln p=b-\frac {1}{s-1}+\sum _{\rho \in Z}\frac {s}{\rho (s-\rho )}$$

Grâce à la série entière complexe 

 $$\frac {z}{1-z}=\sum _{n=1}^{\infty }z^{n}$$

 pour |z| 1. On veut maintenant intégrer cette égalité contre la fonction xs / s (avec x constante fixée). Le contour d'intégration est un rectangle de côté droit {Re(s) = σ} avec σ > 1 et qui s'étend à l'infini verticalement et à gauche. Après des calculs faisant appel au théorème des résidus, on obtient la célèbre formule explicite de Riemann (en), pour x > 0 non puissance d'un nombre premier:

 $$\sum _{p\in \mathbb {P},\;m\geq 1,\;p^{m}<x}\ln p=x-\sum _{\rho }\frac {x^{\rho }{\rho }}-\ln 2\pi -\frac {1}{2}\ln \left(1-\frac {1}{x^{2}}\right)$$

avec cette fois ρ balayant seulement les zéros non triviaux de zêta (les triviaux ont été regroupés dans le dernier terme). À gauche on reconnaît la fonction de Tchebychev ψ(x), asymptotiquement équivalente à π(x)ln(x). Le théorème des nombres premiers est par conséquent presque démontré, puisqu'à droite on voit le terme x attendu. Le dernier point à montrer est que les autres termes de droite sont négligeables devant x, autrement dit qu'il n'y a pas de zéro ρ dont la partie réelle est 1. Ce point a été prouvé par Hadamard et La Vallée Poussin.

## Ce qu'il advint de la « profondeur »

Il est convenu de distinguer plusieurs types de démonstrations mathématiques, en fonction du degré de sophistication des théories mathématiques auxquelles on fait appel; le théorème des nombres premiers fournit un prototype pour ce genre de considérations.
On a longtemps cru, au début du XXe siècle, et notamment Godfrey Hardy, que toute démonstration du théorème des nombres premiers devait forcément faire appel à des théorèmes d'analyse complexe; ce qui par ailleurs pouvait paraître frustrant pour un énoncé semblant porter essentiellement sur les nombres entiers (quoique nécessitant les nombres rationnels, voire les nombres réels pour pouvoir être énoncé). C'était donc un défi pour les mathématiciens d'essayer de trouver une démonstration élémentaire de ce théorème — élémentaire ne voulant pas dire simple, ni peu sophistiquée, mais seulement faisant le moins possible appel à des méthodes externes, à l'arithmétique dans notre cas — ou bien de comprendre précisément pourquoi certains énoncés ne sont accessibles qu'avec des méthodes plus évoluées que ce à quoi on pouvait s'attendre. Hardy parlait donc de « profondeur » des théorèmes et pensait que le théorème des nombres premiers faisait partie des énoncés dont la « profondeur » ne les rendait accessibles que par le biais de l'analyse complexe.
Une première brèche dans cette conception fut la découverte d'une démonstration basée seulement sur le théorème taubérien de Wiener; mais il n'était pas clair qu'on ne puisse pas attribuer à ce théorème une « profondeur » équivalente aux théorèmes issus de l'analyse complexe.
Le débat fut tranché en 1949, quand Paul Erdős et Atle Selberg, donnèrent chacun une démonstration indéniablement élémentaire du théorème des nombres premiers. Quelle que soit la valeur du concept de « profondeur », celle du théorème des nombres premiers n'exigeait pas d'analyse complexe. De manière plus générale, la découverte de ces démonstrations élémentaires provoqua un regain d'intérêt pour les méthodes de crible, qui trouvèrent ainsi toute leur place dans l'arithmétique.
En dépit du caractère « élémentaire » de cette démonstration, elle restait complexe et souvent jugée artificielle; en 1980, Donald J. Newman découvrit une élégante application d'un théorème taubérien permettant (après de nouvelles simplifications) de donner une démonstration très courte n'utilisant guère plus que le théorème des résidus; Don Zagier en a fourni une présentation de deux pages en 1997, pour le centenaire du théorème.

## Approximations du n-ième nombre premier

Le théorème des nombres premiers dit que la suite des nombres premiers, 

 $(p_{n})_{n\in \mathbb {N} }$

, vérifie:

 ∼
 $$\frac {p_{n}{n}}\sim \ln n$$

Des résultats de La Vallée Poussin de 1899, on déduit des développements asymptotiques bien plus précis que cet équivalent. Par exemple (avec la notation o de Landau):

 $$\frac {n}{p_{n}}=\frac {1}{\ln p_{n}}+{\frac {1}{(\ln p_{n})^{2}}}+{\frac {2}{(\ln p_{n})^{3}}}+{\frac {6}{(\ln p_{n})^{4}}}+o\left({\frac {1}{(\ln p_{n})^{4}}}\right),$$

qui permet de démontrer

 $$\frac {p_{n}{n}}=\ln n+\ln \ln n-1+\frac {\ln \ln n-2}{\ln n}-{\frac {(\ln \ln n)^{2}-6\ln \ln n+11}{2(\ln n)^{2}}}+o\left(\frac {1}{(\ln n)^{2}}\right).$$

Le théorème de Rosser montre que pn est supérieur à n ln n. On a pu améliorer cette minoration, et obtenir un encadrement:

 $$\ln n+\ln \ln n-1<\frac {p_{n}{n}}<\ln n+\ln \ln n\quad \text{pour }n\geq 6$$

et même,

 $$\frac {p_{n}{n}}<\ln n+\ln \ln n-0,948\quad \text{pour }n\geq 40~000.$$

## Exemples d'estimations numériques

Voici un tableau qui montre le comportement comparé de π(x) et ses approximations, x/ln(x) et li(x), et les écarts absolus (en différence) et relatifs (en proportion) entre ces trois fonctions:

Notes (les indices « i » dans ces notes correspondent aux renvois « Ti » dans le tableau):
