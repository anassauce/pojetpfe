// Gestion des onglets
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        // Désactive tous les onglets
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Active l'onglet sélectionné
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');

        // Cache les résultats précédents lors du changement d'onglet
        document.getElementById('manual-result').style.display = 'none';
    });
});

// Fonction pour formater le pourcentage
function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
}

// Fonction pour afficher le résultat de l'analyse manuelle
function displayManualResult(result) {
    const resultBox = document.getElementById('manual-result');
    const resultContent = document.getElementById('manual-result-content');
    
    if (result.error) {
        // Affichage de l'erreur
        resultBox.className = 'result-box error';
        let errorHtml = `<p class="error">${result.error}</p>`;
        if (result.details) {
            errorHtml += `<p class="error-details">${result.details}</p>`;
        }
        resultContent.innerHTML = errorHtml;
    } else {
        // Affichage du résultat
        resultBox.className = 'result-box ' + (result.is_fake ? 'fake' : 'authentic');
        
        let html = `
            <div class="verdict">
                <h4 class="verdict-text">${result.is_fake ? 'Compte suspect' : 'Compte authentique'}</h4>
                <p class="verdict-explanation">${result.explanation}</p>
                ${result.confidence ? `<p class="confidence">Confiance: ${formatPercentage(result.confidence)}</p>` : ''}
            `;

        // Ajout des caractéristiques importantes si disponibles
        if (result.important_features) {
            html += `
                <div class="important-features">
                    <h5>Caractéristiques importantes :</h5>
                    <ul class="features-list">
            `;
            
            for (const [feature, info] of Object.entries(result.important_features)) {
                html += `
                    <li>${feature}: ${info.value} 
                        (importance: ${formatPercentage(info.importance)})
                    </li>`;
            }
            
            html += '</ul></div>';
        }

        html += '</div>';
        resultContent.innerHTML = html;
    }
    
    // Affiche le résultat avec une animation
    resultBox.style.display = 'block';
    resultBox.scrollIntoView({ behavior: 'smooth' });
}

// Gestion du formulaire d'analyse manuelle
document.getElementById('analysis-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Désactive le bouton pendant l'analyse
    const submitButton = e.target.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = 'Analyse en cours...';
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        displayManualResult(result);
    } catch (error) {
        displayManualResult({
            error: "Erreur lors de l'analyse",
            details: error.message
        });
    } finally {
        // Réactive le bouton après l'analyse
        submitButton.disabled = false;
        submitButton.textContent = 'Analyser';
    }
});

// Fonction pour afficher le résultat d'un exemple
function displayExampleResult(exampleId, result) {
    const exampleCard = document.getElementById(`example-${exampleId}`);
    const resultDiv = exampleCard.querySelector('.example-result');
    const verdictText = resultDiv.querySelector('.verdict-text');
    const verdictExplanation = resultDiv.querySelector('.verdict-explanation');
    const confidenceElem = resultDiv.querySelector('.confidence');
    const featuresList = resultDiv.querySelector('.features-list');
    
    if (result.error) {
        // Affichage de l'erreur
        verdictText.textContent = "Erreur d'analyse";
        verdictExplanation.textContent = result.details || result.error;
        resultDiv.className = 'example-result error';
        confidenceElem.style.display = 'none';
        featuresList.parentElement.style.display = 'none';
    } else {
        // Récupération des données d'analyse
        const analysis = result.analysis || result;
        
        // Affichage du verdict
        verdictText.textContent = analysis.is_fake ? "Compte suspect" : "Compte authentique";
        verdictExplanation.textContent = analysis.explanation;
        
        // Affichage de la confiance
        if (analysis.confidence) {
            confidenceElem.textContent = `Confiance: ${formatPercentage(analysis.confidence)}`;
            confidenceElem.style.display = 'block';
        } else {
            confidenceElem.style.display = 'none';
        }
        
        // Affichage des caractéristiques importantes
        if (analysis.important_features) {
            featuresList.innerHTML = '';
            for (const [feature, info] of Object.entries(analysis.important_features)) {
                const li = document.createElement('li');
                li.textContent = `${feature}: ${info.value} (importance: ${formatPercentage(info.importance)})`;
                featuresList.appendChild(li);
            }
            featuresList.parentElement.style.display = 'block';
        } else {
            featuresList.parentElement.style.display = 'none';
        }
        
        // Application de la classe de style appropriée
        exampleCard.className = `example-card ${analysis.is_fake ? 'fake' : 'authentic'}`;
    }
    
    // Affichage du résultat
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Cache le bouton d'analyse
    const analyzeButton = exampleCard.querySelector('.analyze-example');
    if (analyzeButton) {
        analyzeButton.style.display = 'none';
    }
}

// Gestion des exemples
document.querySelectorAll('.analyze-example').forEach(button => {
    button.addEventListener('click', async () => {
        const exampleId = button.dataset.id;
        
        // Désactive le bouton et montre l'état d'analyse
        button.disabled = true;
        button.textContent = 'Analyse en cours...';
        
        try {
            const response = await fetch(`/analyze_example/${exampleId}`);
            const data = await response.json();
            
            if (data.error) {
                displayExampleResult(exampleId, data);
            } else {
                displayExampleResult(exampleId, data);
            }
        } catch (error) {
            displayExampleResult(exampleId, {
                error: "Erreur lors de l'analyse",
                details: error.message
            });
        }
    });
});