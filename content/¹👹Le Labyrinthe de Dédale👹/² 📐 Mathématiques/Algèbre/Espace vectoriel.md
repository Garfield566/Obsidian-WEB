---
nom: "espace vectoriel"
qid: Q125977
categorie: espace
tags: "#espace"
  - vecteur
image: https://commons.wikimedia.org/wiki/Special:FilePath/Vector_add_scale.svg
---

# Espace vectoriel

> [!Infobox]
> **Espace vectoriel**
> ![image|300](https://commons.wikimedia.org/wiki/Special:FilePath/Vector_add_scale.svg)
> - **Aspect de** : algèbre linéaire



## Structure d'espace vectoriel

 Espace vectoriel
On appelle **espace vectoriel sur $\mathbb{K}$** (ou $\mathbb{K}$-espace vectoriel) un ensemble $E$ muni de deux lois :
  une **loi interne**, notée $+$, telle que $(E, +)$ soit un **groupe commutatif**. L'élément nul est noté $0_E$.
  une **loi externe**, notée $\cdot$, qui est une application de $\mathbb{K} \times E$ dans $E$ vérifiant :
  . $\forall (\alpha, \beta) \in \mathbb{K}^2, \forall x \in E,\ (\alpha + \beta) \cdot x = \alpha \cdot x + \beta \cdot x$.
  1. $\forall \alpha \in \mathbb{K}, \forall (x, y) \in E^2,\ \alpha \cdot (x + y) = \alpha \cdot x + \alpha \cdot y$.
   2. $\forall (\alpha, \beta) \in \mathbb{K}^2, \forall x \in E,\ \alpha \cdot (\beta \cdot x) = (\alpha \beta) \cdot x$.
   3. $\forall x \in E,\ 1 \cdot x = x$.

 Les éléments de $E$ sont appelés des **vecteurs** et les éléments de $\mathbb{K}$ sont appelés des **scalaires**.

 Exemples d'espaces vectoriels
 - $\mathbb{K}^n$, $\mathbb{K}[X]$, $\mathcal{M}_{n,p}(\mathbb{K})$ sont des espaces vectoriels.
 - Si $A$ est un ensemble, l'ensemble $\mathcal{F}(A, \mathbb{K})$ des fonctions de $A$ dans $\mathbb{K}$ est un espace vectoriel.
 - En particulier, l'ensemble des suites à valeurs réelles (resp. à valeurs complexes) est un $\mathbb{R}$-espace vectoriel (resp. un $\mathbb{C}$-espace vectoriel).

> [!proposition] Produit cartésien d'espaces vectoriels
> Soit $E_1, \dots, E_n$ des $\mathbb{K}$-espaces vectoriels. Alors le produit cartésien $E_1 \times \cdots \times E_n$, muni de l'addition
> $$
> (x_1, \dots, x_n) + (y_1, \dots, y_n) = (x_1 + y_1, \dots, x_n + y_n)
> $$
> et de la multiplication externe
> $$
> \lambda \cdot (x_1, \dots, x_n) = (\lambda x_1, \dots, \lambda x_n)
> $$
> est un $\mathbb{K}$-espace vectoriel.

---

## Famille de vecteurs

Dans cette partie, $E$ désigne un espace vectoriel sur $\mathbb{K}$.

> [!definition] Combinaison linéaire
> Une **combinaison linéaire** de la famille finie de vecteurs $(x_1, \dots, x_n)$ de $E$ est un vecteur $x \in E$ s'écrivant $x = \sum_{i=1}^n \alpha_i x_i$ où les $\alpha_i$ sont des éléments de $\mathbb{K}$.
>
> Une combinaison linéaire d'une famille quelconque $(x_i)_{i \in I}$ est un vecteur $x$ s'écrivant $x = \sum_{i \in I} \alpha_i x_i$ où tous les $\alpha_i$, sauf un nombre fini, sont nuls.

> [!definition] Famille libre / Famille liée
> Une famille finie de vecteurs $(x_1, \dots, x_n)$ est **libre** si, pour tout choix de $\alpha_1, \dots, \alpha_n \in \mathbb{K}$,
> $$
> \sum_{i=1}^n \alpha_i x_i = 0 \implies \forall i \in \{1, \dots, n\},\ \alpha_i = 0.
> $$
>
> Une famille quelconque de vecteurs est **libre** si toute sous-famille finie extraite est libre.
>
> Une famille qui n'est pas libre est une famille **liée**.

> [!example] Famille de polynômes à degrés distincts
> Soit $(P_1, \dots, P_n)$ une famille de $\mathbb{K}[X]$ avec $\deg(P_1) < \deg(P_2) < \cdots < \deg(P_n)$. Alors $(P_1, \dots, P_n)$ est une famille libre.

> [!definition] Famille génératrice
> Une famille $(x_i)_{i \in I}$ est **génératrice** de $E$ si tout vecteur de $E$ est combinaison linéaire des $(x_i)_{i \in I}$.

> [!proposition] Propriétés des familles libres et génératrices
> Soit $X$ et $Y$ deux familles de vecteurs de $E$ avec $X \subset Y$.
>
> - Si $Y$ est libre, alors $X$ est libre.
> - Si $X$ est génératrice, alors $Y$ est génératrice.
> - Si $X$ est une famille génératrice, et si $x \in X$ est combinaison linéaire des vecteurs de $X \setminus \{x\}$, alors $X \setminus \{x\}$ est une famille génératrice.
> - Si $X$ est une famille libre, et si $x \in E$ n'est pas combinaison linéaire des vecteurs de $X$, alors $X \cup \{x\}$ est libre.

---

## Sous-espaces vectoriels

Dans cette partie, $E$ désigne un espace vectoriel sur $\mathbb{K}$.

> [!definition] Sous-espace vectoriel
> Une partie $F$ de $E$ est un **sous-espace vectoriel** de $E$ si $F$ est non-vide et si $F$ est stable par $+$ et $\cdot$. Dans ce cas, $F$ est lui-même un espace vectoriel.

> [!proposition] Caractérisation des sous-espaces vectoriels
> Une partie $F$ de $E$ est un sous-espace vectoriel de $E$ si et seulement si les 3 propriétés suivantes sont vérifiées :
> 1. $0_E \in F$.
> 2. Pour tout $(x, y) \in F^2$, $x + y \in F$.
> 3. Pour tout $x \in F$ et tout $\lambda \in \mathbb{K}$, $\lambda \cdot x \in F$.

> [!example] Exemples de sous-espaces vectoriels
> - $\{0\}$ est un sous-espace vectoriel de $E$.
> - Dans $\mathbb{R}^2$, toute droite vectorielle (passant par l'origine) est un sous-espace vectoriel de $\mathbb{R}^2$.
> - Dans $\mathbb{R}^3$, toute droite vectorielle (passant par l'origine), tout plan vectoriel est un sous-espace vectoriel de $\mathbb{R}^3$.
> - Pour $n \ge 0$, l'ensemble $\mathbb{K}_n[X]$ des polynômes de degré au plus $n$ est un sous-espace de $\mathbb{K}[X]$.
> - L'ensemble des matrices symétriques d'ordre $n$ est un sous-espace vectoriel de $\mathcal{M}_n(\mathbb{K})$.

> [!proposition] Solutions d'un système linéaire homogène
> L'ensemble des solutions d'un système linéaire homogène de $p$ équations à $n$ inconnues est un sous-espace vectoriel de $\mathbb{R}^n$.

> [!proposition] Intersection de sous-espaces vectoriels
> L'intersection de deux sous-espaces vectoriels est un sous-espace vectoriel.

> [!definition] Sous-espace engendré
> Si $X$ est une partie de $E$, il existe un sous-espace vectoriel de $E$ contenant $X$ qui est le plus petit possible (pour l'inclusion). On l'appelle le **sous-espace engendré** par $X$ et on le note $\operatorname{vect}(X)$.
>
> Si $X = \{x_1, \dots, x_n\}$, alors $\operatorname{vect}(X)$ est l'ensemble des combinaisons linéaires des vecteurs $x_1, \dots, x_n$ :
> $$
> \operatorname{vect}(x_1, \dots, x_n) = \left\{ \sum_{i=1}^n \alpha_i x_i \ \middle|\ \alpha_i \in \mathbb{K} \right\}.
> $$

> [!proposition] Propriétés du sous-espace engendré
> - Si $X \subset Y$, alors $\operatorname{vect}(X) \subset \operatorname{vect}(Y)$.
> - Si $F$ est un sous-espace vectoriel contenant $X$, alors $\operatorname{vect}(X) \subset F$.
> - L'espace $\operatorname{vect}(u_1, \dots, u_n)$ est inchangé si on ajoute à un des vecteurs $u_i$ une combinaison linéaire des autres vecteurs.
> - $\operatorname{vect}(u_1, \dots, u_n, 0) = \operatorname{vect}(u_1, \dots, u_n)$.
> - Si $u_n$ est combinaison linéaire de $u_1, \dots, u_{n-1}$, alors $\operatorname{vect}(u_1, \dots, u_n) = \operatorname{vect}(u_1, \dots, u_{n-1})$.

> [!proposition] Caractérisation de $\operatorname{vect}(X) \subset F$
> Soit $X$ une famille de vecteurs de $E$ et $F$ un sous-espace vectoriel de $E$. Alors
> $$
> \operatorname{vect}(X) \subset F \iff \forall u \in X,\ u \in F.
> $$

---

## Somme de sous-espaces vectoriels

> [!definition] Somme de deux sous-espaces
> Soit $F$ et $G$ deux sous-espaces vectoriels de $E$. On appelle **somme** de $F$ et $G$ l'espace vectoriel noté $F + G$ défini par
> $$
> F + G = \{ x + y \mid x \in F,\ y \in G \}.
> $$

> [!definition] Somme directe
> Deux sous-espaces $F$ et $G$ sont en **somme directe** si la décomposition de tout vecteur de $F + G$ comme somme d'un vecteur de $F$ et d'un vecteur de $G$ est unique. On note alors $F \oplus G$.

> [!proposition] Caractérisation de la somme directe
> Deux sous-espaces $F$ et $G$ sont en somme directe si et seulement si $F \cap G = \{0\}$.

> [!definition] Sous-espaces supplémentaires
> On dit que $F$ et $G$ sont **supplémentaires** dans $E$ s'ils sont en somme directe et si $F \oplus G = E$.

> [!definition] Somme de plusieurs sous-espaces
> Plus généralement, on définit la somme de $r$ sous-espaces vectoriels $F_1, \dots, F_r$ de $E$ par
> $$
> F_1 + \cdots + F_r = \{ x_1 + \cdots + x_r \mid x_1 \in F_1, \dots, x_r \in F_r \}.
> $$
> C'est un sous-espace vectoriel de $E$.

> [!definition] Somme directe de plusieurs sous-espaces
> La somme $F_1 + \cdots + F_r$ est **directe** si la décomposition de tout vecteur de $F_1 + \cdots + F_r$ sous la forme $x_1 + \cdots + x_r$ avec $x_i \in F_i$ est unique. Ceci revient à dire que si $x_1 + \cdots + x_r = 0_E$ avec $x_i \in F_i$, alors $x_i = 0$.

> [!warning] Attention
> Si $r \ge 2$, on ne peut pas caractériser le fait que $F_1, \dots, F_r$ sont en somme directe en vérifiant que $F_i \cap F_j = \{0_E\}$ si $i \neq j$.

---

## Applications linéaires

> [!definition] Application linéaire
> Une application $f : E \to F$ est appelée une **application linéaire** si, pour tous $x, y \in E$ et tous $\lambda, \mu \in \mathbb{K}$, on a
> $$
> f(\lambda x + \mu y) = \lambda f(x) + \mu f(y).
> $$
>
> On note $\mathcal{L}(E, F)$ l'ensemble des applications linéaires de $E$ dans $F$, et $\mathcal{L}(E)$ si $E = F$. Une application linéaire de $E$ dans $E$ s'appelle aussi un **endomorphisme** de $E$.

> [!example] Exemples d'applications linéaires
> - L'application $\operatorname{id}_E : E \to E$, $x \mapsto x$, est linéaire et s'appelle l'application **identité** de $E$.
> - Pour $\lambda \in \mathbb{K}$, l'application $E \to E$, $x \mapsto \lambda x$, est une application linéaire et s'appelle l'**homothétie** de rapport $\lambda$.
> - Toute combinaison linéaire d'applications linéaires est linéaire.
> - La composée d'applications linéaires est linéaire. On note souvent $vu$ au lieu de $v \circ u$, et $u^k$ pour $u \circ \cdots \circ u$.

> [!proposition] Structure d'anneau
> $(\mathcal{L}(E), +, \circ)$ est un anneau.

> [!definition] Isomorphisme / Automorphisme
> On dit qu'une application linéaire $f : E \to F$ est un **isomorphisme** si elle est bijective. La fonction réciproque d'un isomorphisme est elle-même une application linéaire.
>
> Un endomorphisme qui est aussi un isomorphisme s'appelle un **automorphisme** de $E$. L'ensemble des automorphismes de $E$ est noté $GL(E)$. $(GL(E), \circ)$ est un groupe.

> [!proposition] Image et image réciproque de sous-espaces
> L'image directe d'un sous-espace vectoriel de $E$ par une application linéaire est un sous-espace vectoriel de $F$.
>
> L'image réciproque d'un sous-espace vectoriel de $F$ par une application linéaire est un sous-espace vectoriel de $E$.

> [!definition] Noyau et image
> On appelle **noyau** de l'application linéaire $f \in \mathcal{L}(E, F)$ le sous-espace vectoriel de $E$
> $$
> \ker(f) = \{ x \in E \mid f(x) = 0 \}.
> $$
>
> On appelle **image** de l'application linéaire $f \in \mathcal{L}(E, F)$ le sous-espace vectoriel de $F$
> $$
> \operatorname{Im}(f) = \{ f(x) \mid x \in E \}.
> $$

> [!theorem] Caractérisation de l'injectivité
> $f \in \mathcal{L}(E, F)$ est injective si et seulement si $\ker(f) = \{0\}$.

> [!proposition] Image d'une famille génératrice
> Si $(x_i)_{i \in I}$ est une famille génératrice de $E$, alors $\operatorname{Im}(f) = \operatorname{vect}(f(x_i) \mid i \in I)$.

---

## Projections et symétries

> [!definition] Projection
> Soit $F$ et $G$ deux sous-espaces supplémentaires de $E$. On appelle **projection** (ou projecteur) sur $F$ parallèlement à $G$ l'application linéaire $p$ définie sur $E$ par $p(z) = x$ où $z \in E$ se décompose uniquement en $z = x + y$ avec $x \in F$ et $y \in G$.
>
> On a alors $\operatorname{Im}(p) = F$ et $\ker(p) = G$.

> [!theorem] Caractérisation des projections
> Un endomorphisme $p \in \mathcal{L}(E)$ est une projection si et seulement si $p \circ p = p$. L'application $p$ est alors la projection sur $\operatorname{Im}(p)$ parallèlement à $\ker(p)$.

> [!definition] Symétrie
> Soit $F$ et $G$ deux sous-espaces supplémentaires de $E$. On appelle **symétrie** par rapport à $F$ parallèlement à $G$ l'application linéaire $s$ définie sur $E$ par $s(z) = x - y$ où $z \in E$ se décompose uniquement en $z = x + y$ avec $x \in F$ et $y \in G$.
>
> On a alors $\ker(s - \operatorname{id}_E) = F$ et $\ker(s + \operatorname{id}_E) = G$.

> [!theorem] Caractérisation des symétries
> Un endomorphisme $s \in \mathcal{L}(E)$ est une symétrie si et seulement si $s \circ s = \operatorname{id}_E$. L'application $s$ est alors la symétrie par rapport à $\ker(s - \operatorname{id}_E)$ parallèlement à $\ker(s + \operatorname{id}_E)$.