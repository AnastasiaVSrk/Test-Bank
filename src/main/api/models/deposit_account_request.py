from pydantic import Field

from src.main.api.models.base_model import BaseModel


class DepositUserRequest(BaseModel):
    account_id: int = Field(alias='accountId')
    amount: float