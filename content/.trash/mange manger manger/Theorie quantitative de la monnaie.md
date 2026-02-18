---
nom: "Theorie quantitative de la monnaie"
qid: Q186588
type: theorie_economique
categorie: theorie_economique
tags: "#economie/theorie"
image: https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/20190721_STACKED_warming_stripes_-_all_countries_-_Climate_Lab_Book_%28Ed_Hawkins%29.png/330px-20190721_STACKED_warming_stripes_-_all_countries_-_Climate_Lab_Book_%28Ed_Hawkins%29.png
---

# Série temporelle

Une série temporelle, ou série chronologique, est une suite de valeurs numériques représentant l'évolution d'une quantité spécifique au cours du temps. De telles suites de variables aléatoires peuvent être exprimées mathématiquement afin d'en analyser le comportement, généralement pour comprendre son évolution passée et pour en prévoir le comportement futur. Une telle transposition mathématique utilise le plus souvent des concepts de probabilités et de statistique.

## Utilisation

Les séries temporelles sont considérées à tort comme étant une branche exclusive de l'économétrie. Cette dernière est une discipline qui est relativement jeune alors que les séries temporelles ont été utilisées bien avant, par exemple en astronomie (1906) et en météorologie (1968).

## En Économie

L'objet des séries temporelles est l'étude des variables au cours du temps. Même s'ils n'ont pas été à l'origine de cette discipline, ce sont les économètres qui ont assuré les grandes avancées qu'a connues cette discipline (beaucoup de « Prix Nobel » d'économie sont des économètres). Parmi ses principaux objectifs figurent la détermination de tendances au sein de ces séries ainsi que la stabilité des valeurs (et de leur variation) au cours du temps.
C'est de la déception des prévisions issues des modèles structurels d'inspiration keynésienne qu'est née la théorie des séries temporelles telle qu'on la connaît aujourd'hui. Et sur ce point, c'est la publication de l'ouvrage de Box et Jenkins en 1970 qui a été décisive. En effet, dans l'ouvrage les deux auteurs développent le très populaire modèle ARMA (Auto Regressive Moving Average). Par exemple, pour prévoir le PIB français en 2020, il ne s'agit plus d'utiliser un modèle structurel qui explique le PIB (par l'intermédiaire de la consommation, de l'investissement, des dépenses publiques, du solde commercial, etc.) puis de projeter les tendances passées, mais, avec le modèle ARMA, de prévoir le PIB de 2020 en exploitant les propriétés statistiques du PIB (moyenne, variance etc.). Ce modèle utilise souvent des valeurs retardées du PIB (d'où le terme Auto Regressive) et de chocs aléatoires qui sont en général de moyenne nulle, de variance constante et non autocorrélés (bruit blanc); quand la variable qui représente ces chocs est retardée, on parle de moyenne mobile.
Le modèle ARMA est un cas particulier d'un modèle beaucoup plus général nommé ARIMA (en) où le I désigne Integrated (« Intégrée » en français). En effet, le modèle ARMA ne permet de traiter que les séries dites stationnaires (des moments du premier ordre qui sont invariants au cours du temps). Les modèles ARIMA permettent de traiter les séries non stationnaires après avoir déterminé le niveau d'intégration (le nombre de fois qu'il faut différencier la série avant de la rendre stationnaire).
Bien que possédant d'excellentes qualités prévisionnelles, le modèle ARIMA ou ARMA souffre d'une lacune majeure: il est incapable de traiter simultanément plus d'une variable (série). Par exemple, si les modèles structurels sont capables de répondre à une question telle que: « quel est l'effet de la hausse des taux d'intérêt sur le PIB? », un modèle ARIMA est incapable d'y répondre. Pour contourner ce problème, il faut pouvoir généraliser le modèle ARIMA dans le cas à plusieurs variables. C'est ce qu'a fait en partie Christopher Sims en proposant en 1980 le modèle Vector Auto Regressive (VAR) qui permet de traiter concomitamment plusieurs variables. Mais, contrairement au modèle structurel à plusieurs variables, dans les modèles VAR, toutes les variables sont endogènes. Cette manière de modéliser en faisant abstraction d'une théorie économique a donné naissance à ce que l'on a appelé l'Économétrie sans théorie.
Ces modèles (ARIMA et VAR) ne permettent de traiter que des phénomènes qui sont linéaires ou approximativement (par exemple le PIB) mais ne permettent pas de « capturer » les propriétés des phénomènes qui sont non linéaires (les variables financières par exemple, inflation, cours d'action etc.). Pour prendre en compte à la fois la non-linéarité et la forte variabilité de ces variables, l'économètre américain Robert F. Engle a le premier développé le modèle dit ARCH (Auto Regressive Conditional Heteroscedasticity) en 1982.
