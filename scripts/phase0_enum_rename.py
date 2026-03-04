#!/usr/bin/env python3
"""Phase 0: Rename all enum classes to *Enum suffix, rename files, update imports.

Strategy:
1. Update ALL file contents first (module paths + class names) in a single pass
2. Then git mv to rename the files
3. Then handle deduplication (deletes)

Key insight: Module path renames must ONLY match import contexts, not attribute access.
e.g., "from .code_enum import" must be updated, but "self.code" must NOT.
"""

import os
import re
import subprocess

WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(WORKTREE, "src", "ffbb_api_client_v2")
MODELS = os.path.join(SRC, "models")
MEILI_MODELS = os.path.join(SRC, "meilisearch_ffbb", "models")

# (old_class, new_class, old_file_stem, new_file_stem, directory)
# Sorted longest old_class first for safe word-boundary replacement
RENAMES = [
    (
        "CompetitionOrigineTypeCompetitionEnum",
        "CompetitionOrigineTypeCompetitionEnum",
        "competition_origine_type_competition",
        "competition_origine_type_competition_enum",
        "models",
    ),
    (
        "CategorieChampionnat3X3LibelleEnum",
        "CategorieChampionnat3X3LibelleEnum",
        "terrains_categorie_championnat_3x3_libelle",
        "terrains_categorie_championnat_3x3_libelle_enum",
        "models",
    ),
    (
        "PublicationInternetEnum",
        "PublicationInternetEnum",
        "publication_internet",
        "publication_internet_enum",
        "models",
    ),
    (
        "DocumentFlyerTypeEnum",
        "DocumentFlyerTypeEnum",
        "document_flyer_type",
        "document_flyer_type_enum",
        "models",
    ),
    (
        "CompetitionTypeEnum",
        "CompetitionTypeEnum",
        "competition_type",
        "competition_type_enum",
        "models",
    ),
    (
        "TypeCompetitionEnum",
        "TypeCompetitionEnum",
        "type_competition",
        "type_competition_enum",
        "models",
    ),
    (
        "OrganisateurTypeEnum",
        "OrganisateurTypeEnum",
        "organisateur_type",
        "organisateur_type_enum",
        "models",
    ),
    (
        "CoordonneesTypeEnum",
        "CoordonneesTypeEnum",
        "coordonnees_type",
        "coordonnees_type_enum",
        "models",
    ),
    (
        "CategorieTypeEnum",
        "CategorieTypeEnum",
        "categorie_type",
        "categorie_type_enum",
        "models",
    ),
    (
        "CodeFonctionEnum",
        "CodeFonctionEnum",
        "code_fonction",
        "code_fonction_enum",
        "models",
    ),
    (
        "ContactRoleEnum",
        "ContactRoleEnum",
        "contact_role",
        "contact_role_enum",
        "models",
    ),
    ("TypeLeagueEnum", "TypeLeagueEnum", "type_league", "type_league_enum", "models"),
    ("NiveauTypeEnum", "NiveauTypeEnum", "niveau_type", "niveau_type_enum", "models"),
    ("PhaseCodeEnum", "PhaseCodeEnum", "phase_code", "phase_code_enum", "models"),
    ("AgeGroupEnum", "AgeGroupEnum", "age_group", "age_group_enum", "models"),
    ("EchelonEnum", "EchelonEnum", "echelon", "echelon_enum", "models"),
    ("GenderEnum", "GenderEnum", "gender", "gender_enum", "models"),
    ("NiveauEnum", "NiveauEnum", "niveau", "niveau_enum", "models"),
    ("ObjectifEnum", "ObjectifEnum", "objectif", "objectif_enum", "models"),
    ("PratiqueEnum", "PratiqueEnum", "pratique", "pratique_enum", "models"),
    ("SexeEnum", "SexeEnum", "sexe", "sexe_enum", "models"),
    ("LabelEnum", "LabelEnum", "label", "label_enum", "models"),
    ("SourceEnum", "SourceEnum", "source", "source_enum", "models"),
    ("StatusEnum", "StatusEnum", "status", "status_enum", "models"),
    ("EtatEnum", "EtatEnum", "etat", "etat_enum", "models"),
    ("JourEnum", "JourEnum", "jour", "jour_enum", "models"),
    ("CodeEnum", "CodeEnum", "code", "code_enum", "models"),
]

