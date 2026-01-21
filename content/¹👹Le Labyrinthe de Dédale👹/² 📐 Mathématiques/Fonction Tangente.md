```tikz
\begin{document}
\begin{tikzpicture}[scale=0.6]
 \draw[very thin,color=gray] (-1,-4) grid (7,4);
 \draw[->] (-1,0) -- (7.2,0) node[right] {$x$};
 \draw[->] (0,-4.2) -- (0,4.5) node[above] {$y$};
 
 \draw[color=red, domain=0:1.4, samples=100] plot (\x,{tan(\x r)});
 \draw[color=red, domain=1.7:3, samples=100] plot (\x,{tan(\x r)});
 \draw[color=red, domain=3.3:4.5, samples=100] plot (\x,{tan(\x r)});
 \draw[color=red, domain=4.9:6.1, samples=100] plot (\x,{tan(\x r)});
 
 \node[red] at (6.5,3) {$\tan(x)$};
 
 \draw[dashed] (1.57,-4) -- (1.57,4);
 \draw[dashed] (4.71,-4) -- (4.71,4);
\end{tikzpicture}
\end{document}
```

## Définitions et Caractérisations

### 1. Définition Algébrique

La fonction tangente, notée **$\tan$**, est définie comme le **rapport** de la fonction sinus sur la fonction cosinus :

```tikz
\begin{document}
\begin{tikzpicture}[scale=2]
 % Triangle rectangle
 \draw[very thick] (0,0) -- (3,0) -- (3,2) -- cycle;
 
 % Angle droit
 \draw (3,0) -- (2.8,0) -- (2.8,0.2) -- (3,0.2);
 
 % Arc pour l'angle
 \draw[very thick, red] (0.6,0) arc (0:33.7:0.6);
 \node[red] at (0.8,0.15) {$\theta$};
 
 % Labels avec couleurs
 \node[below, green!60!black] at (1.5,0) {adjacent};
 \node[right, blue] at (3,1) {oppose};
 \node[above left] at (1.5,1.2) {hypotenuse};
 
 % Formule
 \node[below] at (1.5,-0.5) {$\tan(\theta) = \frac{oppose}{adjacent}$};
\end{tikzpicture}
\end{document}
```
$$\mathbf{\tan(x) = \frac{\sin(x)}{\cos(x)}}$$

### 2. Définition Analytique (Cercle Unité)

Sur le cercle trigonométrique, $\tan(x)$ est la longueur du segment tangent au cercle en $(1, 0)$, intercepté par le prolongement du rayon de l'angle $x$. 

```tikz
\begin{document}
\begin{tikzpicture}[domain=0:360, scale=2]
 % Cercle avec plot
 \draw[thick, samples=100] plot ({cos(\x)}, {sin(\x)});
 
 % Axes
 \draw[->] (-1.3,0) -- (1.5,0) node[right] {$x$};
 \draw[->] (0,-1.3) -- (0,1.5) node[above] {$y$};
 
 % Tangente verticale en x=1
 \draw[very thick, purple] (1,-1) -- (1,1.3);
 
 % Rayon a 45 degres
 \draw[thick, blue] (0,0) -- (0.707,0.707);
 
 % Prolongement du rayon
 \draw[thick, blue, dashed] (0.707,0.707) -- (1,1);
 
 % Segment tangente
 \draw[very thick, orange] (1,0) -- (1,1);
 \node[orange, right] at (1.2,0.5) {$\tan(45)=1$};
 
 \node[below] at (1,0) {$1$};
\end{tikzpicture}
\end{document}
```

---

### Propriétés et Caractéristiques

La fonction tangente est dérivable sur son domaine de définition.

| Caractéristique | Valeur / Propriété | Conséquence |
| :--- | :--- | :--- |
| **Ensemble de Définition** | $\mathbb{R} \setminus \left\{ \frac{\pi}{2} + k\pi, k \in \mathbb{Z} \right\}$ | Non définie là où $\cos(x)=0$. |
| **Ensemble Image** | $\mathbb{R}$ (Toutes les valeurs réelles) | |
| **Parité** | **Impaire** : $\tan(-x) = -\tan(x)$ | Symétrie par rapport à l'origine. |
| **Périodicité** | $\mathbf{\pi}$-périodique : $\tan(x + \pi) = \tan(x)$ | Sa période est moitié celle du sinus et du cosinus. |
| **Valeur en zéro** | $\tan(0) = 0$ | |
| **Zéros (Racines)** | $k\pi \quad \text{avec } k \in \mathbb{Z}$ | Même que $\sin(x)$. |

---

### Dérivée

La **dérivée** de la fonction tangente peut être exprimée sous deux formes équivalentes :

| **Fonction** | **Dérivée** | **Primitive** |
| :----------------- | :--------------------------------------------------------- | ---------------------------------- |
| $\mathbf{\tan(x)}$ | $\mathbf{1 + \tan^2(x)}$ ou $\mathbf{\frac{1}{\cos^2(x)}}$ | $$\mathbf{-\ln(\|\cos(x)\|) + C}$$ |

*Démonstration (par la règle du quotient) :*
$$(\tan(x))' = \left(\frac{\sin(x)}{\cos(x)}\right)' = \frac{(\cos(x))(\cos(x)) - (\sin(x))(-\sin(x))}{\cos^2(x)}$$
$$(\tan(x))' = \frac{\cos^2(x) + \sin^2(x)}{\cos^2(x)} = \frac{1}{\cos^2(x)}$$

### 3. Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable (l'argument de la tangente), et si $\cos(u(x)) \ne 0$, on a :

| **Fonction Composée** | **Dérivée** |
| :--- | :--- |
| $\mathbf{\tan(u)}$ | $\mathbf{(1 + \tan^2(u)) \cdot u'}$ ou $\mathbf{\frac{u'}{\cos^2(u)}}$ |

**Exemple :** Si $f(x) = \tan(x^2 + 1)$.
* $u(x) = x^2 + 1$
* $u'(x) = 2x$
$$f'(x) = 2x \cdot \left(1 + \tan^2(x^2 + 1)\right)$$

---
