from enum import Enum


class Sex(Enum):
    MASCULIN = "Masculin"
    FEMININ = "Féminin"
    MIXTE = "Mixte"


def extract_sex(input_str: str) -> Sex:
    """Extracts the sex from the input string.

    Args:
        input_str (str): The input string containing the sex.

    Returns:
        Sex: The extracted sex.

    """
    input_str = input_str.lower()
    for sex in Sex:
        lower_value = sex.value.lower()
        if lower_value == input_str or lower_value in input_str:
            return sex
    print(f"Unknown sex: {input_str}")
    return None
