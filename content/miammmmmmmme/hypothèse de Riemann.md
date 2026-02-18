---
nom: "hypothèse de Riemann"
qid: Q205966
type: conjecture
categorie: conjecture
tags: "#mathematiques/conjecture"
image: https://commons.wikimedia.org/wiki/Special:FilePath/VignetteRiemannHypothesis.svg
---

# Hypothèse de Riemann

> [!Infobox]
> **Hypothèse de Riemann**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/VignetteRiemannHypothesis.svg|300]]
> - **Nomme d'apres** : Bernhard Riemann
> - **Partie de** : problèmes du prix du millénaire, liste de théorèmes

En mathématiques, l'hypothèse de Riemann est une conjecture formulée en 1859 par le mathématicien allemand Bernhard Riemann, selon laquelle les zéros non triviaux de la fonction zêta de Riemann ont tous une partie réelle égale à 1/2. Sa démonstration améliorerait la connaissance de la répartition des nombres premiers et ouvrirait des nouveaux domaines aux mathématiques.
Cette conjecture constitue l'un des problèmes non résolus les plus importants des mathématiques du début du XXIe siècle: elle est l'un des vingt-trois fameux problèmes de Hilbert proposés en 1900, l'un des sept problèmes du prix du millénaire et l'un des dix-huit problèmes de Smale. Comme pour les six autres problèmes du millénaire, l'énoncé exact de la conjecture à démontrer est accompagné d'une description détaillée, fournissant de nombreuses informations sur l'historique du problème, son importance, et l'état des travaux à son sujet; beaucoup des remarques informelles de cette page en proviennent.

## La fonction zêta de Riemann

La fonction zêta de Riemann est définie pour tous les nombres complexes s de partie réelle strictement supérieure à 1 par 

 $$\zeta (s)=\sum _{n=1}^{\infty }\frac {1}{n^{s}}=\frac {1}{1^{s}}+\frac {1}{2^{s}}+\frac {1}{3^{s}}+\cdots.\!$$

Leonhard Euler l'introduit (sans lui donner de nom) uniquement pour des valeurs réelles de l'argument (mais aussi pour 

 $s=1$

), en liaison, entre autres, avec sa solution du problème de Bâle. Il montre qu'elle est donnée par le produit eulérien 

 premier

 $$\zeta (s)=\prod _{p\text{ premier}}\frac {1}{1-p^{-s}}=\frac {1}{1-2^{-s}}\cdot \frac {1}{1-3^{-s}}\cdot \frac {1}{1-5^{-s}}\cdot \frac {1}{1-7^{-s}}\cdot \frac {1}{1-11^{-s}}\cdots$$

 où le produit infini porte sur tous les nombres premiers p, mais ne converge pas forcément: en effet, dans le Théorème 7 de son article, Euler donne une démonstration de cette formule pour le cas 

 $s=1$

 (tout en notant que 

 $\zeta (1)=\log \infty$

), et il l'établit en général dans son Théorème 8. C'est ce résultat qui explique l'intérêt de la fonction zêta dans l'étude de la répartition des nombres premiers (Euler déduit par exemple du cas 

 $s=1$

, dans le Théorème 19 du même article que la série des inverses des nombres premiers est divergente). Le résultat reste bien entendu valable lorsque l'argument 

 $s$

 est complexe.
L'hypothèse de Riemann porte sur les zéros de cette fonction en dehors du domaine de convergence qu'on vient de voir, ce qui peut sembler n'avoir aucun sens. L'explication tient dans la notion de prolongement analytique: on peut démontrer qu'il existe une fonction holomorphe unique définie pour tout complexe (différent de 1, où elle présente un pôle simple) et coïncidant avec zêta pour les valeurs où cette dernière est définie; on note encore ζ(s) cette nouvelle fonction.
L'une des techniques pour construire ce prolongement est la suivante.

