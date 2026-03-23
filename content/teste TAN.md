---
ccl: menutble
bnner: "![[zzzzz ⚙️ime 1 🖼ime bnquePted ime 20230702214935.pn]]"
---
caca
tube
% === 14*x^{0.5}*y^{0.5} ===
```tikz
\usepackage{pgfplots}
\pgfplotsset{compat=1.16}

\begin{document}
\begin{tikzpicture}
\begin{axis}[
 view={60}{30},
 xlabel=$x$,
 ylabel=$y$,
 zlabel=$z$,
 colormap/cool,
 width=10cm,
 height=8cm
]
\addplot3[
 surf,
 samples=15,
 domain=-5:5,
 y domain=-5:5
] {14*x^{0.5}*y^{0.5}};
\end{axis}
\end{tikzpicture}
\end{document}
```

## 💡 Qu'est-ce que la fonction tangente ?

### Introduction

La fonction tangente apparaît naturellement en trigonométrie pour résoudre des problèmes de triangles rectangles, mais son importance va bien au-delà. Elle émerge lorsque nous cherchons à exprimer le rapport entre l'opposé et l'adjacent dans un triangle rectangle - une relation fondamentale en géométrie. Son comportement oscillatoire et ses propriétés dérivatives en font un outil essentiel en analyse mathématique.

Intuitivement, la tangente mesure l'inclinaison d'une droite par rapport à l'horizontale. Imaginez une rampe : plus elle est raide, plus sa tangente est grande. Cette idée simple se généralise à toutes les fonctions différentiables, où la tangente en un point donne la pente de la droite tangent à la courbe en ce point.

### Définition(s)

> [!abstract] Définition (géométrique)
> Dans un triangle rectangle, la tangente d'un angle θ est le rapport entre la longueur du côté opposé à l'angle et celle du côté adjacent.
>
> $$\tan(\theta) = \frac{\text{opposé}}{\text{adjacent}}$$

> [!abstract] Définition (analytique)
> La fonction tangente peut aussi s'exprimer comme le quotient du sinus par le cosinus :
>
> $$\tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)}$$

Ces deux définitions sont équivalentes car, dans un triangle rectangle, le rapport des longueurs correspond exactement au rapport des valeurs trigonométriques. La définition analytique permet d'étendre la notion à tous les angles, pas seulement ceux des triangles rectangles.

---

## 🔍 Comment ça fonctionne ?

### L'idée centrale

La fonction tangente est périodique avec une période de π (180°), ce qui signifie qu'elle se répète tous les π radians. Son comportement est particulièrement intéressant autour des valeurs où le cosinus s'annule (π/2 + kπ), car c'est là que la fonction devient infinie - ces points correspondent aux asymptotes verticales.

Un exemple concret : si vous mesurez l'angle d'élévation d'un objet, la tangente de cet angle vous donne directement le rapport entre la hauteur et la distance horizontale. Plus l'angle est grand, plus la tangente augmente rapidement.

### Domaine et contraintes

La fonction tangente est définie partout sauf là où cos(θ) = 0, c'est-à-dire aux angles (π/2 + kπ) pour tout entier k. Ces points correspondent aux asymptotes verticales où la fonction "explose" vers l'infini.

Pourquoi cette restriction ? Parce que diviser par zéro est mathématiquement impossible. La tangente "s'échappe" vers l'infini quand l'angle s'approche de π/2, ce qui correspond à une droite verticale dont la pente est infinie.

---

## 📊 Propriétés principales

### Périodicité

La fonction tangente est périodique avec une période de π :
$$\tan(\theta + \pi) = \tan(\theta)$$

**Pourquoi ?** Parce que le cercle trigonométrique se répète tous les 2π, mais comme la tangente est le rapport sinus/cosinus, et que ces deux fonctions ont la même période 2π, leur quotient a une période π.

**Conséquence pratique:** On peut réduire n'importe quel angle modulo π pour étudier la tangente.

### Symétrie

La fonction tangente est impaire :
$$\tan(-\theta) = -\tan(\theta)$$

**Pourquoi ?** Parce que le sinus est impair et le cosinus est pair, donc leur quotient est impair.

**Conséquence pratique:** La courbe est symétrique par rapport à l'origine.

### Dérivée

