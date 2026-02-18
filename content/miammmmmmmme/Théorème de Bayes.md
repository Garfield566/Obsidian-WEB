---
nom: "Théorème de Bayes"
qid: Q182505
type: theoreme
categorie: theoreme
tags: "#mathematiques/theoreme"
---

# Théorème de Bayes

> [!Infobox]
> **Théorème de Bayes**
> - **Nomme d'apres** : Thomas Bayes
> - **Date de découverte ou d'invention** : 1763
> - **Découvert(e) ou inventé(e) par** : Thomas Bayes
> - **Utilisé par** : statistique bayésienne, classification naïve bayésienne, probabilités bayésiennes
> - **Sujet ou thème principal** : probabilité conditionnelle
> - **Discipline dont c'est l'objet** : théorie des probabilités, statistique bayésienne
> - **Partie de** : liste de théorèmes

Le théorème de Bayes (/beɪz/ ) est l'un des principaux théorèmes de la théorie des probabilités. Il est aussi utilisé en statistiques du fait de son application, qui permet de déterminer la probabilité qu'un événement arrive à partir d'un autre évènement qui s'est réalisé, notamment quand ces deux évènements sont interdépendants.
En d'autres termes, à partir de ce théorème, il est possible de calculer précisément la probabilité d'un évènement en tenant compte à la fois des informations déjà connues et des données provenant de nouvelles observations. La formule de Bayes peut être dérivée des axiomes de base de la théorie des probabilités, en particulier de la probabilité conditionnelle.
Sa formulation initiale est issue des travaux du révérend Thomas Bayes. Elle a été trouvée indépendamment par Pierre-Simon de Laplace. La formulation de Bayes en 1763 est plus limitée que les nouvelles formulations d'aujourd'hui.
Outre son utilisation en probabilité, ce théorème est fondamental pour l'inférence bayésienne qui s'est montrée très utile en intelligence artificielle. Il est également utilisé dans plusieurs autres domaines: en médecine, en sciences numériques, en géographie, en démographie, etc.
Pour le mathématicien Harold Jeffreys, les formulations de Bayes et de Laplace sont des axiomes. Il considère également que « le théorème de Bayes est à la théorie des probabilités ce que le théorème de Pythagore est à la géométrie. »

## Histoire

À sa mort en avril 1761, Thomas Bayes laisse à Richard Price ses articles non terminés. C'est ce dernier qui prend l'initiative de publier l'article « An Essay towards solving a Problem in the Doctrine of Chance » et de l'envoyer à la Royal Society deux ans plus tard.
D'après Martyn Hooper, il est probable que Richard Price ait lui-même contribué de manière significative à la rédaction de l'article final et qu'il soit ainsi avec Thomas Bayes l'auteur du théorème connu sous le nom de théorème de Bayes. Cette erreur d'attribution serait une application de la loi d'éponymie de Stigler selon laquelle les découvertes scientifiques sont rarement attribuées à leur premier auteur.
La formule est redécouverte par Pierre-Simon de Laplace en 1774.
Dans son unique article, Bayes cherchait à déterminer ce que l'on appellerait actuellement la distribution a posteriori de la probabilité p d'une loi binomiale. Ses travaux ont été édités et présentés à titre posthume (1763) par son ami Richard Price dans Un essai pour résoudre un problème dans la théorie des risques (An Essay towards solving a Problem in the Doctrine of Chances). Les résultats de Bayes ont été étendus dans un essai de 1774 par le mathématicien français Laplace, lequel n'était apparemment pas au fait du travail de Bayes.
Le résultat principal obtenu par Bayes est le suivant: en considérant une distribution uniforme du paramètre binomial p et une observation O d'une loi binomiale 

 $\mathcal {B}(n+m,p)$

, où m est donc le nombre d'issues positives observées et n le nombre d'échecs observés, la probabilité que p soit entre a et b sachant O vaut:

 $${\frac {{\int _{a}^{b}{n+m \choose m}\,x^{m}(1-x)^{n}\,\mathrm {d} x}}{{\int _{0}^{1}{n+m \choose m}\,x^{m}(1-x)^{n}\,\mathrm {d} x}}}$$

