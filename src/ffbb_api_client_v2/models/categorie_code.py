"""CategorieCode — parsed str subclass for FFBB category codes.

Category codes are structured concatenations of components:
  age group + echelon + division + gender  (e.g. U13D1M)
"""

from __future__ import annotations

import re

from .age_group import AgeGroup
from .echelon import Echelon
from .gender import Gender

# ---------------------------------------------------------------------------
# Compiled regex patterns — tested in priority order
# ---------------------------------------------------------------------------

_YOUTH_ECHELON = re.compile(r"^(U\d{1,2})([DRF])(\d)([MF])$")
_YOUTH_GENDER = re.compile(r"^(U\d{1,2})([MF])$")
_YOUTH_GENERIC = re.compile(r"^(U\d{1,2})$")
_SENIOR_STRUCTURED = re.compile(r"^SE([DRE])(\d)([MF])$")
_NATIONAL = re.compile(r"^N([MF])(\d)$")
_PRE = re.compile(r"^P([NR])([MF])$")
_ADEP = re.compile(r"^ADEP([MF])$")
_AREG = re.compile(r"^AREG([MF])$")
_LF = re.compile(r"^LF(\d)$")
_SENIOR_GENERIC = re.compile(r"^(?:SE|SEN|S|SENIOR)$")
_VETERAN = re.compile(r"^VE$")
_BASKET_FAUTEUIL = re.compile(r"^LBWL$")
_DEP_NIV = re.compile(r"^DEP NIV(\d)([MF])$")

# Special codes — non-structured names used for professional/specific leagues
_SPECIAL_CODES: dict[str, _ParseResult] = {
    "Betclic E": (AgeGroup.SENIOR, Echelon.PRO, None, Gender.MASCULIN, True),
    "PROA": (AgeGroup.SENIOR, Echelon.PRO, None, Gender.MASCULIN, True),
    "PROB": (AgeGroup.SENIOR, Echelon.PRO, None, Gender.MASCULIN, True),
}

_AGE_GROUP_MAP: dict[str, AgeGroup] = {m.value: m for m in AgeGroup}
_ECHELON_LETTER: dict[str, Echelon] = {
    "D": Echelon.DEPARTEMENT,
    "R": Echelon.REGION,
    "F": Echelon.FEDERAL,
}
_SENIOR_ECHELON_LETTER: dict[str, Echelon] = {
    "D": Echelon.DEPARTEMENT,
    "R": Echelon.EXCELLENCE,
    "E": Echelon.EXCELLENCE,
}
_GENDER_LETTER: dict[str, Gender] = {"M": Gender.MASCULIN, "F": Gender.FEMININ}
_PRE_MAP: dict[str, Echelon] = {"N": Echelon.PRE_NATIONAL, "R": Echelon.PRE_REGIONAL}

_ParseResult = tuple[
    AgeGroup | None,
    Echelon | None,
    int | None,
    Gender | None,
    bool,
]


def _resolve_age_group(code: str) -> AgeGroup | None:
    """Resolve a U-prefix age group code (e.g. 'U13') to an AgeGroup."""
    return _AGE_GROUP_MAP.get(code)


