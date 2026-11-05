# ANOS OMNI — RSAK V2

## Vision scientifique

**RSAK (Réorganisation Structurelle Adaptative des Connaissances)** est un prototype de recherche sur la révision contrôlée de connaissances symboliques. Il étudie une question limitée et testable : lorsqu'une règle rencontre des contre-exemples, peut-on détecter le conflit, proposer des partitions explicables des exemples et soumettre ces révisions à une validation explicite ?

À long terme, cette approche pourrait être étudiée comme une couche complémentaire de mémoire et de contrôle pour des systèmes d'IA ou de robotique. **RSAK n'est pas aujourd'hui un modèle de langage, un système robotique, ni un remplacement démontré de ChatGPT, DeepSeek ou d'autres modèles.** La version actuelle manipule des règles structurées et des exemples fournis explicitement.

## Contribution proposée (à évaluer, pas à revendiquer comme acquise)

Le projet propose d'expérimenter un cycle de révision auditable :

1. représenter des règles explicites et leurs conditions ;
2. enregistrer des exemples étiquetés et détecter les désaccords avec les règles actives ;
3. chercher plusieurs attributs observés qui séparent les conclusions ;
4. classer les partitions candidates par un score heuristique transparent ;
5. expliquer la proposition et préserver l'état initial jusqu'à validation humaine ;
6. conserver les propositions, décisions et résultats dans un historique et un snapshot JSON.

Le score de classement **n'est ni une probabilité ni une mesure de confiance**. Une séparation parfaite sur les exemples mémorisés ne démontre pas la généralisation à de nouvelles données.

## Fonctionnalités V2

- Moteur Python sans dépendances externes.
- Règles à conditions exactes, conclusions symboliques et archivage des parents révisés.
- Détection et journalisation des exemples contradictoires.
- Réponses `ANSWER`, `CONFLICT` ou `ABSTENTION`, avec identifiants des règles explicatives.
- Génération de plusieurs propositions candidates, triées de façon déterministe.
- Justification textuelle, support observé et composantes du score heuristique.
- Validation ou rejet explicite ; rejet sans modification de la règle parent.
- Validation d'entrées et refus des identifiants inconnus.
- Sauvegarde JSON atomique et rechargement avec version de schéma.

## Démarrage

Prérequis : Python 3.10+.

```bash
python run_demo.py
python -m unittest test_rsak -v
python lab_server.py
```

Le laboratoire web est accessible localement à `http://127.0.0.1:8000`.

## Exemple conceptuel

Règle générale : `wheels = 4 → motorized`.

Exemples observés :

- `wheels = 4, engine = true → motorized`
- `wheels = 4, engine = false → not_motorized`

RSAK peut proposer une partition selon `engine`. L'humain décide si la proposition doit être appliquée. Cet exemple illustre le mécanisme ; il ne constitue pas une preuve de performance ou de nouveauté scientifique.

## API minimale du moteur

```python
from anos_omni_rsak import AnosOmniRSAK

engine = AnosOmniRSAK()
rule_id = engine.add_rule({"wheels": 4}, "motorized")
engine.add_example({"wheels": 4, "engine": True}, "motorized")
engine.add_example({"wheels": 4, "engine": False}, "not_motorized")

candidates = engine.propose_reorganizations(rule_id)
# Examiner la justification puis décider explicitement :
if candidates:
    engine.validate(candidates[0]["id"], approved=True)

print(engine.query({"wheels": 4, "engine": False}))
engine.save("anos_memory.json")
```

`propose_reorganization(rule_id)` reste disponible pour obtenir uniquement le candidat le mieux classé.

## Limites actuelles et sécurité

- Les conditions sont des égalités exactes sur des attributs JSON ; il n'y a pas de compréhension du langage naturel, de perception ou de raisonnement probabiliste.
- Les exemples et attributs sont supposés fiables et correctement étiquetés. Le système n'est pas résistant au bruit, aux biais ou aux données adversariales.
- Le score sert uniquement à ordonner des candidats construits à partir des données observées. Il ne garantit ni précision future ni sûreté.
- Les exemples de faible taille peuvent produire des règles surajustées.
- L'historique est en mémoire ; le snapshot JSON n'est pas chiffré ni conçu pour des données sensibles ou un usage multi-utilisateur.
- Le serveur du laboratoire est une démonstration locale, pas une API de production.
- Ne pas connecter ce prototype à un robot réel ni à une décision critique sans analyse de risques, simulation, garde-fous indépendants et validation experte.

## Feuille de route de recherche

1. **Formaliser** les définitions de conflit, pertinence d'exemple et qualité de partition.
2. **Comparer** RSAK à des règles statiques, exceptions, révision manuelle et méthodes standard d'arbres de décision.
3. **Séparer** apprentissage, réglage et test indépendant ; répéter les expériences avec graines et jeux de données publiés.
4. **Mesurer** exactitude, couverture, abstention, contradictions résiduelles, complexité (nombre de règles), coût de révision, stabilité et rétention des règles utiles.
5. **Tester les ablations** : sans classement, sans validation humaine, un seul candidat, et différentes tailles/bruits de données.
6. **Évaluer les risques** d'étiquettes erronées, données contradictoires, valeurs manquantes et propositions dangereuses avant toute intégration robotique.
7. **Publier les résultats négatifs aussi**, les jeux de données, scripts, versions et limites afin de rendre l'étude reproductible.

Une contribution scientifique pourra être revendiquée seulement après comparaison reproductible, analyse des limites et examen par la communauté. À ce stade, RSAK est un prototype et un programme expérimental.

## Structure

```text
anos_omni_rsak.py                 Moteur symbolique
run_demo.py                       Démonstration terminal
lab_server.py                     Serveur local de démonstration
interface/index.html              Interface du laboratoire
test_rsak.py                      Tests unitaires
research/PROTOCOLE_EXPERIMENTAL.md Protocole reproductible
```

## Auteur et licence

Malet Sidibé — projet de recherche développé au Mali.
Licence à définir.
