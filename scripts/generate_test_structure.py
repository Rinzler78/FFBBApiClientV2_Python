#!/usr/bin/env python3
"""
Script pour générer l'arbre de dépendance des modules source et créer les fichiers de test conformes.
"""

import ast
from pathlib import Path


class DependencyTreeGenerator:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.dependencies = {}
        self.imports_map = {}

    def extract_imports(self, filepath):
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

    def analyze_all_modules(self):
        """Analyse tous les modules pour identifier les dépendances."""
        # Parcourir tous les fichiers Python dans le répertoire source
        py_files = list(self.source_dir.rglob("*.py"))

        for py_file in py_files:
            if py_file.name not in ["__init__.py", "py.typed"]:
                module_name = py_file.stem  # Nom du fichier sans extension
                imports = self.extract_imports(py_file)

                # Filtrer les imports pour ne garder que ceux qui proviennent du même package
                local_imports = []
                for imp in imports:
                    # Vérifier si l'import est dans notre package
                    if "ffbb_api_client_v2" in imp:
                        # Extraire le dernier élément du chemin d'import
                        parts = imp.split(".")
                        for part in reversed(parts):
                            if part != module_name and part in [
                                f.stem
                                for f in self.source_dir.rglob("*.py")
                                if f.name not in ["__init__.py", "py.typed"]
                            ]:
                                local_imports.append(part)
                                break

                self.imports_map[module_name] = imports
                self.dependencies[module_name] = list(
                    set(local_imports)
                )  # Éliminer les doublons

    def build_dependency_graph(self):
        """Construit un graphe de dépendance."""
        graph = {}
        all_modules = set()

        # Collecter tous les modules
        for module, deps in self.dependencies.items():
            all_modules.add(module)
            all_modules.update(deps)

        # Initialiser le graphe
        for module in all_modules:
            graph[module] = set()

        # Remplir les dépendances
        for module, deps in self.dependencies.items():
            graph[module].update(deps)

        return graph

    def topological_sort(self, graph):
        """Effectue un tri topologique pour déterminer l'ordre de dépendance."""
        # Calculer les dépendances sortantes pour chaque nœud
        outgoing_edges = {node: set() for node in graph}
        for node, deps in graph.items():
            for dep in deps:
                if dep in outgoing_edges:
                    outgoing_edges[dep].add(node)

        # Trouver les nœuds sans dépendances entrantes (niveau 0)
        queue = []
        in_degree = {node: len(graph[node]) for node in graph}

        for node, degree in in_degree.items():
            if degree == 0:
                queue.append(node)

        result = []
        while queue:
            node = queue.pop(0)
            result.append(node)

            # Réduire le degré pour les nœuds dépendants
            for dependent_node in outgoing_edges[node]:
                in_degree[dependent_node] -= 1
                if in_degree[dependent_node] == 0:
                    queue.append(dependent_node)

        # Vérifier s'il y a des cycles
        if len(result) != len(graph):
            print("Attention : détection d'un cycle dans les dépendances")
            # Ajouter les nœuds manquants à la fin
            processed = set(result)
            for node in graph:
                if node not in processed:
                    result.append(node)

        return result

    def generate_numbering_scheme(self):
        """Génère un schéma de numérotation basé sur les dépendances."""
        graph = self.build_dependency_graph()
        ordered_modules = self.topological_sort(graph)

        # Créer un mapping de numéro vers module
        numbering = {}
        current_number = 100

        for module in ordered_modules:
            numbering[current_number] = module
            current_number += 1

        return numbering

    def create_test_file(self, test_dir, number, module_name):
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
        return test_file_path

    def validate_or_create_test_files(self, tests_base_dir):
        """Valide ou crée les fichiers de test pour chaque module."""
        numbering_scheme = self.generate_numbering_scheme()

        print("Generating test files based on dependency tree...")
        print(f"Number of modules to create tests for: {len(numbering_scheme)}")

        # Créer les sous-répertoires pour chaque catégorie
        models_dir = Path(tests_base_dir) / "unit" / "models"
        clients_dir = Path(tests_base_dir) / "unit" / "clients"
        utils_dir = Path(tests_base_dir) / "unit" / "utils"
        helpers_dir = Path(tests_base_dir) / "unit" / "helpers"
        other_dir = Path(tests_base_dir) / "unit" / "other"

        # Créer les répertoires
        models_dir.mkdir(parents=True, exist_ok=True)
        clients_dir.mkdir(parents=True, exist_ok=True)
        utils_dir.mkdir(parents=True, exist_ok=True)
        helpers_dir.mkdir(parents=True, exist_ok=True)
        other_dir.mkdir(parents=True, exist_ok=True)

        created_count = 0
        validated_count = 0

        for number, module_name in numbering_scheme.items():
            # Déterminer le répertoire approprié en fonction du nom du module
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
                target_dir = models_dir
            elif any(keyword in module_name for keyword in ["client", "api"]):
                target_dir = clients_dir
            elif any(
                keyword in module_name for keyword in ["util", "converter", "request"]
            ):
                target_dir = utils_dir
            elif any(
                keyword in module_name
                for keyword in [
                    "helper",
                    "logging",
                    "validation",
                    "retry",
                    "cache",
                    "token",
                ]
            ):
                target_dir = helpers_dir
            else:
                target_dir = other_dir

            # Vérifier si le fichier de test existe déjà
            test_filename = f"test_{number:03d}_{module_name}.py"
            test_file_path = target_dir / test_filename

            if test_file_path.exists():
                print(f"Validated: {test_filename}")
                validated_count += 1
            else:
                self.create_test_file(target_dir, number, module_name)
                created_count += 1

        print("\\nSummary:")
        print(f"- Created: {created_count} test files")
        print(f"- Validated: {validated_count} existing test files")
        print(f"- Total: {created_count + validated_count} test files")


def main():
    # Dossier source
    src_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/src/ffbb_api_client_v2"
    tests_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/tests"

    print("Analysis of source module dependencies...")
    print(f"Source directory: {src_dir}")
    print(f"Tests directory: {tests_dir}")
    print("=" * 80)

    generator = DependencyTreeGenerator(src_dir)
    generator.analyze_all_modules()

    print("Dependency tree generated.")
    print("Creating/updating test files...")

    generator.validate_or_create_test_files(tests_dir)

    print("\\nDependency-based test structure creation completed!")


if __name__ == "__main__":
    main()
