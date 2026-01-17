---
type: Définition
domaine: Analyse
moc_lie: Calcul Différentiel
---

> [!infobox] 📚 Dérivée (Définition)
> ![[Pasted image 20251204201021.png|300]]
> La dérivée d'une fonction en un point est le taux de variation instantané de cette fonction.
> 
> Elle correspond au coefficient directeur (la pente) de la tangente à la courbe de la fonction en ce point.

##  Présentation

### Définition et Contexte

La dérivée est un concept fondamental du **Calcul Différentiel** qui vise à étudier la variation (le changement) des fonctions.

La dérivée d'une fonction $f$ en un point $a$ est définie par la limite de son taux de variation entre $a$ et $a+h$, lorsque $h$ tend vers 0.

$$\text{Si cette limite existe, on la note } f'(a).$$

### Taux de Variation

Le **taux de variation** (ou taux d'accroissement) d'une fonction $f$ entre $a$ et $a+h$ est donné par :

$$\tau(h) = \frac{f(a+h) - f(a)}{h}$$

Géométriquement, ce taux représente la **pente de la sécante** qui relie les points d'abscisses $a$ et $a+h$ sur la courbe de $f$.

---

##  Analyse

### Définition Formelle

Une fonction $f$ est dite **dérivable** en $a$ si et seulement si la limite du taux de variation $\tau(h)$ existe lorsque $h$ tend vers 0.

La dérivée $f'(a)$ est cette limite :

$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

### Interprétation Géométrique

Si la dérivée $f'(a)$ existe, la courbe de la fonction $f$ admet une **tangente** au point d'abscisse $a$.

L'équation de cette tangente $T_a$ est donnée par :

$$T_a : y = f'(a)(x-a) + f(a)$$

$f'(a)$ est donc le **coefficient directeur** de cette droite tangente.

### Interprétation Physique

Si $f(t)$ représente la position d'un objet en fonction du temps $t$, alors $f'(t)$ représente la **vitesse instantanée** de cet objet au temps $t$.

---

## Exemple

### Dérivée de $f(x) = x^2$ en $x=a$

Utilisons la définition formelle :

$$\lim_{h \to 0} \frac{(a+h)^2 - a^2}{h} = \lim_{h \to 0} \frac{a^2 + 2ah + h^2 - a^2}{h}$$

$$= \lim_{h \to 0} \frac{h(2a + h)}{h} = \lim_{h \to 0} (2a + h) = 2a$$

Ainsi, si $f(x)=x^2$, sa dérivée est $f'(x) = 2x$.

### Applications et Liens
#Dérivée 