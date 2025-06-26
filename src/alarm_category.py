import re
from dataclasses import dataclass, field
from itertools import count
from typing import Tuple


@dataclass
class AlarmCategory:
    regex: str
    bg_color: Tuple[int, int, int] = (255,0,0) # Red
    font_color: Tuple[int, int, int] = (0,0,0) # Black
    id: int = field(default_factory=count().__next__)

    pattern: re.Pattern = field(init=False, repr=False)

    def __post_init__(self):
        self.pattern = re.compile(self.regex)

    def is_match(self, symbol_name: str) -> bool:
        return self.pattern.search(symbol_name) is not None
