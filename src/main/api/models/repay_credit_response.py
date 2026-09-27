from pydantic import Field
from src.main.api.models.base_model import BaseModel


class RepayCreditResponse(BaseModel):
    credit_id: int = Field(alias='creditId')
    amount_deposited: float = Field(alias='amountDeposited')