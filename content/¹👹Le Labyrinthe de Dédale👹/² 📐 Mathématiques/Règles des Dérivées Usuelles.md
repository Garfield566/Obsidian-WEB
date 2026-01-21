---
type: Règle
domaine: Analyse
moc_lie: Calcul Différentiel
---
```tikz
\begin{document}
\begin{tikzpicture}[domain=0:10, scale=0.6]
 \draw[very thin,color=gray] (-0.5,-0.5) grid (10.5,10.5);
 \draw[->] (-0.5,0) -- (10.5,0) node[right] {$x$};
 \draw[->] (0,-0.5) -- (0,10.5) node[above] {$y$};
 
 \draw[color=red, domain = 0:5, samples=60] plot (\x,{\x*\x/10}) node[right] {$f(x) = x^2$};
 \draw[color=blue, domain = 0:5, samples=60] plot (\x,{2*\x}) node[right] {$f(x) = 2x$};
\end{tikzpicture}
\end{document}
```
 Présentation
Cette note regroupe les règles de base du calcul différentiel pour les fonctions d'une variable réelle, ainsi que le tableau des dérivées des fonctions usuelles.

## Analyse : Les Règles Opératoires

Soient $u$ et $v$ deux fonctions dérivables sur un intervalle $I$, et $k$ un réel constant. Les règles suivantes permettent de dériver les combinaisons de ces fonctions.

| **Opération** | **Fonction** | **Dérivée** |
| --------------------------------- | ------------------------- | ------------------------ |
| **Somme** | $u + v$ | $u' + v'$ |
| **Produit par Constante** | $k \cdot u$ | $k \cdot u'$ |
| **Produit** | $u \cdot v$ | $u'v + u v'$ |
| **Quotient** | $\frac{u}{v}$ ($v \ne 0$) | $\frac{u'v - u v'}{v^2}$ |
| **Inverse** | $\frac{1}{v}$ ($v \ne 0$) | $-\frac{v'}{v^2}$ |
| **Composée** (Règle de la chaîne) | $g(u(x))$ | $u'(x) \cdot g'(u(x))$ |

## Exemple : Le Tableau des Dérivées Usuelles

Ce tableau liste les dérivées des fonctions élémentaires. Notez que nous utilisons $u$ pour représenter une fonction dérivable (permettant d'appliquer la [[Règle de la Chaîne]]).

|**Fonction f(x)**|**Dérivée f′(x)**|**Fonction Composée f(u)**|**Dérivée f′(u)**|
|---|---|---|---|
|Constante $k$|$0$|||
|$x^n$ ($n \in \mathbb{Z}$)|$n x^{n-1}$|$u^n$|$n u^{n-1} \cdot u'$|
|$\frac{1}{x}$|$-\frac{1}{x^2}$|$\frac{1}{u}$|$-\frac{u'}{u^2}$|
|$\sqrt{x}$ ($x>0$)|$\frac{1}{2\sqrt{x}}$|$\sqrt{u}$ ($u>0$)|$\frac{u'}{2\sqrt{u}}$|
|$\sin(x)$|$\cos(x)$|$\sin(u)$|$\cos(u) \cdot u'$|
|$\cos(x)$|$-\sin(x)$|$\cos(u)$|$-\sin(u) \cdot u'$|
|$\tan(x)$|$1 + \tan^2(x)$ ou $\frac{1}{\cos^2(x)}$|||
|$\mathrm{e}^x$|$\mathrm{e}^x$|$\mathrm{e}^u$|$\mathrm{e}^u \cdot u'$|
|$\ln(x)$ ($x>0$)|$\frac{1}{x}$|$\ln(u)$ ($u>0$)|$\frac{u'}{u}$|

## Applications

### Exemple de Calcul (Produit)

Soit la fonction $f(x) = x^3 \cdot \sin(x)$. On utilise la règle du produit $u'v + u v'$ avec $u=x^3$ et $v=\sin(x)$.

$$f'(x) = (3x^2)(\sin(x)) + (x^3)(\cos(x))$$

$$f'(x) = 3x^2 \sin(x) + x^3 \cos(x)$$

### Exemple de Calcul (Composée)

Soit la fonction $g(x) = \mathrm{e}^{5x+1}$. On utilise la règle de la chaîne avec $u(x) = 5x+1$, donc $u'(x) = 5$.

$$g'(x) = u' \cdot \mathrm{e}^u = 5 \cdot \mathrm{e}^{5x+1}$$

---

Cette note est un **point de convergence** dans votre système. Toutes les autres notes d'exercices ou de théorèmes (comme le [[Théorème des Accroissements Finis]]) pourront facilement créer un lien vers cette page pour citer une règle ou une dérivée usuelle.