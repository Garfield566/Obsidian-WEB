## 💡 Qu'est-ce que la dérivée ?

### Introduction

La dérivée est née d'un problème fondamental en physique : comment décrire le changement instantané ? Galilée et Newton ont posé les bases en étudiant le mouvement des corps. En mathématiques, elle répond à la question : "À quelle vitesse change une fonction à un point précis ?"

Intuitivement, la dérivée mesure la pente de la tangente à la courbe représentative d'une fonction. C'est l'outil central du calcul différentiel, permettant d'étudier les variations et les extrema des fonctions.

### Définition(s)

> [!abstract] Définition (analytique)
> Soit \( f \) une fonction définie sur un intervalle \( I \). La dérivée de \( f \) en un point \( a \in I \) est la limite, si elle existe, du taux d'accroissement de \( f \) en \( a \):
>
> $$ f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} $$
>
> **Illustration graphique (SI POSSIBLE):**
> ```tikz
> \begin{document}
> \begin{tikzpicture}[scale=1.5]
>   % Axes
>   \draw[->] (-1,0) -- (4,0) node[right] {$x$};
>   \draw[->] (0,-1) -- (0,3) node[above] {$y$};
>
>   % Courbe
>   \draw[color=blue, domain=0.5:3.5, smooth, variable=\x] plot ({\x}, {0.5*\x*\x});
>
>   % Point a
>   \filldraw (1,0.5) circle (1.5pt) node[below] {$a$};
>   \filldraw (1,0.5) circle (1.5pt);
>   \draw[dashed] (1,0) -- (1,0.5);
>
>   % Point a+h
>   \filldraw (2,2) circle (1.5pt) node[below] {$a+h$};
>   \filldraw (2,2) circle (1.5pt);
>   \draw[dashed] (2,0) -- (2,2);
>
>   % Tangente
>   \draw[red, thick] (1,0.5) -- (3,4);
>
>   % Taux d'accroissement
>   \draw[<->] (1.1,0.5) -- (1.9,2) node[midway, right] {$\Delta y$};
>   \draw[<->] (1,0) -- (2,0) node[midway, below] {$\Delta x = h$};
> \end{tikzpicture}
> \end{document}
> ```

> [!abstract] Définition (géométrique)
> La dérivée \( f'(a) \) est le coefficient directeur de la tangente à la courbe \( y = f(x) \) au point \( (a, f(a)) \). Elle représente la pente de cette droite tangente.
>
> **Illustration graphique (SI POSSIBLE):**
> ```tikz
> \begin{document}
> \begin{tikzpicture}[scale=1.5]
>   % Axes
>   \draw[->] (-1,0) -- (4,0) node[right] {$x$};
>   \draw[->] (0,-1) -- (0,3) node[above] {$y$};
>
>   % Courbe
>   \draw[color=blue, domain=0.5:3.5, smooth, variable=\x] plot ({\x}, {0.5*\x*\x});
>
>   % Point de tangence
>   \filldraw (1,0.5) circle (1.5pt) node[below] {$a$};
>   \filldraw (1,0.5) circle (1.5pt);
>
>   % Tangente
>   \draw[red, thick] (1,0.5) -- (3,4);
>   \node[red, above] at (2,2.25) {$f'(a) = \text{pente}$};
>
>   % Angle
>   \draw[->] (1,0.5) -- (1.5,1.25);
>   \draw[->] (1,0.5) -- (1.5,0.5);
>   \node at (1.3,0.7) {$\theta$};
> \end{tikzpicture}
> \end{document}
> ```

Ces deux définitions sont équivalentes : la pente de la tangente est précisément la limite du taux d'accroissement quand \( h \) tend vers 0.

---

## 🔍 Comment ça fonctionne ?

### L'idée centrale

La dérivée capture l'idée de variation instantanée. Imaginez une voiture roulant sur une route sinueuse : sa vitesse à chaque instant est la dérivée de sa position par rapport au temps. La dérivée nous dit comment la fonction "se comporte" localement autour d'un point.

**Exemple concret:**
Considérons \( f(x) = x^2 \). Entre \( x = 1 \) et \( x = 2 \), la fonction augmente de 3 unités. Mais à \( x = 1 \), la dérivée est 2, ce qui signifie que la fonction augmente de 2 unités par unité de \( x \) à cet instant précis.

### Domaine et contraintes

La dérivée est définie là où la fonction est "lisse", c'est-à-dire sans cassures ou angles vifs. Les points où la dérivée n'existe pas sont les points anguleux, les cusps ou les points de discontinuité.

**Pourquoi ?**
La dérivée nécessite que la fonction soit continue et que la limite du taux d'accroissement existe. Si la fonction a un angle aigu, la pente change brutalement et la limite n'existe pas.

---

## 📊 Propriétés principales

### Linéarité de la dérivée

La dérivée est un opérateur linéaire : elle respecte les combinaisons linéaires.

$$ (af + bg)' = af' + bg' $$

**Pourquoi ?**
La dérivée mesure la variation instantanée. Si on combine deux fonctions, leur variation combinée est la somme de leurs variations individuelles.

**Conséquence pratique:**
Cela permet de dériver facilement les polynômes et les combinaisons de fonctions.

### Règle du produit

La dérivée d'un produit de deux fonctions est donnée par:

$$ (uv)' = u'v + uv' $$

**Pourquoi ?**
Quand on multiplie deux fonctions, leur variation combinée est la somme de la variation de la première multipliée par la deuxième, plus la première multipliée par la variation de la deuxième.

---

### Règle de la chaîne

La dérivée d'une fonction composée est:

$$ (f \circ g)' = (f' \circ g) \cdot g' $$

