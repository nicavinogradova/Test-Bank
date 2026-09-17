from typing import Annotated, Literal
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

UserRole = Literal["ROLE_USER", "ROLE_CREDIT_SECRET"]


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')]
    role: UserRole
