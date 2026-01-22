---
ccl: menutble
bnner: "![[zzzzz ⚙️ime 1 🖼ime bnquePted ime 20230702214935.pn]]"
---
```tikz
\usepackage{pgfplots}
\pgfplotsset{compat=1.16}

\begin{document}
\begin{tikzpicture}
\begin{axis}[
 axis lines=middle,
 grid=both,
 domain=-6.28:6.28,
 samples=200,
 xlabel={$x$},
 ylabel={$f(x)$},
 width=10cm,
 height=8cm
]
\addplot[blue, thick] {cos(deg(x))};
\end{axis}
\end{tikzpicture}
\end{document}
```

```tikz
\begin{document}
\begin{tikzpicture}[scale=3]
 % Axes
 \draw[->] (-1.3,0) -- (1.3,0) node[right] {$x$};
 \draw[->] (0,-1.3) -- (0,1.3) node[above] {$y$};

 % Cercle
 \draw[thick] (0,0) circle (1);

 % Angle (exemple: 40 degrés)
 \draw[very thick, red] (0.5,0) arc (0:40:0.5);
 \node[red] at (0.6,0.2) {$\theta$};

 % Point sur le cercle
 \draw[thick, blue] (0,0) -- (0.766,0.643);
 \fill[blue] (0.766,0.643) circle (0.03);
 \node[blue, above right] at (0.766,0.643) {$M$};

 % Projection pour cos (ligne verticale rouge)
 \draw[very thick, red, dashed] (0.766,0) -- (0.766,0.643);

 % Projection pour cos (ligne horizontale verte)
 \draw[very thick, green!60!black] (0,0) -- (0.766,0);
 \node[green!60!black, below] at (0.383,0) {$\cos(\theta)$};

 % Projection pour sin
 \draw[thick, orange] (0,0) -- (0,0.643);
 \node[orange, left] at (0,0.32) {$\sin(\theta)$};

 % Graduations
 \node[below left] at (0,0) {$O$};
 \node[below] at (1,0) {$1$};
 \node[left] at (0,1) {$1$};
\end{tikzpicture}
\end{document}
```

## 💡 Définition et Caractérisation

La **fonction cosinus**, notée **$\cos(x)$**, est définie sur l'intervalle $\mathbf{\mathbb{R}}$ (ensemble des nombres réels).

Elle représente la projection sur l'axe des abscisses d'un point $M$ se déplaçant sur le cercle unité de centre $O$ et d'angle $\theta$ avec l'axe des abscisses. Cette fonction est périodique de période $2\pi$ et est une fonction paire, c'est-à-dire qu'elle vérifie $\cos(-x) = \cos(x)$.

$$ \cos(x) = \frac{e^{ix} + e^{-ix}}{2} $$

---
### 📊 Propriétés Fondamentales

| **Caractéristique** | **Valeur / Propriété** | **Conséquence** |
|---|---|---|
| **Ensemble de Définition** | $\mathbb{R}$ | La fonction est définie pour tout nombre réel. |
| **Ensemble Image** | $[-1, 1]$ | La fonction atteint son maximum en 1 et son minimum en -1. |
| **Parité** | Paire | $\cos(-x) = \cos(x)$ |
| **Périodicité** | Oui - période $2\pi$ | $\cos(x + 2\pi) = \cos(x)$ |
| **Continuité** | Oui - partout continue | La fonction ne présente aucune discontinuité. |
| **Dérivabilité** | Oui - partout dérivable | La dérivée est $-\sin(x)$. |
| **Limites** | $\lim_{x \to \infty} \cos(x)$ n'existe pas | La fonction oscille entre -1 et 1. |
| **Zéros/Racines** | $\cos(x) = 0 \iff x = \frac{\pi}{2} + k\pi, k \in \mathbb{Z}$ | Les racines sont situées aux multiples de $\frac{\pi}{2}$. |

---
### 📐 Propriétés Algébriques

| **Opération** | **Formule** | **Condition** |
|---|---|---|
| **Formule d'addition** | $\cos(a + b) = \cos(a)\cos(b) - \sin(a)\sin(b)$ | $a, b \in \mathbb{R}$ |
| **Formule de soustraction** | $\cos(a - b) = \cos(a)\cos(b) + \sin(a)\sin(b)$ | $a, b \in \mathbb{R}$ |
| **Formule de duplication** | $\cos(2x) = 2\cos^2(x) - 1$ | $x \in \mathbb{R}$ |