def _parse(value: str) -> _ParseResult:
    """Parse a category code string into its components.

    Returns (age_group, echelon, division, gender, parsed).
    """
    # Special codes (professional leagues, non-structured names)
    special = _SPECIAL_CODES.get(value)
    if special is not None:
        return special

    # Youth + echelon + division + gender: U13D1M, U15R2F, U18F1M
    m = _YOUTH_ECHELON.match(value)
    if m:
        return (
            _resolve_age_group(m.group(1)),
            _ECHELON_LETTER[m.group(2)],
            int(m.group(3)),
            _GENDER_LETTER[m.group(4)],
            True,
        )

    # Youth + gender: U7M, U9F
    m = _YOUTH_GENDER.match(value)
    if m:
        return (
            _resolve_age_group(m.group(1)),
            None,
            None,
            _GENDER_LETTER[m.group(2)],
            True,
        )

    # Youth generic: U11, U13
    m = _YOUTH_GENERIC.match(value)
    if m:
        return (_resolve_age_group(m.group(1)), None, None, None, True)

    # Senior structured: SED1M, SER2F, SEE1M
    m = _SENIOR_STRUCTURED.match(value)
    if m:
        return (
            AgeGroup.SENIOR,
            _SENIOR_ECHELON_LETTER[m.group(1)],
            int(m.group(2)),
            _GENDER_LETTER[m.group(3)],
            True,
        )

    # National: NM1, NF2
    m = _NATIONAL.match(value)
    if m:
        return (
            AgeGroup.SENIOR,
            Echelon.NATIONAL,
            int(m.group(2)),
            _GENDER_LETTER[m.group(1)],
            True,
        )

    # Pre-national / pre-regional: PNM, PNF, PRM, PRF
    m = _PRE.match(value)
    if m:
        return (
            AgeGroup.SENIOR,
            _PRE_MAP[m.group(1)],
            None,
            _GENDER_LETTER[m.group(2)],
            True,
        )

    # Association departementale: ADEPM, ADEPF
    m = _ADEP.match(value)
    if m:
        return (
            None,
            Echelon.ASSOCIATION_DEPARTEMENTALE,
            None,
            _GENDER_LETTER[m.group(1)],
            True,
        )

    # Association regionale: AREGM, AREGF
    m = _AREG.match(value)
    if m:
        return (
            None,
            Echelon.ASSOCIATION_REGIONALE,
            None,
            _GENDER_LETTER[m.group(1)],
            True,
        )

    # Ligue feminine: LF2
    m = _LF.match(value)
    if m:
        return (
            None,
            Echelon.LIGUE_FEMININE,
            int(m.group(1)),
            Gender.FEMININ,
            True,
        )

    # Senior generic: SE, SEN, S, SENIOR
    if _SENIOR_GENERIC.match(value):
        return (AgeGroup.SENIOR, None, None, None, True)

    # Veteran: VE
    if _VETERAN.match(value):
        return (AgeGroup.VETERAN, None, None, None, True)

    # Basket fauteuil: LBWL
    if _BASKET_FAUTEUIL.match(value):
        return (None, Echelon.BASKET_FAUTEUIL, None, None, True)

    # Departement with space: DEP NIV1F, DEP NIV2M
    m = _DEP_NIV.match(value)
    if m:
        return (
            None,
            Echelon.DEPARTEMENT,
            int(m.group(1)),
            _GENDER_LETTER[m.group(2)],
            True,
        )

    # Fallback — unrecognized code
    return (None, None, None, None, False)


class CategorieCode(str):
    """Code categorie FFBB parse en composants.

    Herite de str pour compatibilite (==, in, hash, json).
    Accepte tout string. Parse les composants si le format est reconnu.

    Examples:
        >>> CategorieCode("U13D1M").age_group
        <AgeGroup.U13: 'U13'>
        >>> CategorieCode("U13D1M").echelon
        <Echelon.DEPARTEMENT: 'D'>
        >>> CategorieCode("U13D1M").division
        1
        >>> CategorieCode("U13D1M").gender
        <Gender.MASCULIN: 'M'>
        >>> CategorieCode("U13D1M") == "U13D1M"
        True
    """

    __slots__ = ("_age_group", "_echelon", "_division", "_gender", "_parsed")

    _age_group: AgeGroup | None
    _echelon: Echelon | None
    _division: int | None
    _gender: Gender | None
    _parsed: bool

    def __new__(cls, value: str) -> CategorieCode:
        instance = str.__new__(cls, value)
        ag, ech, div, gen, parsed = _parse(value)
        instance._age_group = ag
        instance._echelon = ech
        instance._division = div
        instance._gender = gen
        instance._parsed = parsed
        return instance

    @property
    def age_group(self) -> AgeGroup | None:
        return self._age_group

    @property
    def echelon(self) -> Echelon | None:
        return self._echelon

    @property
    def division(self) -> int | None:
        return self._division

    @property
    def gender(self) -> Gender | None:
        return self._gender

    @property
    def is_parsed(self) -> bool:
        return self._parsed

    def __repr__(self) -> str:
        return f"CategorieCode({str.__repr__(self)})"