SPECIAL_RENAMES = [
    (
        "HitType",
        "PratiquesHitTypeEnum",
        "pratiques_hit_type",
        "pratiques_hit_type_enum",
        "models",
    ),
    (
        "HitType",
        "TournoisHitTypeEnum",
        "tournois_hit_type",
        "tournois_hit_type_enum",
        "models",
    ),
    (
        "TournoiTypes3x3LibelleEnum",
        "TournoiTypes3x3LibelleEnum",
        "tournoi_types_3x3_libelle_enum",
        "tournoi_types_3x3_libelle_enum",
        "models",
    ),
    ("Name", "TerrainsNameEnum", "terrains_name", "terrains_name_enum", "meili"),
    (
        "Storage",
        "TerrainsStorageEnum",
        "terrains_storage",
        "terrains_storage_enum",
        "meili",
    ),
]


def find_all_python_files(*roots):
    result = []
    for root in roots:
        full_root = os.path.join(WORKTREE, root)
        if not os.path.isdir(full_root):
            continue
        for dirpath, _, filenames in os.walk(full_root):
            for fn in filenames:
                if fn.endswith(".py"):
                    result.append(os.path.join(dirpath, fn))
    return sorted(set(result))


def update_module_paths(content):
    """Replace old module stems with new ones ONLY in import statements.

    Matches patterns like:
    - from .code_enum import ...
    - from ..models.code_enum import ...
    - from .code_fonction_enum import ...
    Does NOT match:
    - self.code
    - result["code"]
    """
    all_renames = RENAMES + SPECIAL_RENAMES
    sorted_renames = sorted(all_renames, key=lambda r: len(r[2]), reverse=True)

    for _, _, old_stem, new_stem, _ in sorted_renames:
        if old_stem == new_stem:
            continue
        # Only replace in import contexts:
        # Pattern: "from" ... "." old_stem " import" or just "." old_stem at end of from clause
        # The key: the dot must be preceded by another dot or whitespace (import context)
        # not by a word character (attribute access like self.code)
        content = re.sub(
            r"((?:from\s+\.[\w.]*)\.)" + re.escape(old_stem) + r"(?=\s)",
            lambda m: m.group(1) + new_stem,
            content,
        )
        # Simpler approach: match ".old_stem import" or ".old_stem\n" where preceded by a dot
        # i.e., the character before our dot is also a dot (relative import) or space
        content = re.sub(
            r"(\.)" + re.escape(old_stem) + r"(\s+import\b)",
            r"\g<1>" + new_stem + r"\2",
            content,
        )
        # Handle: from .old_stem import (single level)
        content = re.sub(
            r"(from\s+\.)" + re.escape(old_stem) + r"(\s+import\b)",
            r"\1" + new_stem + r"\2",
            content,
        )
        # Handle path strings like "/old_stem.py"
        content = content.replace(f"/{old_stem}.py", f"/{new_stem}.py")
        # Handle string references like "old_stem" in test paths etc.
        content = content.replace(f'"{old_stem}.py"', f'"{new_stem}.py"')

    return content


def update_class_names(content, file_path):
    """Replace old class names with new ones (PascalCase only, word-boundary)."""
    for old_cls, new_cls, _, _, _ in RENAMES:
        if old_cls == new_cls:
            continue
        content = re.sub(r"\b" + re.escape(old_cls) + r"\b", new_cls, content)

    # Handle HitType (context-dependent)
    if re.search(r"\bHitType\b", content):
        has_pratiques = (
            "pratiques_hit_type" in content
            or "pratiques" in os.path.basename(file_path)
        )
        has_tournois = "tournois_hit_type" in content or "tournois" in os.path.basename(
            file_path
        )
        if has_pratiques and not has_tournois:
            content = re.sub(r"\bHitType\b", "PratiquesHitTypeEnum", content)
        elif has_tournois and not has_pratiques:
            content = re.sub(r"\bHitType\b", "TournoisHitTypeEnum", content)

    # Handle TournoiTypes3x3LibelleEnum (only in tournoi_types_3x3 context)
    if re.search(r"\bLibelle\b", content):
        if (
            "tournoi_types_3x3_libelle_enum" in content
            or "tournoi_types_3x3_libelle_enum" in file_path
        ):
            content = re.sub(r"\bLibelle\b", "TournoiTypes3x3LibelleEnum", content)

    # Handle Name -> TerrainsNameEnum (only in terrains_name file)
    if re.search(r"\bName\b", content) and "terrains_name" in file_path:
        content = re.sub(r"\bName\b", "TerrainsNameEnum", content)

    # Handle Storage -> TerrainsStorageEnum (only in terrains_storage file)
    if re.search(r"\bStorage\b", content) and "terrains_storage" in file_path:
        content = re.sub(r"\bStorage\b", "TerrainsStorageEnum", content)

    return content


