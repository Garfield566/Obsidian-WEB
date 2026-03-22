\section*{Structure d'espace vectoriel}

On appelle espace vectoriel sur $\mathbb{K}$ (ou $\mathbb{K}$-espace vectoriel) un ensemble $E$ muni de deux lois :

\begin{itemize}
\item une loi interne, notée $+$, telle que $(E,+)$ soit un groupe commutatif. L'élément nul est noté $0_E$.
\item une loi externe, notée $\cdot$, qui est une application de $\mathbb{K} \times E$ dans $E$ vérifiant :
\end{itemize}

\[
\forall (\alpha,\beta) \in \mathbb{K}^2,\ \forall x \in E,\quad (\alpha + \beta)\cdot x = \alpha \cdot x + \beta \cdot x
\]

\[
\forall \alpha \in \mathbb{K},\ \forall (x,y) \in E^2,\quad \alpha \cdot (x + y) = \alpha \cdot x + \alpha \cdot y
\]

\[
\forall (\alpha,\beta) \in \mathbb{K}^2,\ \forall x \in E,\quad \alpha \cdot (\beta \cdot x) = (\alpha \beta)\cdot x
\]

\[
\forall x \in E,\quad 1 \cdot x = x
\]

Les éléments de $E$ sont appelés des vecteurs et les éléments de $\mathbb{K}$ sont appelés des scalaires.

\medskip

\textbf{Exemples :} $\mathbb{K}^n$, $\mathbb{K}[X]$, $M_{n,p}(\mathbb{K})$ sont des espaces vectoriels.  
Si $A$ est un ensemble, l'ensemble $F(A,\mathbb{K})$ des fonctions de $A$ dans $\mathbb{K}$ est lui aussi un espace vectoriel.  
En particulier, l'ensemble des suites à valeurs réelles (resp. complexes) est un $\mathbb{R}$-espace vectoriel (resp. un $\mathbb{C}$-espace vectoriel).

\medskip

\textbf{Proposition :} Soient $E_1,\dots,E_n$ des $\mathbb{K}$-espaces vectoriels.  
Alors le produit cartésien $E_1 \times \cdots \times E_n$, muni de l'addition
\[
(x_1,\dots,x_n)+(y_1,\dots,y_n) = (x_1+y_1,\dots,x_n+y_n)
\]
et de la multiplication externe
\[
\lambda \cdot (x_1,\dots,x_n) = (\lambda x_1,\dots,\lambda x_n)
\]
est un $\mathbb{K}$-espace vectoriel.

\section*{Famille de vecteurs}

Dans cette partie, $E$ désigne un espace vectoriel sur $\mathbb{K}$.

\medskip

Une combinaison linéaire de la famille finie $(x_1,\dots,x_n)$ est un vecteur $x \in E$ s'écrivant
\[
x = \sum_{i=1}^{n} \alpha_i x_i
\]
où les $\alpha_i \in \mathbb{K}$.

Une combinaison linéaire d'une famille $(x_i)_{i \in I}$ est un vecteur
\[
x = \sum_{i \in I} \alpha_i x_i
\]
où tous les $\alpha_i$, sauf un nombre fini, sont nuls.

\medskip

Une famille finie $(x_1,\dots,x_n)$ est libre si
\[
\sum_{i=1}^{n} \alpha_i x_i = 0 \;\Rightarrow\; \forall i \in \{1,\dots,n\},\ \alpha_i = 0.
\]

Une famille quelconque est libre si toute sous-famille finie extraite est libre.

Une famille qui n'est pas libre est dite liée.

\medskip

\textbf{Exemple :} Soit $(P_1,\dots,P_n)$ dans $\mathbb{K}[X]$ avec
\[
\deg(P_1) < \deg(P_2) < \cdots < \deg(P_n).
\]
Alors la famille est libre.

\medskip

Une famille $(x_i)_{i \in I}$ est génératrice de $E$ si
\[
\forall x \in E,\quad x = \sum_{i \in I} \alpha_i x_i.
\]

\medskip

\textbf{Propriétés :} Soient $X \subset Y$ deux familles :

\begin{itemize}
\item si $Y$ est libre, alors $X$ est libre ;
\item si $X$ est génératrice, alors $Y$ est génératrice ;
\item si $X$ est génératrice et $x \in X$ combinaison des autres, alors $X \setminus \{x\}$ est génératrice ;
\item si $X$ est libre et $x \notin \mathrm{Vect}(X)$, alors $X \cup \{x\}$ est libre.
\end{itemize}

\section*{Sous-espaces vectoriels}

Une partie $F$ de $E$ est un sous-espace vectoriel si $F$ est non vide et stable par $+$ et $\cdot$.

\medskip

\textbf{Caractérisation :}

\[
0_E \in F
\]
\[
x,y \in F \Rightarrow x+y \in F
\]
\[
\lambda \in \mathbb{K},\ x \in F \Rightarrow \lambda x \in F
\]

\medskip

\textbf{Exemples :}

\begin{itemize}
\item $\{0\}$ est un sous-espace ;
\item droites vectorielles de $\mathbb{R}^2$ ;
\item plans de $\mathbb{R}^3$ ;
\item $\mathbb{K}_n[X]$ ;
\item matrices symétriques de $M_n(\mathbb{K})$.
\end{itemize}

\medskip

\textbf{Proposition :} L'ensemble des solutions d'un système homogène est un sous-espace de $\mathbb{R}^n$.

\medskip

\textbf{Proposition :} L'intersection de deux sous-espaces est un sous-espace vectoriel.

\medskip

\textbf{Définition :} $\mathrm{Vect}(X)$ est le plus petit sous-espace contenant $X$.

Si $X = \{x_1,\dots,x_n\}$ :
\[
\mathrm{Vect}(x_1,\dots,x_n)
= \left\{ \sum_{i=1}^{n} \alpha_i x_i \mid \alpha_i \in \mathbb{K} \right\}.
\]

\section*{Somme de sous-espaces}

\[
F+G = \{x+y \mid x \in F,\ y \in G\}
\]

\[
F \oplus G \iff F \cap G = \{0\}
\]

\section*{Applications linéaires}

\[
f(\lambda x + \mu y) = \lambda f(x) + \mu f(y)
\]

\[
\ker(f) = \{x \in E \mid f(x)=0\}
\]

\[
\mathrm{Im}(f) = \{f(x) \mid x \in E\}
\]

\[
f \text{ injective } \iff \ker(f) = \{0\}
\]

\section*{Projections et symétries}


\[
p(z) = x \quad \text{avec } z = x+y
\]

\[
p \circ p = p
\]

\[
s(z) = x - y
\]

\[
s \circ s = \mathrm{Id}
\]