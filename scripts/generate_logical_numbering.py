#!/usr/bin/env python3
"""
Script pour générer une numérotation logique basée sur les relations de dépendance réelles entre les modules.
"""

import ast
from pathlib import Path


def extract_imports_from_file(file_path):
    """Extrait les imports d'un fichier Python."""
    with open(file_path, encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            print(
                f"Avertissement: Impossible de parser {file_path} - erreur de syntaxe"
            )
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


def build_dependency_graph(source_dir):
    """Construit un graphe de dépendances entre les modules."""
    # Lire la liste des modules source de manière récursive
    modules = {}
    for file_path in source_dir.rglob("*.py"):
        if file_path.name not in ["__init__.py", "py.typed"]:
            module_name = file_path.stem
            modules[module_name] = {
                "path": file_path,
                "imports": extract_imports_from_file(file_path),
            }

    print(f"Trouvé {len(modules)} modules")

    # Construire le graphe de dépendances
    dependencies = {}
    for module_name, module_info in modules.items():
        dependencies[module_name] = set()

        for imported_module in module_info["imports"]:
            # Si l'import est un module local (dans notre projet)
            imported_parts = imported_module.split(".")
            # On s'intéresse au premier élément qui pourrait être un module local
            if imported_parts[0] in modules:
                dependencies[module_name].add(imported_parts[0])
            # Si l'import est de la forme "from . import module" ou "import module"
            elif len(imported_parts) == 1 and imported_parts[0] in modules:
                dependencies[module_name].add(imported_parts[0])

    return dependencies


def topological_sort(dependencies):
    """
    Effectue un tri topologique pour déterminer l'ordre de dépendance.
    Retourne une liste de couches où chaque couche contient des modules
    qui peuvent être traités ensemble car ils ne dépendent que de modules
    des couches précédentes.
    """
    # Copier les dépendances pour ne pas modifier l'original
    graph = {k: v.copy() for k, v in dependencies.items()}

    # Trouver tous les modules sans dépendances
    no_deps = [k for k, v in graph.items() if not v]

    layers = []
    processed = set()

    while no_deps:
        # Cette couche contient tous les modules sans dépendances restantes
        current_layer = no_deps[:]
        layers.append(current_layer)
        processed.update(current_layer)

        # Supprimer ces modules des dépendances des autres
        for module in current_layer:
            del graph[module]

        # Mettre à jour la liste des modules sans dépendances
        no_deps = [k for k, v in graph.items() if not v - processed]

    # Vérifier s'il reste des modules (ce qui indiquerait un cycle)
    if graph:
        print("Attention: Cycle détecté dans les dépendances:")
        for module, deps in graph.items():
            print(f"  {module} dépend de {deps}")
        # Ajouter les modules restants dans une dernière couche
        remaining = list(graph.keys())
        layers.append(remaining)

    return layers


def create_dependency_based_numbering():
    """Crée un mapping basé sur les relations de dépendance réelles entre les modules."""

    source_dir = Path(
        "/Users/bleclereperso/Projects/Python/FFBBApiClientV2_Python/src/ffbb_api_client_v2"
    )

    # Construire le graphe de dépendances
    dependencies = build_dependency_graph(source_dir)

    # Effectuer un tri topologique pour obtenir les couches
    layers = topological_sort(dependencies)

    # Créer le mapping de numérotation
    mapping = {}
    current_number = 0

    for layer_idx, layer in enumerate(layers):
        print(f"Couche {layer_idx}: {len(layer)} modules")
        # Tous les modules de la même couche reçoivent le même numéro
        for module in sorted(layer):
            mapping[module] = current_number
        # Passer au numéro suivant pour la prochaine couche
        current_number += 1

    return mapping, layers


def main():
    mapping, layers = create_dependency_based_numbering()

    print("\nSchéma de numérotation basé sur les relations de dépendance :")
    print("=" * 60)

    # Afficher un échantillon pour vérifier
    print(f"\nTotal: {len(mapping)} modules répartis en {len(layers)} couches")
    print("\nRépartition par couche:")
    for idx, layer in enumerate(layers):
        print(
            f"Couche {idx:03d}: {len(layer)} modules - {sorted(layer)[:10]}{'...' if len(layer) > 10 else ''}"
        )

    print("\nPremiers modules avec leurs numéros:")
    count = 0
    for module in sorted(mapping.keys(), key=lambda x: mapping[x]):
        print(f"{mapping[module]:03d} - {module}")
        count += 1
        if count >= 30:  # Limiter l'affichage
            print("...")
            break

    # Vérifier les exemples spécifiques mentionnés
    print("\nExemples spécifiques:")
    modules_to_check = [
        "logo",
        "id_engagement_equipe",
        "id_organisme_equipe",
        "purple_logo",
    ]
    for module in modules_to_check:
        if module in mapping:
            print(f"{module}: {mapping[module]:03d}")
        else:
            print(f"{module}: non trouvé")

    print("\nAnalyse:")
    print("Si 'logo' ou 'purple_logo' est une propriété de 'id_engagement_equipe',")
    print(
        "alors 'logo'/'purple_logo' devrait avoir un numéro inférieur à 'id_engagement_equipe'"
    )

    # Vérifier si les dépendances conceptuelles sont respectées
    print("\nVérification des relations conceptuelles:")
    if "logo" in mapping and "id_engagement_equipe" in mapping:
        if mapping["logo"] < mapping["id_engagement_equipe"]:
            print(
                f"✓ logo ({mapping['logo']:03d}) < id_engagement_equipe ({mapping['id_engagement_equipe']:03d}) - OK"
            )
        else:
            print(
                f"✗ logo ({mapping['logo']:03d}) > id_engagement_equipe ({mapping['id_engagement_equipe']:03d}) - PROBLÈME"
            )

    if "purple_logo" in mapping and "id_organisme_equipe" in mapping:
        if mapping["purple_logo"] < mapping["id_organisme_equipe"]:
            print(
                f"✓ purple_logo ({mapping['purple_logo']:03d}) < id_organisme_equipe ({mapping['id_organisme_equipe']:03d}) - OK"
            )
        else:
            print(
                f"✗ purple_logo ({mapping['purple_logo']:03d}) > id_organisme_equipe ({mapping['id_organisme_equipe']:03d}) - PROBLÈME"
            )


if __name__ == "__main__":
    main()
