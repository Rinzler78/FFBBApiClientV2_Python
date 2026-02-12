#!/usr/bin/env python3
"""
Script pour séparer les fichiers de test qui contiennent plusieurs classes de test
afin de respecter la règle 'un module de test par module source'.
"""

import ast
import re
from pathlib import Path


def extract_test_classes_from_file(filepath):
    """Extrait toutes les classes de test d'un fichier."""
    with open(filepath, encoding="utf-8") as file:
        try:
            content = file.read()
            tree = ast.parse(content)
        except SyntaxError:
            print(f"Erreur de syntaxe dans le fichier: {filepath}")
            return []

    # Diviser le contenu en lignes pour extraire les parties de code
    lines = content.split("\n")

    test_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Vérifier si la classe hérite de unittest.TestCase
            inherits_unittest = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "TestCase":
                    inherits_unittest = True
                    break
                elif isinstance(base, ast.Attribute) and base.attr == "TestCase":
                    inherits_unittest = True
                    break

            if inherits_unittest:
                # Extraire le contenu de la classe
                start_line = node.lineno - 1
                # Trouver la fin de la classe en fonction de l'indentation
                end_line = start_line

                # Trouver la fin de la classe en fonction de l'indentation
                class_indent = (
                    len(lines[start_line]) - len(lines[start_line].lstrip())
                    if lines[start_line].strip()
                    else float("inf")
                )

                for i in range(start_line + 1, len(lines)):
                    if i < len(lines) and lines[i].strip():
                        line_indent = len(lines[i]) - len(lines[i].lstrip())
                        if line_indent <= class_indent:
                            end_line = i - 1
                            break
                    elif i >= len(lines):
                        end_line = len(lines) - 1
                        break
                else:
                    end_line = len(lines) - 1

                # S'assurer que end_line est valide
                if end_line < start_line:
                    end_line = len(lines) - 1

                class_content = "\n".join(lines[start_line : end_line + 1])

                test_classes.append(
                    {
                        "name": node.name,
                        "content": class_content,
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )

    return test_classes


def get_file_header(content, first_class_line):
    """Extrait l'en-tête d'un fichier (jusqu'à la première classe)."""
    lines = content.split("\n")
    header_lines = []

    for i, line in enumerate(lines):
        if i >= first_class_line:
            break
        header_lines.append(line)

    return "\n".join(header_lines)


def separate_multi_class_test_files():
    """Sépare les fichiers avec plusieurs classes de test."""
    # Dossier des tests
    tests_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"
    )

    print("Séparation des fichiers de test avec plusieurs classes...")
    print(f"Dossier des tests: {tests_dir}")
    print("=" * 80)

    # Trouver tous les fichiers de test
    test_files = list(tests_dir.rglob("test_*.py"))

    # Identifier les fichiers avec plusieurs classes
    multi_class_files = []
    for test_file in test_files:
        classes = extract_test_classes_from_file(test_file)
        if len(classes) > 1:
            multi_class_files.append((test_file, classes))

    print(f"Fichiers avec plusieurs classes trouvés: {len(multi_class_files)}")

    # Traiter chaque fichier avec plusieurs classes
    total_new_files = 0
    for original_file, classes in multi_class_files:
        print(f"\nTraitement de {original_file.name} ({len(classes)} classes):")

        # Lire le contenu original pour extraire l'en-tête
        with open(original_file, encoding="utf-8") as f:
            original_content = f.read()

        # Trouver la première classe pour extraire l'en-tête
        first_class_line = min(c["start_line"] for c in classes) if classes else 0
        header_content = get_file_header(original_content, first_class_line)

        # Créer un fichier séparé pour chaque classe
        for i, test_class in enumerate(classes):
            # Extraire le numéro du fichier original pour le conserver
            original_match = re.match(r"test_(\d+)_", original_file.name)
            if original_match:
                original_number = original_match.group(1)

                # Pour les classes supplémentaires, on crée un nom dérivé
                if i == 0:
                    # Première classe garde le nom original
                    new_filename = original_file.name
                    new_content = f"{header_content}\n\n{test_class['content']}\n"
                else:
                    # Autres classes reçoivent un nom dérivé basé sur le nom de la classe
                    class_name = test_class["name"]
                    # Enlever le préfixe 'Test' et le numéro
                    clean_name = re.sub(r"^Test\d*", "", class_name)
                    # Convertir de CamelCase à snake_case
                    import re as regex

                    snake_case = regex.sub(
                        "([a-z0-9])([A-Z])", r"\1_\2", clean_name
                    ).lower()
                    new_filename = f"test_{original_number}_{snake_case}.py"
                    new_content = f"{header_content}\n\n{test_class['content']}\n"

                # Créer le nouveau fichier
                new_file_path = original_file.parent / new_filename
                with open(new_file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"  - Créé {new_filename} pour la classe {test_class['name']}")
                total_new_files += 1
            else:
                print(
                    f"  - Impossible de déterminer le numéro pour {original_file.name}"
                )

    # Supprimer les fichiers originaux qui avaient plusieurs classes
    for original_file, classes in multi_class_files:
        if len(classes) > 1:
            print(
                f"Suppression de l'ancien fichier {original_file.name} (contenait {len(classes)} classes)"
            )
            original_file.unlink()

    print(f"\nTotal nouveaux fichiers créés: {total_new_files}")
    print(
        "La structure des tests est maintenant conforme à 'un module de test par module source'"
    )


def main():
    separate_multi_class_test_files()


if __name__ == "__main__":
    main()
