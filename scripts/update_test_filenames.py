#!/usr/bin/env python3
"""
Script pour mettre à jour les noms de fichiers de test selon la nouvelle numérotation logique.
"""

import os
import re
from pathlib import Path

from generate_logical_numbering import create_dependency_based_numbering


def update_test_filenames():
    """Met à jour les noms de fichiers de test selon la nouvelle numérotation."""

    # Obtenir la nouvelle numérotation
    mapping, layers = create_dependency_based_numbering()

    print(f"Nombre total de modules: {len(mapping)}")
    print(f"Nombre de couches: {len(layers)}")

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

    # Trouver tous les fichiers de test dans tous les dossiers
    all_test_files = []
    for test_dir in test_dirs:
        if test_dir.exists():
            test_files = list(test_dir.glob("test_*.py"))
            all_test_files.extend(test_files)

    print(f"Nombre total de fichiers de test trouvés: {len(all_test_files)}")

    # Pour chaque fichier de test, extraire le nom de module et le numéro actuel
    updates_needed = []

    for test_file in all_test_files:
        # Extraire le numéro et le nom de module à partir du nom de fichier
        match = re.match(r"test_(\d+)_(.+)\.py", test_file.name)
        if match:
            current_number = int(match.group(1))
            module_name = match.group(2)

            # Vérifier si le module existe dans notre mapping
            if module_name in mapping:
                new_number = mapping[module_name]

                if current_number != new_number:
                    new_filename = f"test_{new_number:03d}_{module_name}.py"
                    updates_needed.append(
                        (
                            test_file,
                            Path(new_filename),
                            current_number,
                            new_number,
                            module_name,
                            test_file.parent,
                        )
                    )
            else:
                print(
                    f"Avertissement: Module '{module_name}' non trouvé dans le mapping (fichier: {test_file.name})"
                )

    print(f"\nFichiers nécessitant une mise à jour: {len(updates_needed)}")

    # Afficher les changements qui vont être faits
    for (
        old_path,
        new_filename,
        old_num,
        new_num,
        module_name,
        parent_dir,
    ) in updates_needed:
        print(f"{old_num:03d} -> {new_num:03d}: {module_name}")

    # Procéder aux changements
    if updates_needed:
        for (
            old_path,
            new_filename,
            old_num,
            new_num,
            module_name,
            parent_dir,
        ) in updates_needed:
            new_path = parent_dir / new_filename
            print(f"Renommage: {old_path.name} -> {new_path.name}")
            os.rename(old_path, new_path)
        print("Mise à jour terminée!")
    else:
        print("Aucune mise à jour nécessaire.")


if __name__ == "__main__":
    update_test_filenames()
