---
nom: "Hypothèse du continu"
qid: Q208416
type: conjecture
categorie: conjecture
tags: "#mathematiques/conjecture"
---

# Hypothèse du continu

> [!Infobox]
> **Hypothèse du continu**
> - **Découvert(e) ou inventé(e) par** : Georg Cantor
> - **Partie de** : problèmes de Hilbert, liste de théorèmes, liste d'axiomes
> - **Résolu par** : Kurt Gödel, Paul Cohen
> - **Date de découverte ou d'invention** : 1877
> - **Nomme d'apres** : puissance du continu
> - **Caractérisé par** : indépendance
> - **Nom court** : HC
> - **Discipline dont c'est l'objet** : théorie des ensembles

En théorie des ensembles, l'hypothèse du continu (HC), due à Georg Cantor, affirme qu'il n'existe aucun ensemble dont le cardinal est strictement compris entre le cardinal de l'ensemble des entiers naturels et celui de l'ensemble des nombres réels. En d'autres termes: tout ensemble strictement plus grand, au sens de la cardinalité, que l'ensemble des entiers naturels doit contenir une « copie » de l'ensemble des nombres réels.

## Historique

Cantor avait démontré (et publié en 1874) que le cardinal de l'ensemble des nombres réels était strictement plus grand que celui des nombres entiers; il formula plus tard l'hypothèse du continu, qui résultait d'une analyse des sous-ensembles de la droite réelle, et de sa hiérarchisation des cardinaux infinis, mais il tenta en vain de la démontrer. Cette démonstration constituait le premier de la célèbre liste des 23 problèmes de Hilbert, que celui-ci avait établie pour le congrès international des mathématiciens de 1900 à Paris, afin de guider la recherche en mathématiques du siècle alors naissant.
Ce n'est que bien plus tard, en 1963, que Paul Cohen introduisit sa méthode de forcing pour montrer que cette hypothèse ne pouvait se déduire des axiomes de la théorie des ensembles ZFC, généralement considérée comme une formalisation adéquate de la théorie des ensembles de Cantor, qui n'était pas encore axiomatisée en 1900. Kurt Gödel avait précédemment démontré, en 1938, que cette hypothèse n'était pas non plus réfutable dans ZFC. Elle est donc indépendante des axiomes de la théorie des ensembles ZFC, ou encore indécidable dans cette théorie.
La méthode du forcing de Cohen a connu depuis de nombreux développements en théorie des ensembles. Son résultat n'a pas mis un point final aux travaux sur le sujet. La recherche d'hypothèses naturelles à ajouter à la théorie ZFC et d'arguments qui permettraient de trancher pour ou contre l'hypothèse du continu constitue toujours un sujet actif en théorie des ensembles.

## Énoncé de l'hypothèse du continu

Un ensemble est dit dénombrable quand il est en bijection avec l'ensemble ℕ des entiers naturels. L'argument diagonal permet de montrer que l'ensemble ℝ des réels (le continu) n'est pas dénombrable, donc que son cardinal est strictement supérieur au cardinal du dénombrable. Se pose le problème de l'existence de cardinaux intermédiaires entre celui de ℕ et celui de ℝ. Cantor faisait l'hypothèse qu'il n'en existe pas, et c'est ce que l'on appelle hypothèse du continu.
Le cardinal du dénombrable est noté ℵ0 (aleph-zéro). Le cardinal qui suit immédiatement ℵ0 est noté ℵ1, on peut le définir dans la théorie des ensembles de Zermelo-Fraenkel ZF (sans nécessairement l'axiome du choix). On montre que le cardinal de ℝ est celui de l'ensemble des parties de ℕ, que l'on note 2ℵ0. L'existence d'un tel cardinal (défini comme ordinal) suppose, elle, l'axiome du choix, du moins le fait que ℝ peut être bien ordonné. L'hypothèse du continu s'écrit alors

 ℵ

 ℵ

 $2^{\aleph _{0}}=\aleph _{1}$

c'est-à-dire qu'il n'existe pas de cardinaux qui soient strictement compris entre celui du dénombrable et celui du continu (le fait que deux cardinaux soient nécessairement comparables est une conséquence de l'axiome du choix). Le cardinal ℵ1 est par définition le cardinal du premier ordinal non dénombrable noté ω₁.
En l'absence de l'axiome du choix, on peut démontrer l'existence de ω₁ et l'égalité 2ℵ0=ℵ1 signifie que ℝ peut être bien ordonné par un bon ordre de type ω₁, soit, à la fois que ℝ peut être bien ordonné et l'hypothèse du continu. Dans une théorie des ensembles sans axiome du choix, il est quand même possible d'exprimer l'hypothèse du continu sans que cela entraîne l'existence d'un bon ordre sur ℝ, en revenant aux définitions primitives qui sous-tendent la définition des cardinaux et de l'ordre sur ceux-ci, soit en termes de bijection et d'injection, voir le paragraphe suivant.

