#!/usr/bin/env python3
"""
Script pour renommer les fonctions de test dans chaque fichier selon une séquence logique.
"""

import ast
import re
from pathlib import Path


def update_test_function_names_in_file(filepath):
    """Met à jour les noms des fonctions de test dans un fichier."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Parser le contenu du fichier
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Erreur de syntaxe dans {filepath}: {e}")
        return False

    # Trouver toutes les fonctions de test
    test_functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("test_"):
                # Vérifier si le nom contient déjà un numéro
                match = re.match(r"test_(\d+)_(.+)", node.name)
                if match:
                    current_number = int(match.group(1))
                    description = match.group(2)
                    test_functions.append(
                        {
                            "node": node,
                            "name": node.name,
                            "line_start": node.lineno,
                            "current_number": current_number,
                            "description": description,
                        }
                    )
                else:
                    # Cas où le nom ne contient pas de numéro
                    # Extraire la description après 'test_'
                    description = node.name[5:]  # Enlever 'test_'
                    test_functions.append(
                        {
                            "node": node,
                            "name": node.name,
                            "line_start": node.lineno,
                            "current_number": None,  # Aucun numéro existant
                            "description": description,
                        }
                    )

    if not test_functions:
        print(f"Aucune fonction de test trouvée dans {filepath}")
        return False

    # Trier les fonctions par ligne pour maintenir l'ordre d'apparition
    test_functions.sort(key=lambda x: x["line_start"])

    # Créer un mapping des anciens noms vers les nouveaux noms
    function_mapping = {}
    for idx, func_info in enumerate(test_functions):
        new_number = idx
        new_name = f"test_{new_number:03d}_{func_info['description']}"
        function_mapping[func_info["name"]] = new_name

    # Remplacer les noms dans le contenu
    updated_content = content
    for old_name, new_name in sorted(
        function_mapping.items(), key=lambda x: len(x[0]), reverse=True
    ):
        # Remplacer les références aux fonctions dans le contenu
        updated_content = re.sub(
            r"\b" + re.escape(old_name) + r"\b", new_name, updated_content
        )

    if updated_content != content:
        # Écrire le contenu mis à jour dans le fichier
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"Mis à jour {len(function_mapping)} fonctions de test dans {filepath}:")
        for old_name, new_name in function_mapping.items():
            if old_name != new_name:
                print(f"  {old_name} -> {new_name}")

        return True
    else:
        print(f"Aucune modification nécessaire dans {filepath}")
        return False


def update_all_test_function_names():
    """Met à jour les noms de toutes les fonctions de test dans tous les fichiers de test."""

    # Dossiers des tests unitaires
    test_dirs = [
        Path(
            "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests/unit/models"
        ),
        Path(
            "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests/unit/utils"
        ),
        Path(
            "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests/unit/helpers"
        ),
        Path(
            "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests/unit/clients"
        ),
    ]

    updated_files_count = 0

    for test_dir in test_dirs:
        if test_dir.exists():
            # Trouver tous les fichiers de test dans le dossier
            test_files = list(test_dir.glob("test_*.py"))

            for test_file in test_files:
                print(f"\nTraitement de {test_file}")
                if update_test_function_names_in_file(test_file):
                    updated_files_count += 1

    print(f"\nTerminé : {updated_files_count} fichiers de test mis à jour.")


if __name__ == "__main__":
    update_all_test_function_names()
