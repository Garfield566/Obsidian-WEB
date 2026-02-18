---
nom: "Théorème de Noether"
qid: Q578555
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Noether_theorem_1st_page.png
---

# Théorème de Noether (physique)

> [!Infobox]
> **Théorème de Noether (physique)**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Noether_theorem_1st_page.png|300]]
> - **Nomme d'apres** : Emmy Noether
> - **Découvert(e) ou inventé(e) par** : Emmy Noether
> - **Partie de** : liste de théorèmes
> - **Suivi par** : second théorème de Noether

Le théorème de Noether exprime l'équivalence qui existe entre les lois de conservation et l'invariance du lagrangien d'un système par certaines transformations (appelées symétries) des coordonnées.
Démontré en 1915 et publié en 1918 par la mathématicienne Emmy Noether à Göttingen, ce théorème fut qualifié par Albert Einstein de « monument de la pensée mathématique » dans une lettre envoyée à David Hilbert en vue de soutenir la carrière de la mathématicienne.
Il est abondamment utilisé aujourd'hui par la physique théorique, où tout phénomène est abordé, chaque fois que possible, en matière de symétrie d'espace, de charges électriques, et même de temps.

## Énoncés

Un autre énoncé équivalent est:

Chaque « invariance » traduit le fait que les lois de la physique ne changent pas lorsqu'une expérience subit la transformation correspondante, et donc, qu'il n'y a pas de référence absolue pour mener une telle expérience.

## Démonstrations

Remarque: Dans le cas général, on n'a pas nécessairement un unique paramètre 

 $s$

 mais plutôt un jeu de paramètres 

 $s_{j}$

 auxquels vont correspondre les invariants 

 ˙

 $$I_{j}=\frac {\partial L}{\partial {\dot {q}_{i}}}{\frac {\partial q_{i}(\vec {s})}{\partial s_{j}}}.$$

## Exemples

Détaillons quelques-uns de ces exemples.

## Quantité de mouvement

Prenons tout d'abord le cas d'une particule libre, on a donc le lagrangien 

 ˙

 $$L=\frac {1}{2}m\dot {\vec {q}}^{2}$$

invariant par translation. On voit bien ici que si on change l'origine des coordonnées, cela ne va pas modifier la physique de notre particule libre. Le lagrangien est donc invariant par la transformation de translation

 ~

 $q_{i}\rightarrow \tilde {q}_{i}=q_{i}+\alpha _{i}$

avec les 

 $\alpha _{i}$

 les composantes du vecteur décrivant la translation. On voit ici que l'on a, pour une translation infinitésimale d'un vecteur 

 $\vec {\delta \alpha }=\delta \alpha _{i}\vec {e}_{i}$

, une variation de nos coordonnées généralisées qui vaut 

 ~

 $\delta q_{i}=\tilde {q}_{i}-q_{i}=\delta \alpha _{i}$

. Les quantités conservées associées à cette transformation sont donc 

 ˙

 ˙

 ˙

 $$I_{i}=\sum _{j}\frac {\partial L}{\partial {\dot {q}_{j}}}\frac {\partial q_{j}{\partial \alpha _{i}}}=\sum _{j}\frac {\partial L}{\partial {\dot {q}_{j}}}\delta _{ij}=m\dot {q}_{i}=p_{i}$$

 $\delta _{ij}$

 le delta de Kronecker, on retrouve bien les composantes du vecteur quantité de mouvement.

## Moment cinétique

Considérons maintenant le cas d'un système invariant par rotation, prenons par exemple une particule placée dans un potentiel central 

 $\Phi (r)$

, on a alors 

 ˙

 $$L=\frac {1}{2}m\dot {\vec {q}}^{2}-\Phi (r)$$

