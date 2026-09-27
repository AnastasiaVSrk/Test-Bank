from random import uniform, randint
from src.main.api.generators.amount_limits import AmountRange


class RandomAmountGenerator:

    @staticmethod
    def generate_valid_amount(amount_range: AmountRange) -> float :
        return round(uniform(amount_range.min_value, amount_range.max_value), 2)

    @staticmethod
    def generate_below_min(amount_range: AmountRange) -> float :
        return round(uniform(1, amount_range.min_value - 1), 2)


    @staticmethod
    def generate_above_max(amount_range: AmountRange) -> float :
        return round(uniform(amount_range.max_value + 1, amount_range.max_value + 9999), 2)

    @staticmethod
    def generate_valid_term_months(amount_range: AmountRange) -> int:
        return randint(amount_range.min_value, amount_range.max_value)



