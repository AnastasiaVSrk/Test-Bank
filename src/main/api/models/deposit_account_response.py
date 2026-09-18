from src.main.api.models.base_model import BaseModel


class DepositUserResponse(BaseModel):
    id: int
    balance: float