## Cardinalité

Deux ensembles S et T sont équipotents, ou encore ont même cardinalité, lorsqu'il existe une bijection entre S et T. Cela signifie que l'on peut associer à chaque élément de S un unique élément de T et que tout élément de T est l'image d'un unique élément de S. Cette notion de cardinalité suffit pour bien des aspects élémentaires, sans qu'il soit nécessaire de définir le cardinal proprement dit. La définition d'un cardinal en tant qu'ensemble, plus précisément d'ordinal, due également à Cantor, nécessite l'axiome du choix. Étant donné cet axiome, on peut définir proprement le cardinal d'un ensemble comme le plus petit ordinal auquel est bijectif cet ensemble. L'existence de ce plus petit ordinal est garantie par le principe du bon ordre qui vaut sur la collection des ordinaux.
Une caractéristique des ensembles infinis est que ceux-ci sont équipotents à certaines de leurs parties propres, contrairement à ce qui se passe pour les ensembles finis. Ainsi bien qu'il semble y avoir « plus » de rationnels que d'entiers, il est possible d'énumérer tous les rationnels en les indexant par les entiers naturels, c'est-à-dire d'établir une bijection entre ces deux ensembles (voir l'article Ensemble dénombrable). Un tel ensemble, équipotent à l'ensemble des entiers naturels, est dit dénombrable ou infini dénombrable.
L'ensemble des nombres réels, noté ℝ, est un exemple d'ensemble non-dénombrable. Cantor en a proposé en 1891 une seconde démonstration très simple utilisant l'argument de la diagonale. Le continu désigne la droite réelle ℝ, d'où le nom de l'hypothèse. On dit d'un ensemble équipotent à ℝ qu'il a la puissance du continu.
On peut reformuler ainsi l'hypothèse du continu, sans faire appel aux cardinaux (ni à l'axiome du choix).

## Indécidabilité