Ces résultats préliminaires impliquent le résultat que l'on appelle théorème de Bayes, mais il ne semble pas que Bayes se soit concentré ou ait insisté sur ce résultat.
Ce qui est « bayésien » (au sens actuel du mot) dans ce résultat, c'est que Bayes ait présenté cela comme une probabilité sur le paramètre p. Cela revient à dire qu'on peut déterminer non seulement des probabilités à partir d'observations issues d'une expérience, mais aussi les paramètres relatifs à ces probabilités. C'est le même type de calcul analytique qui permet de déterminer par inférence les deux. En revanche, si l'on s'en tient à une interprétation fréquentiste, on est censé ne pas considérer de probabilité de distribution du paramètre p et en conséquence, on ne peut raisonner sur p qu'avec un raisonnement d'inférence (logique) non-probabiliste.
Depuis l'an 2000, les publications à son sujet se multiplient en raison de ses nombreuses applications.

## Énoncé

Le théorème de Bayes est un corollaire du théorème de probabilité totale. Il énonce des probabilités conditionnelles de plusieurs évènements. Par exemple, pour les évènements A et B, il permet de déterminer la probabilité de A sachant B, à partir des probabilités de A, de B et de B sachant A, à condition que la probabilité de B ne soit pas égale à 0.
Dans sa formulation de 1763, le théorème était énoncé:

 ∣
 ∣
 $P(A\mid B)=\dfrac {P(B\mid A)P(A)}{P(B)}$

, à condition que 

 $P(B)\neq 0$

, et où:

 $A$

 $B$

 sont deux évènements;

 $P(A)$

 $P(B)$

 sont la probabilité des deux évènements;

 ∣
 $P(A\mid B)$

 est la probabilité conditionnelle que l'évènement A se réalise étant donné que l'évènement B s'est réalisé.

 ∣
 $P(B\mid A)$

 est la probabilité conditionnelle que l'évènement B se réalise étant donné que l'évènement A s'est réalisé.
Il peut également s'écrire:

 ∣
 ∩
 ∩
 ∣
 $P(A\mid B)\,P(B)=P(A\cap B)=P(B\cap A)=P(B\mid A)\,P(A)$

, où:

 $P(A)$

 $P(B)$

 sont les probabilités a priori de 

 $A$

 et de 

 $B$

 ∣
 $P(A\mid B)$

 est la probabilité conditionnelle de 

 $A$

 sachant 

 $B$

 ou probabilité a posteriori;

 ∣
 $P(B\mid A)$

 est la probabilité conditionnelle de 

 $B$

 sachant 

 $A$

 ou probabilité a posteriori.

## Autres formulations intégrant la fonction de vraisemblance

Le théorème est également reformulé afin d'intégrer la fonction de vraisemblance marginale (en) (fonction de vraisemblance intégrant la constante de normalisation). Il se formule ainsi:
Dans un univers 

 $\Omega$

, les partitions d'un ensemble 

 $A_{1},\ldots,A_{n}$

 (c'est-à-dire 

 ∅

 ∩

 ∅

 $$\ A_{i}\neq \varnothing \ \forall i,\ A_{i}\cap A_{j}=\varnothing \ \forall i\neq j$$

 ∪

 $\cup _{i=1}^{n}A_{i}=\Omega$

), la probabilité conditionnelle des évènements mutuellement exclusifs et exhaustifs (

 $\{A_{1},A_{2},...,A_{n}\}$

), à condition que 

 $P(B)\neq 0$

, en sachant 

 $B$

 se calcule:

 $$P(A_{i}|B)={\frac {P(B|A_{i})P(A_{i})}{P(B)}}={\frac {P(B|A_{i})P(A_{i})}{\sum _{j=1}^{n}P(B|A_{j})P(A_{j})}}$$

où:

 $P(A)$

 $P(B)$

 sont les probabilités a priori de 

 $A$

 et de 

 $B$

 ∣
 $P(A\mid B)$

 est la probabilité conditionnelle de 

 $A$

 sachant 

 $B$

 ou probabilité a posteriori;

 ∣
 $P(B\mid A)$

 est la probabilité conditionnelle de 

 $B$

 sachant 

 $A$

 ou probabilité a posteriori.
