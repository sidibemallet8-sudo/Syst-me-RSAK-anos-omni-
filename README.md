
# ANOS OMNI — RSAK V1

### Réorganisation Structurelle Adaptative des Connaissances

**Projet de recherche en intelligence artificielle — Mali**

## 1. Présentation

ANOS OMNI RSAK est un prototype expérimental qui étudie une approche de gestion adaptative des connaissances.

Son objectif est de permettre à un système fondé sur des règles de détecter des contre-exemples, d'analyser les contradictions et de proposer une réorganisation de ses connaissances.

Les modifications importantes nécessitent une validation humaine.

## 2. Fonctionnalités

- Apprentissage incrémental à partir d'exemples.
- Mémorisation des règles.
- Détection des contre-exemples.
- Proposition de réorganisation structurelle.
- Validation ou rejet humain.
- Conservation de l'historique.
- Abstention lorsque les informations sont insuffisantes.
- Sauvegarde des connaissances au format JSON.

## 3. Architecture

```text
ANOS OMNI RSAK V1
│
├── anos_omni_rsak.py
│   └── Moteur principal RSAK
│
├── test_rsak.py
│   └── Tests automatiques
│
├── README.md
│   └── Documentation
│
└── anos_memory.json
    └── Mémoire générée à l'exécution
```

## 4. Installation

Python 3.10 ou supérieur recommandé.

Aucune bibliothèque externe n'est nécessaire.

## 5. Exécution

Lancer la démonstration :

```bash
python anos_omni_rsak.py
```

Lancer les tests :

```bash
python -m unittest test_rsak -v
```

## 6. Principe expérimental

Exemple :

Une première règle affirme :

`wheels = 4 → motorized`

Le système reçoit ensuite un contre-exemple :

`wheels = 4, engine = false → not_motorized`

Il détecte la contradiction et propose une séparation selon la présence du moteur.

La réorganisation n'est appliquée qu'après validation humaine.

## 7. Statut scientifique

RSAK V1 est un prototype de recherche préliminaire.

Les performances, la nouveauté scientifique et la généralisation de la méthode restent à évaluer par des expériences reproductibles et des comparaisons avec des méthodes de référence.

## 8. Auteur

Malet Sidibé

Projet de recherche développé au Mali.

## 9. Licence

À définir.
