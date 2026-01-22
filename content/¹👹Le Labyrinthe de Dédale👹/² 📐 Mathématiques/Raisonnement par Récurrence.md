---
type: Théorème
domine: Anlye
---
> [!infobox] Raisonnement par Récurrence (Principe)
> 
> ![[Pasted image 20251204153056.png|350]]
> Le raisonnement par récurrence est comme une [suite de dominos](https://fr.wikipedia.org/wiki/Effet_domino "Effet domino"). Si la propriété est vraie au rang n0 (_[i. e.](https://fr.wikipedia.org/wiki/I._e. "I. e.")_ le premier domino de numéro 0 tombe) et si sa véracité au rang _n_ implique celle au rang _n_ + 1 (_i. e._ la chute du domino numéro _n_ fait tomber le domino numéro _n_ + 1) alors la propriété est vraie pour tout entier (_i. e._ tous les dominos tombent).

## Présentation

 Définition et Contexte
Le raisonnement par récurrence (parfois appelé induction mathématique) est une méthode de démonstration qui permet de prouver qu'une propriété $\mathcal{P}(n)$ est vraie pour **tout entier naturel $n$ supérieur ou égal à un certain rang initial $n_0$.
Ce principe est attribué au mathématicien italien Giuseppe Peano.
 L'Analogie des Dominos
L'intuition repose sur l'image d'une file illimitée de dominos:

 * Si le **premier domino tombe** (Initialisation).
 * Et si la chute d'un domino **entraîne toujours la chute du suivant** (Hérédité).
**Alors, on est assuré que tous les dominos de la file tombent**.
Le principe est validé si la propriété $\mathcal{P}$ est :

1. [cite_start]Vraie au rang $n_0$ (Initialisation).
2. [cite_start]Héréditaire à partir du rang $n_0$ (Hérédité).

---

---
## Analyse

Pour une démonstration par récurrence, les deux étapes suivantes sont nécessaires et successives :

 #### **1.L'Initialisation**
Il faut vérifier que la propriété $\mathcal{P}(n)$ est vraie pour le **premier rang $n_0$**.
$$\text{Vérifier que } \mathcal{P}(n_0) \text{ est vraie.}$$
**Rappel Important : L'étape de l'initialisation est indispensable. Sans elle, on peut démontrer l'hérédité pour une propriété qui n'est jamais vraie (par exemple, " $2^n$ est divisible par 3").**

#### **2\. L'Hérédité**
L'objectif est de prouver le caractère héréditaire de la propriété.

## Exemple
#### 1-Hypothèse de Récurrence (H.R.)

On **suppose** la propriété vraie pour un certain entier $k$ fixé tel que $k \ge n_0$.

$$\text{On suppose } \mathcal{P}(k) \text{ vraie.}$$
#### 2-Démonstration
À partir de cette hypothèse $\mathcal{P}(k)$, on doit **démontrer** que la propriété est également vraie pour le rang suivant $k+1$
$$\text{Démontrer que } \mathcal{P}(k+1) \text{ est vraie.}$$
$$\text{C'est la démonstration que } \mathcal{P}(k) \implies \mathcal{P}(k+1)$$

-----

> [!info] Applications et Liens
>
écurrence
