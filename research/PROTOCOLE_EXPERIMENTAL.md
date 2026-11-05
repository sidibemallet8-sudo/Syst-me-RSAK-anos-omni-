
# PROTOCOLE EXPÉRIMENTAL — ANOS OMNI RSAK V1

## 1. Objectif

Évaluer la capacité du mécanisme RSAK (Réorganisation Structurelle Adaptative des Connaissances) à détecter des contradictions dans une base de règles et à proposer une réorganisation de ces règles à partir de nouveaux exemples.

RSAK V1 est un prototype expérimental. Ses performances et sa contribution scientifique restent à établir.

## 2. Question de recherche

Un système fondé sur des règles peut-il détecter qu'une règle générale devient insuffisante face à des contre-exemples, puis proposer une réorganisation de ses connaissances qui améliore ses réponses sans supprimer arbitrairement les connaissances précédentes ?

## 3. Hypothèse

Lorsqu'une règle générale rencontre des contre-exemples, RSAK peut identifier une caractéristique discriminante dans les exemples observés et proposer des règles plus spécifiques.

La proposition doit être soumise à validation avant de remplacer la règle initiale.

## 4. Comportements à évaluer

- Détection des contradictions.
- Identification d'une caractéristique discriminante.
- Génération de règles candidates.
- Conservation de la règle précédente avant validation.
- Réorganisation après validation.
- Abstention lorsqu'une information nécessaire est inconnue.
- Rejet d'une proposition sans modification injustifiée de la base.

## 5. Exemple expérimental

Règle initiale :

Si un objet possède quatre roues, alors il est motorisé.

Nouveaux exemples :

- Objet avec quatre roues et moteur : motorisé.
- Objet avec quatre roues sans moteur : non motorisé.

Résultat attendu :

Le système détecte que la règle initiale est trop générale. Il peut proposer une séparation selon la présence du moteur.

Cette démonstration illustre le mécanisme. Elle ne constitue pas, à elle seule, une preuve de performance scientifique.

## 6. Méthode expérimentale

Les expériences devront comparer quatre approches :

1. Règles statiques : aucune modification après création.
2. Gestion par exceptions : ajout d'exceptions aux règles existantes.
3. Révision manuelle : modification des règles par un opérateur.
4. RSAK : détection et proposition de réorganisation structurelle.

Les mêmes jeux de données devront être utilisés pour les différentes approches.

## 7. Données et séparation expérimentale

Créer des jeux de données artificiels contrôlés, puis des jeux de données plus variés.

Séparer les exemples en :

- Données d'apprentissage.
- Données de validation.
- Données de test indépendantes.

Les exemples de test ne doivent pas être utilisés pour construire ou modifier les règles.

## 8. Indicateurs de mesure

Mesurer :

- Exactitude : proportion de réponses correctes.
- Couverture : proportion de questions auxquelles le système répond.
- Abstention : proportion de questions sans réponse certaine.
- Contradictions non résolues : conflits restant dans la base.
- Nombre de règles : taille de la base après adaptation.
- Coût de révision : nombre de modifications nécessaires.
- Rétention : capacité à conserver les connaissances utiles après réorganisation.

## 9. Conditions de validation

Une proposition de réorganisation ne sera considérée comme utile que si elle :

- réduit les erreurs sur des données indépendantes ;
- ne provoque pas une augmentation excessive de la complexité ;
- conserve les connaissances qui restent valides ;
- respecte le mécanisme de validation humaine prévu.

## 10. Reproductibilité

Chaque expérience devra enregistrer :

- La version du programme.
- Les données utilisées.
- Les règles initiales.
- Les exemples ajoutés.
- Les propositions produites.
- Les décisions de validation.
- Les résultats obtenus.

Les expériences devront être répétées sur plusieurs jeux de données.

## 11. Limites actuelles

RSAK V1 ne démontre pas encore :

- Une intelligence générale.
- Un apprentissage autonome comparable à celui d'un grand modèle neuronal.
- Une supériorité sur les méthodes existantes.
- Une robustesse sur des données réelles à grande échelle.

Ces points nécessitent des expériences et des comparaisons supplémentaires.

## 12. Conclusion

RSAK V1 constitue une première implémentation expérimentale d'un mécanisme de détection de contradictions et de proposition de réorganisation des règles.

La prochaine étape scientifique consiste à exécuter le protocole, mesurer les résultats et comparer le système à des approches de référence.
