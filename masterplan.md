# Plan Directeur - Détecteur de Faux Comptes Instagram

## 1. Présentation et Objectifs
- Application web simple pour identifier les faux comptes Instagram
- Interface minimaliste et intuitive
- Utilisation d'un arbre de décision
- Projet académique à but éducatif

## 2. Structure du Projet
```
projet/
├── app.py              # Application Flask et routes
├── model.py            # Entraînement et gestion du modèle
├── templates/
│   └── index.html      # Page unique
├── static/
│   └── style.css       # Styles minimalistes
├── data/
│   ├── train.csv       # Données d'entraînement
│   ├── test.csv        # Données de test
│   └── examples.json   # Exemples prédéfinis
├── models/
│   └── model_dt.pkl    # Modèle entraîné (généré automatiquement)
```

## 3. Composants Principaux

### 3.1 Interface Utilisateur (index.html)
- Page unique avec deux sections principales :
  * Formulaire d'analyse manuelle
  * Exemples prédéfinis
- Design responsive et minimaliste
- Messages clairs et explicatifs

### 3.2 Backend (app.py)
- Gestion des routes Flask :
  * Page principale ('/')
  * Analyse d'un compte ('/analyze')
  * Analyse d'exemple ('/analyze_example/<id>')
- Chargement des exemples depuis examples.json
- Pas de logique métier, uniquement routage et présentation

### 3.3 Modèle IA (model.py)
- Classe InstagramDetector :
  * Chargement/entraînement du modèle
  * Prédictions
  * Formatage des explications
- Gestion du fichier pickle pour la persistance
- Utilisation de toutes les caractéristiques pour l'entraînement

### 3.4 Exemples Prédéfinis (examples.json)
- 6 cas d'étude (3 authentiques, 3 faux)
- Format JSON structuré
- Caractéristiques affichables et valeurs brutes
- Facilement modifiable et maintenable

## 4. Fonctionnalités

### 4.1 Analyse Manuelle
- Formulaire avec champs principaux :
  * Photo de profil (oui/non)
  * Proportion de chiffres dans le username
  * Longueur de la description
  * Compte privé (oui/non)
  * Nombre de posts/abonnés/abonnements

### 4.2 Exemples Prédéfinis
- Affichage neutre de 6 cas représentatifs
- Caractéristiques présentées clairement
- Possibilité d'analyser chaque exemple

## 5. Aspects Techniques

### 5.1 Frontend
- HTML/CSS simple et propre
- Design responsive basique
- Messages d'erreur clairs

### 5.2 Backend
- Flask pour le serveur web
- Scikit-learn pour l'arbre de décision
- Pandas pour la manipulation des données
- Pickle pour la persistance du modèle

### 5.3 Données
- Utilisation des datasets fournis (train.csv, test.csv)
- Exemples prédéfinis en JSON
- Séparation claire données/code

## 6. Phases de Développement

### Phase 1 : Mise en place
- Configuration de l'environnement Python
- Création de la structure de fichiers
- Préparation des exemples JSON

### Phase 2 : Modèle
- Implémentation de model.py
- Tests du modèle
- Validation des prédictions

### Phase 3 : Application
- Développement de app.py
- Création des templates
- Intégration avec le modèle

### Phase 4 : Tests
- Validation de bout en bout
- Tests des différents cas
- Vérification des exemples

## 9. Livrables
- Code source commenté
- Guide d'utilisation
- Exemples prédéfinis
- Modèle entraîné (généré)