Le calcul de 

 $P(B)$

 dépend de son champ d'application. En sciences numériques, elle est nommée « preuve » pour désigner la fonction de vraisemblance marginale et appliquée en médecine, elle désigne un rapport de vraisemblance.
Il peut également s'écrire:

 ∩
 ¯

 ∩
 ¯

 ¯

 $P(B)=P(A\cap B)+P(\bar {A}\cap B)=P(B|A)P(A)+P(B|\bar {A})P(\bar {A})$

 ¯

 ¯

 $$P(A|B)=\frac {P(B|A)P(A)}{P(B|A)P(A)+P(B|{\bar {A})P(\bar {A})}}$$

où:

 ¯

 $\bar {A}$

 est le complémentaire de 

 $A$

. Plus généralement, si 

 $\{A_{i}\}$

 est un système quasi complet d'évènements fini ou dénombrable,

 $$P(A_{i}|B)={\frac {P(B|A_{i})P(A_{i})}{\sum _{j}P(B|A_{j})P(A_{j})}}\,$$

, pour tout évènement du système 

 $\{A_{i}\}$

## Explications

Pour aboutir au théorème de Bayes, on part d'une des définitions de la probabilité conditionnelle:

 ∩
 $P(A\cap B)=P(A)\cdot P(B\vert A)=P(B)\cdot P(A\vert B)$

Cette formulation ne fait que traduire en langage mathématique des remarques relativement triviales:

La probabilité 

 ∩
 $P(A\cap B)$

 d'avoir observé les évènements A et B, en supposant par exemple que A arrive le premier, c'est la probabilité d'avoir l'évènement A, c'est-à-dire P(A), puis d'observer B lorsque A est présent, qui a alors (par définition) la probabilité P(B|A).
La valeur de la probabilité d'ensemble est donc le produit des deux probabilités de base: 

 ∩
 $P(A\cap B)=P(A)\cdot P(B\vert A)$

Mais comme il est indifférent, pour observer A et B, de savoir dans quel ordre ils sont apparus, on a évidemment 

 $P(A)\cdot P(B\vert A)=P(B)\cdot P(A\vert B)$

En divisant de part et d'autre par P(B), on obtient:

 $$P(A|B)=\frac {P(B|A)P(A)}{P(B)}$$

soit le théorème de Bayes.

## De quelle urne vient la boule ?

À titre d'exemple, on imagine deux urnes remplies de boules. La première contient dix (10) boules noires et trente (30) blanches; la seconde en a vingt (20) de chaque. On tire sans préférence particulière une des urnes au hasard et dans cette urne, on tire une boule au hasard. Quelle est la probabilité qu'on ait tiré cette boule dans la première urne sachant qu'elle est blanche?
Intuitivement, on comprend bien qu'il est plus probable que cette boule provienne de la première urne, que de la seconde. Donc, cette probabilité devrait être supérieure à 50 %. La réponse exacte (60 %) peut se calculer à partir du théorème de Bayes.
Soit H1 l'hypothèse « On tire dans la première urne. » et H2 l'hypothèse « On tire dans la seconde urne. ». Comme on tire sans préférence particulière, P(H1) = P(H2); de plus, comme on a certainement tiré dans une des deux urnes, la somme des deux probabilités vaut 1: chacune vaut 50 %.
On note D l'information donnée « On tire une boule blanche. » Comme on tire une boule au hasard dans une des urnes, la probabilité de D sachant l'hypothèse H1 réalisée vaut:

 %

 $$P(D|H_{1})=\frac {30}{40}=75\,\%$$

De même la probabilité de D sachant l'hypothèse H2 réalisée vaut:

 %

 $$P(D|H_{2})=\frac {20}{40}=50\,\%$$

La formule de Bayes dans le cas discret donne donc:

 %
 %

 %
 %
 %
 %

 %

 $${\begin{matrix}P(H_{1}|D)&=&{\frac {P(H_{1})\cdot P(D|H_{1})}{P(H_{1})\cdot P(D|H_{1})+P(H_{2})\cdot P(D|H_{2})}}\\\\\ &=&\frac {50\%\cdot 75\%}{50\%\cdot 75\%+50\%\cdot 50\%}\\\\\ &=&60\%\end{matrix}}$$

