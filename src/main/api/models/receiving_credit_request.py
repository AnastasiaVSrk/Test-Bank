from pydantic import Field
from src.main.api.models.base_model import BaseModel


class ReceivingCreditRequest(BaseModel):
    account_id: int = Field(alias='accountId')
    amount: float
    term_months: int = Field(alias='termMonths')