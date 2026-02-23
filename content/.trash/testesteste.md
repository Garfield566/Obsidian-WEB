================================================================================
🧮 ÉQUATION TRIGONOMÉTRIQUE SUR [0, 4π]
================================================================================

📝 Problème: Résoudre sin(θ) = √2/2 pour θ ∈ [0, 4π] (2 tours complets)

💡 Solution mathématique:
 sin(θ) = √2/2

 Sur [0, 2π], les solutions sont:
 • θ₁ = 45° = π/4 rad
 • θ₂ = 135° = 3π/4 rad

 Sur [2π, 4π] (2ème tour), on ajoute 2π = 360°:
 • θ₃ = 405° = 45° + 360° = 9π/4 rad
 • θ₄ = 495° = 135° + 360° = 11π/4 rad

 TOTAL: 4 solutions sur [0, 4π]

================================================================================
📊 VISUALISATION DES 4 SOLUTIONS
================================================================================

🔵 PREMIER TOUR [0, 2π]:
================================================================================

1️⃣ Solution 1: θ = 45° = π/4
 Description: 1er tour - 1er quadrant
--------------------------------------------------------------------------------
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=5]
 % Axes
 \draw[->] (-1.3,0) -- (1.3,0) node[right] {$x$};
 \draw[->] (0,-1.3) -- (0,1.3) node[above] {$y$};

 % Cercle unitaire
 \draw[thick, black] (0,0) circle (1);

 % Rayon vers le point M
 \draw[very thick, blue] (0,0) -- (0.707,0.707);
 \fill[blue] (0.707,0.707) circle (0.03);
 \node[blue, above right, fill=white] at (0.707,0.707) {$M$};

 % Arc d'angle
 \draw[very thick, red] (0.4,0) arc (0:45:0.4);
 \node[red, fill=white] at (0.46,0.19) {$\theta$};

 % Projections
 \draw[dashed, red] (0.707,0) -- (0.707,0.707);
 \draw[dashed, red] (0,0.707) -- (0.707,0.707);

 % Valeurs cosinus et sinus
 \draw[very thick, green!60!black] (0,0) -- (0.707,0);
 \node[green!60!black, below, fill=white] at (0.354,-0.05) {$\cos(\theta) = \frac{\sqrt{2}}{2}$};

 \draw[very thick, orange] (0,0) -- (0,0.707);
 \node[orange, left, fill=white] at (-0.05,0.354) {$\sin(\theta) = \frac{\sqrt{2}}{2}$};

 % Affichage radian et degré
 \node[above, fill=white] at (0,1.25) {$\theta = \frac{\pi}{4}$ rad $= 45^\circ$};

 % Coordonnées du point M
 \node[below, fill=white] at (0,-1.25) {$M(\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2})$};

 % Graduations
 \node[below left] at (0,0) {$O$};
 \node[below] at (1,0) {$1$};
 \node[left] at (0,1) {$1$};
 \node[below] at (-1,0) {$-1$};
 \node[left] at (0,-1) {$-1$};
\end{tikzpicture}
\end{document}
```

2️⃣ Solution 2: θ = 135° = 3π/4
 Description: 1er tour - 2ème quadrant
--------------------------------------------------------------------------------
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=5]
 % Axes
 \draw[->] (-1.3,0) -- (1.3,0) node[right] {$x$};
 \draw[->] (0,-1.3) -- (0,1.3) node[above] {$y$};

 % Cercle unitaire
 \draw[thick, black] (0,0) circle (1);

 % Rayon vers le point M
 \draw[very thick, blue] (0,0) -- (-0.707,0.707);
 \fill[blue] (-0.707,0.707) circle (0.03);
 \node[blue, above right, fill=white] at (-0.707,0.707) {$M$};

 % Arc d'angle
 \draw[very thick, red] (0.4,0) arc (0:135:0.4);
 \node[red, fill=white] at (0.19,0.46) {$\theta$};

 % Projections
 \draw[dashed, red] (-0.707,0) -- (-0.707,0.707);
 \draw[dashed, red] (0,0.707) -- (-0.707,0.707);

 % Valeurs cosinus et sinus
 \draw[very thick, green!60!black] (0,0) -- (-0.707,0);
 \node[green!60!black, below, fill=white] at (-0.354,-0.05) {$\cos(\theta) = -\frac{\sqrt{2}}{2}$};

 \draw[very thick, orange] (0,0) -- (0,0.707);
 \node[orange, left, fill=white] at (-0.05,0.354) {$\sin(\theta) = \frac{\sqrt{2}}{2}$};

 % Affichage radian et degré
 \node[above, fill=white] at (0,1.25) {$\theta = \frac{3\pi}{4}$ rad $= 135^\circ$};

 % Coordonnées du point M
 \node[below, fill=white] at (0,-1.25) {$M(-\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2})$};

 % Graduations
 \node[below left] at (0,0) {$O$};
 \node[below] at (1,0) {$1$};
 \node[left] at (0,1) {$1$};
 \node[below] at (-1,0) {$-1$};
 \node[left] at (0,-1) {$-1$};
\end{tikzpicture}
\end{document}
```

🟢 DEUXIÈME TOUR [2π, 4π]:
================================================================================

Note: Sur le cercle trigonométrique, les positions sont identiques
car sin(θ + 2π) = sin(θ) (périodicité)

3️⃣ Solution 3: θ = 9π/4 ≡ π/4 (mod 2π)
 Angle équivalent sur [0, 360°]: 45°
 Description: 2ème tour - même position que 45°
--------------------------------------------------------------------------------
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=5]
 % Axes
 \draw[->] (-1.3,0) -- (1.3,0) node[right] {$x$};
 \draw[->] (0,-1.3) -- (0,1.3) node[above] {$y$};

 % Cercle unitaire
 \draw[thick, black] (0,0) circle (1);

 % Rayon vers le point M
