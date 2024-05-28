from enum import Enum


class CompetitionType(Enum):
    CHAMPIONSHIP = "championship"
    CUP = "cup"


def extract_competition_type(input_str: str) -> CompetitionType:
    """
    Extracts the competition type from the given input string.

    Args:
        input_str (str): The input string to extract the competition type from.

    Returns:
        CompetitionType: The extracted competition type.

    """
    input_str = input_str.lower()
    for competition_type in CompetitionType:
        lower_value = competition_type.value.lower()
        if lower_value == input_str or lower_value in input_str:
            return competition_type

    if "coup" in input_str:
        return CompetitionType.CUP

    return CompetitionType.CHAMPIONSHIP
