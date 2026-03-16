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
        subprocess.run(
            ["git", "rm", "-f", filepath], cwd=WORKTREE, check=True, timeout=30
        )
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


def _step1_fix_purple_logo(all_py: list) -> None:
    """Step 1: Replace PurpleLogo -> Logo and remove purple_logo module."""
    print("=== 1. Logo -> Logo ===")
    n = regex_replace_in_all(all_py, r"\bPurpleLogo\b", "Logo")
    print(f"  Replaced Logo -> Logo in {n} files")
    n = remove_import_line(all_py, r"from\s+\.purple_logo\s+import")
    print(f"  Removed purple_logo imports from {n} files")
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


def _step2_fix_categorie(all_py: list) -> None:
    """Step 2: Replace CompetitionIDCategorie -> Categorie."""
    print("\n=== 2. Categorie -> Categorie ===")
    n = regex_replace_in_all(all_py, r"\bCompetitionIDCategorie\b", "Categorie")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".categorie import", ".categorie import")
    print(f"  Fixed module imports in {n} files")
    comp_id = os.path.join(MODELS, "competition_id.py")
    if os.path.exists(comp_id):
        with open(comp_id, encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        seen_categorie = False
        new_lines = []
        for ln in lines:
            if "from .categorie import Categorie" in ln:
                if not seen_categorie:
                    seen_categorie = True
                    new_lines.append(ln)
            else:
                new_lines.append(ln)
        content = "\n".join(new_lines)
        with open(comp_id, "w", encoding="utf-8") as f:
            f.write(content)
    git_rm(os.path.join(MODELS, "competition_id_categorie.py"))
    print("  Deleted competition_id_categorie.py")


def _dedup_import_in_files(all_py: list, import_fragment: str) -> None:
    """Remove duplicate import lines containing import_fragment."""
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen: set[str] = set()
        new_lines = []
        for ln in lines:
            if import_fragment in ln:
                key = ln.strip()
                if key in seen:
                    continue
                seen.add(key)
            new_lines.append(ln)
        if len(new_lines) != len(lines):
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)


def _dedup_all_imports_in_files(all_py: list) -> None:
    """Remove all duplicate import lines in files."""
    for fpath in all_py:
        if not os.path.exists(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        seen: set[str] = set()
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


def _step3_fix_type_competition_generique(all_py: list) -> None:
    """Step 3: Merge *TypeCompetitionGenerique -> TypeCompetitionGenerique."""
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
    n = replace_in_all(
        all_py,
        ".type_competition_generique import",
        ".type_competition_generique import",
    )
    print(f"  Fixed module imports in {n} files")
    _dedup_import_in_files(
        all_py, "from .type_competition_generique import TypeCompetitionGenerique"
    )
    git_rm(os.path.join(MODELS, "competition_id_type_competition_generique.py"))
    git_rm(os.path.join(MODELS, "competition_origine_type_competition_generique.py"))
    print("  Deleted both redundant files")


def _step4_fix_team_engagement(all_py: list) -> None:
    """Step 4: Replace TeamEngagement -> EngagementEquipe."""
    print("\n=== 4. EngagementEquipe -> EngagementEquipe ===")
    n = regex_replace_in_all(all_py, r"\bTeamEngagement\b", "EngagementEquipe")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".engagement_equipe import", ".engagement_equipe import")
    print(f"  Fixed module imports in {n} files")
    _dedup_import_in_files(all_py, "engagement_equipe import EngagementEquipe")
    git_rm(os.path.join(MODELS, "team_engagement.py"))
    print("  Deleted team_engagement.py")


def _step5_fix_id_engagement_equipe(all_py: list) -> None:
    """Step 5: Replace IDEngagementEquipe -> EngagementEquipe."""
    print("\n=== 5. EngagementEquipe -> EngagementEquipe ===")
    n = regex_replace_in_all(all_py, r"\bIDEngagementEquipe\b", "EngagementEquipe")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".engagement_equipe import", ".engagement_equipe import")
    print(f"  Fixed module imports in {n} files")
    _dedup_all_imports_in_files(all_py)
    git_rm(os.path.join(MODELS, "id_engagement_equipe.py"))
    print("  Deleted id_engagement_equipe.py")


def _step6_fix_organisme_equipe(all_py: list) -> None:
    """Step 6: Merge OrganismeEquipe -> OrganismeEquipe (id superset)."""
    print("\n=== 6. OrganismeEquipe -> OrganismeEquipe ===")
    n = regex_replace_in_all(all_py, r"\bOrganismeEquipe\b(?!\.)", "OrganismeEquipe")
    print(f"  Replaced OrganismeEquipe -> OrganismeEquipe in {n} files")
    n = replace_in_all(all_py, "OrganismeEquipe", "OrganismeEquipe")
    print(f"  Fixed double-ID in {n} files")
    n = replace_in_all(
        all_py, ".id_organisme_equipe import", ".id_organisme_equipe import"
    )
    print(f"  Fixed module imports in {n} files")
    _dedup_import_in_files(all_py, "id_organisme_equipe import OrganismeEquipe")
    git_rm(os.path.join(MODELS, "organisme_equipe.py"))
    print("  Deleted organisme_equipe.py")


