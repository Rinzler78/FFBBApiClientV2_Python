from dataclasses import dataclass
from typing import Optional


# Query Parameters Model
@dataclass
class SaisonsQuery:
    fields_: list[str] = None  # Original: fields[]
    filter: Optional[str] = '{"actif":{"_eq":true}}'  # Original: filter


# Response is a simple type
# ResponseType = List[SaisonsitemModel]
