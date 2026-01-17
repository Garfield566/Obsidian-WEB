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


## 💡 Définition et Caractérisation

En mathématiques, la **fonction exponentielle**, notée **$\exp$** ou $\mathbf{x \mapsto \mathrm{e}^x}$, est la fonction unique qui vérifie deux conditions fondamentales :

1. Elle est égale à sa propre dérivée sur $\mathbb{R}$ :

$$\forall x \in \mathbb{R}, \quad \exp'(x) = \exp(x)$$
2. Elle prend la valeur 1 en 0 :

$$\exp(0) = 1$$

---

### Modélisation de la Croissance Exponentielle

La fonction exponentielle est l'outil de modélisation privilégié pour les phénomènes où une **différence constante** sur la variable $x$ conduit à un **rapport constant** sur les images $f(x)$. Ces phénomènes sont caractérisés par une **croissance dite « exponentielle »** (exemples : croissance démographique non limitée, désintégration radioactive, intérêts composés).

On appelle également parfois fonction exponentielle toute fonction dont l'expression est de la forme $f(x)=A\mathrm{e}^{\lambda x}$, où $A$ et $\lambda$ sont des constantes.

### La Base $\mathrm{e}$ et Notation

La valeur de la fonction exponentielle en $x=1$ est un nombre irrationnel noté $\mathbf{\mathrm{e}}$.

- $\mathrm{e} = \exp(1) \approx 2,71828$
    
- Ce nombre est appelé la base de la fonction exponentielle et permet la notation alternative :
    
    $$\forall x \in \mathbb{R}, \quad \exp(x) = \mathrm{e}^x$$
    

---

###  Relations Algébriques et Réciproque

La fonction exponentielle est la seule fonction continue sur $\mathbb{R}$ qui transforme une somme en produit (propriété des puissances) :

$$\exp(a+b) = \exp(a) \cdot \exp(b) \quad \text{ou} \quad \mathrm{e}^{a+b} = \mathrm{e}^a \cdot \mathrm{e}^b$$

C'est une **bijection** de $\mathbb{R}$ vers $\mathbb{R}^{*+}$ (l'ensemble des réels strictement positifs). Sa fonction réciproque est la **fonction logarithme népérien** ($\ln$).

---

###  Applications et Généralisations

Les applications élémentaires des fonctions exponentielles réelles ou complexes concernent notamment :

- La résolution des **équations différentielles** linéaires.
    
- La mise en place de la **théorie de Fourier**.
    

Sa définition permet de l'étendre à des espaces plus complexes (fonctions de $\mathbb{C}$ vers $\mathbb{C}^*$), où elle s'utilise en **géométrie riemannienne**, dans la théorie des **groupes de Lie**, ou encore dans l'étude des **algèbres de Banach**.
#Fonction/Exponentielle #Fonction/Logarithme 