La dérivée de la tangente est particulièrement simple :
$$\frac{d}{d\theta} \tan(\theta) = 1 + \tan^2(\theta) = \sec^2(\theta)$$

**Pourquoi ?** Par la règle de dérivation des quotients, en utilisant que la dérivée de sin est cos et celle de cos est -sin.

**Conséquence pratique:** Cette propriété est cruciale pour résoudre des équations différentielles et en analyse complexe.

---

## 🧮 Calculs et manipulations

### Calcul de la tangente d'un angle

Pour calculer tan(θ), on peut utiliser soit la définition géométrique (si on a un triangle rectangle), soit la définition analytique.

**Pourquoi cette formule ?** Parce que la tangente mesure l'inclinaison, et cette inclinaison est directement donnée par le rapport des côtés.

| Angle (en radians) | Valeur de tan(θ) | Pourquoi c'est intéressant |
|---|---|---|
| 0 | 0 | La tangente de 0 est 0 car le côté opposé est nul |
| π/4 | 1 | La tangente de 45° est 1 car les côtés sont égaux |
| π/3 | √3 ≈ 1.732 | Valeur importante en géométrie des triangles équilatéraux |
| π/6 | 1/√3 ≈ 0.577 | Valeur importante en géométrie des triangles rectangles |

---

## 🎯 Applications et exemples

### Exemple 1: Calcul de la hauteur d'un bâtiment

**Contexte:** Vous mesurez l'angle d'élévation d'un bâtiment depuis un point au sol et vous connaissez la distance horizontale jusqu'au bâtiment.

**Problème:** Si l'angle d'élévation est de 30° et la distance horizontale est de 50 mètres, quelle est la hauteur du bâtiment ?

**Résolution:**

Étape 1: On utilise la définition de la tangente
$$\tan(30°) = \frac{\text{hauteur}}{50}$$

Étape 2: On connaît tan(30°) = 1/√3 ≈ 0.577
$$0.577 = \frac{\text{hauteur}}{50}$$

Étape 3: On isole la hauteur
$$\text{hauteur} = 50 \times 0.577 ≈ 28.85 \text{ mètres}$$

**Interprétation:** La hauteur du bâtiment est d'environ 28.85 mètres. Cet exemple montre comment la tangente permet de calculer des distances inaccessibles directement.

---

### Exemple 2: Résolution d'une équation trigonométrique

**Contexte:** On veut résoudre l'équation tan(x) = 2 dans l'intervalle [0, π].

**Résolution:**

Étape 1: On connaît la définition de la tangente
$$x = \arctan(2)$$

Étape 2: On calcule la valeur principale
$$x ≈ 1.107 \text{ radians}$$

Étape 3: On utilise la périodicité pour trouver toutes les solutions
$$x = 1.107 + k\pi \text{ pour tout entier } k$$

**Interprétation:** La solution générale montre que la tangente est périodique, et que chaque intervalle de π radians contient une solution.

---

## 🔗 Liens avec d'autres concepts

- **[[Fonction sinus]]**: La tangente est le quotient du sinus par le cosinus, ce qui explique ses propriétés
- **[[Fonction cosinus]]**: Le cosinus apparaît au dénominateur, ce qui explique les asymptotes
- **[[Fonction cotangente]]**: La cotangente est l'inverse de la tangente
- **[[Fonction exponentielle]]**: La tangente est liée aux fonctions hyperboliques via la relation tan(x) = -i tanh(ix)

---

## 📝 À retenir

> [!summary] L'essentiel
>
> La fonction tangente mesure l'inclinaison d'une droite par rapport à l'horizontale. Elle est définie comme le rapport entre le côté opposé et le côté adjacent dans un triangle rectangle, ou comme le quotient du sinus par le cosinus. Sa périodicité de π et ses asymptotes en font une fonction oscillante avec des comportements particuliers. La tangente est impaire et sa dérivée est particulièrement simple, ce qui en fait un outil fondamental en analyse. Elle apparaît naturellement dans les problèmes de géométrie, d'optique et de physique.
>
> Formule clé :
> $$\tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)}$$
>
> Ce qu'il faut retenir : la tangente est une fonction qui capture l'idée d'inclinaison, avec des propriétés mathématiques riches et des applications concrètes dans de nombreux domaines.

#Fonction/Trigonométrie #Analyse éométrie