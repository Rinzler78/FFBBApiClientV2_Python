#!/usr/bin/env python3
"""
Script pour corriger les incohérences de nommage après la séparation des fichiers de test.
"""

import ast
import re
from pathlib import Path


def fix_test_file_naming_after_separation(test_file_path):
    """Fixe le nom de la classe dans un fichier de test après séparation."""
    with open(test_file_path, encoding="utf-8") as file:
        content = file.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"Erreur de syntaxe dans le fichier: {test_file_path}")
        return False

    # Extraire le nom de la classe attendu à partir du nom du fichier
    filename = test_file_path.name
    # Format: test_XXX_module_name.py
    match = re.match(r"test_(\d+)_(.+)\.py", filename)
    if not match:
        print(f"Nom de fichier non conforme: {filename}")
        return False

    number, module_part = match.groups()

    # Convertir le nom du module en PascalCase pour le nom de la classe
    # Remplacer les underscores par des espaces, capitaliser chaque mot, puis retirer les espaces
    class_name_parts = module_part.split("_")
    pascal_case_module = "".join(part.capitalize() for part in class_name_parts)
    expected_class_name = f"Test{number}{pascal_case_module}"

    # Trouver la classe de test dans le fichier
    test_class_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Vérifier si la classe hérite de unittest.TestCase
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "TestCase":
                    test_class_node = node
                    break
                elif isinstance(base, ast.Attribute) and base.attr == "TestCase":
                    test_class_node = node
                    break

    if not test_class_node:
        print(f"Aucune classe de test trouvée dans: {filename}")
        return False

    current_class_name = test_class_node.name

    if current_class_name == expected_class_name:
        # print(f"✓ {filename} - Déjà correct")
        return False  # Pas de changement nécessaire

    # Remplacer le nom de la classe dans le contenu
    updated_content = content.replace(
        f"class {current_class_name}(", f"class {expected_class_name}("
    )

    # Vérifier si la modification a été effectuée
    if updated_content != content:
        # Écrire le contenu mis à jour dans le fichier
        with open(test_file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

        print(
            f"✓ {filename} - Mis à jour: {current_class_name} -> {expected_class_name}"
        )
        return True
    else:
        print(
            f"✗ {filename} - Impossible de remplacer {current_class_name} par {expected_class_name}"
        )
        return False


def main():
    # Dossier des tests
    tests_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"
    )

    print("Correction des incohérences de nommage après séparation...")
    print(f"Dossier traité: {tests_dir}")
    print("-" * 60)

    # Trouver tous les fichiers de test
    test_files = list(tests_dir.rglob("test_*.py"))

    print(f"Nombre de fichiers de test à traiter: {len(test_files)}")

    updated_count = 0
    for test_file in test_files:
        try:
            if fix_test_file_naming_after_separation(test_file):
                updated_count += 1
        except Exception as e:
            print(f"Erreur lors du traitement de {test_file}: {str(e)}")

    print("-" * 60)
    print(
        f"Terminé ! {updated_count} fichiers mis à jour sur {len(test_files)} fichiers de test."
    )


if __name__ == "__main__":
    main()