---
### 🧮 Dérivée et Primitive

#### Dérivée Simple

| **Fonction** | **Dérivée** | **Domaine de dérivabilité** |
|---|---|---|
| $\mathbf{\cos(x)}$ | $\mathbf{-\sin(x)}$ | $\mathbb{R}$ |

#### Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable, on applique la règle de la chaîne :

| **Fonction Composée** | **Dérivée** | **Condition** |
|---|---|---|
| $\mathbf{\cos(u(x))}$ | $\mathbf{-\sin(u(x)) \cdot u'(x)}$ | $u$ dérivable |

**Exemple :** Soit $g(x) = \cos(3x^2)$.

- $u(x) = 3x^2$
- $u'(x) = 6x$
- Donc : $g'(x) = -\sin(3x^2) \cdot 6x = -6x \sin(3x^2)$

#### Primitive

| **Fonction** | **Primitive** | **Domaine** |
|---|---|---|
| $\mathbf{\cos(x)}$ | $\mathbf{\sin(x) + C}$ | $\mathbb{R}$ |

---
### 🔄 Fonction Réciproque

La fonction cosinus n'est pas injective sur $\mathbb{R}$. Pour définir une réciproque, on la **restreint** à l'intervalle $\mathbf{[0, \pi]}$, sur lequel elle est bijective.

La fonction réciproque est **l'arccosinus**, notée $\arccos(x)$ :

$$ \arccos(x) : [-1, 1] \to [0, \pi] $$

Elle vérifie :
$$ \forall x \in [-1, 1], \quad \cos(\arccos(x)) = x $$

**Graphiquement :** Les courbes de $\cos(x)$ et $\arccos(x)$ sont symétriques par rapport à la droite $y = x$.

---
### 🌊 Développements et Séries

#### Série de Taylor/Maclaurin

$$ \cos(x) = \sum_{n=0}^{+\infty} \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \dots $$

Cette série converge pour $x \in \mathbb{R}$.

#### Formule d'Euler

$$ \cos(x) = \frac{e^{ix} + e^{-ix}}{2} $$

---
### 📈 Variations et Représentation Graphique

#### Tableau de Variations

| $x$ | $-\infty$ | | $-\frac{3\pi}{2}$ | | $-\pi$ | | $-\frac{\pi}{2}$ | | $0$ | | $\frac{\pi}{2}$ | | $\pi$ | | $\frac{3\pi}{2}$ | | $+\infty$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\cos'(x)$ | | + | | - | | + | | - | | + | | - | | + | | - | |
| $\cos(x)$ | | 1 | | 0 | | -1 | | 0 | | 1 | | 0 | | -1 | | 0 | | 1 |

#### Points Remarquables

- **Extrema locaux** : $(0, 1)$, $(\pi, -1)$, etc.
- **Points d'inflexion** : $(\frac{\pi}{2}, 0)$, $(\frac{3\pi}{2}, 0)$, etc.
- **Asymptotes** : Aucune asymptote.

---
### 🎯 Applications et Contextes

La fonction cosinus est omniprésente en mathématiques et en physique. Elle permet de modéliser des phénomènes périodiques comme les ondes, les oscillations mécaniques, et les signaux électriques.

**Domaines d'application :**
- **Trigonométrie** : Résolution de triangles, calculs d'angles.
- **Physique ondulatoire** : Description des ondes lumineuses et sonores.
- **Analyse harmonique** : Décomposition de signaux en séries de Fourier.

**Modélisation :** La fonction cosinus permet de modéliser des phénomènes périodiques comme les marées, les oscillations d'un pendule, ou les variations de température saisonnières.

---
### 💡 Remarques et Astuces

> [!tip] Astuce de Calcul
> Pour calculer $\cos(x)$ pour un angle donné, on peut utiliser le cercle trigonométrique et les valeurs remarquables (0, $\frac{\pi}{6}$, $\frac{\pi}{4}$, $\frac{\pi}{3}$, $\frac{\pi}{2}$).

> [!warning] Attention
> La fonction cosinus n'est pas injective sur $\mathbb{R}$, il faut donc la restreindre pour définir une réciproque.

> [!info] Rappel Important
> La fonction cosinus est une fonction paire, ce qui signifie que $\cos(-x) = \cos(x)$.

#Fonction/Trigonométrique #Mathématiques #Analyse