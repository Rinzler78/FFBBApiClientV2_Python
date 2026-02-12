#!/usr/bin/env python3
"""
Script pour corriger la structure des tests en s'assurant qu'il y ait un module de test
par module source, avec une numérotation cohérente basée sur les dépendances.
"""

import ast
from pathlib import Path


def create_source_module_mapping():
    """Crée un mapping des modules source avec des numéros logiques basés sur les catégories."""
    # Lire la liste des modules source
    source_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/src/ffbb_api_client_v2"
    )
    source_files = list(source_dir.glob("*.py"))

    # Extraire les noms des modules (sans l'extension .py)
    modules = []
    for file in source_files:
        if file.name not in ["__init__.py", "py.typed"]:
            module_name = file.stem
            modules.append(module_name)

    # Trier les modules par catégorie pour une attribution ordonnée
    models_modules = []
    client_modules = []
    utils_modules = []
    helper_modules = []
    other_modules = []

    for module in modules:
        if any(
            keyword in module
            for keyword in [
                "response",
                "hit",
                "facet",
                "multi_search",
                "model",
                "field",
                "query",
            ]
        ):
            models_modules.append(module)
        elif any(keyword in module for keyword in ["client", "api"]):
            client_modules.append(module)
        elif any(keyword in module for keyword in ["util", "converter", "request"]):
            utils_modules.append(module)
        elif any(
            keyword in module
            for keyword in [
                "helper",
                "logging",
                "validation",
                "retry",
                "cache",
                "token",
            ]
        ):
            helper_modules.append(module)
        else:
            other_modules.append(module)

    # Attribuer des numéros
    mapping = {}
    current_number = 100

    # Modèles (100-199)
    for module in sorted(models_modules):
        mapping[module] = current_number
        current_number += 1

    # Clients (200-299)
    for module in sorted(client_modules):
        mapping[module] = current_number
        current_number += 1

    # Utilitaires (300-399)
    for module in sorted(utils_modules):
        mapping[module] = current_number
        current_number += 1

    # Helpers (400-499)
    for module in sorted(helper_modules):
        mapping[module] = current_number
        current_number += 1

    # Autres (500+)
    for module in sorted(other_modules):
        mapping[module] = current_number
        current_number += 1

    return mapping, modules


def extract_imports_from_file(filepath):
    """Extrait les imports d'un fichier Python."""
    with open(filepath, encoding="utf-8") as file:
        try:
            content = file.read()
            tree = ast.parse(content)
        except SyntaxError:
            print(f"Erreur de syntaxe dans le fichier: {filepath}")
            return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def find_source_module_in_imports(imports, source_modules):
    """Trouve le module source correspondant dans les imports."""
    for imp in imports:
        # Vérifier si l'import est dans notre package
        if "ffbb_api_client_v2" in imp:
            # Extraire le dernier élément du chemin d'import
            parts = imp.split(".")
            for part in reversed(parts):
                if part in source_modules:
                    return part
    return None


def create_test_file_mapping():
    """Crée un mapping entre les modules source et les fichiers de test."""
    # Charger le mapping des numéros et la liste des modules
    source_mapping, source_modules = create_source_module_mapping()

    # Dossier des tests
    tests_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"
    )

    print("Analyse des fichiers de test existants...")
    print(f"Dossier des tests: {tests_dir}")
    print("=" * 80)

    # Trouver tous les fichiers de test
    test_files = list(tests_dir.rglob("test_*.py"))

    print(f"Nombre de fichiers de test trouvés: {len(test_files)}")

    # Créer un mapping entre modules source et fichiers de test
    module_to_test_files = {}

    for test_file in test_files:
        # Extraire les imports du fichier de test
        imports = extract_imports_from_file(test_file)

        # Trouver le module source correspondant dans les imports
        source_module = find_source_module_in_imports(imports, source_modules)

        if source_module:
            if source_module not in module_to_test_files:
                module_to_test_files[source_module] = []
            module_to_test_files[source_module].append(test_file)

    print(f"Modules source avec fichiers de test associés: {len(module_to_test_files)}")

    # Afficher les associations
    for module, test_files_list in module_to_test_files.items():
        print(f"{module}: {len(test_files_list)} fichier(s)")
        for tf in test_files_list:
            print(f"  - {tf.name}")

    # Créer un mapping pour les modules sans fichiers de test
    modules_without_tests = []
    for module in source_modules:
        if module not in module_to_test_files:
            modules_without_tests.append(module)

    print(f"\\nModules sans fichiers de test: {len(modules_without_tests)}")
    for module in modules_without_tests:
        print(f"  - {module}")

    return module_to_test_files, modules_without_tests, source_mapping


def main():
    module_to_test_files, modules_without_tests, source_mapping = (
        create_test_file_mapping()
    )

    print("\\n" + "=" * 80)
    print("RÉSUMÉ:")
    print(f"- Nombre total de modules source: {len(source_mapping)}")
    print(f"- Modules avec tests: {len(module_to_test_files)}")
    print(f"- Modules sans tests: {len(modules_without_tests)}")

    print("\\nRECOMMANDATIONS:")
    print("1. Créer des fichiers de test pour les modules sans tests")
    print("2. Fusionner les fichiers de test multiples pour un même module")
    print("3. Numéroter les fichiers de test selon le mapping source")

    # Afficher le mapping source pour référence
    print("\\nMapping des modules source:")
    print("-" * 40)
    for module, number in sorted(source_mapping.items(), key=lambda x: x[1]):
        print(f"{number:3d} - {module}")


if __name__ == "__main__":
    main()
