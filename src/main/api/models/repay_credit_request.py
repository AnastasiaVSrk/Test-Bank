from pydantic import Field
from src.main.api.models.base_model import BaseModel


class RepayCreditRequest(BaseModel):
    credit_id: int = Field(alias='creditId')
    account_id: int = Field(alias='accountId')
    amount: float