Avec:

 $P(D)=P(H_{1})\cdot P(D|H_{1})+P(H_{2})\cdot P(D|H_{2})$

Avant que l'on regarde la couleur de la boule, la probabilité d'avoir choisi la première urne est une probabilité a priori, P(H1) soit 50 %. Après avoir regardé la boule, on révise notre jugement et on considère P(H1|D), soit 60 %, ce qui confirme notre intuition première.
Remarque: Les schémas que sont les arbres de probabilité peuvent servir utilement de support à la résolution de tels problèmes élémentaires.

## Applications

Ce théorème élémentaire (originellement nommé « de probabilité des causes ») a des applications considérables.
Le théorème de Bayes est utilisé dans l'inférence statistique pour mettre à jour ou actualiser les estimations d'une probabilité ou d'un paramètre quelconque, à partir des observations et des lois de probabilité de ces observations. Il y a une version discrète et une version continue du théorème.

L'école bayésienne utilise les probabilités comme moyen de traduire numériquement un degré de connaissance (la théorie mathématique des probabilités n'oblige en effet nullement à associer celles-ci à des fréquences, qui n'en représentent qu'une application particulière résultant de la loi des grands nombres). Dans cette optique, le théorème de Bayes peut s'appliquer à toute proposition, quelle que soit la nature des variables et indépendamment de toute considération ontologique.
L'école fréquentiste utilise les propriétés de long terme de la loi des observations et ne considère pas de loi sur les paramètres, inconnus mais fixés.

## Inférence bayésienne

Les règles de la théorie mathématique des probabilités s'appliquent à des probabilités en tant que telles, pas uniquement à leur application en tant que fréquences relatives d'évènements aléatoires (voir Événement (probabilités)). On peut décider de les appliquer à des degrés de croyance en certaines propositions. Ces degrés de croyance s'affinent au regard d'expériences en appliquant le théorème de Bayes.
Le Théorème de Cox-Jaynes justifie aujourd'hui très bien cette approche, qui n'eut longtemps que des fondements intuitifs et empiriques.

## Réseaux bayésiens

Dans The Book of Why, Judea Pearl présente la règle de Bayes comme un cas particulier d'un réseau bayésien à deux nœuds et un lien. Les réseaux bayésiens constituent une extension de la règle de Bayes à des réseaux de plus grande taille.

## « Faux positifs » médicaux

Les faux positifs sont une difficulté inhérente à tous les tests: aucun test n'est parfait. Parfois, le résultat sera positif à tort, ce que l'on nomme parfois risque du premier ordre ou risque alpha.
Par exemple, quand on teste une personne pour savoir si elle est affectée par une maladie, il y a un risque, généralement infime, que le résultat soit positif, alors que le patient n'a pas contracté la maladie. Le problème alors n'est pas de mesurer ce risque dans l'absolu (avant de procéder au test), il faut encore déterminer la probabilité qu'un test positif le soit à tort. On va montrer comment, dans le cas d'une maladie très rare, le même test, par ailleurs très fiable, peut aboutir à une nette majorité de positifs illégitimes.
Pour illustrer le phénomène, on imagine un test extrêmement fiable:

si un patient a contracté la maladie, le test le fait remarquer, c'est-à-dire est positif, presque systématiquement, 99 % des fois, soit avec une probabilité 0,99;
si un patient est sain, le test est correct, c'est-à-dire négatif dans 95 % des cas, soit avec une probabilité 0,95.
On suppose que la maladie ne touche qu'une personne sur mille, soit avec une probabilité 0,001. Cela peut paraître peu, mais c'est considérable dans le cas d'une maladie mortelle. On a alors toutes les informations nécessaires pour déterminer la probabilité qu'un test soit positif à tort, ce qui peut causer un surdiagnostic.
On désigne par A l'événement « Le patient a contracté la maladie » et par B l'événement « Le test est positif ». La seconde forme du théorème de Bayes dans le cas discret donne alors:

 ¯

 ¯

 $$P(A|B)=\frac {P(B|A)P(A)}{P(B)}=\frac {P(B|A)P(A)}{P(B|A)P(A)+P(B|{\bar {A})P(\bar {A})}}={\frac {0{,}99\times 0{,}001}{0{,}99\times 0{,}001+0{,}05\times 0{,}999}}\approx 0{,}019.$$

