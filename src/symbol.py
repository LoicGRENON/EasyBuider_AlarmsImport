from dataclasses import dataclass


@dataclass
class Symbol:
    name: str
    type: str
    comment: str
