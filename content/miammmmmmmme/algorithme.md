---
nom: "algorithme"
qid: Q8366
type: concept
categorie: concept
tags: "#concept"
image: https://commons.wikimedia.org/wiki/Special:FilePath/Euclid_flowchart_1.png
---

# Algorithme

> [!Infobox]
> **Algorithme**
> ![[https://commons.wikimedia.org/wiki/Special:FilePath/Euclid_flowchart_1.png|300]]
> - **Nomme d'apres** : Al-Khawarizmi
> - **Partie de** : informatique, algorithmique, mathématiques
> - **Caractérisé par** : complexité algorithmique
> - **Shape Expression de cette classe** : Q
> - **Discipline dont c'est l'objet** : théorie du calcul, analyse de la complexité des algorithmes, science de l'information, théorie de la complexité

Un algorithme est une suite finie et non ambiguë d'instructions et d'opérations permettant de résoudre une classe de problèmes.
Le domaine qui étudie les algorithmes est appelé l'algorithmique. On retrouve aujourd'hui des algorithmes dans de nombreuses applications informatiques, dont dans les systèmes permettant le fonctionnement des ordinateurs, la cryptographie, le routage d'informations, la planification et l'utilisation optimale des ressources, le traitement d'images, le traitement de textes, la bio-informatique, l'intelligence artificielle, l'automatique, etc.
L'algorithme peut être mis en forme de façon graphique dans un algorigramme ou organigramme de programmation.

## Étymologie et histoire

Le mot algorithme a une longue histoire.
'Al-Khwârizmî (en arabe: الخوارزمي) est un mathématicien persan du IXe siècle, dont le nom est relatif au Khwarezm, une région située au Sud de la mer d'Aral. Le traité qu'il écrivit en arabe, au IXe siècle, sera traduit en latin au XIIe siècle, sous le titre Algoritmi de numero Indorum. "Algoritmie des nombres indiens". Algoritmie est la latinisation de son nom par les traducteurs: Alchoarismi puis Algorismi, Algorismo, Algoritmi. 
Un de ses ouvrages, Abrégé du calcul par la restauration et la comparaison, a d'ailleurs donné son nom à l'algèbre. Le titre de la traduction par Gilbert de Cremone en latin est Liber Maumeti filii Moysi Alchoarismi de Algebra et Almuquabala. On y retrouve traduit son nom: Maumeti filii Moysi Alchoarismi (Muhammad Ben Musa al Kwuwarizmi) et le fameux Alchoarismi.
Joannes Sacrobosco, moine ayant étudié à Oxford, est reçu à l'université de la Sorbonne le 5 juin 1221 et élu professeur de Quadrivium peu après. C'est vers cette date qu'il compose De Algorismo. Il est l'un des premiers docteurs du Moyen Âge à utiliser les écrits astronomiques des Arabes, considéré d'ailleurs en Angleterre comme ayant introduit l'usage des « chiffres » (sifer) que le pape Sylvestre II avait tenté en vain de répandre plus tôt.
En 1240, Alexandre de Villedieu écrit son Carmen de Algorismo sur la science des chiffres.
Algoritmie désigne alors aussi ce nouveau système de numération, le système de numération de position avec le zéro.
Sous l'influence de l'ancien espagnol algorismo, le mot apparaît aussi en français déjà vers 1230 sous la forme augorisme, puis algorisme au XIIIe siècle, pour désigner le calcul en chiffres, l'arithmétique. La forme moderne du terme reprend le latin médiéval algorithmus, altération influencée par arithmetica et d'autres, du grec ancien arithmos = nombre.
En 1842, Ada Lovelace écrit le premier algorithme de programmation de l'histoire. Elle le fait à partir de la machine analytique de Babbage et devient la première informaticienne de l'humanité.

## Définition générale

Un algorithme est une méthode générale pour résoudre un type de problèmes. Il est dit correct lorsque, pour chaque instance du problème, il se termine en produisant la bonne sortie, c'est-à-dire qu'il résout le problème posé.
L'efficacité d'un algorithme est mesurée notamment par:

sa durée de calcul (en partant du principe que chaque instruction a un temps d'exécution constant);
sa consommation de mémoire vive;
la précision des résultats obtenus (par exemple avec l'utilisation de méthodes probabilistes);
sa scalabilité;
sa parallélisation;
son ergonomie et en particulier sa contrôlabilité son introspectabilité;
sa robustesse, résilience ou antifragilité au bruit, aux chocs et en particulier l'émergence et le chaos;
Les ordinateurs sur lesquels s'exécutent ces algorithmes ne sont pas infiniment rapides, car le temps de machine reste une ressource limitée, malgré une augmentation constante des performances des ordinateurs. Un algorithme sera donc dit performant s'il utilise avec parcimonie les ressources dont il dispose, c'est-à-dire le temps de processeur, la mémoire vive et, objet de recherches récentes, la consommation électrique. L'analyse de la complexité des algorithmes permet de décrire l'évolution en temps calcul nécessaire pour amener un algorithme à son terme, lorsque la quantité de données à traiter grandit.

L'émergence des langages de niveaux supérieurs pose le problème du temps:

soit on passe du temps à programmer avec des langages de bas niveau (le programme est alors rapide);
soit on utilise des langages de haut niveau où une instruction est déjà constituée de plusieurs instructions de base. Le temps d'utilisation de la machine augmente alors de façon importante.
L'algorithme composé de boites peut ainsi être plus ou moins détaillé, précis.

## Quelques définitions connexes

Donald Knuth (1938-) liste, comme prérequis d'un algorithme, cinq propriétés:

finitude: « un algorithme doit toujours se terminer après un nombre fini d'étapes »;
définition précise: « chaque étape d'un algorithme doit être définie précisément, les actions à transposer doivent être spécifiées rigoureusement et sans ambiguïté pour chaque cas »;
entrées: « quantités qui lui sont données avant qu'un algorithme ne commence. Ces entrées sont prises dans un ensemble d'objets spécifié »;
sorties: « quantités ayant une relation spécifiée avec les entrées »;
rendement: « toutes les opérations que l'algorithme doit accomplir doivent être suffisamment basiques pour pouvoir être en principe réalisées dans une durée finie par un homme utilisant un papier et un crayon ».
George Boolos (1940-1996), philosophe et mathématicien, propose la définition suivante:

« Des instructions explicites pour déterminer le nième membre d'un ensemble, pour n un entier arbitrairement grand. De telles instructions sont données de façon bien explicite, sous une forme qui puisse être utilisée par une machine à calculer ou par un humain qui est capable de transposer des opérations très élémentaires en symboles. »
Gérard Berry (1948-), chercheur en science informatique, en donne la définition grand public suivante:

« Un algorithme, c'est tout simplement une façon de décrire dans ses moindres détails comment procéder pour faire quelque chose. Il se trouve que beaucoup d'actions mécaniques, toutes probablement, se prêtent bien à une telle décortication. Le but est d'évacuer la pensée du calcul, afin de le rendre exécutable par une machine numérique (ordinateur…). On ne travaille donc qu'avec un reflet numérique du système réel avec qui l'algorithme interagit. »
Les entrées sont généralement associées à des capteurs et les sorties à des actions, actionneurs ou opérateurs (affichage, moteur, etc.).

## Algorithmes numériques

Les algorithmes sont des objets historiquement dédiés à la résolution de problèmes arithmétiques, comme la multiplication de deux nombres. Ils ont été formalisés bien plus tard avec l'avènement de la logique mathématique et l'émergence des machines qui permettaient de les mettre en œuvre, à savoir les ordinateurs.

## Algorithmes non numériques

La plupart des algorithmes ne sont pas numériques.
On peut distinguer:

des algorithmes généralistes qui s'appliquent à toute donnée numérique ou non numérique: par exemple les algorithmes liés au chiffrement, ou qui permettent de les mémoriser ou de les transmettre;
des algorithmes dédiés à un type de données particulier (par exemple ceux liés au traitement d'images).
Voir aussi: Liste de sujets généraux sur les algorithmes (en)

## Algorithmes dans la vie quotidienne

L'algorithmique intervient de plus en plus dans la vie quotidienne.

Une recette de cuisine peut être réduite à un algorithme si on peut réduire sa spécification aux éléments constitutifs:
des entrées (les ingrédients, le matériel utilisé);
des instructions élémentaires simples (frire, flamber, rissoler, braiser, blanchir, etc.) dont les exécutions dans un ordre précis amènent au résultat voulu;
un résultat: le plat préparé.
Cependant, les recettes de cuisine ne sont en général pas présentées rigoureusement sous forme non ambiguë: il est d'usage d'y employer des termes vagues laissant une liberté d'appréciation à l'exécutant alors qu'un algorithme non probabiliste stricto sensu doit être précis et sans ambiguïté.
Le tissage, surtout tel qu'il a été automatisé par le métier Jacquard, est une activité que l'on peut dire algorithmique.
Le tricot est enseigné parfois comme éveil aux algorithmes: les machines à tricoter des années 1980 fonctionnaient avec des cartes perforées.
Un casse-tête, comme le Rubik's Cube, peut être résolu de façon systématique par un algorithme qui mécanise sa résolution.
En sport, l'exécution de séquences répondant à des finalités d'attaque, de défense, de progression, correspond à des algorithmes (dans un sens assez lâche du terme). Voir en particulier l'article tactique (football).
En soins infirmiers, le jugement clinique est assimilable à un algorithme. Le jugement clinique désigne l'ensemble des procédés cognitifs et métacognitifs qui aboutissent au diagnostic infirmier. Il met en jeu des processus de pensée et de prise de décision dans le but d'améliorer l'état de santé et le bien-être des personnes que les soignants accompagnent.
Un code juridique, qui décrit un ensemble de procédures applicables à un ensemble de cas, est un algorithme.
Les procédures de dépannage sont des algorithmes.
Le montage/démontage d'un meuble
Les progrès de ce qu'on appelle l'intelligence artificielle s'appuient sur un algorithmique de plus en plus complexe qui devient l'un des rouages cachés du Web 2.0 et des grands réseaux sociaux.

## Critiques

Dans la vie quotidienne, un glissement de sens s'est opéré, ces dernières années, dans le concept d'« algorithme » qui devient à la fois plus réducteur, puisque ce sont pour l'essentiel des algorithmes de gestion du big data, et d'autre part plus universel en ce sens qu'il intervient dans tous les domaines du comportement quotidien[réf. incomplète]. La famille des algorithmes dont il est question effectue des calculs à partir de grandes masses de données (les big data). Ils réalisent des classements, sélectionnent des informations et en déduisent un profil, en général de consommation, qui est ensuite utilisé ou exploité commercialement. Les implications sont nombreuses et touchent les domaines les plus variés. Mais les libertés individuelles et collectives pourraient être finalement mises en péril, comme le montre la mathématicienne américaine Cathy O'Neil dans le livre Weapons of Math Destruction, publié en 2016 et sorti en français en 2018 sous le titre Algorithmes: la bombe à retardement (aux éditions Les Arènes).

« Aujourd'hui, les modèles mathématiques et les algorithmes prennent des décisions majeures, servent à classer et catégoriser les personnes et les institutions, influent en profondeur sur le fonctionnement des États sans le moindre contrôle extérieur. Et avec des effets de bords incontrôlables. […] Il s'agit d'un pouvoir utilisé contre les gens. Et pourquoi ça marche? Parce que les gens ne connaissent pas les maths, parce qu'ils sont intimidés. C'est cette notion de pouvoir et de politique qui m'a fait réaliser que j'avais déjà vu ça quelque part. La seule différence entre les modèles de risque en finances et ce modèle de plus-value en science des données, c'est que, dans le premier cas, en 2008, tout le monde a vu la catastrophe liée à la crise financière. Mais, dans le cas des profs, personne ne voit l'échec. Ça se passe à un niveau individuel. Des gens se font virer en silence, ils se font humilier, ils ont honte d'eux. »

Dans cet ouvrage, l'auteure alerte le lecteur sur les décisions majeures que nous déléguons aujourd'hui aux algorithmes dans des domaines aussi variés que l'éducation, la santé, l'emploi et la justice, sous prétexte qu'ils sont neutres et objectifs, alors que, dans les faits, ils donnent lieu à « des choix éminemment subjectifs, des opinions, voire des préjugés insérés dans des équations mathématiques ».
La notion de bulle de filtre (ou filter bubble en anglais), popularisée par Eli Pariser, désigne l'effet des algorithmes de personnalisation utilisés par les plateformes en ligne qui isolent les utilisateurs dans une sorte de bulle en leur proposant des contenus correspondant à leurs préférences et croyances antérieures. En d'autres termes, l'exposition à des informations et opinions diversifiées est limitée, ayant pour conséquence de renforcer les biais cognitifs et les visions préexistantes de la réalité. Les auteurs J. Farchy et S. Tallec ont analysé l'impact de ces bulles de filtre sur la découverte de contenus culturels, tels que les films ou la musique. Leur étude révèle que, dans un environnement où les algorithmes favorisent la personnalisation au détriment de la diversité, la diversité culturelle est menacée.
L'opacité des algorithmes est l'une des raisons principales de ces critiques. Une meilleure information sur leur mode de fonctionnement spécifique permettrait de rendre plus clair le "contrat social passé entre les internautes et les calculateurs". La description pour chaque algorithme de son propre principe de classement de l'information aide l'utilisateur à mieux comprendre les choix proposés par l'algorithme et les résultats obtenus.

## Morale, responsabilité et agents artificiels

Depuis les années 2000, l'usage croissant d'algorithmes dans des domaines variés (publicité, politique, services numériques) soulève des questions éthiques et sociétales. Souvent perçus comme des « boîtes noires », ces systèmes automatisés influencent les comportements individuels sans que leurs mécanismes internes soient toujours compréhensibles ou transparents.

Des philosophes comme Wendell Wallach et Colin Allen ont interrogé la capacité de ces systèmes à prendre des décisions à portée morale, introduisant la notion d'« agents moraux artificiels »: des systèmes qui, sans être imputables comme les humains, peuvent néanmoins avoir un impact éthique significatif. Dans cette lignée, Martin Gibert insiste sur le rôle central de la programmation dans les choix moraux intégrés aux algorithmes: « Quelles règles implanter dans les robots, et comment le faire? »
« Les agents moraux artificiels (AMA) ne sont pas cependant des agents moraux au sens fort du terme. Contrairement aux humains, ils ne semblent pas imputables [sic] de leurs actes. Ils n'ont toutefois pas besoin de l'être pour prendre des décisions moralement significatives et soulever tout un tas de questions en éthique des algorithmes. »

## Reproduction des inégalités et biais structurels

Une approche sociologique des technologies algorithmiques, portée notamment par les chercheur·e·s en Science and Technology Studies (STS), met en lumière la manière dont ces systèmes s'inscrivent dans des dynamiques sociales complexes. Loin d'être le produit d'intentions malveillantes ou de détournements délibérés, les biais et discriminations générés par ces technologies résultent de processus collectifs de conception, d'entraînement et de déploiement, façonnés par des structures sociales inégalitaires et des jeux d'acteurs aux intérêts multiples, parfois contradictoires.
Les données mobilisées pour entraîner ces systèmes sont elles-mêmes issues de contextes marqués par des rapports sociaux — qu'ils soient raciaux, genrés ou économiques. En l'absence d'une analyse rigoureuse de ces structures, les technologies algorithmiques tendent à reproduire et amplifier les inégalités existantes, non par malveillance, mais parce qu'elles sont conçues et mises en œuvre dans un environnement social traversé par des normes, des hiérarchies et des logiques d'exclusion. Ce phénomène renvoie à ce que certain·e·s nomment le façonnement sociotechnique des technologies: les algorithmes ne sont pas neutres, ils sont le produit de choix techniques influencés par des pratiques professionnelles, des logiques économiques, des imaginaires sociaux et des contraintes institutionnelles.

Ainsi, les algorithmes incarnent une forme de priorisation de ce qui est techniquement exécutable, au détriment de la complexité sociale et humaine. Les décisions intégrées dans les modèles — que ce soit dans la sélection des données, les critères de classification, ou la manière dont les sorties sont interprétées — résultent de compromis entre acteurs (développeurs, entreprises, institutions) aux intérêts et responsabilités parfois flous ou dispersés. " L'idée selon laquelle un simple accroissement des données pourrait éliminer les biais ignore ce point fondamental: les données ne sont pas neutres, elles sont le reflet de réalités sociales déjà marquées par des inégalités. " Un exemple marquant concerne les systèmes de reconnaissance d'images, tels que Google Cloud Vision ou Amazon Rekognition, qui attribuent davantage d'étiquettes liées à l'apparence aux femmes (« fille », « présentatrice télé »), tandis que les hommes se voient associés à des fonctions ou statuts (« homme d'affaires », « gentleman »). Ce constat ne relève pas d'une intention sexiste des programmeurs, mais d'un apprentissage à partir de données historiquement genrées, elles-mêmes issues de contextes où les rôles sociaux sont inégalement répartis. En ce sens, ces technologies renforcent des stéréotypes en les répliquant, sous couvert de neutralité technique.
Il est donc essentiel de comprendre que les technologies algorithmiques ne « créent » pas les inégalités, mais qu'elles opèrent comme des amplificateurs de dynamiques sociales existantes. Leur prétendue objectivité masque en réalité leur ancrage dans des environnements sociohistoriques inégalitaires. Les processus techniques ne sont jamais isolés: ils prennent forme à travers des chaînes de décisions, des arbitrages politiques, économiques et normatifs, et des formes de rationalisation qui occultent, volontairement ou non, les implications sociales de ces choix.
Finalement, penser les algorithmes exige une réflexion qui dépasse la technique: il s'agit de comprendre les conditions sociales de production des technologies, les rapports sociaux qui les traversent, et les effets sociaux qu'elles produisent. Sans cela, les tentatives de "corriger" les biais risqueraient de rester superficielles, et les inégalités de continuer d'être inscrites dans des systèmes perçus comme neutres ou universels.

## Instrumentalisation et détournement algorithmique

Au-delà des biais involontaires, les algorithmes peuvent aussi être intentionnellement détournés à des fins idéologiques ou politiques. En juillet 2024, une étude de l'Institute for Strategic Dialogue a révélé que certains utilisateurs de TikTok affiliés à l'extrême droite manipulaient l'algorithme de recommandation de la plateforme pour diffuser, de manière dissimulée, des discours d'Adolf Hitler. En insérant des extraits entre des séquences musicales ou des contenus populaires, ces comptes contournent les mécanismes de modération tout en exploitant les logiques de viralité du système.
Ces pratiques illustrent une tendance plus large: les algorithmes, loin d'être neutres, participent activement à la structuration de l'espace public numérique. Qu'il s'agisse de biais involontaires ou d'instrumentalisation délibérée, les enjeux éthiques, sociaux et politiques liés à leur usage appellent à une réflexion collective sur leur conception et leur gouvernance.
