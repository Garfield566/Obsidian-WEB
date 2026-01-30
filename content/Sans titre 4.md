## Types de vocabulaire (validation de domaine)

| Type            | Nom complet               | Description                                                 | Validation                                            |
| --------------- | ------------------------- | ----------------------------------------------------------- | ----------------------------------------------------- |
| **VSC**         | Valide Si Contexte        | Vocabulaire technique spécifique                            | 1 autre VSC même domaine OU 4 VSCA même domaine       |
| **VSCA**        | Valide Si Contexte Appuyé | Vocabulaire courant/ambigu                                  | 3 autres mots même domaine DONT 1 VSC minimum         |
| **specialized** | Terme spécialisé          | Concept/phénomène spécifique (ex: `massification-scolaire`) | Terme exact OU 90% définition + domaine parent validé |

## Types d'entités (EntityType)

|Type|Description|Exemple|
|---|---|---|
|`PERSON`|Personne|Adam Smith, Durkheim|
|`PLACE`|Lieu géographique|Paris, Alpes|
|`POLITICAL_ENTITY`|Entité politique|France, Empire romain|
|`DISCIPLINE`|Discipline académique|économie, philosophie|
|`CONCEPT`|Concept théorique|anomie, capitalisme|
|`ART_MOVEMENT`|Mouvement artistique|impressionnisme|
|`DATE`|Date/Siècle|XIXe siècle, 1789|
|`OTHER_NAME`|Marques, œuvres, etc.|Netflix, Star Wars|

## Familles de tags (TagFamily)

|Famille|Format|Exemple|
|---|---|---|
|`PERSON`|Tirets entre parties|`Adam-Smith`|
|`GEO`|`geo\...`|`geo\france\paris`|
|`ENTITY`|`entité\...`|`entité\empire-romain`|
|`DATE`|Chiffres romains|`XIXe`|
|`DISCIPLINE`|Hiérarchique|`économie\microéconomie`|
|`CONCEPT_AUTHOR`|`concept\auteur`|`anomie\durkheim`|

C'est bien **specialized** le type pour les termes comme `massification-scolaire` ?