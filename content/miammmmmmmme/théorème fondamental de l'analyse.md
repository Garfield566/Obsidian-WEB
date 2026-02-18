---
nom: "théorème fondamental de l'analyse"
qid: Q1217677
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/GodfreyKneller-IsaacNewton-1689.jpg/330px-GodfreyKneller-IsaacNewton-1689.jpg
---

# Théorème fondamental de l'analyse

> [!Infobox]
> **Théorème fondamental de l'analyse**
> ![[https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/GodfreyKneller-IsaacNewton-1689.jpg/330px-GodfreyKneller-IsaacNewton-1689.jpg|300]]
> - **Nomme d'apres** : Isaac Newton, Gottfried Wilhelm Leibniz
> - **Aspect de** : calcul infinitésimal
> - **Discipline dont c'est l'objet** : calcul infinitésimal
> - **Nom court** : HDI
> - **Partie de** : liste de théorèmes

En mathématiques, le théorème fondamental de l'analyse (ou théorème fondamental du calcul différentiel et intégral) établit que les deux opérations de base de l'analyse, la dérivation et l'intégration, sont, dans une certaine mesure, réciproques l'une de l'autre. Il est constitué de deux familles d'énoncés (plus ou moins généraux selon les versions, et dépendant de la théorie de l'intégration choisie):

premier théorème: certaines fonctions sont « la dérivée de leur intégrale »;
second théorème: certaines fonctions sont « l'intégrale de leur dérivée ».
(La numérotation est inverse dans certains ouvrages.)
Une conséquence importante du second théorème est de permettre de calculer une intégrale en utilisant une primitive de la fonction à intégrer.

## Historique

Avant la découverte du théorème fondamental de l'analyse, la relation entre intégration et dérivation n'était pas soupçonnée. Les mathématiciens grecs savaient déjà calculer des aires et des volumes à l'aide d'infinitésimaux, une opération qui serait actuellement appelée une intégration. La notion de différentiation fut introduite elle aussi dès le Moyen Âge; ainsi, les notions de continuité de fonctions et de vitesse de déplacement furent étudiées par les Calculateurs d'Oxford au XIVe siècle. L'importance historique du théorème ne fut pas tant de faciliter le calcul des intégrales que de faire prendre conscience que ces deux opérations apparemment sans rapport (le calcul d'aires, et le calcul de vitesses) sont en fait étroitement reliées.
Le premier énoncé (et sa démonstration) d'une forme partielle du théorème fut publié par James Gregory en 1668. Isaac Barrow en démontra une forme plus générale, mais c'est Isaac Newton (élève de Barrow) qui acheva de développer la théorie mathématique englobant le théorème. Gottfried Wilhelm Leibniz systématisa ces résultats sous forme d'un calcul des infinitésimaux, et introduisit les notations toujours actuellement utilisées.

## Énoncé

Si F est une primitive de f sur I et si f est localement intégrable au sens de Lebesgue, alors

 $$\forall a,b\in I\quad \int _{a}^{b}f\,\mathrm {d} \lambda =F(b)-F(a),$$

ce qui équivaut à: F est absolument continue et F' = f presque partout (la continuité absolue est indispensable, comme le montre le contre-exemple de l'escalier de Cantor).
Plus généralement: si F est une primitive généralisée de f, alors f est intégrable au sens de Kurzweil-Henstock et l'on a encore (en ce sens)

 $$\forall a,b\in I\quad \int _{a}^{b}f=F(b)-F(a).$$

## Démonstration

Supposons que f admet une limite à droite f(c+) en c. Soit ε > 0. Il existe η > 0 tel que pour tout t ∈ ]c, c + η], f(t) soit (bien défini et) ε-proche de f(c+). Par suite, pour tout x ∈ ]c, c + η] (et en commençant par utiliser la relation de Chasles):

 $${\begin{aligned}\left|F(x)-F(c)-(x-c)f(c^{+})\right|&=\left|\int _{c}^{x}f(t)\mathrm {d} t-(x-c)f(c^{+})\right|\\&=\left|\int _{c}^{x}\left(f(t)-f(c^{+})\right)\mathrm {d} t\right|\\&\leq \int _{c}^{x}\left|f(t)-f(c^{+})\right|\mathrm {d} t\\&\leq \varepsilon (x-c)\end{aligned}}$$

 $$\left|\frac {F(x)-F(c)}{x-c}-f(c^{+})\right|\leq \varepsilon.$$