**Pourquoi ?**
Quand on compose deux fonctions, la variation de la fonction composée est la variation de la fonction extérieure multipliée par la variation de la fonction intérieure.

---

## 🧮 Calculs et manipulations

### Calcul de la dérivée d'une fonction polynomiale

Pour une fonction polynomiale \( f(x) = a_nx^n + \dots + a_1x + a_0 \), la dérivée est:

$$ f'(x) = na_nx^{n-1} + \dots + a_1 $$

**Pourquoi cette formule ?**
Chaque terme \( a_kx^k \) a une dérivée \( ka_kx^{k-1} \), car la dérivée d'une puissance est proportionnelle à la puissance précédente.

### Cas particuliers remarquables

| Fonction | Dérivée | Pourquoi c'est intéressant |
|---|---|---|
| \( f(x) = x^n \) | \( f'(x) = nx^{n-1} \) | Base de la dérivée des polynômes |
| \( f(x) = \sin x \) | \( f'(x) = \cos x \) | Lien fondamental entre sinus et cosinus |
| \( f(x) = e^x \) | \( f'(x) = e^x \) | La seule fonction qui se dérive en elle-même |

---

## 🎯 Applications et exemples

### Exemple 1: Vitesse instantanée

**Contexte:**
Un objet se déplace selon la loi \( s(t) = t^2 + 3t \) (en mètres). Quelle est sa vitesse à \( t = 2 \) secondes ?

**Résolution:**

Étape 1: La vitesse est la dérivée de la position
$$ v(t) = s'(t) $$

Étape 2: Calculons la dérivée
$$ s'(t) = 2t + 3 $$

Étape 3: Évaluons à \( t = 2 \)
$$ v(2) = 2 \times 2 + 3 = 7 \, \text{m/s} $$

**Interprétation:**
L'objet se déplace à 7 mètres par seconde à cet instant précis.

---

### Exemple 2: Optimisation

**Contexte:**
Trouver le minimum de la fonction \( f(x) = x^2 - 4x + 3 \).

**Résolution:**

Étape 1: Trouvons les points critiques
$$ f'(x) = 2x - 4 $$

Étape 2: Résolvons \( f'(x) = 0 \)
$$ 2x - 4 = 0 \implies x = 2 $$

Étape 3: Vérifions que c'est un minimum
$$ f''(x) = 2 > 0 \implies \text{minimum} $$

Étape 4: Calculons \( f(2) \)
$$ f(2) = 4 - 8 + 3 = -1 $$

**Interprétation:**
La fonction atteint son minimum en \( x = 2 \) avec une valeur de -1.

---

## 🔗 Liens avec d'autres concepts

- **[[Intégrale]]**: La dérivée et l'intégrale sont liées par le théorème fondamental de l'analyse, qui dit que la dérivée est l'inverse de l'intégrale.
- **[[Équation différentielle]]**: Les dérivées sont au cœur des équations différentielles, qui modélisent des phénomènes dynamiques.
- **[[Limite]]**: La dérivée est définie comme une limite, ce qui en fait un concept fondamental en analyse.

---

## 📝 À retenir

> [!summary] L'essentiel
>
> La dérivée mesure la variation instantanée d'une fonction. Elle est définie comme la limite du taux d'accroissement et représente la pente de la tangente à la courbe. Les propriétés principales incluent la linéarité, la règle du produit et la règle de la chaîne. La dérivée est essentielle pour étudier les extrema, les taux de variation et modéliser des phénomènes dynamiques.
>
> Formules clés:
> - \( f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} \)
> - \( (uv)' = u'v + uv' \)
> - \( (f \circ g)' = (f' \circ g) \cdot g' \)
>
> Ce qu'il faut retenir:
> - La dérivée capture l'idée de changement instantané
> - Elle permet de trouver les extrema des fonctions
> - Elle est liée à l'intégrale par le théorème fondamental de l'analyse

#Fonction/Analyse #{CalculDifferentiel} #{Optimisation}