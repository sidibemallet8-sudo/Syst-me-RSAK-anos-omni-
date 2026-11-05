# PROTOCOLE EXPÉRIMENTAL — ANOS OMNI RSAK V2

## 1. Statut et objectif

Ce protocole définit comment évaluer le prototype RSAK, un mécanisme déterministe de détection de contradictions et de proposition de partitions de règles. Il ne présume pas que RSAK est supérieur aux méthodes existantes. L'objectif est de produire des résultats reproductibles, y compris si l'hypothèse est infirmée.

Question de recherche : **dans quels scénarios, s'il y en a, une révision de règles guidée par des contre-exemples et soumise à validation améliore-t-elle la qualité des prédictions ou leur auditabilité par rapport à des méthodes de référence ?**

## 2. Hypothèses falsifiables

- H1 : sur des tâches synthétiques où une variable cachée/discriminante est présente et correctement observée, RSAK peut produire une partition cohérente avec les exemples d'entraînement.
- H2 : l'approbation d'une proposition n'améliore la performance sur données indépendantes que lorsque les attributs candidats restent pertinents dans le test.
- H3 : l'abstention et la validation humaine réduisent certaines erreurs non résolues, au prix possible d'une couverture ou d'un coût de révision plus faible.

Chaque hypothèse devra être accompagnée de critères de succès préenregistrés. Une démonstration sur un exemple construit ne suffit pas à valider ces hypothèses.

## 3. Méthodes de référence

Comparer, sur les mêmes partitions et données :

1. règles statiques, sans adaptation ;
2. règle avec exception ajoutée manuellement ;
3. révision manuelle par un opérateur selon un guide documenté ;
4. arbre de décision standard, avec paramètres réglés uniquement sur validation ;
5. RSAK avec propositions classées et validation ;
6. ablations RSAK : candidat unique/non classé, absence d'explication, ou absence de validation (simulation seulement).

Ne pas comparer les méthodes sur des données différentes ni sélectionner après coup les cas favorables à RSAK.

## 4. Jeux de données et séparation

Commencer par des données synthétiques contrôlées avec règle génératrice connue, plusieurs attributs corrélés, valeurs manquantes, bruit d'étiquetage et différents taux de contre-exemples. Compléter ensuite par des jeux de données publics adaptés à la tâche, avec licences vérifiées.

Séparer les observations en apprentissage, validation et test indépendant. Aucun exemple de test ne doit intervenir dans la génération, le classement ou la validation des propositions. Documenter les graines aléatoires, les transformations, les critères d'exclusion et les versions.

## 5. Procédure

Pour chaque dataset et graine :

1. créer les règles initiales uniquement à partir du protocole prédéfini ;
2. fournir les exemples d'apprentissage et enregistrer les conflits détectés ;
3. générer les candidats RSAK et conserver l'ensemble des propositions, scores et explications ;
4. faire approuver/rejeter les propositions par les évaluateurs selon des critères préétablis, ou mesurer séparément l'oracle simulé ;
5. exécuter toutes les méthodes sur le test indépendant ;
6. répéter sur plusieurs graines, tailles de données et niveaux de bruit ;
7. rapporter tous les scénarios, y compris les échecs et abstentions.

Pour une évaluation humaine, définir le nombre et le profil des évaluateurs, randomiser l'ordre si possible, mesurer l'accord inter-évaluateurs et distinguer leurs décisions des résultats automatiques.

## 6. Mesures

- exactitude, précision/rappel ou F1 selon la tâche ;
- couverture et taux d'abstention ;
- taux de conflits non résolus ;
- performance conditionnelle aux prédictions émises ;
- nombre de règles, profondeur et taille des conditions ;
- nombre de propositions, proportion acceptée et coût humain ;
- rétention des exemples antérieurement corrects ;
- stabilité des partitions entre graines et petits changements des données ;
- taux de propositions invalides ou dangereuses dans les scénarios contrôlés.

Le `heuristic_score` actuel est un rang interne, pas une probabilité calibrée. Ne pas l'évaluer comme une confiance statistique.

## 7. Analyse et critères

Publier les résultats agrégés avec dispersion/incertitude et résultats par sous-groupe/scénario. Préenregistrer les métriques principales, les comparaisons et les exclusions. Toute conclusion de supériorité devra être limitée aux tâches, jeux et conditions étudiés et étayée par des tests indépendants.

Une proposition est considérée utile uniquement si elle améliore les critères prédéfinis sur test indépendant sans dégradation inacceptable de couverture, complexité, rétention ou sécurité. Définir les seuils avant l'expérience.

## 8. Reproductibilité et éthique

Archiver code/version, configuration, données ou instructions d'accès, graines, règles initiales, exemples d'apprentissage, propositions, décisions humaines, métriques et environnement d'exécution. Ne pas publier de données personnelles sans base légale et protections appropriées. Documenter les biais possibles et les limites de généralisation.

## 9. Sécurité robotique

Une expérience robotique future doit commencer en simulation, puis en environnement contrôlé avec supervision et arrêt d'urgence. RSAK ne doit pas autoriser seul la modification de règles de sécurité ou l'exécution d'actions physiques. Exiger validation indépendante, contraintes de sécurité non modifiables par RSAK et analyse de risques avant tout essai matériel.

## 10. Limites et statut

RSAK V2 reste un prototype à règles exactes. Il ne démontre pas l'intelligence générale, l'apprentissage autonome à grande échelle, la supériorité sur les modèles de langage ni la sûreté robotique. Les résultats restent à établir par les expériences ci-dessus.
