---
"-":
---

-----
// Base template GRAPHIQUES 
 
 
```tikz
\begin{document}
 \begin{tikzpicture}[domain=0:4]
 \draw[very thin,color=gray] (-0.1,-1.1) grid (3.9,3.9);
 \draw[->] (-0.2,0) -- (4.2,0) node[right] {$x$};
 \draw[->] (0,-1.2) -- (0,4.2) node[above] {$f(x)$};
 \draw[color=red] plot (\x,\x) node[right] {$f(x) =x$};
 \draw[color=blue] plot (\x,{sin(\x r)}) node[right] {$f(x) = \sin x$};
 \draw[color=orange] plot (\x,{0.05*exp(\x)}) node[right] {$f(x) = \frac{1}{20} \mathrm e^x$};
 \end{tikzpicture}
\end{document}
```
// exemple 2 graphe
```tikz
\begin{document}
\begin{tikzpicture}[domain=0:10, scale=0.6]
 \draw[very thin,color=gray] (-0.5,-0.5) grid (10.5,10.5);
 \draw[->] (-0.5,0) -- (10.5,0) node[right] {$x$};
 \draw[->] (0,-0.5) -- (0,10.5) node[above] {$y$};
 
 \draw[color=red, domain = 0:2, samples=60] plot (\x,{exp(\x)}) node[right] {$f(x) = e^x$};
 \draw[color=blue, domain = 0:2, samples=60] plot (\x,{\x}) node[right] {$f(x) = x$};
\end{tikzpicture}
\end{document}
```
// cercle_trigonometrique
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
// vecteurs-cube
 
```tikz
\usepackage{tikz-cd}

\begin{document}

\begin{tikzcd}[row sep=2.5em]

A' \arrow[rr,"f'"] \arrow[dr,swap,"a"] \arrow[dd,swap,"g'"] &&
  B' \arrow[dd,swap,"h'" near start] \arrow[dr,"b"] \\
& A \arrow[rr,crossing over,"f" near start] &&
  B \arrow[dd,"h"] \\
C' \arrow[rr,"k'" near end] \arrow[dr,swap,"c"] && D' \arrow[dr,swap,"d"] \\
& C \arrow[rr,"k"] \arrow[uu,<-,crossing over,"g" near end]&& D

\end{tikzcd}

\end{document}
```

// geometrie_triangle
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

 
 
// circuit_electrique

```tikz
\usepackage{circuitikz}
\begin{document}

\begin{circuitikz}[american, voltage shift=0.5]
\draw (0,0)
to[isource, l=$I_0$, v=$V_0$] (0,3)
to[short, -*, i=$I_0$] (2,3)
to[R=$R_1$, i>_=$i_1$] (2,0) -- (0,0);
\draw (2,3) -- (4,3)
to[R=$R_2$, i>_=$i_2$]
(4,0) to[short, -*] (2,0);
\end{circuitikz}

\end{document}
```

 
 // graphe 3D
 
```tikz
\usepackage{pgfplots}
\pgfplotsset{compat=1.16}

\begin{document}

\begin{tikzpicture}
\begin{axis}[colormap/viridis]
\addplot3[
	surf,
	samples=18,
	domain=-3:3
]
{exp(-x^2-y^2)*x};
\end{axis}
\end{tikzpicture}

\end{document}
```

