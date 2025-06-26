from dataclasses import dataclass

from alarm_category import AlarmCategory
from symbol import Symbol


@dataclass
class Alarm:
    symbol: Symbol
    category: AlarmCategory
