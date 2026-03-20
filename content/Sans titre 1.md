
```tikz
\begin{document}
\begin{tikzpicture}[domain=0:4]
 \draw[very thin,color=gray] (-0.1,-1.1) grid (3.9,3.9);
 \draw[->] (-0.2,0) -- (4.2,0) node[right] {$x$};
 \draw[->] (0,-1.2) -- (0,4.2) node[above] {$y$};
 \draw[color=red] plot (\x,\x) node[right] {$f(x) =x$};
\end{tikzpicture}
\end{document}
```
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
```tikz
\begin{document}
\begin{tikzpicture}[scale=1.9]
 \draw[very thin, color=gray] (0,-1.5) grid (10,1.5);
 \draw[->] (-0.2,0) -- (10.5,0) node[right] {$x$};
 \draw[->] (0,-1.7) -- (0,1.7) node[above] {$y$};
 
 \draw[color=red, domain=0:9, samples=100] plot (\x,{[FONCTION]}) node[right] {$[NOM]$};
\end{tikzpicture}
\end{document}
```

## 💡 Définition et Caractérisation

#### Def 1
#### Def 2
---

## Propriétés et Caractéristiques

[Tableau synthétique des propriétés]

| **Caractéristique** | **Valeur / Propriété** | **Conséquence** |
|---|---|---|
| **Ensemble de Définition** | $[DOMAINE]$ | |
| **Ensemble Image** | $[IMAGE]$ | |
| **Parité** | [Paire/Impaire/Ni l'un ni l'autre] | [Conséquence géométrique] |
| **Périodicité** | [Valeur ou Non périodique] | |
| **Limites** | [Limites importantes] | |
| **Zéros** | [Valeurs qui annulent] | |

### Dérivée

| **Fonction** | **Dérivée** | **Primitive** |
|---|---|---|
| $\mathbf{[FONCTION]}$ | $\mathbf{[DERIVEE]}$ | $\mathbf{[PRIMITIVE]}$ |

### Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable :

| **Fonction Composée** | **Dérivée** |
|---|---|
| $\mathbf{[f(u)]}$ | $\mathbf{[f'(u) \cdot u']}$ |

[Exemple concret de calcul]

---

## Visualisation
```tikz
\begin{document}
\begin{tikzpicture}[scale=2]
 [GRAPHIQUE DÉTAILLÉ : cercle trigonométrique, représentation géométrique, etc.]
\end{tikzpicture}
\end{document}
```

[Autre graphique TikZ si pertinent - minimum 2 graphiques par note]

---

### Réciproque (si applicable)

[Description de la fonction réciproque]

---

> [!infobox] ![Placeholder pour image Wikipedia]

#Fonction/[Type] #Fonction/[Lié]