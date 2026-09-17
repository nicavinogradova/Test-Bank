from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_response import CreateUserResponse


class TransferParticipants(BaseModel):
    sender_user: CreateUserResponse
    sender_account: CreateAccountResponse
    recipient_user: CreateUserResponse
    recipient_account: CreateAccountResponse
