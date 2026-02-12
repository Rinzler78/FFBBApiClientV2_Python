#!/usr/bin/env python3
"""
Script pour détecter les incohérences entre les noms des modules de test
et les noms des classes de test dans le projet.
"""

import ast
import re
from pathlib import Path


def get_number_prefix(filename):
    """
    Extrait le préfixe numérique d'un nom de fichier de test.
    Par exemple, 'test_100_competition_id_categorie.py' -> '100'
    """
    match = re.match(r"test_(\d+)", filename)
    return match.group(1) if match else None


def get_expected_class_name(filename):
    """
    Génère le nom de classe attendu à partir du nom de fichier.
    Par exemple, 'test_100_competition_id_categorie.py' -> 'Test100CompetitionIdCategorie'
    """
    # Enlever le préfixe 'test_' et l'extension '.py'
    basename = filename[5:-3]  # Enlève 'test_' et '.py'

    # Divise le nom en segments séparés par des underscores
    parts = basename.split("_")

    # Le premier segment est le numéro
    number = parts[0]

    # Les autres segments forment le reste du nom
    remaining_parts = parts[1:]

    # Convertir chaque segment en PascalCase
    capitalized_parts = []
    for part in remaining_parts:
        # Capitaliser la première lettre de chaque mot
        capitalized_part = "".join(word.capitalize() for word in part.split())
        capitalized_parts.append(capitalized_part)

    # Former le nom de la classe
    class_name = f'Test{number}{"".join(capitalized_parts)}'
    return class_name


def find_test_classes_in_file(filepath):
    """
    Trouve toutes les classes de test dans un fichier donné.
    """
    with open(filepath, encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read())
        except SyntaxError:
            print(f"Erreur de syntaxe dans le fichier: {filepath}")
            return []

    test_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Vérifier si la classe hérite de unittest.TestCase
            inherits_unittest = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "TestCase":
                    inherits_unittest = True
                elif isinstance(base, ast.Attribute) and base.attr == "TestCase":
                    inherits_unittest = True

            if inherits_unittest:
                test_classes.append(node.name)

    return test_classes


def check_test_naming_consistency(root_dir):
    """
    Vérifie la cohérence entre les noms de fichiers et de classes de test.
    """
    root_path = Path(root_dir)
    test_files = list(root_path.rglob("test_*.py"))

    inconsistencies = []

    for test_file in test_files:
        filename = test_file.name

        # Extraire le préfixe numérique
        number_prefix = get_number_prefix(filename)
        if not number_prefix:
            continue  # Ce n'est pas un fichier de test numéroté

        # Obtenir le nom de classe attendu
        expected_class_name = get_expected_class_name(filename)

        # Trouver les classes de test dans le fichier
        actual_classes = find_test_classes_in_file(test_file)

        if not actual_classes:
            # Aucune classe de test trouvée
            inconsistencies.append(
                {
                    "file": str(test_file),
                    "expected_class": expected_class_name,
                    "actual_classes": [],
                    "issue": "No test classes found",
                }
            )
        else:
            # Vérifier si la classe attendue est présente
            if expected_class_name not in actual_classes:
                inconsistencies.append(
                    {
                        "file": str(test_file),
                        "expected_class": expected_class_name,
                        "actual_classes": actual_classes,
                        "issue": "Expected class name does not match any actual class name",
                    }
                )

    return inconsistencies


def main():
    # Dossier racine du projet
    root_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"

    print("Vérification de la cohérence des noms de tests...")
    print(f"Dossier analysé: {root_dir}")
    print("-" * 60)

    inconsistencies = check_test_naming_consistency(root_dir)

    if not inconsistencies:
        print("✅ Tous les noms de tests sont cohérents !")
    else:
        print(f"❌ {len(inconsistencies)} incohérence(s) détectée(s):")
        print()

        for i, inc in enumerate(inconsistencies, 1):
            print(f"{i}. Fichier: {inc['file']}")
            print(f"   Classe attendue: {inc['expected_class']}")
            print(f"   Classes trouvées: {inc['actual_classes']}")
            print(f"   Problème: {inc['issue']}")
            print()

    print(
        f"Total des fichiers de test analysés: {len(list(Path(root_dir).rglob('test_*.py')))}"
    )


if __name__ == "__main__":
    main()
