import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
import joblib
import os

class InstagramDetector:
    def __init__(self):
        """Initialisation du détecteur"""
        self.model = None
        self.scaler = StandardScaler()
        model_file="models/model.pkl"
        self.model_file = model_file
        self.data_train_file='data/train.csv'
        self.data_test_file='data/test.csv'

        # Caractéristiques utilisées pour la détection
        self.features = [
            'profile pic', 
            'nums/length username',
            'description length',
            'private',
            '#posts',
            '#followers',
            '#follows'
        ]
        self.numeric_features = [
            'nums/length username',
            'description length',
            '#posts',
            '#followers',
            '#follows'
            ]

    def train_model(self):
        print("Entraînement du modèle...")
        try:
            # Charger et préparer les données
            train = pd.read_csv(self.data_train_file)
            train = train.dropna()

            # Préparation des features
            X_train = train[self.features].copy()
            y_train = train['fake']

            # Standardiser les features numériques
            X_train.loc[:, self.numeric_features] = self.scaler.fit_transform(X_train[self.numeric_features])

            # Entraînement du modèle
            self.model = DecisionTreeClassifier(
                max_depth=5,           # Évite le surapprentissage
                min_samples_leaf=10,   # Minimum d'échantillons par feuille
                random_state=42        # Reproductibilité
            )

            # Validation croisée
            cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
            print(f"Scores de validation croisée: {cv_scores}")
            print(f"Score moyen: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

            # Entraînement final du modèle
            self.model.fit(X_train, y_train)

            # Sauvegarder le modèle et le scaler
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, self.model_file)
            print(f"Modèle sauvegardé sous {self.model_file}")
        except Exception as e:
            print(f"Erreur lors de l'entraînement du modèle: {e}")
            raise

    def load_model(self):
        print(f"Chargement du modèle depuis {self.model_file}...")
        try:
            saved_objects = joblib.load(self.model_file)
            self.model = saved_objects['model']
            self.scaler = saved_objects['scaler']
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            self.train_model()

    def evaluate(self):
        # Charger et préparer les données de test
        test = pd.read_csv(self.data_test_file)
        test = test.dropna()
        
        X_test = test[self.features].copy()
        y_test = test['fake']

        # Standardiser les features numériques
        X_test.loc[:, self.numeric_features] = self.scaler.transform(X_test[self.numeric_features])

        # Prédictions
        y_pred = self.model.predict(X_test)

        # Affichage des métriques
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Précision (Accuracy) : {accuracy:.2f}")

        print("\nRapport de classification :")
        print(classification_report(y_test, y_pred))

    def load_or_train(self):
        # Charger un modèle existant ou entraîner un nouveau modèle
        if os.path.exists(self.model_file):
            self.load_model()
        else:
            self.train_model()

        # Évaluer le modèle
        self.evaluate()

    def predictor(self, features):
        """Prédit si un compte est faux ou authentique"""
        try:
            # Conversion des features en DataFrame
            features_df = pd.DataFrame([features])
            
            # Standardiser les features numériques
            numerical_features = [
                'nums/length username',
                'description length',
                '#posts',
                '#followers',
                '#follows'
            ]
            features_df[numerical_features] = self.scaler.transform(features_df[numerical_features])
            
            # Prédiction
            prediction = self.model.predict(features_df)[0]
            proba = self.model.predict_proba(features_df)[0]
            
            # Calcul des caractéristiques importantes
            importance_dict = self.get_feature_importance(features)
            
            return {
                'is_fake': bool(prediction),
                'confidence': float(max(proba)),
                'important_features': importance_dict,
                'explanation': self.generate_explanation(prediction, importance_dict)
            }
            
        except Exception as e:
            print(f"Erreur lors de la prédiction: {e}")
            return {
                'error': "Une erreur est survenue lors de l'analyse du compte."
            }
        
    def get_feature_importance(self, features):
        """Calcule l'importance des caractéristiques pour la prédiction"""
        importance = list(zip(self.features, self.model.feature_importances_))
        importance.sort(key=lambda x: x[1], reverse=True)
        
        return {
            feat: {
                'importance': float(imp),
                'value': features[feat]
            }
            for feat, imp in importance[:3]  # Top 3 caractéristiques
        }
    
    def generate_explanation(self, prediction, importance_dict):
        """Génère une explication détaillée de la prédiction"""
        if prediction == 0:
            base_text = "Ce compte semble authentique"
        else:
            base_text = "Ce compte semble suspect"
        
        details = []
        for feature, info in importance_dict.items():
            if prediction == 1:  # Compte suspect
                # Analyse des caractéristiques suspectes
                if feature == 'profile pic' and info['value'] == 0:
                    details.append("absence de photo de profil")
                elif feature == 'nums/length username' and info['value'] > 0.3:
                    details.append("proportion élevée de chiffres dans le nom d'utilisateur")
                elif feature == 'description length' and info['value'] == 0:
                    details.append("absence de description")
                elif feature == 'private' and info['value'] == 1:
                    details.append("compte privé")
                elif feature == '#posts' and info['value'] < 5:
                    details.append("très peu de posts")
                elif feature == '#followers' and info['value'] < 10:
                    details.append("très peu d'abonnés")
                elif feature == '#follows' and info['value'] > 7500:
                    details.append("nombre d'abonnements anormalement élevé")
            else:  # Compte authentique
                # Analyse des caractéristiques d'authenticité
                if feature == 'profile pic' and info['value'] == 1:
                    details.append("photo de profil présente")
                elif feature == 'nums/length username' and info['value'] <= 0.3:
                    details.append("nom d'utilisateur naturel")
                elif feature == 'description length' and info['value'] > 0:
                    details.append("description personnalisée")
                elif feature == 'private' and info['value'] == 0:
                    details.append("compte public")
                elif feature == '#posts' and info['value'] >= 5:
                    details.append("activité régulière avec plusieurs posts")
                elif feature == '#followers' and info['value'] >= 10:
                    details.append("nombre d'abonnés cohérent")
                elif feature == '#follows' and 10 <= info['value'] <= 7500:
                    details.append("nombre d'abonnements équilibré")
        
        # Toujours inclure une explication, même si aucun détail spécifique n'est trouvé
        if details:
            explanation = f"{base_text} ({', '.join(details)})"
        else:
            # Explications par défaut selon le type de compte
            if prediction == 0:
                explanation = f"{base_text} (combinaison équilibrée des métriques du profil)"
            else:
                explanation = f"{base_text} (combinaison inhabituelle des caractéristiques)"
                
        return explanation