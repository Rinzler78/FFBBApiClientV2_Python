#!/usr/bin/env python3
"""Phase 1: Model deduplication - merge subset models into supersets."""

import os
import re
import subprocess

WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(WORKTREE, "src", "ffbb_api_client_v2")
MODELS = os.path.join(SRC, "models")
MEILI_MODELS = os.path.join(SRC, "meilisearch_ffbb", "models")


def find_all_python_files(*roots):
    result = []
    for root in roots:
        full = os.path.join(WORKTREE, root)
        if not os.path.isdir(full):
            continue
        for dp, _, fns in os.walk(full):
            for fn in fns:
                if fn.endswith(".py"):
                    result.append(os.path.join(dp, fn))
    return sorted(set(result))


def replace_in_all(files, old, new):
    """Simple string replacement across all files."""
    count = 0
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        if old not in content:
            continue
        content = content.replace(old, new)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
    return count


def regex_replace_in_all(files, pattern, replacement):
    """Regex replacement across all files."""
    count = 0
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
    return count


def git_rm(filepath):
    if os.path.exists(filepath):
        subprocess.run(["git", "rm", "-f", filepath], cwd=WORKTREE, check=True)
        return True
    return False


def remove_import_line(files, pattern):
    """Remove import lines matching a pattern."""
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
    all_py = find_all_python_files("src", "tests", "scripts", "examples")

    # ========================================================================
    # 1. Logo -> Logo
    # ========================================================================
    print("=== 1. Logo -> Logo ===")
    # Replace class references
    n = regex_replace_in_all(all_py, r"\bPurpleLogo\b", "Logo")
    print(f"  Replaced Logo -> Logo in {n} files")
    # (Logo import should already exist or we need to add it)
    # Remove purple_logo import lines
    n = remove_import_line(all_py, r"from\s+\.purple_logo\s+import")
    print(f"  Removed purple_logo imports from {n} files")
    # In competition_origine_type_competition_generique.py, ensure Logo import
    cotcg = os.path.join(MODELS, "competition_origine_type_competition_generique.py")
    if os.path.exists(cotcg):
        with open(cotcg, encoding="utf-8") as f:
            content = f.read()
        if "from .logo import Logo" not in content:
            content = content.replace(
                "from ..utils.converter_utils",
                "from .logo import Logo\nfrom ..utils.converter_utils",
            )
            with open(cotcg, "w", encoding="utf-8") as f:
                f.write(content)
    git_rm(os.path.join(MODELS, "purple_logo.py"))
    print("  Deleted purple_logo.py")

    # ========================================================================
    # 2. Categorie -> Categorie
    # ========================================================================
    print("\n=== 2. Categorie -> Categorie ===")
    n = regex_replace_in_all(all_py, r"\bCompetitionIDCategorie\b", "Categorie")
    print(f"  Replaced in {n} files")
    # Fix imports: replace competition_id_categorie module ref with categorie
    n = replace_in_all(all_py, ".categorie import", ".categorie import")
    print(f"  Fixed module imports in {n} files")
    # Remove duplicate categorie imports in competition_id.py
    comp_id = os.path.join(MODELS, "competition_id.py")
    if os.path.exists(comp_id):
        with open(comp_id, encoding="utf-8") as f:
            content = f.read()
        # Remove the old import line for competition_id_categorie (now pointing to categorie)
        # Keep only one categorie import
        lines = content.split("\n")
        seen_categorie = False
        new_lines = []
        for ln in lines:
            if "from .categorie import Categorie" in ln:
                if not seen_categorie:
                    seen_categorie = True
                    new_lines.append(ln)
                # skip duplicate
            else:
                new_lines.append(ln)
        content = "\n".join(new_lines)
        with open(comp_id, "w", encoding="utf-8") as f:
            f.write(content)
    git_rm(os.path.join(MODELS, "competition_id_categorie.py"))
    print("  Deleted competition_id_categorie.py")

    # ========================================================================
    # 3. TypeCompetitionGenerique +
    #    TypeCompetitionGenerique -> TypeCompetitionGenerique
    # ========================================================================
    print("\n=== 3. Merge *TypeCompetitionGenerique -> TypeCompetitionGenerique ===")
    n = regex_replace_in_all(
        all_py, r"\bCompetitionIDTypeCompetitionGenerique\b", "TypeCompetitionGenerique"
    )
    print(f"  Replaced TypeCompetitionGenerique in {n} files")
    n = regex_replace_in_all(
        all_py,
        r"\bCompetitionOrigineTypeCompetitionGenerique\b",
        "TypeCompetitionGenerique",
    )
    print(f"  Replaced TypeCompetitionGenerique in {n} files")
    # Fix module imports
    n = replace_in_all(
        all_py,
        ".type_competition_generique import",
        ".type_competition_generique import",
    )
    print(f"  Fixed module imports (id) in {n} files")
    n = replace_in_all(
        all_py,
        ".type_competition_generique import",
        ".type_competition_generique import",
    )
    print(f"  Fixed module imports (origine) in {n} files")
    # Deduplicate imports in files that now have two type_competition_generique imports
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen = set()
        new_lines = []
        for ln in lines:
            if "from .type_competition_generique import TypeCompetitionGenerique" in ln:
                key = ln.strip()
                if key in seen:
                    continue
                seen.add(key)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    git_rm(os.path.join(MODELS, "competition_id_type_competition_generique.py"))
    git_rm(os.path.join(MODELS, "competition_origine_type_competition_generique.py"))
    print("  Deleted both redundant files")

    # ========================================================================
    # 4. EngagementEquipe -> EngagementEquipe
    # ========================================================================
    print("\n=== 4. EngagementEquipe -> EngagementEquipe ===")
    n = regex_replace_in_all(all_py, r"\bTeamEngagement\b", "EngagementEquipe")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".engagement_equipe import", ".engagement_equipe import")
    print(f"  Fixed module imports in {n} files")
    # Deduplicate engagement_equipe imports
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen = set()
        new_lines = []
        for ln in lines:
            stripped = ln.strip()
            if "engagement_equipe import EngagementEquipe" in stripped:
                if stripped in seen:
                    continue
                seen.add(stripped)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    git_rm(os.path.join(MODELS, "team_engagement.py"))
    print("  Deleted team_engagement.py")

    # ========================================================================
    # 5. EngagementEquipe -> EngagementEquipe
    # ========================================================================
    print("\n=== 5. EngagementEquipe -> EngagementEquipe ===")
    n = regex_replace_in_all(all_py, r"\bIDEngagementEquipe\b", "EngagementEquipe")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".engagement_equipe import", ".engagement_equipe import")
    print(f"  Fixed module imports in {n} files")
    # Deduplicate again
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen = set()
        new_lines = []
        for ln in lines:
            stripped = ln.strip()
            if stripped in seen:
                continue
            seen.add(stripped)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    git_rm(os.path.join(MODELS, "id_engagement_equipe.py"))
    print("  Deleted id_engagement_equipe.py")

    # ========================================================================
    # 6. IDOrganismeEquipe -> IDOrganismeEquipe
    # (IDOrganismeEquipe has only logo; IDOrganismeEquipe is superset)
    # ========================================================================
    print("\n=== 6. IDOrganismeEquipe -> IDOrganismeEquipe ===")
    n = regex_replace_in_all(all_py, r"\bOrganismeEquipe\b(?!\.)", "IDOrganismeEquipe")
    print(f"  Replaced IDOrganismeEquipe -> IDOrganismeEquipe in {n} files")
    # But be careful: IDOrganismeEquipe was already replaced once (so IDOrganismeEquipe)
    # Fix double-replacement
    n = replace_in_all(all_py, "IDOrganismeEquipe", "IDOrganismeEquipe")
    print(f"  Fixed double-ID in {n} files")
    # Fix module imports
    n = replace_in_all(
        all_py, ".id_organisme_equipe import", ".id_organisme_equipe import"
    )
    print(f"  Fixed module imports in {n} files")
    # Deduplicate
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen = set()
        new_lines = []
        for ln in lines:
            stripped = ln.strip()
            if "id_organisme_equipe import IDOrganismeEquipe" in stripped:
                if stripped in seen:
                    continue
                seen.add(stripped)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    git_rm(os.path.join(MODELS, "organisme_equipe.py"))
    print("  Deleted organisme_equipe.py")

    # ========================================================================
    # 7. Organisateur -> Organisateur (align id/commune types)
    # ========================================================================
    print("\n=== 7. Organisateur -> Organisateur ===")
    # Organisateur has id:int, commune:int
    # Organisateur has id:str, commune:str
    # Plan says align to str. Since Organisateur is the superset, just replace.
    n = regex_replace_in_all(all_py, r"\bOrganismeIDPere\b", "Organisateur")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".organisateur import", ".organisateur import")
    print(f"  Fixed module imports in {n} files")
    # Deduplicate
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen = set()
        new_lines = []
        for ln in lines:
            stripped = ln.strip()
            if "organisateur import Organisateur" in stripped:
                if stripped in seen:
                    continue
                seen.add(stripped)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    git_rm(os.path.join(MODELS, "organisme_id_pere.py"))
    print("  Deleted organisme_id_pere.py")

    # ========================================================================
    # 8. Delete OrganismeId, update PhaseEngagement.id_organisme to str
    # ========================================================================
    print("\n=== 8. Delete OrganismeId ===")
    # Update phase_engagement.py: id_organisme: OrganismeId -> str
    pe = os.path.join(MODELS, "phase_engagement.py")
    if os.path.exists(pe):
        with open(pe, encoding="utf-8") as f:
            content = f.read()
        # Remove OrganismeId import
        # Change type annotation
        content = content.replace(
            "id_organisme: OrganismeId | None", "id_organisme: str | None"
        )
        # Change from_dict: from_obj(OrganismeId.from_dict, ...) -> from_str(...)
        content = content.replace(
            'from_obj(OrganismeId.from_dict, obj, "idOrganisme")',
            'from_str(obj, "idOrganisme")',
        )
        # Remove from_obj import if only used for OrganismeId
        if "from_obj" not in content.replace("from_obj", "", 1):
            content = content.replace(", from_obj", "")
            content = content.replace("from_obj, ", "")
        # Change to_dict: self.id_organisme.to_dict() -> self.id_organisme
        content = content.replace("self.id_organisme.to_dict()", "self.id_organisme")
        with open(pe, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Updated phase_engagement.py")

    # Remove OrganismeId references from other files
    remove_import_line(all_py, r"from.*organisme_id\s+import\s+OrganismeId")
    git_rm(os.path.join(MODELS, "organisme_id.py"))
    print("  Deleted organisme_id.py")

    # ========================================================================
    # 9. CompetitionTypeFacet -> CompetitionTypeFacet
    # ========================================================================
    print("\n=== 9. CompetitionTypeFacet -> CompetitionTypeFacet ===")
    # This is a rename, not a merge
    n = regex_replace_in_all(
        all_py, r"\bCompetitionIDTypeCompetition\b", "CompetitionTypeFacet"
    )
    print(f"  Replaced in {n} files")
    n = replace_in_all(
        all_py, ".competition_type_facet import", ".competition_type_facet import"
    )
    print(f"  Fixed module imports in {n} files")
    # Rename the file
    old_path = os.path.join(MODELS, "competition_id_type_competition.py")
    new_path = os.path.join(MODELS, "competition_type_facet.py")
    if os.path.exists(old_path):
        # Update class name in file
        with open(old_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"\bCompetitionIDTypeCompetition\b", "CompetitionTypeFacet", content
        )
        with open(old_path, "w", encoding="utf-8") as f:
            f.write(content)
        subprocess.run(["git", "mv", old_path, new_path], cwd=WORKTREE, check=True)
        print("  Renamed file to competition_type_facet.py")

    # ========================================================================
    # 10. Update __init__.py exports
    # ========================================================================
    print("\n=== 10. Clean up __init__.py ===")
    init_py = os.path.join(MODELS, "__init__.py")
    if os.path.exists(init_py):
        with open(init_py, encoding="utf-8") as f:
            content = f.read()

        # Remove deleted module imports and exports
        deleted_classes = [
            "Logo",
            "Categorie",
            "TypeCompetitionGenerique",
            "TypeCompetitionGenerique",
            "CompetitionOrigineCategorie",
            "EngagementEquipe",
            "EngagementEquipe",
            "IDOrganismeEquipe",  # merged into IDOrganismeEquipe
            "Organisateur",
            "OrganismeId",
        ]
        deleted_modules = [
            "purple_logo",
            "competition_id_categorie",
            "competition_id_type_competition_generique",
            "competition_origine_type_competition_generique",
            "team_engagement",
            "id_engagement_equipe",
            "organisme_equipe",
            "organisme_id_pere",
            "organisme_id",
        ]

        lines = content.split("\n")
        new_lines = []
        for ln in lines:
            skip = False
            for mod in deleted_modules:
                if f".{mod} import" in ln or f".{mod}" in ln:
                    skip = True
                    break
            for cls in deleted_classes:
                if f'"{cls}"' in ln:
                    skip = True
                    break
            if not skip:
                new_lines.append(ln)

        # Add CompetitionTypeFacet to exports if not present
        content = "\n".join(new_lines)
        if '"CompetitionTypeFacet"' not in content:
            content = content.replace(
                '"CompetitionPhase"', '"CompetitionPhase",\n    "CompetitionTypeFacet"'
            )
        # Add CompetitionTypeFacet import if not present
        if "from .competition_type_facet import CompetitionTypeFacet" not in content:
            content = content.replace(
                "from .competition_phase import CompetitionPhase",
                "from .competition_phase import CompetitionPhase\n"
                "from .competition_type_facet import CompetitionTypeFacet",
            )

        with open(init_py, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Cleaned up __init__.py")

    print("\n=== Phase 1 complete ===")


if __name__ == "__main__":
    main()
