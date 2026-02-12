#!/usr/bin/env python3
"""
Script pour identifier les fichiers de test avec plusieurs classes de test.
"""

import ast
from pathlib import Path


def count_test_classes_in_file(filepath):
    """Compte les classes de test dans un fichier."""
    with open(filepath, encoding="utf-8") as file:
        try:
            content = file.read()
            tree = ast.parse(content)
        except SyntaxError:
            print(f"Erreur de syntaxe dans le fichier: {filepath}")
            return 0

    test_class_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Vérifier si la classe hérite de unittest.TestCase
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "TestCase":
                    test_class_count += 1
                    break
                elif isinstance(base, ast.Attribute) and base.attr == "TestCase":
                    test_class_count += 1
                    break

    return test_class_count


def main():
    # Dossier des tests
    tests_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"
    )

    print("Identification des fichiers de test avec plusieurs classes...")
    print(f"Dossier des tests: {tests_dir}")
    print("=" * 60)

    # Trouver tous les fichiers de test
    test_files = list(tests_dir.rglob("test_*.py"))

    multi_class_files = []
    single_class_files = []

    for test_file in test_files:
        class_count = count_test_classes_in_file(test_file)
        if class_count > 1:
            multi_class_files.append((test_file, class_count))
        elif class_count == 1:
            single_class_files.append((test_file, class_count))

    print(f"Fichiers avec une seule classe: {len(single_class_files)}")
    print(f"Fichiers avec plusieurs classes: {len(multi_class_files)}")

    if multi_class_files:
        print("\nFichiers avec plusieurs classes:")
        print("-" * 40)
        for file_path, count in multi_class_files:
            print(f"{count} classes - {file_path.name}")

    print(f"\nTotal des fichiers de test: {len(test_files)}")


if __name__ == "__main__":
    main()
