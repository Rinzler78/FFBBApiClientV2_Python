#!/bin/bash

# Script to generate clean HTML report from the team analysis notebook
# This creates a report showing only outputs and text, without code cells

echo "🏀 Génération du rapport d'analyse d'équipe..."

# Activate virtual environment
source .venv/bin/activate

# Generate clean HTML report (without code cells)
jupyter nbconvert --to html --no-input examples/team_analysis_notebook.ipynb --output team_analysis_report.html

echo "✅ Rapport généré: examples/team_analysis_report.html"
echo "📊 Le rapport contient tous les graphiques et analyses sans le code source"
echo "🌐 Ouvrez le fichier HTML dans votre navigateur pour voir le rapport complet"