. Le système étant invariant par rotation (la norme de la vitesse est invariante par rotation), il semble pertinent de se placer en coordonnées sphériques, pour lesquelles 

 $q=r\vec {e}_{r}$

 ˙

 ˙

 ˙

 ϕ
 ˙

 ϕ

 $$\dot {\vec {q}}=\dot {r}\vec {e}_{r}+r\dot {\theta }\vec {e}_{\theta }+r\sin(\theta )\dot {\phi }\vec {e}_{\phi }$$

. On a alors 

 ˙

 ˙

 ϕ
 ˙

 $$L=\frac {m}{2}\left(\dot {r}^{2}+r^{2}\dot {\theta }^{2}+r^{2}\sin ^{2}(\theta )\dot {\phi }^{2}\right)-\Phi (r).$$

La transformation associée à la rotation en coordonnées sphériques peut s'écrire comme 

 ϕ
 ~

 ϕ
 ~

 ϕ
 $$(r,\theta,\phi )\rightarrow (r,\tilde {\theta }=\theta +\chi,\tilde {\phi }=\phi +\psi )$$

, avec 

 $\chi$

 $\psi$

 les deux angles caractérisant la transformation. Pour une transformation infinitésimale on a donc 

 ϕ

 $\delta q=r\vec {e}_{\theta }\delta \chi +r\vec {e}_{\phi }\delta \psi$

. On voit donc ici que les deux quantités conservées vont être 

 ˙

 ˙

 ϕ

 ϕ
 ˙

 ϕ

 ϕ
 ˙

 $$I_{\theta }=\frac {\partial L}{\partial (r{\dot {\theta })}}\frac {\partial q}{\partial \chi }\cdot \vec {e}_{\theta }=mr^{2}\dot {\theta }\qquad \mathrm {et} \qquad I_{\phi }=\frac {\partial L}{\partial (r\sin(\theta ){\dot {\phi })}}\frac {\partial q}{\partial \psi }\cdot \vec {e}_{\phi }=mr^{2}\sin(\theta )\dot {\phi }$$

c'est-à-dire les deux composantes angulaires du moment cinétique 

 $\vec {L}=\vec {r}\times \vec {p}$

, à un signe près pour 

 $L_{\theta }$

. Attention cependant aux indices, on a 

 ϕ

 $I_{\theta }=L_{\phi }$

 ϕ

 $I_{\phi }=-L_{\theta }$

, et on a bien sûr 

 $L_{r}=0$

 par définition du produit vectoriel.

## Énergie

Si on a cette fois un système qui est invariant dans le temps, on a alors un lagrangien qui est indépendant du temps 

 $L(t+\delta t)=L(t)$

 $\partial _{t}L=0$

. La transformation est ici une translation dans le temps, et se traduit pour les coordonnées temporelles par 

 ~

 ˙

 $$q_{i}(t)\rightarrow \tilde {q}_{i}(t)=q_{i}(t+\delta t)=q_{i}(t)+\delta t\dot {q}_{i}$$

ce qui conduit à la quantité conservée 

 ˙

 $$I=\sum _{i}\frac {\partial L}{\partial {\dot {q_{i}}}}\frac {\partial q_{i}{\partial t}}.$$

Le lagrangien étant conservé aussi, on a la quantité totale 

 ˙

 ˙

 $$H=\sum _{i}\frac {\partial L}{\partial {\dot {q}_{i}}}\dot {q}_{i}-L$$

qui est conservée, or ce n'est rien d'autre que le hamiltonien du système. Le hamiltonien (l'énergie) est donc conservé pour les systèmes indépendants (explicitement) du temps.

## Théorie des champs classique

Le théorème de Noether est aussi valide en théorie des champs classique où le lagrangien est remplacé par une densité lagrangienne qui dépend de champs plutôt que de variables dynamiques. La formulation du théorème reste sensiblement la même:

## Invariance de jauge et second théorème de Noether

On considère de manière générale pour une densité de lagrangien quelconque 

 $\mathcal {L}[\psi _{i},\partial _{\mu }\psi _{i},x^{\mu }]$

dont l'action associée doit être stationnaire pour toute transformation infinitésimale des champs selon le Principe de Hamilton. On a donc

 $$\delta S=\int \textrm {d}^{4}x\;\left[\frac {\partial {\mathcal {L}}{\partial \psi _{i}}}\delta \psi _{i}+\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}\delta \partial _{\mu }\psi _{i}\right]=\int \textrm {d}^{4}x\;\left[\left(\frac {\partial {\mathcal {L}}{\partial \psi _{i}}}-\partial _{\mu }\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}\right)\delta \psi _{i}+\partial _{\mu }\left(\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}\delta \psi _{i}\right)\right]=0$$