Avec:

 $P(A|B)$

 = la probabilité que le patient soit malade sachant que le test est positif

 $P(B|A)$

 = la probabilité que le test soit positif sachant que le patient est malade

 $P(A)$

 = la probabilité à priori que le patient soit malade

 $P(B)$

 = la probabilité à priori que le test soit positif = 

 ¯

 ¯

 $P(B|A)P(A)+P(B|\bar {A})P(\bar {A})$

, c'est-à-dire le cas où le patient est détecté positif alors qu'il est réellement malade (vrai positif) ainsi que le cas où le patient est détecté positif alors qu'il est sains (faux positif).

Traduit en langage courant, cette équation signifie que « la probabilité que le patient ait réellement contracté la maladie, quand le test est positif, n'est que de 1,9 % ».
Sachant que le test est positif, la probabilité que le patient soit sain vaut donc environ:
(1 − 0,019) = 0,981. Du fait du très petit nombre de malades, en effet,

pratiquement tous les malades présentent un test positif, mais aussi
pratiquement tous les tests positifs désignent des personnes saines.
Si le traitement est très lourd, coûteux ou dangereux pour un patient sain, il peut être alors opportun de faire subir, à tous les patients positifs, un test complémentaire (qui sera sans doute plus précis et plus coûteux, le premier test n'ayant servi qu'à écarter les cas les plus évidents).
On a tout de même réussi, avec le premier test, à isoler une population vingt fois moindre, qui contient pratiquement tous les malades. En effet, en enlevant les patients dont le test est négatif et qui sont donc supposés sains, on a ramené le rapport des malades sur la population étudiée d'un individu sur mille à un individu sur cinquante (

 $P(A|B)$

 est proche de 

 $1/50$

). En procédant à d'autres tests, on peut espérer améliorer la fiabilité de la détection.
Le théorème de Bayes nous montre que dans le cas d'une probabilité faible de la maladie recherchée, le risque d'être déclaré positif à tort a un impact très fort sur la fiabilité. Le dépistage d'une maladie rare peut causer le surdiagnostic.
Cette erreur intuitive, commune, d'estimation est un biais cognitif appelé "oubli de la fréquence de base".

## Problème de Monty Hall

La démonstration du problème de Monty Hall utilise le théorème de Bayes. En effet, il est nécessaire de se servir de ce théorème pour prouver qu'il vaut mieux changer de porte pour gagner à la suite de l'intervention du présentateur.

## Aspects sociaux, juridiques et politiques

Un problème régulièrement soulevé par l'approche bayésienne est le suivant: si une probabilité de comportement (délinquance, par exemple) est fortement dépendante de certains facteurs sociaux, culturels ou héréditaires, alors:

d'un côté, on peut se demander si cela ne suppose pas une partielle réduction de responsabilité, morale à défaut de juridique, des délinquants. Ou, ce qui revient au même, à une augmentation de responsabilité de la société, qui n'a pas su ou pas pu neutraliser ces facteurs, comme elle aurait peut-être dû le faire.
d'un autre côté, on peut souhaiter utiliser cette information pour orienter au mieux une politique de prévention, et il faut voir si l'intérêt public ou la morale s'accommoderont de cette discrimination de facto des citoyens (fût-elle positive).
Les statistiques ont été évoquées à plusieurs reprises dans les tribunaux et dans certains cas impliquées dans des erreurs judiciaires importantes, comme les cas de Sally Clark ou de Lucia de Berk. La formule de Bayes a été soit méconnue soit mal utilisée. Ainsi l'accusation estimait faible voire quasi nulle la probabilité pour un innocent d'être reconnu coupable en de tels cas. Ce n'est qu'après la sentence que des experts protestèrent et démontrèrent que cette probabilité prise en considération n'avait pas de sens et qu'il fallait au contraire étudier celles d'être coupable ou innocent sachant qu'il y a eu décès (ce qui donne des chiffres largement différents laissant place à un doute légitime). Pudiquement, on désigne par sophisme du procureur ces confusions entre probabilités conditionnelles.
