import re
from dataclasses import dataclass, field
from itertools import count
from typing import Tuple


def rgb_to_hex(red, green, blue):
    return f'#{red:02x}{green:02x}{blue:02x}'


@dataclass
class AlarmCategory:
    regex: str = field(default="")
    _regex: str = field(init=False, repr=False)
    bg_color: Tuple[int, int, int] = (255,0,0) # Red
    fg_color: Tuple[int, int, int] = (0, 0, 0) # Black
    id: int = field(default_factory=count().__next__)

    pattern: re.Pattern = field(init=False, repr=False)

    def is_match(self, symbol_name: str) -> bool:
        return self.pattern.search(symbol_name) is not None

    @property
    def bg_color_hex(self) -> str:
        return rgb_to_hex(self.bg_color[0], self.bg_color[1], self.bg_color[2])

    @property
    def fg_color_hex(self) -> str:
        return rgb_to_hex(self.fg_color[0], self.fg_color[1], self.fg_color[2])

    @property
    def regex(self) -> str:
        return self._regex

    @regex.setter
    def regex(self, value: str):
        self._regex = value
        # Avoid using '' as default regexp as it matches everything ... Use '^$' to match nothing
        self.pattern = re.compile(self._regex if self._regex != '' else r'^$')