où on a utilisé la convention d'Einstein pour la sommation sur les indices répétés, et où on a mis de côté les possibles transformations de l'espace-temps (on a pris 

 $\delta x^{\mu }=0$

 ). On voit donc que l'on peut reformuler ce résultat de manière générale comme 

 $$[\psi ]_{i}\delta \psi _{i}=-\partial _{\mu }\left(\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}\delta \psi _{i}\right),\qquad [\psi ]_{i}=\frac {\partial {\mathcal {L}}{\partial \psi _{i}}}-\partial _{\mu }\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}$$

 $[\psi ]_{i}$

 représentant donc les équations du mouvement pour le champ 

 $\psi _{i}$

On s'intéresse maintenant à une densité de lagrangien invariante sous une transformation de jauge, c'est-à-dire une transformation locale des champs. Dans ce cas on va voir que l'on applique cette fois le second théorème de Noether.
Plus précisément on considère ici une densité de lagrangien invariante sous un groupe de transformation de dimension infinie et dépendant continûment de 

 $\rho$

 fonctions 

 $p_{\alpha }(x^{\mu }),\;\;\alpha =1,\;...,\;\rho$

, groupe que l'on notera 

 $G_{\infty \rho }$

. On voit que dans le cas d'une telle transformation la variation infinitésimale des champs 

 $\delta \psi _{i}$

 dans l'équation ci-dessus se décompose comme 

 $$\delta \psi _{i}=\sum _{\alpha }\left[a_{\alpha i}(\psi _{i},\partial _{\mu }\psi _{i},x^{\mu })\Delta p_{\alpha }(x^{\mu })+b_{\alpha i}^{\nu }(\psi _{i},\partial _{\mu }\psi _{i},x^{\mu })\partial _{\nu }\Delta p_{\alpha }(x^{\mu })\right]$$

où la notation 

 $\Delta p_{\alpha }$

 dénote le fait que l'on considère un 

 $p_{\alpha }$

 infinitésimal. On voit donc que l'on peut reprendre l'équation précédente sous forme intégrale pour obtenir 

 $$\int d^{4}x\,[\psi ]_{i}\left(a_{\alpha i}\Delta p_{\alpha }+b_{\alpha i}^{\nu }\partial _{\nu }\Delta p_{\alpha }\right)=\int d^{4}x\,\left(a_{\alpha i}[\psi ]_{i}-\partial _{\nu }\left(b_{\alpha i}^{\nu }[\psi ]_{i}\right)\right)\Delta p_{\alpha }+\int d^{4}x\,\partial _{\nu }\left(b_{\alpha i}^{\nu }[\psi ]_{i}\partial _{\nu }\Delta p_{\alpha }\right)$$

 $$\Longrightarrow \qquad \int d^{4}x\left(a_{\alpha i}[\psi ]_{i}-\partial _{\nu }\left(b_{\alpha i}^{\nu }[\psi ]_{i}\right)\right)\Delta p_{\alpha }=-\int d^{4}x\,\partial _{\mu }\left(\frac {\partial {\mathcal {L}}{\partial (\partial _{\mu }\psi _{i})}}\delta \psi _{i}+b_{\alpha i}^{\mu }[\psi ]_{i}\Delta p_{\alpha }\right)$$

