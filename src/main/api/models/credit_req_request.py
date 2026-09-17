from src.main.api.models.base_model import BaseModel


class CreditReqRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int
