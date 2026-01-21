```tikz
\begin{document}
\begin{tikzpicture}[scale=1.9]
 \draw[color=red, domain=0:10, samples=200, color=gray] ;
 \draw[very thin, color=gray] (0,-1.5) grid (10,1.5);
 \draw[->] (-0.2,0) -- (10.5,0) node[right] {$x$};
 \draw[->] (0,-1.7) -- (0,1.7) node[above] {$y$};
 
 \draw[color=red, domain=0:9, samples=100] plot (\x,{cos(\x r)}) node[right] {$\cos(x)$};
\end{tikzpicture}
\end{document}
```

## Définitions et Caractérisations

### 1. Définition Géométrique (Triangle Rectangle)

Dans un triangle rectangle, le **cosinus** d'un angle aigu $\hat{A}$ est défini comme le **rapport** de la longueur du côté **adjacent** sur la longueur de l'**hypoténuse** :

$$\mathbf{\cos(\hat{A}) = \frac{\text{Côté adjacent}}{\text{Hypoténuse}}}$$

Ce rapport est constant pour tous les triangles rectangles ayant le même angle $\hat{A}$.
```tikz
\begin{document}
\begin{tikzpicture}[scale=2]
 % Triangle rectangle
 \draw[very thick] (0,0) -- (3,0) -- (3,2) -- cycle;
 
 % Angle droit
 \draw (3,0) -- (2.8,0) -- (2.8,0.2) -- (3,0.2);
 
 % Arc pour l'angle (en rouge)
 \draw[very thick, red] (0.6,0) arc (0:33.7:0.6);
 \node[red] at (0.8,0.15) {$\theta$};
 
 % Labels
 \node[below] at (1.5,0) {adjacent};
 \node[right] at (3,1) {oppose};
 \node[above left] at (1.5,1.2) {hypotenuse};
 
 % Formule
 \node[below] at (1.5,-0.5) {$\cos(\theta) = \frac{adjacent}{hypotenuse}$};
\end{tikzpicture}
\end{document}
```
### 2. Définition Analytique (Cercle Unité)

Le plan euclidien étant rapporté à un repère $(Oxy)$, sur le **cercle trigonométrique** (cercle de rayon 1 centré à l'origine), le $\mathbf{\cos(\theta)}$ est défini comme l'**abscisse** du point $M$ associé à l'angle orienté de mesure $\theta$.
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
### 3. Définition par Séries Entières

La fonction cosinus peut être définie par la **série entière** qui converge pour tout réel $x$ :

$$\mathbf{\cos(x) = \sum_{n=0}^{+\infty} \frac{(-1)^n}{(2n)!} x^{2n} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \dots}$$

Cette définition est équivalente à la formule d'Euler :

$$\mathbf{\cos(x) = \frac{\mathrm{e}^{ix} + \mathrm{e}^{-ix}}{2}}$$

---

## Propriétés et Caractéristiques

La fonction cosinus est dérivable sur l'ensemble des réels $\mathbb{R}$.

|**Caractéristique**|**Valeur / Propriété**|**Conséquence**|
|---|---|---|
|**Ensemble de Définition**|$\mathbb{R}$||
|**Ensemble Image**|$[-1; 1]$||
|**Parité**|**Paire** : $\cos(-x) = \cos(x)$|Symétrie par rapport à l'axe des ordonnées.|
|**Périodicité**|$2\pi$-périodique : $\cos(x + 2\pi) = \cos(x)$|Modélise les phénomènes ondulatoires.|
|**Relation avec $\sin$**|$\cos(x) = \sin\left(\frac{\pi}{2} - x\right)$|(Le cosinus est le sinus du complémentaire).|
|**Valeur en zéro**|$\cos(0) = 1$||
|**Zéros (Racines)**|$\frac{\pi}{2} + k\pi \quad \text{avec } k \in \mathbb{Z}$||

---

### 1. Dérivée

La **dérivée** de la fonction cosinus est l'**opposée de la fonction sinus** :

| **Fonction** | **Dérivée** | **Primitive** |
| ------------------ | ------------------- | ------------------------ |
| $\mathbf{\cos(x)}$ | $\mathbf{-\sin(x)}$ | $$\mathbf{\sin(x) + C}$$ |

### 3. Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable (l'argument du cosinus), on applique la règle de la chaîne :

|**Fonction Composée**|**Dérivée**|
|---|---|
|$\mathbf{\cos(u)}$|$\mathbf{-\sin(u) \cdot u'}$|

Exemple : Si $f(x) = \cos(\sqrt{x})$, alors $u = \sqrt{x}$ et $u' = \frac{1}{2\sqrt{x}}$.

$$f'(x) = -\sin(\sqrt{x}) \cdot \frac{1}{2\sqrt{x}} = -\frac{\sin(\sqrt{x})}{2\sqrt{x}}$$

---

### Réciproque : Arc Cosinus

La fonction cosinus étant périodique, elle n'est pas injective sur $\mathbb{R}$. Pour définir une fonction réciproque, on la **restreint** à l'intervalle $\mathbf{[0; \pi]}$, sur lequel elle est bijective.

La fonction réciproque est l'arc cosinus, notée $\arccos$ :

$$\arccos : [-1, 1] \to [0, \pi]$$

Elle vérifie : $\forall x \in [-1, 1], \quad \cos(\arccos(x)) = x$

---
> [!infobox] ![[Pasted image 20251208172350.png]]

#Fonction/Cosinus #Fonction/Sinus 