or on voit ici que le second terme de la seconde équation est un terme de bord, et les fonctions 

 $p_{\alpha }$

 étant arbitraires on peut toujours les choisir de sorte que ce terme s'annule. On obtient alors le second théorème de Noether

## Exemple

Considérons par exemple la densité de Lagrangien 

 ∗

 ∗

 $$\mathcal {L}=(\partial _{\mu }+iqA_{\mu })\psi (\partial ^{\mu }+iqA^{\mu })\psi ^{*}-m^{2}\psi \psi ^{*}-\frac {1}{4}F^{\mu \nu }F_{\mu \nu }$$

où 

 $F_{\mu \nu }$

ne dépend que des dérivées première de 

 $A_{\mu }$

 (dans le cas abélien du moins). Elle est invariante sous la transformation de jauge locale 

 ~

 ∗

 ~

 ∗

 ∗

 ~

 $$\psi \rightarrow \tilde {\psi }=e^{iq\theta (x)}\psi,\qquad \psi ^{*}\rightarrow \tilde {\psi }^{*}=e^{-iq\theta (x)}\psi ^{*},\qquad A_{\mu }\rightarrow \tilde {A}_{\mu }=A_{\mu }+\partial _{\mu }\theta (x)$$

où voit qu'ici on a une seule fonction continue 

 $p_{\alpha }$

 dans notre groupe de transformation, que l'on a noté 

 $\theta (x)$

. Cette transformation correspond sous forme infinitésimale à 

 ∗

 ∗

 $$\delta \psi =iq\delta \theta \psi,\qquad \delta \psi ^{*}=-iq\delta \theta \psi ^{*},\qquad \delta A_{\mu }=\partial _{\mu }\theta$$

on a alors 

 ∗

 ∗

 $$a_{\psi }=iq\psi,\qquad a_{\psi ^{*}}=-iq\psi,\qquad b_{\psi }=b_{\psi ^{*}}a_{A_{\mu }}=0,\qquad b_{A_{\mu }}^{\nu }=\delta _{\mu }^{\nu }.$$

On en déduit que dans le cas de cette densité de Lagrangien on a la relation 

 ∗

 ∗

 $$[\psi ]iq\psi +[\psi ^{*}](-iq\psi ^{*})=\partial _{\mu }\left([A_{\nu }]\delta _{\nu }^{\mu }\right)=\partial _{\mu }[A_{\mu }].$$

On voit alors ici que si les équations du mouvement sont satisfaites pour les deux champs de masse 

 $\psi$

 ∗

 $\psi ^{*}$

 on a alors 

 $$\partial _{\mu }\left(\frac {\partial {\mathcal {L}}{\partial A_{\mu }}}-\partial _{\nu }\frac {\partial {\mathcal {L}}{\partial (\partial _{\nu }A_{\mu })}}\right)=0$$

or sachant que l'on a 

 $$\frac {\partial {\mathcal {L}}{\partial A_{\mu }}}=0$$

 $$\frac {\partial {\mathcal {L}}{\partial (\partial _{\nu }A_{\mu })}}=F^{\mu \nu }$$

 on en déduit qu'ici le courant 

 $J^{\mu }=\partial _{\nu }F^{\mu \nu }$

 est conservé. Cela implique notamment que 

 $F^{\mu \nu }$

 soit complètement antisymétrique, et donc construit à partir de 

 $\partial _{\mu }A_{\nu }-\partial _{\nu }A_{\mu }$

De même si à l'inverse on impose que les équations de l'électromagnétisme soient satisfaites c'est-à-dire 

 $[A_{\mu }]=0$

 on obtient l'équation de conservation du quadri courant électrique usuel 

 ∗

 ∗

 $$\partial _{\mu }j^{\mu }=0,\qquad j^{\mu }=iq\left(\psi ^{*}(\partial ^{\mu }+iqA^{\mu })\psi -\psi (\partial ^{\mu }+iqA^{\mu })\psi ^{*}\right).$$
