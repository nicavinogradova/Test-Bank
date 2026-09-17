import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.transfer_participants import TransferParticipants


def _create_user(api_manager: ApiManager, role: str) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest, role=role)
    api_manager.admin_steps.create_user(user_request)
    return user_request


def _create_user_response(api_manager: ApiManager, role: str) -> CreateUserResponse:
    user_request = RandomModelGenerator.generate(CreateUserRequest, role=role)
    response = api_manager.admin_steps.create_user(user_request)
    return CreateUserResponse(
        id=response.id,
        username=response.username,
        password=user_request.password,
        role=response.role,
    )


def _create_account(api_manager: ApiManager, user: CreateUserRequest | CreateUserResponse) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(user)


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    return _create_user(api_manager, "ROLE_USER")


@pytest.fixture
def create_user_credit_request(api_manager: ApiManager) -> CreateUserRequest:
    return _create_user(api_manager, "ROLE_CREDIT_SECRET")


@pytest.fixture
def create_account_response(api_manager: ApiManager, create_user_request: CreateUserRequest) -> CreateAccountResponse:
    return _create_account(api_manager, create_user_request)


@pytest.fixture
def create_credit_account_response(api_manager: ApiManager,
                                   create_user_credit_request: CreateUserRequest) -> CreateAccountResponse:
    return _create_account(api_manager, create_user_credit_request)


@pytest.fixture
def transfer_participants(api_manager: ApiManager) -> TransferParticipants:
    sender_user = _create_user_response(api_manager, "ROLE_USER")
    sender_account = _create_account(api_manager, sender_user)

    recipient_user = _create_user_response(api_manager, "ROLE_USER")
    recipient_account = _create_account(api_manager, recipient_user)

    return TransferParticipants(
        sender_user=sender_user,
        sender_account=sender_account,
        recipient_user=recipient_user,
        recipient_account=recipient_account,
    )
