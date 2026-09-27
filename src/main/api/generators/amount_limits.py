from dataclasses import dataclass

@dataclass
class AmountRange:
    min_value: int
    max_value: int


class AmountLimits:
    DEPOSIT = AmountRange(1000, 9000)
    TRANSFER = AmountRange(500, 10000)
    CREDIT = AmountRange(5000, 15000)
    TERM_MONTHS = AmountRange(1, 60)
