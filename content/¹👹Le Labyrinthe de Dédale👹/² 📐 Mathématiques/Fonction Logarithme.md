
```tikz
\begin{document}
\begin{tikzpicture}[domain=0:10, scale=0.6]
  \draw[very thin,color=gray] (-0.5,-0.5) grid (10.5,10.5);
  \draw[->] (-0.5,0) -- (10.5,0) node[right] {$x$};
  \draw[->] (0,-0.5) -- (0,10.5) node[above] {$y$};
  
  \draw[color=red, domain = 0.5:10, samples=60] plot (\x,{ln(\x)}) node[right] {$f(x) = ln(x)$};
  \draw[color=blue, domain = -1:10, samples=60] plot (\x,{\x}) node[right] {$f(x) = x$};
\end{tikzpicture}
\end{document}
```

##  Définition et Caractérisation

La **fonction logarithme népérien**, notée **$\ln$**, est définie sur l'intervalle $\mathbf{]0, +\infty[}$.

Elle est la bijection réciproque de la fonction exponentielle $\exp$. Cela signifie que :

$$\forall x > 0, \quad y = \ln(x) \quad \iff \quad x = \mathrm{e}^y$$

- Le logarithme annule l'exponentielle : $\mathbf{\ln(\mathrm{e}^x) = x}$ (pour tout $x \in \mathbb{R}$)
    
- L'exponentielle annule le logarithme : $\mathbf{\mathrm{e}^{\ln(x)} = x}$ (pour tout $x > 0$)

Elle est caractérisée comme l'unique primitive de la fonction $x \mapsto \frac{1}{x}$ sur $\mathbb{R}^{*+}$ qui s'annule en 1.

$$\forall x > 0, \quad \ln(x) = \int_{1}^{x} \frac{1}{t} dt$$

### 1. Propriétés Algébriques (Primales)

Avant de dériver, il est souvent utile de simplifier l'expression $\ln(x)$ grâce à ses propriétés :

|**Opération**|**Formule**|**Condition**|
|---|---|---|
|**Logarithme d'un Produit**|$\ln(ab) = \ln(a) + \ln(b)$|$a>0, b>0$|
|**Logarithme d'un Quotient**|$\ln\left(\frac{a}{b}\right) = \ln(a) - \ln(b)$|$a>0, b>0$|
|**Logarithme d'une Puissance**|$\ln(a^n) = n \ln(a)$|$a>0, n \in \mathbb{R}$|

### 2. Composée (Règle de la Chaîne)

Si $u(x)$ est une fonction dérivable et **strictement positive** ($u(x) > 0$), on applique la règle de la chaîne.

|**Fonction Composée**|**Dérivée**|**Condition**|
|---|---|---|
|$\mathbf{\ln(u)}$|$\mathbf{\frac{u'}{u}}$|$u(x) > 0$|

**Exemple :** Soit $f(x) = \ln(x^2+5)$.

- $u(x) = x^2+5$ (toujours positif)
    
- $u'(x) = 2x$
    
- $f'(x) = \frac{2x}{x^2+5}$
    
#Fonction/Exponentielle #Fonction/Logarithme 