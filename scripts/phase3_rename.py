#!/usr/bin/env python3
"""Phase 3: Model Renaming - remove ID/Class/Ref suffixes."""

import glob
import os
import re
import subprocess

WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(WORKTREE, "src", "ffbb_api_client_v2", "models")
MEILI_MODELS = os.path.join(
    WORKTREE, "src", "ffbb_api_client_v2", "meilisearch_ffbb", "models"
)


def find_all_py(*dirs):
    files = []
    for d in dirs:
        full = os.path.join(WORKTREE, d)
        files.extend(glob.glob(os.path.join(full, "**", "*.py"), recursive=True))
    return files


def replace_class(files, old_cls, new_cls):
    """Word-boundary class rename across all files."""
    count = 0
    pattern = re.compile(r"\b" + re.escape(old_cls) + r"\b")
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        new_content = pattern.sub(new_cls, content)
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
    return count


def replace_module(files, old_mod, new_mod):
    """Replace module path in import statements only."""
    count = 0
    # Match: from .old_mod import  or  from ...models.old_mod import
    pattern = re.compile(r"(from\s+[.\w]*)\." + re.escape(old_mod) + r"(\s+import\b)")
    replacement = r"\1." + new_mod + r"\2"
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        new_content = pattern.sub(replacement, content)
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
    return count


def git_mv(old_path, new_path):
    if os.path.exists(old_path):
        subprocess.run(["git", "mv", old_path, new_path], cwd=WORKTREE, check=True)


def git_rm(path):
    if os.path.exists(path):
        subprocess.run(["git", "rm", "-f", path], cwd=WORKTREE, check=True)


def remove_import_line(files, pattern):
    count = 0
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = [ln for ln in lines if not re.search(pattern, ln)]
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            count += 1
    return count


def main():
    os.chdir(WORKTREE)
    all_py = find_all_py("src", "tests", "scripts", "examples")

    # === Simple renames (class + file, in models/) ===
    simple_renames = [
        # (old_cls, new_cls, old_file_stem, new_file_stem, base_dir)
        (
            "ExternalCompetition",
            "ExternalCompetition",
            "external_competition_id",
            "external_competition",
            MODELS,
        ),
        (
            "ExternalRencontre",
            "ExternalRencontre",
            "external_id",
            "external_rencontre",
            MODELS,
        ),
        (
            "OrganismeEquipe",
            "OrganismeEquipe",
            "id_organisme_equipe",
            "organisme_equipe",
            MODELS,
        ),
        ("SexeFacet", "SexeFacet", "sexe_class", "sexe_facet", MODELS),
        ("NiveauFacet", "NiveauFacet", "niveau_class", "niveau_facet", MODELS),
        ("TypeFacet", "TypeFacet", "type_class", "type_facet", MODELS),
        (
            "TournoiTypeFacet",
            "TournoiTypeFacet",
            "tournoi_type_class",
            "tournoi_type_facet",
            MODELS,
        ),
        (
            "PratiquesTypeFacet",
            "PratiquesTypeFacet",
            "pratiques_type_class",
            "pratiques_type_facet",
            MEILI_MODELS,
        ),
    ]

    for old_cls, new_cls, old_stem, new_stem, base_dir in simple_renames:
        print(f"\n=== {old_cls} -> {new_cls} ===")

        # 1) Update module paths in imports (before git mv)
        n = replace_module(all_py, old_stem, new_stem)
        print(f"  Module paths: {n} files")

        # 2) Update class names
        n = replace_class(all_py, old_cls, new_cls)
        print(f"  Class names: {n} files")

        # 3) Git mv the file
        old_path = os.path.join(base_dir, f"{old_stem}.py")
        new_path = os.path.join(base_dir, f"{new_stem}.py")
        git_mv(old_path, new_path)
        print(f"  Renamed {old_stem}.py -> {new_stem}.py")

    # === Poule -> Poule (merge, not rename) ===
    print("\n=== Poule -> Poule (merge) ===")
    # Replace class name
    n = replace_class(all_py, "Poule", "Poule")
    print(f"  Class names: {n} files")
    # Replace module: id_poule -> poule
    n = replace_module(all_py, "id_poule", "poule")
    print(f"  Module paths: {n} files")
    # Delete id_poule.py
    git_rm(os.path.join(MODELS, "id_poule.py"))
    print("  Deleted id_poule.py")

    print("\n=== Phase 3 complete ===")


if __name__ == "__main__":
    main()