Il est d'abord facile de vérifier que, pour s de partie réelle > 1, on a:

 $$\left(1-{2}^{1-s}\right)\zeta (s)=\eta (s)=\sum _{n=1}^{\infty }\frac {(-1)^{n+1}{n^{s}}}=\frac {1}{1^{s}}-\frac {1}{2^{s}}+\frac {1}{3^{s}}-\cdots \;$$

 or la série de droite (appelée fonction êta de Dirichlet) converge pour tout s de partie réelle strictement positive. On prolonge ainsi ζ à tous les s ≠ 1 de partie réelle > 0 (même ceux de la forme 1 + 2ikπ/ln(2) avec k entier non nul, car on montre qu'en ces points, la fonction possède une limite finie).

On montre ensuite, pour tout s de partie réelle strictement comprise entre 0 et 1, l'identité fonctionnelle 

 $$\zeta (s)=2^{s}\pi ^{s-1}\ \sin \left(\frac {\pi s}{2}\right)\ \Gamma (1-s)\ \zeta (1-s)\!,$$

 où Γ est la fonction Gamma d'Euler. Il devient alors possible d'utiliser cette formule pour définir zêta pour tout s de partie réelle négative (avec ζ(0) = –1/2 par passage à la limite).
On en déduit que les entiers pairs strictement négatifs sont des zéros de zêta (appelés zéros triviaux) et que les zéros non triviaux sont symétriques par rapport à l'axe Re(s) = 1/2 et sont tous de partie réelle comprise, au sens large, entre 0 et 1; cette région du plan complexe s'appelle la bande critique.
De plus, il n'y a aucun zéro sur l'axe Re(s) = 1 (ce résultat est équivalent au théorème des nombres premiers, voir section historique ci-dessous). Du coup, l'hypothèse de Riemann peut se reformuler ainsi: si 0 < Re(s) < 1 et si s est un zéro de ζ (ou, ce qui revient au même, de η), alors sa partie réelle vaut 1/2.

## Historique de la conjecture

« […] es ist sehr wahrscheinlich, dass alle Wurzeln reell sind. Hiervon wäre allerdings ein strenger Beweis zu wünschen; ich habe indess die Aufsuchung desselben nach einigen flüchtigen vergeblichen Versuchen vorläufig bei Seite gelassen, da er für den nächsten Zweck meiner Untersuchung entbehrlich schien. »

« […] il est fort probable que toutes les racines soient réelles. Bien sûr, une démonstration rigoureuse en serait souhaitable; pour le moment, après quelques vagues tentatives restées vaines, j'ai provisoirement mis de côté la recherche d'une preuve, car elle semble inutile pour l'objectif suivant de mes investigations. »

— énoncé par Riemann de l'hypothèse, dans l'article de 1859; Riemann y parle d'une fonction obtenue à partir de zêta, dont toutes les racines devraient être réelles plutôt que sur la ligne critique.
Riemann mentionna la conjecture, appelée plus tard « hypothèse de Riemann », dans son article paru en 1859, Sur le nombre de nombres premiers inférieurs à une taille donnée (Über die Anzahl der Primzahlen unter einer gegebenen Grösse en allemand), dans lequel il donnait une formule explicite pour le nombre de nombres premiers π(x) inférieurs à un nombre donné x.

Cette formule affirme que les zéros de la fonction zêta contrôlent les oscillations des nombres premiers autour de leur position « attendue ». Riemann savait que les zéros non triviaux de zêta étaient distribués symétriquement autour de l'axe s = ½ + it, et aussi qu'ils devaient tous être dans la bande critique 0 ≤ Re(s) ≤ 1. Il vérifia que les premiers zéros avaient pour partie réelle exactement 1/2 (ce point sera discuté plus bas; il s'agit bien d'une démonstration, et non d'un calcul numérique approché) et suggéra qu'ils pourraient bien être tous sur l'axe de symétrie (la ligne critique) Re(s)=1/2; c'est cette conjecture qu'on appelle l'hypothèse de Riemann.
En 1896, Hadamard et La Vallée-Poussin prouvèrent indépendamment qu'aucun zéro ne pouvait se trouver sur la ligne Re(s) = 1, et donc que tous les zéros non triviaux devaient se trouver dans l'intérieur de la bande critique 0 < Re(s) < 1. Ceci s'avéra être un résultat-clé dans la première démonstration complète du théorème des nombres premiers.
En 1900, Hilbert inclut l'hypothèse de Riemann dans sa célèbre liste de 23 problèmes non résolus: c'est le 8e problème. Il aurait dit à son propos: « Si je devais me réveiller après avoir dormi pendant mille ans, ma première question serait: l'hypothèse de Riemann a-t-elle été prouvée? ».
En 1914, Hardy prouva qu'il y a une infinité de zéros sur la droite critique Re(s) = 1/2. Cependant il reste possible qu'il y ait une infinité de zéros non triviaux ailleurs. Des travaux ultérieurs de Hardy et Littlewood en 1921, puis de Selberg en 1942 ont donné une estimation de la densité moyenne de zéros sur la droite critique.
Des travaux plus récents se sont focalisés sur le calcul explicite d'endroits où se trouvent beaucoup de zéros (dans l'espoir de trouver un contre-exemple) et de placer des bornes supérieures sur la proportion de zéros se trouvant ailleurs que sur la droite critique (dans l'espoir de la réduire à zéro).
L'hypothèse de Riemann est l'un des sept problèmes de Hilbert non encore résolus, et fut d'ailleurs le seul problème de Hilbert choisi pour figurer dans la liste des problèmes du prix du millénaire de l'institut de mathématiques Clay.

## Tests numériques

Dès l'énoncé par Riemann de la conjecture, des calculs numériques des premiers zéros non triviaux de la fonction permirent de la confirmer (on trouvera dans la table ci-dessous un exposé des divers résultats obtenus). Dans les années 1980, Andrew Odlyzko s'était spécialisé dans ce type de calcul, et on affirme ainsi généralement que le milliard et demi de zéros calculés par lui vérifient tous l'hypothèse de Riemann; on pourrait penser que cela signifie seulement qu'ils sont positionnés assez près de la droite critique (au sens où l'imprécision de calcul ne permettrait pas d'exclure qu'ils peuvent y être exactement); il n'en est rien, comme on va le voir. Cependant, si on a une certitude mathématique pour, mettons, les premiers millions de zéros, la complexité (y compris informatique) des calculs rend plus relative la confiance qu'on peut avoir dans les derniers résultats; cette question est soigneusement analysée par Xavier Gourdon 2004 (page 3, et plus précisément section 3.3.1) où il annonce le record de vérification des 1013 premiers zéros (et des tests statistiques sur des zéros bien plus éloignés encore).
Les méthodes de vérification numérique partent le plus souvent de la remarque selon laquelle la fonction: 

 $s\mapsto \pi ^{-s/2}\Gamma (s/2)\zeta (s)$

 a les mêmes zéros que zêta dans la bande critique, et qu'elle est réelle sur la droite critique (à cause de l'équation fonctionnelle vue plus haut reliant 

 $\zeta (s)$

 $\zeta (1-s)$

). Il est alors facile de montrer l'existence d'au moins un zéro entre deux points de cette droite en vérifiant numériquement que cette fonction a des signes opposés en ces deux points. En pratique, on utilise la fonction Z (en) de Hardy et la fonction θ de Riemann-Siegel, avec: 

 $\zeta (1/2+it)=Z(t)e^{-i\pi \theta (t)}\$

; en déterminant de nombreux intervalles dans lesquels Z change de signe, on montre l'existence du même nombre de zéros sur la ligne critique. Pour contrôler l'hypothèse de Riemann jusqu'à une partie imaginaire T donnée, il reste à démontrer qu'il n'y a pas d'autres zéros dans cette région; il suffit pour cela de calculer le nombre total de zéros dans la région en question (le rectangle de sommets 0,1, iT et 1+iT), ce qui peut se faire en appliquant le théorème des résidus à la fonction 1/ζ (techniquement, le problème d'éventuels zéros doubles fait qu'on utilise en réalité la fonction ζ'/ζ, même si une autre conjecture est qu'il n'en existe pas): comme ce nombre doit être entier, un calcul numérique suffisamment précis de l'intégrale appropriée donne une certitude. La table suivante recense les calculs effectués jusqu'ici (lesquels, bien sûr, ont tous confirmé l'hypothèse) et donne des indications sur les méthodes utilisées.

## Essais de démonstration

Des approches directes ayant régulièrement échoué, plusieurs lignes d'attaque plus élaborées ont été proposées. Il est d'abord possible de transformer l'hypothèse en termes de théorie des nombres; on montre par exemple que plusieurs conjectures, comme la conjecture de Mertens, entraîneraient l'hypothèse de Riemann (on dit qu'elles sont plus fortes). Malheureusement, cette approche n'a eu comme seul résultat que de réfuter, par exemple, la conjecture de Mertens.
Certaines conjectures analogues, à première vue plus générales, se sont paradoxalement révélées un peu plus faciles à démontrer. C'est le cas des conjectures de Weil, dans lesquelles la fonction zêta est remplacée par les fonctions L: elles ont été démontrées par Pierre Deligne en 1974 à l'aide des puissants outils de géométrie algébrique développés par Alexandre Grothendieck, mais cette technique semble impossible à adapter au cas de la fonction zêta.
Une autre piste part d'étranges analogies entre la répartition empirique des zéros connus et le spectre de certains opérateurs; là encore, il n'a pas été possible d'en tirer même un plan d'attaque.
En juin 2019, une percée jugée prometteuse reprend un résultat de 1927 dû à George Pólya qui relie l'hypothèse à une propriété des zéros de certains polynômes (les polynômes de Jensen); Ken Ono, Don Zagier et deux autres chercheurs démontrent cette propriété pour une vaste classe de polynômes (insuffisante néanmoins pour résoudre le problème) par une approche complètement originale.

## Arguments pour et contre l'hypothèse de  Riemann

Les articles mathématiques sur l'hypothèse de Riemann ont tendance à refuser prudemment de s'engager quant à sa vérité. Parmi les auteurs qui expriment une opinion, la plupart, comme 
Riemann lui-même et Bombieri laissent entendre qu'ils s'attendent à ce qu'elle soit vraie, ou du moins qu'ils l'espèrent. Quelques auteurs expriment de sérieux doutes à son sujet, comme Ivić, qui énumère quelques raisons à son scepticisme, et Littlewood, qui déclare carrément qu'il la croit fausse et qu'il n'y a aucune raison imaginable pour qu'elle soit vraie. Les articles de synthèse s'accordent à dire que les preuves sont fortes mais pas accablantes, de sorte que, même si elle est probablement vraie, il existe un doute raisonnable; ils listent à ce sujet les arguments suivants:

Plusieurs résultats analogues ont été démontrés; la démonstration des conjectures de Weil par Deligne (correspondant au cas des variétés sur un corps fini) est peut-être la plus forte raison théorique en faveur de l'hypothèse, et donne des raisons d'espérer que soit vraie une conjecture plus générale, portant sur les fonctions analogues associées à des formes automorphes. De même, des analogues de l'hypothèse de Riemann sont vraies pour les fonctions zêta de Selberg, et pour la fonction zêta de Goss. En revanche, certaines fonctions zêta d'Epstein (en) ne la vérifient pas, mais ces fonctions ont moins d'analogies avec la fonction de Riemann, n'ayant pas de produit eulérien ni de relations avec des formes automorphes.
Il semblerait à première vue que la vérification numérique de ce que tous les zéros jusqu'à une hauteur T de 

 $10^{13}$

 sont sur la droite critique est une forte confirmation de l'hypothèse. Mais en théorie analytique des nombres, il est souvent arrivé que des conjectures de ce genre soient réfutées, les premières exceptions se produisant pour des valeurs bien plus grandes que ce que permet de tester une approche directe, comme dans le cas de la conjecture ayant donné naissance au nombre de Skewes. Le problème vient de ce que le comportement de la fonction zêta à la hauteur T est influencé par des termes grandissant comme log log T, et tendant vers l'infini si lentement que le calcul ne permet pas de les détecter: ainsi, un terme correctif (noté généralement S(T) dans la littérature) augmenterait de 2 à chaque passage de zéros non sur la droite critique, or il se comporte en (log log T)1/2 et ne dépasse guère 3 partout où on a pu le calculer; T devrait donc être supérieur à 

 $10^{10^{20}}$

 pour que l'on ait une chance, selon ce raisonnement, de voir apparaître des contre-exemples à la conjecture; une telle hauteur est inaccessible au calcul avec nos méthodes actuelles.
Arnaud Denjoy a donné un argument probabiliste en faveur de l'hypothèse de Riemann, basé sur la remarque selon laquelle si μ est une suite aléatoire de « 1 » et de « −1 », alors pour tout ε > 0, les sommes partielles 

 $$M(x)=\sum _{n\leq x}\mu (n)$$

 (dont les valeurs sont les positions d'une marche aléatoire) satisfont presque sûrement 

 $M(x)=O(x^{1/2+\varepsilon })$

. L'hypothèse de Riemann est équivalente à ce résultat pour la fonction de Möbius μ et pour la fonction de Mertens M correspondante; en d'autres mots, l'hypothèse de Riemann est en un certain sens équivalente à dire que la fonction de Möbius se comporte comme une suite de tirages au sort à pile ou face, et compte tenu de la définition de cette fonction, à dire que la parité du nombre de facteurs premiers d'un entier se comporte au hasard. En théorie des nombres, des arguments de ce genre donnent souvent la bonne réponse, mais s'avèrent difficiles à rendre rigoureusement, et échouent parfois, comme dans le cas du théorème de Maier (en).
Les calculs faits par Odlyzko montrent que les zéros de la fonction zêta se comportent comme les valeurs propres d'une matrice hermitienne aléatoire, suggérant que ce pourraient être les valeurs propres d'un opérateur auto-adjoint (ce qui impliquerait l'hypothèse de Riemann). Cependant, toutes les tentatives de construire un tel opérateur ont échoué.
Plusieurs théorèmes, comme la conjecture faible de Goldbach, d'abord démontrés à l'aide de l'hypothèse de Riemann (généralisée), furent par la suite démontrés inconditionnellement. Cela peut être considéré comme une indication de ce que l'hypothèse est vraie.
L'existence de paires de Lehmer (en) (deux zéros très proches) est parfois vue comme indication de ce que l'hypothèse est fausse. Mais cela se produirait même si elle était vraie, comme le montrent les calculs d'Odlyzko confirmant la conjecture de Montgomery (en).
Samuel James Patterson (en) suggère que pour la plupart des mathématiciens, l'argument le plus fort en faveur de l'hypothèse est l'espoir que les nombres premiers soient distribués le plus régulièrement possible.

## Pseudo-démonstrations

De nombreuses preuves supposées de l'hypothèse de Riemann sont régulièrement proposées, principalement sur Internet, ainsi que quelques infirmations, souvent le fait d'amateurs en marge du système universitaire traditionnel, mais parfois aussi de mathématiciens professionnels, mais s'éloignant de leur domaine d'expertise (les plus célèbres de ces dernières tentatives étant dues à Louis de Branges en 2004 et à Michael Atiyah en 2018). Aucun de ces travaux n'a pour le moment reçu l'assentiment de la communauté mathématique.
Le site du mathématicien britannique Matthew R. Watkins recense quelques-unes de ces supposées preuves — y compris des « preuves » que l'hypothèse serait fausse —, en plus de quelques parodies.

## Visualisation

*Courbe $\frac{1}{x}$ illustrant le comportement asymptotique*

```tikz
\usepackage{pgfplots}
\pgfplotsset{compat=1.16}

\begin{document}
\begin{tikzpicture}
\begin{axis}[
    axis lines=middle,
    grid=both,
    domain=-5:5,
    samples=200,
    xlabel={$x$},
    ylabel={$f(x)$},
    width=10cm,
    height=8cm
]
\addplot[blue, thick] {1/x};
\end{axis}
\end{tikzpicture}
\end{document}
```