def _step7_fix_organisateur(all_py: list) -> None:
    """Step 7: Replace OrganismeIDPere -> Organisateur."""
    print("\n=== 7. Organisateur -> Organisateur ===")
    n = regex_replace_in_all(all_py, r"\bOrganismeIDPere\b", "Organisateur")
    print(f"  Replaced in {n} files")
    n = replace_in_all(all_py, ".organisateur import", ".organisateur import")
    print(f"  Fixed module imports in {n} files")
    _dedup_import_in_files(all_py, "organisateur import Organisateur")
    git_rm(os.path.join(MODELS, "organisme_id_pere.py"))
    print("  Deleted organisme_id_pere.py")


def _step8_fix_organisme_id(all_py: list) -> None:
    """Step 8: Delete OrganismeId, update PhaseEngagement.id_organisme to str."""
    print("\n=== 8. Delete OrganismeId ===")
    pe = os.path.join(MODELS, "phase_engagement.py")
    if os.path.exists(pe):
        with open(pe, encoding="utf-8") as f:
            content = f.read()
        content = content.replace(
            "id_organisme: OrganismeId | None", "id_organisme: str | None"
        )
        content = content.replace(
            'from_obj(OrganismeId.from_dict, obj, "idOrganisme")',
            'from_str(obj, "idOrganisme")',
        )
        if "from_obj" not in content.replace("from_obj", "", 1):
            content = content.replace(", from_obj", "")
            content = content.replace("from_obj, ", "")
        content = content.replace("self.id_organisme.to_dict()", "self.id_organisme")
        with open(pe, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Updated phase_engagement.py")
    remove_import_line(all_py, r"from.*organisme_id\s+import\s+OrganismeId")
    git_rm(os.path.join(MODELS, "organisme_id.py"))
    print("  Deleted organisme_id.py")


def _step9_fix_competition_type_facet(all_py: list) -> None:
    """Step 9: Rename CompetitionIDTypeCompetition -> CompetitionTypeFacet."""
    print("\n=== 9. CompetitionTypeFacet -> CompetitionTypeFacet ===")
    n = regex_replace_in_all(
        all_py, r"\bCompetitionIDTypeCompetition\b", "CompetitionTypeFacet"
    )
    print(f"  Replaced in {n} files")
    n = replace_in_all(
        all_py, ".competition_type_facet import", ".competition_type_facet import"
    )
    print(f"  Fixed module imports in {n} files")
    old_path = os.path.join(MODELS, "competition_id_type_competition.py")
    new_path = os.path.join(MODELS, "competition_type_facet.py")
    if os.path.exists(old_path):
        with open(old_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"\bCompetitionIDTypeCompetition\b", "CompetitionTypeFacet", content
        )
        with open(old_path, "w", encoding="utf-8") as f:
            f.write(content)
        subprocess.run(
            ["git", "mv", old_path, new_path], cwd=WORKTREE, check=True, timeout=30
        )
        print("  Renamed file to competition_type_facet.py")


def _step10_update_init_exports(all_py: list) -> None:  # noqa: ARG001
    """Step 10: Update models __init__.py — remove deleted, add CompetitionTypeFacet."""
    print("\n=== 10. Clean up __init__.py ===")
    deleted_classes = [
        "Logo",
        "Categorie",
        "TypeCompetitionGenerique",
        "TypeCompetitionGenerique",
        "CompetitionOrigineCategorie",
        "EngagementEquipe",
        "EngagementEquipe",
        "OrganismeEquipe",
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
    init_py = os.path.join(MODELS, "__init__.py")
    if not os.path.exists(init_py):
        return
    with open(init_py, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    new_lines = []
    for ln in lines:
        skip = any(
            f".{mod} import" in ln or f".{mod}" in ln for mod in deleted_modules
        ) or any(f'"{cls}"' in ln for cls in deleted_classes)
        if not skip:
            new_lines.append(ln)
    content = "\n".join(new_lines)
    if '"CompetitionTypeFacet"' not in content:
        content = content.replace(
            '"CompetitionPhase"', '"CompetitionPhase",\n    "CompetitionTypeFacet"'
        )
    if "from .competition_type_facet import CompetitionTypeFacet" not in content:
        content = content.replace(
            "from .competition_phase import CompetitionPhase",
            "from .competition_phase import CompetitionPhase\n"
            "from .competition_type_facet import CompetitionTypeFacet",
        )
    with open(init_py, "w", encoding="utf-8") as f:
        f.write(content)
    print("  Cleaned up __init__.py")


def main():
    os.chdir(WORKTREE)
    all_py = find_all_python_files("src", "tests", "scripts", "examples")

    _step1_fix_purple_logo(all_py)
    _step2_fix_categorie(all_py)
    _step3_fix_type_competition_generique(all_py)
    _step4_fix_team_engagement(all_py)
    _step5_fix_id_engagement_equipe(all_py)
    _step6_fix_organisme_equipe(all_py)
    _step7_fix_organisateur(all_py)
    _step8_fix_organisme_id(all_py)
    _step9_fix_competition_type_facet(all_py)
    _step10_update_init_exports(all_py)

    print("\n=== Phase 1 complete ===")


if __name__ == "__main__":
    main()
