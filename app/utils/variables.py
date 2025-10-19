from enum import Enum

# Languages
class Languages(Enum):
    NORW_CODE = "no"
    PL_CODE = "pl"
    ENG_CODE = "eng"

# Diretions
class Directions(Enum):
    DIRECTION_NORW_ENG = "no-eng"
    DIRECTION_NORW_PL = "no-pl"
    DIRECTION_ENG_PL = "eng-pl"
    DIRECTION_ENG_NORW = "eng-no"
    DIRECTION_PL_NORW = "pl-no"
    DIRECTION_PL_ENG = "pl-eng"