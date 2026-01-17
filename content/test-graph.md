# GRAPHIQUES TIKZ À TESTER DANS OBSIDIAN

  

Copiez les blocs ````tikz` dans Obsidian pour les tester.

  

---

  

## SECTION 1: POLYNÔMES

  

### 1.1 - Fonction linéaire x

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {x};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 1.2 - Fonction quadratique x²

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {x^2};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 1.3 - Fonction cubique x³

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {x^3};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 1.4 - Polynôme degré 5 (x⁵)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {x^5};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 1.5 - Polynôme avec gros coefficient (100x²)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-1:1,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {100*x^2};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 2: FONCTIONS TRIGONOMÉTRIQUES

  

### 2.1 - Sinus simple sin(x)

  

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

\addplot[blue, thick] {sin(x r)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 2.2 - Cosinus simple cos(x)

  

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

\addplot[blue, thick] {cos(x r)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 2.3 - Tangente tan(x)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-1.4:1.4,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {tan(x r)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 2.4 - Sinus haute fréquence sin(5x)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-1.2566359999999999:1.2566359999999999,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {sin(5*x r)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 3: FONCTIONS EXPONENTIELLES

  

### 3.1 - Exponentielle simple e^x

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-3:3,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {exp(x)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 3.2 - Exponentielle décroissante e^(-x)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-3:3,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {exp(-x)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 4: FONCTIONS LOGARITHMIQUES

  

### 4.1 - Logarithme népérien ln(x)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=0.1:10,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {ln(x)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 5: FRACTIONS RATIONNELLES

  

### 5.1 - Inverse 1/x

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {1/x};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 5.2 - Inverse carré 1/x²

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {1/(x^2)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 5.3 - Fraction rationnelle x/(x²+1)

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=-5:5,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {x/(x^2+1)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 6: RACINES

  

### 6.1 - Racine carrée √x

  

```tikz

\usepackage{pgfplots}

\pgfplotsset{compat=1.16}

  

\begin{document}

\begin{tikzpicture}

\begin{axis}[

    axis lines=middle,

    grid=both,

    domain=0:10,

    samples=200,

    xlabel={$x$},

    ylabel={$f(x)$},

    width=10cm,

    height=8cm

]

\addplot[blue, thick] {sqrt(x)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  

## SECTION 7: SURFACES 3D

  

### 7.1 - Paraboloïde x² + y²

  

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

    width=12cm,

    height=10cm,

    xmin=-5, xmax=5,

    ymin=-5, ymax=5,

    zmin=-5, zmax=55

]

\addplot3[

    surf,

    samples=18,

    domain=-5:5,

    y domain=-5:5

] {x^2+y^2};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 7.2 - Selle x² - y²

  

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

    width=12cm,

    height=10cm,

    xmin=-5, xmax=5,

    ymin=-5, ymax=5,

    zmin=-30, zmax=30

]

\addplot3[

    surf,

    samples=18,

    domain=-5:5,

    y domain=-5:5

] {x^2-y^2};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 7.3 - Cône √(x² + y²)

  

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

    width=12cm,

    height=10cm,

    xmin=-5, xmax=5,

    ymin=-5, ymax=5,

    zmin=0, zmax=8

]

\addplot3[

    surf,

    samples=18,

    domain=-5:5,

    y domain=-5:5

] {sqrt(x^2+y^2)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 7.4 - Surface cubique x³ + y³
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
    width=12cm,
    height=10cm,
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=-60, zmax=60
]
\addplot3[
    mesh,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```
  

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
    xmin=-2, xmax=2,
    ymin=-2, ymax=2,
    zmin=-16, zmax=16
]
\addplot3[
    surf,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```

  
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
    xmin=-2, xmax=2,
    ymin=-2, ymax=2,
    zmin=-16, zmax=16
]
\addplot3[
    surf,
    samples=15,
    domain=-2:2,
    y domain=-2:2
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```
### 7.5 - Surface trigonométrique sin(x) + cos(y)

  

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

    width=12cm,

    height=10cm,

    xmin=-3, xmax=3,

    ymin=-3, ymax=3,

    zmin=-2.5, zmax=2.5

]

\addplot3[

    surf,

    samples=18,

    domain=-3:3,

    y domain=-3:3

] {sin(x r)+cos(y r)};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 7.6 - Selle hyperbolique xy

  

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

    width=12cm,

    height=10cm,

    xmin=-5, xmax=5,

    ymin=-5, ymax=5,

    zmin=-25, zmax=25

]

\addplot3[

    surf,

    samples=10,

    domain=-5:5,

    y domain=-5:5

] {x*y};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

### 7.7 - Surface degré 5 (x⁵ + y⁵)

  

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

    height=10cm,

    xmin=-2, xmax=2,

    ymin=-2, ymax=2,

    zmin=-60, zmax=70

]

\addplot3[

    surf,

    samples=18,

    domain=-2:2,

    y domain=-2:2

] {x^5+y^5};

\end{axis}

\end{tikzpicture}

\end{document}

```

  

---

  
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
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=-60, zmax=60
]
\addplot3[
    mesh,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```


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
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=-60, zmax=60
]
\addplot3[
    surf,
    samples=25,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```


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
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=-60, zmax=60
]
\addplot3[
    surf,
    faceted color=black,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```

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
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=-60, zmax=60
]
\addplot3[
    surf,
    opacity=0.8,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};

\addplot3[
    mesh,
    draw=black,
    samples=18,
    domain=-3:3,
    y domain=-3:3
] {x^3+y^3};
\end{axis}
\end{tikzpicture}
\end{document}
```


```tikz
```
## RÉSUMÉ

  

**20 graphiques** prêts à tester couvrant:

  

✅ **Polynômes** (5 graphiques) - degré 1 à 5, avec coefficients variés

✅ **Trigonométrie** (4 graphiques) - sin, cos, tan, haute fréquence

✅ **Exponentielles** (2 graphiques) - croissance et décroissance

✅ **Logarithmes** (1 graphique) - ln(x) avec domaine positif

✅ **Fractions** (3 graphiques) - 1/x, 1/x², rationnelles

✅ **Racines** (1 graphique) - √x avec domaine positif

✅ **Surfaces 3D** (7 graphiques) - paraboloïde, selle, cône, etc.

  

**Tous les graphiques ont:**

- ✅ Domaines adaptatifs intelligents

- ✅ Limites X, Y, Z définies pour les 3D

- ✅ Format compatible Obsidian (TikZJax)

- ✅ Taille adaptée pour documents