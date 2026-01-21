================================================================================
📐 TRIANGLES QUELCONQUES CORRIGÉS
================================================================================

✅ Corrections appliquées:
 1. Échelle adaptative (petits triangles pour grandes dimensions)
 2. Angles affichés avec valeurs en degrés (α = 53.1°, β = 36.9°, etc.)

================================================================================
1️⃣ Triangle 3-4-5 (Rectangle Classique)
================================================================================
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=1.5]
 % Triangle
 \draw[very thick] (0,0) -- (5,0) -- (3.20,2.40) -- cycle;

 % Points
 \fill (0,0) circle (0.05);
 \fill (5,0) circle (0.05);
 \fill (3.20,2.40) circle (0.05);

 % Labels des sommets
 \node[below left] at (0,0) {$A$};
 \node[below right] at (5,0) {$B$};
 \node[above] at (3.20,2.40) {$C$};

 % Labels des côtés
 \node[below] at (2.5,0) {$c = 5$};
 \node[left] at (1.60,1.20) {$b = 4$};
 \node[right] at (4.10,1.20) {$a = 3$};

 % Angles avec valeurs en degrés
 \node[red, right, fill=white] at (0.5,0.2) {$\alpha = 36.9^\circ$};
 \node[red, left, fill=white] at (4.5,0.2) {$\beta = 53.1^\circ$};
 \node[red, below, fill=white] at (3.20,2.00) {$\gamma = 90.0^\circ$};
\end{tikzpicture}
\end{document}
```

================================================================================
2️⃣ Triangle 5-12-13 (Triplet Pythagoricien - GRAND)
================================================================================
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=0.5]
 % Triangle
 \draw[very thick] (0,0) -- (13,0) -- (11.08,4.62) -- cycle;

 % Points
 \fill (0,0) circle (0.05);
 \fill (13,0) circle (0.05);
 \fill (11.08,4.62) circle (0.05);

 % Labels des sommets
 \node[below left] at (0,0) {$A$};
 \node[below right] at (13,0) {$B$};
 \node[above] at (11.08,4.62) {$C$};

 % Labels des côtés
 \node[below] at (6.5,0) {$c = 13$};
 \node[left] at (5.54,2.31) {$b = 12$};
 \node[right] at (12.04,2.31) {$a = 5$};

 % Angles avec valeurs en degrés
 \node[red, right, fill=white] at (0.5,0.2) {$\alpha = 22.6^\circ$};
 \node[red, left, fill=white] at (12.5,0.2) {$\beta = 67.4^\circ$};
 \node[red, below, fill=white] at (11.08,4.22) {$\gamma = 90.0^\circ$};
\end{tikzpicture}
\end{document}
```

================================================================================
3️⃣ Triangle 8-15-17 (Triplet Pythagoricien - TRÈS GRAND)
================================================================================
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=0.5]
 % Triangle
 \draw[very thick] (0,0) -- (17,0) -- (13.24,7.06) -- cycle;

 % Points
 \fill (0,0) circle (0.05);
 \fill (17,0) circle (0.05);
 \fill (13.24,7.06) circle (0.05);

 % Labels des sommets
 \node[below left] at (0,0) {$A$};
 \node[below right] at (17,0) {$B$};
 \node[above] at (13.24,7.06) {$C$};

 % Labels des côtés
 \node[below] at (8.5,0) {$c = 17$};
 \node[left] at (6.62,3.53) {$b = 15$};
 \node[right] at (15.12,3.53) {$a = 8$};

 % Angles avec valeurs en degrés
 \node[red, right, fill=white] at (0.5,0.2) {$\alpha = 28.1^\circ$};
 \node[red, left, fill=white] at (16.5,0.2) {$\beta = 61.9^\circ$};
 \node[red, below, fill=white] at (13.24,6.66) {$\gamma = 90.0^\circ$};
\end{tikzpicture}
\end{document}
```

================================================================================
4️⃣ Triangle 7-8-9 (Quelconque)
================================================================================
```tikz
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=0.8]
 % Triangle
 \draw[very thick] (0,0) -- (9,0) -- (5.33,5.96) -- cycle;

 % Points
 \fill (0,0) circle (0.05);
 \fill (9,0) circle (0.05);
 \fill (5.33,5.96) circle (0.05);

 % Labels des sommets
 \node[below left] at (0,0) {$A$};
 \node[below right] at (9,0) {$B$};
 \node[above] at (5.33,5.96) {$C$};

 % Labels des côtés
 \node[below] at (4.5,0) {$c = 9$};
 \node[left] at (2.67,2.98) {$b = 8$};
 \node[right] at (7.17,2.98) {$a = 7$};

 % Angles avec valeurs en degrés
 \node[red, right, fill=white] at (0.5,0.2) {$\alpha = 48.2^\circ$};
 \node[red, left, fill=white] at (8.5,0.2) {$\beta = 58.4^\circ$};
 \node[red, below, fill=white] at (5.33,5.56) {$\gamma = 73.4^\circ$};
\end{tikzpicture}
\end{document}
```

#premier-geurre-mondial 