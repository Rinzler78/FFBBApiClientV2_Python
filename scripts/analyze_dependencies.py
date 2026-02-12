#!/usr/bin/env python3
"""
Script pour analyser les dépendances entre les modules source et générer une numérotation logique.
"""

import ast
from pathlib import Path


class DependencyAnalyzer:
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
                        if len(parts) > 0:
                            module_part = parts[-1]
                            if module_part != module_name and module_part in [
                                f.stem
                                for f in self.source_dir.glob("*.py")
                                if f.name not in ["__init__.py", "py.typed"]
                            ]:
                                local_imports.append(module_part)

                self.imports_map[module_name] = imports
                self.dependencies[module_name] = local_imports

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
        # Calculer les dépendances entrantes pour chaque nœud
        incoming_edges = {node: 0 for node in graph}
        for node, deps in graph.items():
            for dep in deps:
                if dep in incoming_edges:
                    incoming_edges[node] += 1

        # Trouver les nœuds sans dépendances entrantes
        queue = []
        for node in graph:
            if incoming_edges[node] == 0:
                queue.append(node)

        result = []
        while queue:
            node = queue.pop(0)
            result.append(node)

            # Réduire le compteur pour les nœuds dépendants
            for dependent_node in graph:
                if node in graph[dependent_node]:
                    incoming_edges[dependent_node] -= 1
                    if incoming_edges[dependent_node] == 0:
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

        # Créer un mapping de module vers numéro
        numbering = {}

        # Regrouper par niveaux de dépendance
        levels = {}
        for module in ordered_modules:
            level = self.calculate_level(module, graph, {})
            if level not in levels:
                levels[level] = []
            levels[level].append(module)

        # Attribuer des numéros par niveau
        current_number = 100
        for level in sorted(levels.keys()):
            modules_in_level = sorted(levels[level])
            for module in modules_in_level:
                numbering[module] = current_number
                current_number += 1

        return numbering

    def calculate_level(self, module, graph, memo):
        """Calcule le niveau de dépendance d'un module."""
        if module in memo:
            return memo[module]

        if not graph[module]:  # Aucune dépendance
            memo[module] = 0
            return 0

        # Le niveau est le maximum des niveaux de dépendances + 1
        max_dep_level = 0
        for dep in graph[module]:
            dep_level = self.calculate_level(dep, graph, memo)
            max_dep_level = max(max_dep_level, dep_level)

        level = max_dep_level + 1
        memo[module] = level
        return level

    def print_analysis(self):
        """Affiche l'analyse des dépendances."""
        print("Analyse des dépendances entre modules :")
        print("-" * 50)
        for module, deps in self.dependencies.items():
            if deps:
                print(f"{module}: dépend de {deps}")
            else:
                print(f"{module}: aucune dépendance")

        print("\nGraphe des dépendances :")
        print("-" * 50)
        graph = self.build_dependency_graph()
        for module, deps in graph.items():
            print(f"{module} <- {list(deps)}")

        print("\nOrdre de dépendance (tri topologique) :")
        print("-" * 50)
        ordered = self.topological_sort(graph)
        for i, module in enumerate(ordered):
            print(f"{i+1:2d}. {module}")

        print("\nSchéma de numérotation proposé :")
        print("-" * 50)
        numbering = self.generate_numbering_scheme()
        for module in sorted(numbering.keys(), key=lambda x: numbering[x]):
            print(f"{numbering[module]:3d} - {module}")


def main():
    # Dossier source
    src_dir = "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/src/ffbb_api_client_v2"

    print("Analyse des dépendances entre modules source...")
    print(f"Dossier analysé: {src_dir}")
    print("=" * 80)

    analyzer = DependencyAnalyzer(src_dir)
    analyzer.analyze_all_modules()
    analyzer.print_analysis()


if __name__ == "__main__":
    main()