On raisonnerait de même pour la dérivée à gauche.
Par construction, F est continue. Supposons que f est réglée. Alors, ses discontinuités sont de première espèce donc (cf. Théorème de Froda) forment un ensemble au plus dénombrable, si bien que (d'après 1.) F est une primitive généralisée de f.
G – H est continue et de dérivée nulle sur le complémentaire d'un ensemble dénombrable. Elle est donc constante, d'après l'inégalité des accroissements finis généralisée.

## Généralisation

Ce premier théorème fondamental s'étend aux fonctions non continues de la façon suivante: si f est une fonction intégrable au sens de Lebesgue sur [a, b] et si F est définie sur [a, b] par 

 $$F(x)=\int _{a}^{x}f\,\mathrm {d} \lambda$$

 alors, pour tout point de Lebesgue c de f (donc presque partout — d'après le théorème de différentiation de Lebesgue — et en particulier si f est continue en c), 

 $F^{\prime }(c)=f(c)$

Plus généralement:

Si f est intégrable au sens de Kurzweil-Henstock sur [a, b], alors la fonction 

 $$F:x\mapsto \int _{a}^{x}f(t)\,\mathrm {d} t$$

 admet presque partout une dérivée égale à f.

## Explication intuitive

Intuitivement, le second théorème dit simplement que si l'on connaît tous les petits changements instantanés d'une certaine quantité, alors on peut calculer le changement général de cette quantité en additionnant tous les petits changements.
Pour se donner une idée de cette affirmation, commençons par donner un exemple.
Supposons que nous voyagions sur une ligne droite, et que nous partions à l'instant t = 0, et avec une vitesse variable. Si, à l'instant t, d(t) indique notre distance à l'origine et v(t) représente notre vitesse, alors v(t) est le taux d'accroissement « infinitésimal » de d et est la valeur de la dérivée de d en t. Supposons que nous n'ayons qu'un compteur de vitesse qui indique la vitesse v(t), et que nous voulions retrouver notre distance d(t). Le théorème fondamental de l'analyse dit qu'il suffit pour cela de chercher une primitive de v.
Et ceci est exactement ce que nous aurions fait, même sans connaître ce théorème: enregistrer la vitesse à des intervalles réguliers, peut-être toutes les minutes, et alors multiplier la première vitesse par 1 minute pour obtenir une estimation de la distance parcourue dans la première minute, puis multiplier la deuxième vitesse par 1 minute pour obtenir la distance parcourue dans la deuxième minute etc., et enfin ajouter toutes les distances précédentes. Pour obtenir une meilleure estimation de notre distance actuelle, nous avons besoin d'enregistrer les vitesses à des intervalles de temps plus courts. La limite quand la longueur des intervalles tend vers zéro est exactement la définition de l'intégrale de v.

## Généralisations

Le second théorème fondamental, appliqué à une fonction F de classe C1, est la formule de Taylor avec reste intégral à l'ordre 0. Cette formule se généralise à l'ordre n, pour une fonction de classe Cn+1.
Il existe une version du second théorème fondamental pour les fonctions de la variable complexe: si U est un ouvert de ℂ et si f: U → ℂ admet une primitive holomorphe F sur U alors, pour toute courbe γ: [a, b] → U, l'intégrale sur cette courbe peut être obtenue par:

 $$\int _{\gamma }f(z)\,\mathrm {d} z=F{\bigl (}\gamma (b){\bigr )}-F{\bigl (}\gamma (a){\bigr )}.$$

Le théorème fondamental peut être généralisé à des intégrales sur des contours ou sur des surfaces dans des dimensions supérieures et sur des espaces vectoriels (voir le théorème de Stokes).
