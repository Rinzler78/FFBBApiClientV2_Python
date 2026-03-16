#!/usr/bin/env python3
"""
Script to detect if from_dict methods in model files use manual deserialization
instead of from_* helper functions from converter_utils.

Usage: python scripts/check_from_dict_compliance.py

This script scans all Python files in src/ffbb_api_client_v2/models/ for from_dict class methods,
analyzes their implementation, and reports any that use manual deserialization patterns
like str(data.get(...)), int(data.get(...)), etc., instead of the standardized from_* helpers.
"""

import ast
import re
import sys
from pathlib import Path


class FromDictComplianceChecker:
    """Checker for from_dict method compliance with converter_utils helpers."""

    # Patterns that indicate manual deserialization
    MANUAL_DESERIALIZATION_PATTERNS = [
        r"str\s*\(\s*data\.get\s*\(",
        r"int\s*\(\s*data\.get\s*\(",
        r"float\s*\(\s*data\.get\s*\(",
        r"bool\s*\(\s*data\.get\s*\(",
    ]

    # Helper function names from converter_utils
    HELPER_FUNCTIONS = {
        "from_str",
        "from_int",
        "from_float",
        "from_bool",
        "from_datetime",
        "from_time",
        "from_enum",
        "from_categorie_code",
        "from_obj",
        "from_list",
        "from_uuid",
    }

    def __init__(self, models_dir: str):
        self.models_dir = Path(models_dir)
        self.results: dict[str, list[str]] = {
            "compliant": [],
            "non_compliant": [],
            "errors": [],
        }

    def check_compliance(self) -> dict[str, list[str]]:
        """Check all model files for from_dict compliance."""
        if not self.models_dir.exists():
            self.results["errors"].append(
                f"Models directory not found: {self.models_dir}"
            )
            return self.results

        for py_file in self.models_dir.glob("**/*.py"):
            try:
                self._check_file(py_file)
            except Exception as e:
                self.results["errors"].append(f"Error processing {py_file}: {e}")

        return self.results

    def _check_file(self, file_path: Path) -> None:
        """Check a single Python file for from_dict methods."""
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Quick check if file has from_dict
        if "def from_dict" not in content:
            return

        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            self.results["errors"].append(f"Syntax error in {file_path}: {e}")
            return

        # Find all from_dict methods
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "from_dict":
                method_info = self._analyze_from_dict_method(node, content)
                if method_info:
                    file_rel = file_path.relative_to(self.models_dir.parent.parent)
                    method_name = f"{file_rel}:{node.lineno}"

                    if method_info["compliant"]:
                        self.results["compliant"].append(method_name)
                    else:
                        violations = method_info["violations"]
                        self.results["non_compliant"].append(
                            f"{method_name} - Violations: {', '.join(violations)}"
                        )

    def _analyze_from_dict_method(
        self, method_node: ast.FunctionDef, content: str
    ) -> dict:
        """Analyze a from_dict method for compliance."""
        violations = []
        uses_helpers = False

        # Get the method body as text for pattern matching
        method_lines = content.splitlines()
        start_line = method_node.lineno - 1  # 0-indexed
        end_line = method_node.end_lineno

        method_text = "\n".join(method_lines[start_line:end_line])

        # Check for manual deserialization patterns
        for pattern in self.MANUAL_DESERIALIZATION_PATTERNS:
            if re.search(pattern, method_text):
                violations.append(f"Manual {pattern.split()[0]} conversion found")

        # Check if helpers are used
        for helper in self.HELPER_FUNCTIONS:
            if helper in method_text:
                uses_helpers = True
                break

        # If no helpers used and has manual patterns, mark as non-compliant
        compliant = uses_helpers or not violations

        return {"compliant": compliant, "violations": violations}

    def print_report(self) -> None:
        """Print the compliance report."""
        print("From Dict Compliance Report")
        print("=" * 50)

        print(f"\nCompliant methods ({len(self.results['compliant'])}):")
        for method in self.results["compliant"]:
            print(f"  ✓ {method}")

        print(f"\nNon-compliant methods ({len(self.results['non_compliant'])}):")
        for method in self.results["non_compliant"]:
            print(f"  ✗ {method}")

        if self.results["errors"]:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"  ! {error}")

        total_methods = len(self.results["compliant"]) + len(
            self.results["non_compliant"]
        )
        if total_methods > 0:
            pct = len(self.results["compliant"]) / total_methods * 100
            print(f"\nCompliance rate: {pct:.1f}%")


def main():
    """Main entry point."""
    models_dir = "src/ffbb_api_client_v2/models"

    checker = FromDictComplianceChecker(models_dir)
    results = checker.check_compliance()
    checker.print_report()

    # Exit with non-zero if there are non-compliant methods
    return 1 if results["non_compliant"] else 0


if __name__ == "__main__":
    sys.exit(main())
