 
# ANOS OMNI — RSAK V1

### Réorganisation Structurelle Adaptative des Connaissances

**Projet de recherche en intelligence artificielle — Mali**

## 1. Présentation

ANOS OMNI RSAK est un prototype expérimental consacré à la gestion adaptative des connaissances par règles.

Le système cherche à détecter les contre-exemples, analyser les contradictions et proposer une réorganisation des règles. Les modifications structurelles nécessitent une validation humaine.

## 2. Fonctionnalités

- Apprentissage incrémental à partir d'exemples.
- Mémorisation des règles et des connaissances.
- Détection des contre-exemples.
- Proposition de réorganisation structurelle.
- Validation ou rejet humain.
- Conservation de l'historique.
- Abstention lorsque les informations sont insuffisantes.
- Sauvegarde JSON.
- Interface web de laboratoire.

## 3. Architecture

```text
ANOS OMNI RSAK V1
│
├── anos_omni_rsak.py
├── test_rsak.py
├── run_demo.py
├── lab_server.py
├── requirements.txt
├── .gitignore
├── README.md
├── research/
│   └── PROTOCOLE_EXPERIMENTAL.md
└── interface/
    └── index.html
```

## 4. Prérequis

- Python 3.10 ou supérieur recommandé.
- Aucune bibliothèque externe nécessaire.
- Navigateur web moderne pour le laboratoire.

## 5. Démonstration en terminal

```bash
python run_demo.py
```

Ou :

```bash
python anos_omni_rsak.py
```

## 6. Lancer le laboratoire web

Depuis le dossier du projet :

```bash
python lab_server.py
```

Puis ouvrir :

```text
http://127.0.0.1:8000
```

L'interface permet de consulter la mémoire, examiner la proposition, approuver ou rejeter une réorganisation et tester des requêtes.

Le serveur est local : il doit rester lancé pendant l'utilisation de l'interface.

## 7. Tests automatiques

```bash
python -m unittest test_rsak -v
```

## 8. Exemple de fonctionnement

Règle initiale :

`wheels = 4 → motorized`

Contre-exemple :

`wheels = 4, engine = false → not_motorized`

Le système détecte une contradiction et peut proposer une séparation selon la présence du moteur.

La réorganisation est appliquée uniquement après validation.

## 9. Protocole scientifique

Le protocole expérimental se trouve dans :

`research/PROTOCOLE_EXPERIMENTAL.md`

Il définit les hypothèses, les approches de comparaison, les indicateurs et les conditions de validation.

## 10. Limites scientifiques

RSAK V1 est un prototype préliminaire.

Sa nouveauté scientifique, ses performances et sa capacité de généralisation ne sont pas encore démontrées. Des expériences reproductibles et des comparaisons avec des méthodes de référence sont nécessaires.

## 11. Auteur

Malet Sidibé

Projet développé au Mali.

## 12. Licence

À définir.