def main():
    os.chdir(WORKTREE)
    all_py = find_all_python_files("src", "tests", "scripts", "examples")

    # === Step 1: Update ALL file contents ===
    print("=== Step 1: Update file contents ===")
    count = 0
    for fpath in all_py:
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        original = content
        content = update_module_paths(content)
        content = update_class_names(content, fpath)

        # Fix SexeEnum.MIXTE -> SexeEnum.MIXTE
        content = content.replace("SexeEnum.MIXTE", "SexeEnum.MIXTE")
        content = content.replace('MIXTE = "Mixte"', 'MIXTE = "Mixte"')

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1

    print(f"  Updated {count} files")

    # === Step 2: Verify source enum class definitions ===
    print("\n=== Step 2: Verify source enum class definitions ===")
    for items in [RENAMES, SPECIAL_RENAMES]:
        for old_cls, new_cls, old_stem, _, loc in items:
            if old_cls == new_cls:
                continue
            dirpath = MODELS if loc == "models" else MEILI_MODELS
            filepath = os.path.join(dirpath, f"{old_stem}.py")
            if not os.path.exists(filepath):
                continue
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            if f"class {old_cls}(" in content:
                new_content = re.sub(
                    r"\b" + re.escape(old_cls) + r"\b", new_cls, content
                )
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  Fixed class def: {old_cls} -> {new_cls} in {old_stem}.py")

    # === Step 3: Git mv files ===
    print("\n=== Step 3: Git mv files ===")
    all_renames = RENAMES + SPECIAL_RENAMES
    for _, _, old_stem, new_stem, loc in all_renames:
        if old_stem == new_stem:
            continue
        dirpath = MODELS if loc == "models" else MEILI_MODELS
        old_path = os.path.join(dirpath, f"{old_stem}.py")
        new_path = os.path.join(dirpath, f"{new_stem}.py")
        if not os.path.exists(old_path):
            print(f"  SKIP: {old_stem}.py (not found)")
            continue
        subprocess.run(["git", "mv", old_path, new_path], cwd=WORKTREE, check=True)
        print(f"  {old_stem}.py -> {new_stem}.py")

    # === Step 4: Meilisearch deduplication ===
    print("\n=== Step 4: Deduplication ===")
    tournois_hit = os.path.join(MEILI_MODELS, "tournois_hit.py")
    if os.path.exists(tournois_hit):
        with open(tournois_hit, encoding="utf-8") as f:
            content = f.read()
        content = content.replace(
            "from .terrains_sexe_enum import SexeEnum",
            "from ...models.sexe_enum import SexeEnum",
        )
        with open(tournois_hit, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Updated tournois_hit.py -> global SexeEnum")

    terrains_sexe = os.path.join(MEILI_MODELS, "terrains_sexe_enum.py")
    if os.path.exists(terrains_sexe):
        subprocess.run(["git", "rm", "-f", terrains_sexe], cwd=WORKTREE, check=True)
        print("  Deleted terrains_sexe_enum.py")

    tournois_libelle = os.path.join(MEILI_MODELS, "tournois_libelle.py")
    if os.path.exists(tournois_libelle):
        subprocess.run(["git", "rm", "-f", tournois_libelle], cwd=WORKTREE, check=True)
        print("  Deleted tournois_libelle.py")

    # === Step 5: Verify no stale module refs ===
    print("\n=== Step 5: Check stale refs ===")
    all_renames_dict = {r[2]: r[3] for r in all_renames if r[2] != r[3]}
    stale = 0
    new_py = find_all_python_files("src", "tests", "scripts", "examples")
    for fpath in new_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        for old_stem, new_stem in all_renames_dict.items():
            # Check for import-style references to old module
            if re.search(r"from\s+.*\." + re.escape(old_stem) + r"\s+import", content):
                print(
                    f"  STALE import: .{old_stem} in {os.path.relpath(fpath, WORKTREE)}"
                )
                stale += 1
    if stale == 0:
        print("  No stale import references found")

    print("\n=== Phase 0 complete ===")


if __name__ == "__main__":
    main()
