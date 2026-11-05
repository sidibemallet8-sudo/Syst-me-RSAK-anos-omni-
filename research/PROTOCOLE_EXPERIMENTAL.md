# PROTOCOLE EXPÉRIMENTAL — ANOS OMNI RSAK V2

## 1. Statut et objectif

Ce document décrit un protocole à exécuter ; il ne rapporte pas des résultats déjà obtenus. RSAK V2 est un prototype de révision explicable de règles. L'objectif est de mesurer dans des tâches symboliques contrôlées si sa génération et son classement de propositions apportent un avantage mesurable par rapport à des méthodes de référence.

## 2. Question et hypothèses

**Question :** lorsqu'une règle générale rencontre des contre-exemples, RSAK peut-il produire une révision plus précise et interprétable, qui améliore les décisions sur des observations indépendantes sans créer une complexité excessive ?

- H1 : une réorganisation validée réduit les erreurs de classification sur le test indépendant par rapport à la règle statique.
- H2 : le classement par gain d'information/couverture sélectionne une caractéristique discriminante aussi bien ou mieux que des choix aléatoires et des règles d'exception simples.
- H3 : l'abstention réduit les réponses incorrectes dans les cas où les attributs nécessaires sont absents, au prix d'une couverture plus faible.

Ces hypothèses ne sont pas garanties et doivent être analysées avec intervalles d'incertitude et résultats négatifs inclus.

## 3. Comparateurs

Comparer sur les mêmes partitions :

1. règle statique, sans adaptation ;
2. règle avec exceptions ajoutées selon une procédure prédéfinie ;
3. révision manuelle par un annotateur selon des consignes documentées ;
4. RSAK avec validation humaine ;
5. baseline aléatoire pour le choix de l'attribut, si plusieurs attributs candidats existent.

Décrire exactement chaque baseline et éviter de donner à RSAK accès à des informations indisponibles aux comparateurs.

## 4. Jeux de données et protocole

Commencer avec des données synthétiques générées par des scripts versionnés : variables discriminantes, variables corrélées non causales, valeurs manquantes, exemples bruités et scénarios de dérive. Ajouter ensuite, si possible, des données publiques adaptées et documenter leur licence.

Séparer les exemples en apprentissage, validation et test indépendant. Seuls apprentissage et validation peuvent influencer les règles ou le choix de proposition. Le test ne doit jamais être utilisé pour construire ou réviser des règles. Répéter avec plusieurs graines al��atoires et publier les graines, distributions et paramètres.

## 5. Variables et indicateurs

Mesurer au minimum :

- exactitude et taux d'erreur sur le test ;
- couverture (part des requêtes auxquelles une réponse est fournie) ;
- taux d'abstention ;
- nombre et taux de conflits non résolus ;
- nombre de règles avant/après révision ;
- coût de révision (propositions examinées, décisions et temps humain si mesuré) ;
- stabilité des règles sur les graines et partitions ;
- qualité de l'explication : présence de l'attribut, des exemples justificatifs et des alternatives.

Présenter les résultats avec dénominateurs, intervalles d'incertitude et résultats par scénario. Ne pas résumer la performance par un score propriétaire non comparé.

## 6. Procédure

1. Fixer les règles initiales et la génération des données avant les essais.
2. Séparer les partitions et enregistrer leurs empreintes/version.
3. Apprendre uniquement sur la partition d'entraînement.
4. Choisir les paramètres sur validation, sans consulter le test.
5. Générer et enregistrer les propositions RSAK, y compris les rejets.
6. Appliquer les validations selon une règle humaine prédéfinie et documentée.
7. Évaluer une seule fois les modèles/règles finalisés sur le test.
8. Répéter et publier le code, la configuration, les journaux anonymisés et les résultats.

## 7. Critères d'interprétation

Une amélioration est intéressante seulement si elle se reproduit sur les tests indépendants, reste robuste aux données manquantes/bruitées et ne repose pas sur une hausse incontrôlée du nombre de règles. Les résultats doivent inclure le compromis couverture/erreur et les coûts humains. Une réussite sur le seul exemple des quatre roues ne constitue pas une preuve de généralisation.

## 8. Reproductibilité et limites

Archiver version du code, paramètres, données ou générateur, graines, règles initiales, exemples d'apprentissage, propositions, décisions et sorties de test. Ne pas exposer de données personnelles. Le prototype actuel n'est ni un modèle de langage ni un contrôleur de robot. Toute exploration robotique doit commencer en simulation et conserver des mécanismes de sécurité indépendants ; RSAK ne doit pas décider seul d'actions physiques critiques.

## 9. Conclusion

Ce protocole vise à transformer une intuition de conception en hypothèses réfutables. La valeur scientifique d'ANOS OMNI RSAK dépendra des comparaisons, de la reproductibilité, de la revue de littérature et de la capacité à reconnaître ses échecs autant que ses réussites.
