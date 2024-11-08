from flask import Flask, render_template, request, jsonify
from model import InstagramDetector
import json

app = Flask(__name__)
detector = None

def init_detector():
    """Initialise le détecteur"""
    global detector
    try:
        detector = InstagramDetector()
        detector.load_or_train()
        return True
    except Exception as e:
        print(f"Erreur d'initialisation du détecteur: {e}")
        return False

def load_examples():
    """Charge les exemples depuis le fichier JSON"""
    try:
        with open('data/examples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('examples', [])
    except Exception as e:
        print(f"Erreur lors du chargement des exemples: {e}")
        return []

@app.route('/')
def index():
    """Page principale avec formulaire et exemples"""
    examples = load_examples()
    return render_template('index.html', example_cases=examples)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse un compte Instagram"""
    if not detector:
        return jsonify({
            'error': "Le détecteur n'est pas initialisé correctement"
        }), 500
        
    try:
        # Préparation des features pour le modèle
        features = {
            'profile pic': int(request.form.get('profile_pic', 'false') == 'true'),
            'nums/length username': float(request.form.get('username_numbers', 0)) / 100,
            'description length': int(request.form.get('description_length', 0)),
            'private': int(request.form.get('private', 'false') == 'true'),
            '#posts': int(request.form.get('posts', 0)),
            '#followers': int(request.form.get('followers', 0)),
            '#follows': int(request.form.get('follows', 0))
        }
        
        # Analyse avec le modèle
        result = detector.predictor(features)
        
        if not result or 'error' in result:
            return jsonify({
                'error': result.get('error', "Erreur lors de l'analyse"),
                'details': "Le modèle n'a pas pu analyser ce compte"
            }), 500
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'error': "Données invalides",
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': "Erreur lors de l'analyse",
            'details': str(e)
        }), 500

@app.route('/analyze_example/<example_id>')
def analyze_example(example_id):
    """Analyse un exemple prédéfini"""
    if not detector:
        return jsonify({
            'error': "Le détecteur n'est pas initialisé correctement"
        }), 500
        
    try:
        # Recherche de l'exemple
        examples = load_examples()
        example = next((ex for ex in examples if ex['id'] == example_id), None)
        
        if not example:
            return jsonify({
                'error': "Exemple non trouvé",
                'details': "L'identifiant fourni est invalide"
            }), 404
        
        # Analyse avec le modèle
        result = detector.predictor(example['raw_values'])
        
        if not result or 'error' in result:
            return jsonify({
                'error': result.get('error', "Erreur lors de l'analyse"),
                'details': "Le modèle n'a pas pu analyser cet exemple"
            }), 500
            
        return jsonify({
            'success': True,
            'example': example,
            'analysis': result
        })
        
    except Exception as e:
        return jsonify({
            'error': "Erreur lors de l'analyse de l'exemple",
            'details': str(e)
        }), 500


# Point d'entrée principal
if __name__ == '__main__':
    # Initialisation du détecteur
    if init_detector():
        app.run(debug=True)
    else:
        print("Erreur critique : Impossible d'initialiser le détecteur")