Kurt Gödel a démontré en 1938 que l'ajout de l'hypothèse du continu à la théorie des ensembles, définie par exemple par les axiomes de Zermelo-Fraenkel (sans nécessairement l'axiome du choix, noté AC ci-dessous), ne changeait rien à la cohérence de cette théorie: si la théorie ZF est cohérente, la théorie (ZF + Hypothèse du continu) est cohérente.
Il est arrivé à cette démonstration en construisant, sous l'hypothèse de la cohérence de ZF, un certain modèle de ZF satisfaisant aussi l'axiome de constructibilité. Il s'agit d'un modèle intérieur, c'est-à-dire, d'un modèle transitif qui contient la collection des ordinaux et sur lequel la relation d'appartenance satisfait les axiomes ZF. À l'intérieur de ce modèle, l'hypothèse du continu est aussi satisfaite. Un tel modèle intérieur satisfaisant l'axiome de constructibilité s'appelle l'univers constructible 

 $L$

Paul Cohen a montré en 1963 que l'hypothèse du continu n'était pas démontrable dans la théorie des ensembles basée sur les axiomes de Zermelo-Fraenkel, démonstration pour laquelle il invente la méthode de forcing. Elle est donc indépendante de la théorie des ensembles, c'est-à-dire, de ZFC + l'axiome de fondation (noté AF ci-dessous).
Un raisonnement informel peut nous aiguiller sur la manière de procéder pour obtenir ce résultat d'indépendance. D'après une proposition fondamentale en théorie des ensembles, on sait que la non-contradiction de ZFC+AF implique l'existence d'une théorie 

 $T$

 satisfaisant ces axiomes et contenant un modèle de ZFC+AC, 

 $M$

, qui est un ensemble transitif et dénombrable. On considère le produit 

 ℵ

 $\pi \times \aleph _{0}$

 où 

 $\pi$

 signifie un cardinal strictement supérieur à 

 ℵ

 $\aleph _{1}$

 interprété dans 

 $M$

 et où 

 ℵ

 $\aleph _{0}$

 conserve la même signification que dans les sections plus haut. On peut construire une fonction 

 $f_{\alpha }:n\rightarrow \{0,1\}$

 qui, pour un élément fixe 

 $\alpha \in \pi$

, associe à chaque 

 $n$

 un élément de l'ensemble 

 $\{0,1\}$

. Puisque le cardinal 

 $\pi$

 est interprété comme un élément d'un ensemble transitif et dénombrable 

 $M$

, il est lui-même transitif et dénombrable comme élément de cet ensemble. On peut donc imaginer une procédure inductive qui définit pour chaque 

 $\alpha \in \pi$

 une fonction différente 

 $f_{\alpha }$

. Chacune de ces fonctions correspond à une partie différente de 

 ℵ

 $\aleph _{0}$

. Il y a donc une injection, 

 $F:\alpha \rightarrow f_{\alpha }$

, qui à chaque élément du cardinal 

 $\pi$

 associe un élément différent de l'ensemble des parties de 

 ℵ

 $\aleph _{0}$

. Donc, par le théorème de Cantor-Bernstein, la cardinalité de cet ensemble des parties est au moins égale à celle de 

 $\pi$

 et, donc, strictement supérieure à la cardinalité de 

 ℵ

 $\aleph _{1}$

Toute la subtilité de l'argument repose sur la question de savoir si cette fonction, 

 $F$

, que l'on définit appartient rigoureusement à l'ensemble 

 $M$

 et donc appartient à un modèle de ZFC+AC. Le forcing de Cohen permet de construire le plus petit modèle transitif dénombrable, 

 $M[F]$

, contenant une telle fonction et possédant les mêmes cardinaux que 

 $M$

Il n'y a pas a priori de raison d'être surpris de l'existence d'énoncés ne pouvant être démontrés ou infirmés à partir d'un système d'axiomes donné, c'est par exemple le cas du postulat d'Euclide relativement à son système « axiomatique ». D'ailleurs, on sait qu'il doit en exister dans tout système mathématique assez puissant; c'est le théorème d'indécidabilité de Gödel. Mais l'hypothèse du continu paraissait devoir admettre une solution: c'est à ce genre d'énoncé que David Hilbert pensait en déclarant: « Il n'y a pas d'ignorabimus en mathématiques; nous devons savoir; nous saurons. ».
L'hypothèse du continu n'est pas sans rapport avec des énoncés d'analyse, ou de théorie de la mesure.
Historiquement, les mathématiciens en faveur d'une large classe d'ensembles rejettent l'hypothèse du continu, alors que ceux favorables au contraire à une ontologie ensembliste plus restreinte l'acceptent.
Plus précisément, les résultats de Paul Cohen, combinés avec un théorème de König, montrent que 

 ℵ

 ℵ

 $2^{\aleph _{0}}=\aleph _{\alpha }$

 est compatible avec ZFC si et seulement si 

 $\alpha$

 (non nul) n'est pas de cofinalité 

 $\omega$

## Généralisation

L'hypothèse généralisée du continu dit qu'il n'existe pas d'ensemble dont le cardinal est strictement compris entre 

 ℵ

 $\aleph _{\alpha }$

 ℵ

 $2^{\aleph _{\alpha }}$

 $\alpha$

 parcourant les ordinaux et 

 $2^{\kappa }$

 étant le cardinal de l'ensemble des parties d'un ensemble de cardinal 

 $\kappa$

Elle dit ainsi 

 ℵ

 ℵ

 $2^{\aleph _{\alpha }}=\aleph _{\alpha +1}$

: il n'y a pas d'ensemble infini dont la cardinalité est intermédiaire entre celle de cet ensemble et l'ensemble de ses parties; la notion de cardinalité étant envisagée en termes de classe d'équipotence (soit, deux ensembles en bijection ont même cardinalité).
Cette hypothèse est plus forte que celle du continu. En 1938, Gödel a en fait montré directement que l'hypothèse généralisée du continu est compatible avec les axiomes de ZFC: plus précisément, l'univers constructible satisfait cette hypothèse généralisée et l'axiome du choix, même si l'univers initial ne satisfait que les axiomes de ZF. On a donc l'indépendance de l'hypothèse généralisée du continu par le résultat de Cohen.

## Hypothèse généralisée du continu et axiome du choix

Pour définir la notion de nombre cardinal d'un ensemble dans la théorie ZFC on a besoin de l'axiome du choix. Un cardinal est un ordinal qui n'est pas équipotent à un ordinal strictement plus petit (c'est-à-dire en bijection avec celui-ci), et on peut associer à tout ensemble un ordinal en utilisant le théorème de Zermelo (équivalent à l'axiome du choix). Si on se contente d'une notion plus informelle de cardinal — une classe d'équivalence pour la relation d'équipotence (une telle classe ne peut être un ensemble), il faut prendre garde, qu'en l'absence de l'axiome du choix, deux classes ne sont pas nécessairement comparables. Plus précisément on dit que a est subpotent à b quand il existe une injection de a dans b, strictement subpotent quand de plus il n'y a pas de bijection entre a et b. La « totalité » de l'ordre ainsi défini (voir théorème de Cantor-Bernstein) entre cardinaux, est historiquement appelée propriété de trichotomie des cardinaux, car elle peut s'énoncer ainsi: étant donnés deux ensembles a et b, soit a est strictement subpotent à b, soit b est strictement subpotent à a, soit a et b sont équipotents. La propriété de trichotomie des cardinaux est équivalente à l'axiome du choix dans ZF.
On peut cependant énoncer de façon naturelle l'hypothèse du continu généralisée dans la théorie ZF:

Cet énoncé est bien équivalent aux énoncés précédents de l'hypothèse généralisée du continu, en présence de l'axiome du choix.
On peut donc se poser la question dans la théorie ZF du rapport entre l'hypothèse du continu généralisée et l'axiome du choix. Wacław Sierpiński a montré en 1947 que l'hypothèse généralisée du continu, énoncée de cette façon, a pour conséquence l'axiome du choix dans la théorie ZF (sa démonstration utilise, entre autres, l'ordinal de Hartogs).
Toutefois, la théorie ZF seule n'implique pas l'axiome du choix, comme l'a montré Paul Cohen dans le même article que celui sur l'indépendance de l'hypothèse du continu, en utilisant sa méthode de forcing, combinée avec la méthode de permutation développée par Adolf Fraenkel puis Andrzej Mostowski (qui avaient déjà obtenu ce résultat pour une théorie analogue à ZF mais avec des Ur-elements).

## Nouveaux axiomes

Les travaux de Cohen ne mettent pas forcément fin au débat: il reste la possibilité de découvrir de nouveaux axiomes « plausibles » résolvant la question dans un sens ou dans l'autre. Cohen lui-même a montré que les axiomes de grands cardinaux ne peuvent à eux seuls modifier l'indécidabilité de l'hypothèse du continu, mais dans des travaux du début des années 2000, W. Hugh Woodin envisage que l'hypothèse du continu puisse être essentiellement fausse en introduisant une méta-logique appelée Ω-logique (en) basée sur les ensembles projectifs (en). La Ω-conjecture de Woodin dit que tout énoncé essentiellement vrai dans la Ω-logique est Ω-prouvable. En utilisant des axiomes de grands cardinaux, plus la conjecture ci-dessus, on en déduit alors que l'hypothèse du continu serait essentiellement fausse, et plus précisément que 

 ℵ

 $2^{\aleph _{0}}$

 serait égal à 

 ℵ

 $\aleph _{2}$

 (hypothèse déjà envisagée par Gödel), mais ces résultats sont loin de faire l'unanimité chez les théoriciens. D'ailleurs, à partir de 2010, Woodin, explorant une variante (compatible avec les axiomes de grands cardinaux) de l'axiome de constructibilité, identifiant la classe des ensembles V avec un univers constructible étendu, Lultime, aboutit au contraire à des modèles où l'hypothèse du continu est « naturellement » vraie.
