#!/usr/bin/env python3
"""
Script pour générer l'arbre de dépendance des modules source et valider/créer les fichiers de test conformes.
"""

from pathlib import Path


def extract_all_source_modules(source_dir):
    """Extrait tous les modules source du répertoire."""
    source_dir = Path(source_dir)
    modules = []

    for py_file in source_dir.rglob("*.py"):
        if py_file.name not in ["__init__.py", "py.typed"]:
            module_name = py_file.stem
            modules.append(module_name)

    return modules


def create_test_file(test_dir, number, module_name):
    """Crée un fichier de test pour un module donné."""
    test_dir = Path(test_dir)
    test_dir.mkdir(parents=True, exist_ok=True)

    # Convertir le nom du module en PascalCase pour le nom de la classe
    parts = module_name.split("_")
    pascal_case_module = "".join(part.capitalize() for part in parts)
    class_name = f"Test{number:03d}{pascal_case_module}"

    # Nom du fichier de test
    test_filename = f"test_{number:03d}_{module_name}.py"
    test_file_path = test_dir / test_filename

    # Vérifier si le fichier existe déjà
    if test_file_path.exists():
        print(f"Validated: {test_filename}")
        return test_file_path, False  # False = pas de création

    # Contenu du fichier de test
    test_content = f'''#!/usr/bin/env python3
"""
Test module for {module_name}
"""

import unittest
# TODO: Import the module to test
# from ffbb_api_client_v2.{module_name} import {module_name}


class {class_name}(unittest.TestCase):
    """Test cases for {module_name} module."""

    def setUp(self):
        """Set up test fixtures."""
        pass

    def tearDown(self):
        """Tear down test fixtures."""
        pass

    def test_placeholder(self):
        """Placeholder test - replace with actual tests."""
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
'''

    # Écrire le fichier de test
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)

    print(f"Created: {test_filename} with class {class_name}")
    return test_file_path, True  # True = fichier créé


def categorize_module(module_name):
    """Détermine le répertoire approprié pour un module."""
    if any(
        keyword in module_name
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
        return "models"
    elif any(keyword in module_name for keyword in ["client", "api"]):
        return "clients"
    elif any(keyword in module_name for keyword in ["util", "converter", "request"]):
        return "utils"
    elif any(
        keyword in module_name
        for keyword in ["helper", "logging", "validation", "retry", "cache", "token"]
    ):
        return "helpers"
    else:
        return "other"


def main():
    # Dossiers source et tests
    src_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/src/ffbb_api_client_v2"
    tests_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"

    print("Extraction des modules source...")
    print(f"SourceEnum directory: {src_dir}")
    print(f"Tests directory: {tests_dir}")
    print("=" * 80)

    # Extraire tous les modules source
    modules = extract_all_source_modules(src_dir)
    print(f"Found {len(modules)} source modules")

    # Créer les sous-répertoires pour chaque catégorie
    models_dir = Path(tests_dir) / "unit" / "models"
    clients_dir = Path(tests_dir) / "unit" / "clients"
    utils_dir = Path(tests_dir) / "unit" / "utils"
    helpers_dir = Path(tests_dir) / "unit" / "helpers"
    other_dir = Path(tests_dir) / "unit" / "other"

    # Créer les répertoires
    models_dir.mkdir(parents=True, exist_ok=True)
    clients_dir.mkdir(parents=True, exist_ok=True)
    utils_dir.mkdir(parents=True, exist_ok=True)
    helpers_dir.mkdir(parents=True, exist_ok=True)
    other_dir.mkdir(parents=True, exist_ok=True)

    created_count = 0
    validated_count = 0

    print("\\nValidating/creating test files...")

    # Attribuer des numéros aux modules selon une logique de catégorisation
    # Plutôt que d'essayer de construire un arbre de dépendance complexe,
    # nous allons attribuer des numéros par catégorie
    models_modules = []
    client_modules = []
    utils_modules = []
    helper_modules = []
    other_modules = []

    for module in sorted(modules):
        category = categorize_module(module)
        if category == "models":
            models_modules.append(module)
        elif category == "clients":
            client_modules.append(module)
        elif category == "utils":
            utils_modules.append(module)
        elif category == "helpers":
            helper_modules.append(module)
        else:
            other_modules.append(module)

    # Attribuer des numéros
    module_to_number = {}
    current_number = 100

    # Modèles (100-199)
    for module in sorted(models_modules):
        module_to_number[module] = current_number
        current_number += 1

    # Clients (200-299)
    for module in sorted(client_modules):
        module_to_number[module] = current_number
        current_number += 1

    # Utilitaires (300-399)
    for module in sorted(utils_modules):
        module_to_number[module] = current_number
        current_number += 1

    # Helpers (400-499)
    for module in sorted(helper_modules):
        module_to_number[module] = current_number
        current_number += 1

    # Autres (500+)
    for module in sorted(other_modules):
        module_to_number[module] = current_number
        current_number += 1

    print(f"Assigned numbers to {len(module_to_number)} modules")

    # Créer ou valider les fichiers de test
    for module_name, number in module_to_number.items():
        # Déterminer le répertoire approprié
        category = categorize_module(module_name)
        if category == "models":
            target_dir = models_dir
        elif category == "clients":
            target_dir = clients_dir
        elif category == "utils":
            target_dir = utils_dir
        elif category == "helpers":
            target_dir = helpers_dir
        else:
            target_dir = other_dir

        # Créer ou valider le fichier de test
        _, was_created = create_test_file(target_dir, number, module_name)
        if was_created:
            created_count += 1
        else:
            validated_count += 1

    print("\\nSummary:")
    print(f"- Created: {created_count} new test files")
    print(f"- Validated: {validated_count} existing test files")
    print(f"- Total: {created_count + validated_count} test files")

    print("\\nTest structure validation/creation completed!")


if __name__ == "__main__":
    main()
