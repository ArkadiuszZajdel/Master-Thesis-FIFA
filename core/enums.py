from enum import Enum
from core.rankings import FIFA93, FIFA06, FIFAcurrent

class Ranking(Enum):
    FIFA93_98 = FIFA93
    FIFA06_18 = FIFA06
    FIFAcurrent = FIFAcurrent