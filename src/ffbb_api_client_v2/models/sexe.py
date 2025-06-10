import logging
from enum import Enum

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class Sexe(Enum):
    FÉMININ = "Féminin"
    MASCULIN = "Masculin"
    MIXTE = "Mixte"


def extract_sex(input_str: str) -> Sexe:
    """Extracts the sex from the input string.

    Args:
        input_str (str): The input string containing the sex.

    Returns:
        Sex: The extracted sex.

    """
    input_str = input_str.lower()
    for sex in Sexe:
        lower_value = sex.value.lower()
        if lower_value == input_str or lower_value in input_str:
            return sex
    logger.debug("Unknown sex: %s", input_str)
    return None
