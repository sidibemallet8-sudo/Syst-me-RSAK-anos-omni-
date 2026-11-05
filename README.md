# ANOS OMNI — RSAK V2

## Vision scientifique

**ANOS OMNI RSAK (Réorganisation Structurelle Adaptative des Connaissances)** est un prototype de recherche sur la révision explicable de connaissances symboliques. Il étudie une question précise : lorsqu'une règle rencontre des contre-exemples, peut-on détecter le conflit, proposer une partition plus précise et conserver le contrôle humain sur la modification ?

> **Hypothèse de recherche :** dans des tâches contrôlées de classification symbolique, le classement de propositions par gain d'information et couverture peut aider à produire des révisions de règles plus explicables que l'ajout manuel non structuré d'exceptions, sans dégrader les résultats sur des données de test indépendantes.

Cette hypothèse reste à tester. RSAK V2 est un prototype expérimental : il ne constitue pas un modèle de langage, un système général d'intelligence, un contrôleur robotique, ni un remplacement démontré de ChatGPT, DeepSeek ou d'autres systèmes. La vision à long terme est d'étudier RSAK comme une possible couche de mémoire et de révision auditable pouvant compléter des systèmes d'IA, sous des garanties et évaluations adaptées.

## Contribution proposée (à valider expérimentalement)

Le prototype réunit un cycle de révision explicite :

1. représenter des connaissances par des règles conditionnelles ;
2. enregistrer des exemples et signaler les règles contradictoires ;
3. générer des attributs candidats, les classer par gain d'information empirique pondéré par la couverture ;
4. fournir les exemples justificatifs et les règles candidates ;
5. attendre une décision explicite avant d'archiver la règle parente et d'activer les règles filles ;
6. conserver un historique et permettre la sauvegarde/reprise de l'état.

La nouveauté scientifique n'est pas revendiquée comme établie. La contribution éventuelle devra être déterminée par une revue de littérature, des comparaisons de référence, des résultats reproductibles et une analyse des limites.

## Architecture

- `anos_omni_rsak.py` : moteur symbolique, détection de conflits, requête avec abstention/conflit, classement des révisions, validation humaine et persistance JSON.
- `test_rsak.py` : tests unitaires des cas fonctionnels et des erreurs.
- `run_demo.py` : démonstration terminale (utilise la démonstration du module principal).
- `lab_server.py` et `interface/index.html` : laboratoire web local existant.
- `research/PROTOCOLE_EXPERIMENTAL.md` : protocole de validation proposé.

## Installation et exécution

Prérequis : Python 3.10+ ; aucune dépendance externe nécessaire.

```bash
python -m unittest test_rsak -v
python anos_omni_rsak.py
```

Pour le laboratoire web local :

```bash
python lab_server.py
```

Puis ouvrir `http://127.0.0.1:8000`. Le serveur est conçu pour un usage local de démonstration, pas pour être exposé sur Internet.

## Exemple

Règle initiale : `wheels = 4 → motorized`.

Deux observations :

- `wheels = 4, engine = true → motorized`
- `wheels = 4, engine = false → not_motorized`

Le moteur peut proposer une séparation selon `engine`, avec les exemples justificatifs, la couverture et le gain d'information. Une proposition n'est pas une vérité : l'opérateur doit l'examiner et valider ou rejeter. Après validation, une requête sans valeur de `engine` s'abstient plutôt que d'inventer une conclusion.

## Limites et sécurité

- Les attributs et conclusions sont symboliques et doivent être fournis sous forme structurée ; aucune compréhension de texte libre n'est implémentée.
- Le score est un outil heuristique de classement, pas une probabilité ni une mesure de confiance calibrée.
- Une proposition peut surapprendre les exemples observés ; il faut l'évaluer sur des données indépendantes.
- Les règles sont simples ; le moteur ne gère pas causalité, logique temporelle, incertitude probabiliste ou contraintes complexes.
- Le prototype n'est pas certifié pour la santé, la finance, la sécurité ou le contrôle d'un robot. Ne pas connecter ses décisions à des actions physiques critiques.
- L'historique JSON n'est pas une base sécurisée multi-utilisateur ; ne pas y stocker de données sensibles.

## Feuille de route

1. établir une revue de littérature et définir précisément la contribution par rapport aux systèmes de révision de règles existants ;
2. créer des jeux synthétiques reproductibles avec bruit, attributs manquants et dérive de concept ;
3. comparer RSAK à des règles statiques, une approche par exceptions et une révision manuelle, avec séparation apprentissage/validation/test ;
4. mesurer exactitude, couverture, abstention, conflits non résolus, nombre de règles, coût de révision et stabilité ;
5. publier les données, scripts, versions et résultats, y compris les résultats négatifs ;
6. seulement ensuite étudier l'intégration comme couche consultative d'un assistant ou d'un robot en simulation, avec garde-fous indépendants.

## Auteur et statut

Projet de recherche expérimental développé au Mali par Malet Sidibé. Licence à définir. Les résultats scientifiques restent à établir.
