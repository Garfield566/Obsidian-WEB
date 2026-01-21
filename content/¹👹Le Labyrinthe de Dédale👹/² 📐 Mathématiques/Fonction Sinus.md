```tikz
\begin{document}
\begin{tikzpicture}[scale=1.9]
 \draw[color=red, domain=0:10, samples=200, color=gray] ;
 \draw[very thin, color=gray] (0,-1.5) grid (10,1.5);
 \draw[->] (-0.2,0) -- (10.5,0) node[right] {$x$};
 \draw[->] (0,-1.7) -- (0,1.7) node[above] {$y$};
 
 
 \draw[color=blue, domain=0:8, samples=100] plot (\x,{sin(\x r)}) node[right] {$\sin(x)$};
\end{tikzpicture}
\end{document}
```

## Définitions et Caractérisations

### 1. Définition Géométrique (Triangle Rectangle)

Dans un triangle rectangle, le **sinus** d'un angle aigu $\hat{A}$ est défini comme le **rapport** de la longueur du côté **opposé** sur la longueur de l'**hypoténuse** :
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
 \node[right, blue] at (3,1) {oppose};
 \node[above left] at (1.5,1.2) {hypotenuse};
 
 % Mise en évidence du côté opposé (pour sin)
 \draw[very thick, blue] (3,0) -- (3,2);
 
 % Formule
 \node[below, blue] at (1.5,-0.5) {$\sin(\theta) = \frac{oppose}{hypotenuse}$};
\end{tikzpicture}
\end{document}
```
### 2. Définition Analytique (Cercle Unité)

Sur le **cercle trigonométrique** (cercle de rayon 1 centré à l'origine), le $\mathbf{\sin(\omega)}$ est défini comme l'**ordonnée** du point $M$ associé à l'angle orienté de mesure $\omega$.

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

La fonction sinus peut être définie par la **série entière** qui converge pour tout réel $x$ :

$$\mathbf{\sin(x) = \sum_{n=0}^{+\infty} \frac{(-1)^n}{(2n+1)!} x^{2n+1} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \dots}$$

Cette définition est également liée à la formule d'Euler :

$$\mathbf{\sin(x) = \frac{\mathrm{e}^{ix} - \mathrm{e}^{-ix}}{2i}}$$

---

### Propriétés et Caractéristiques

La fonction sinus est dérivable sur l'ensemble des réels $\mathbb{R}$.

|**Caractéristique**|**Valeur / Propriété**|**Conséquence**|
|---|---|---|
|**Ensemble de Définition**|$\mathbb{R}$||
|**Ensemble Image**|$[-1; 1]$||
|**Parité**|**Impaire** : $\sin(-x) = -\sin(x)$|Symétrie par rapport à l'origine.|
|**Périodicité**|$2\pi$-périodique : $\sin(x + 2\pi) = \sin(x)$|Modélisation des ondes.|
|**Relation avec $\cos$**|$\sin(x) = \cos\left(x - \frac{\pi}{2}\right)$|(Le sinus est le cosinus décalé).|
|**Valeur en zéro**|$\sin(0) = 0$||
|**Zéros (Racines)**|$k\pi \quad \text{avec } k \in \mathbb{Z}$||

### Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable (l'argument du sinus), on applique la règle de la chaîne :

| **Fonction** | **Dérivée** | **Primitive** |
| ------------------ | ------------------ | ------------------------- |
| $\mathbf{\sin(x)}$ | $\mathbf{\cos(x)}$ | $$\mathbf{-\cos(x) + C}$$ |

|**Fonction Composée**|**Dérivée**|
|---|---|
|$\mathbf{\sin(u)}$|$\mathbf{\cos(u) \cdot u'}$|

**Exemple :** Si $f(x) = \sin(\mathrm{e}^{x^2})$.

- $u(x) = \mathrm{e}^{x^2}$
 
- $u'(x) = 2x\mathrm{e}^{x^2}$
 
 $$f'(x) = \cos(\mathrm{e}^{x^2}) \cdot (2x\mathrm{e}^{x^2}) = 2x\mathrm{e}^{x^2} \cos(\mathrm{e}^{x^2})$$
 

---

### Réciproque : Arc Sinus

La fonction sinus est non injective sur $\mathbb{R}$. Pour définir une réciproque, on la **restreint** à l'intervalle $\mathbf{[-\frac{\pi}{2}; \frac{\pi}{2}]}$, sur lequel elle est bijective.

La fonction réciproque est l'arc sinus, notée $\arcsin$ :

$$\arcsin : [-1, 1] \to \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$$

Elle vérifie : $\forall x \in [-1, 1], \quad \sin(\arcsin(x)) = x$
> [!infobox] ![[Pasted image 20251208172350.png]]

#Fonction/Cosinus #Fonction/Sinus 