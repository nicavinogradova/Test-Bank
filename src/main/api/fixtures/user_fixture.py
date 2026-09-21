import random

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_req_request import CreditReqRequest
from src.main.api.models.credit_req_response import CreditReqResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_participants import TransferParticipants
from src.main.api.models.transfer_request import TransferRequest


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
def deposit_request(create_account_response: CreateAccountResponse) -> DepositRequest:
    random_amount = round(random.uniform(1000.00, 9000.00), 2)
    return DepositRequest(
        accountId=create_account_response.id,
        amount=random_amount
    )


@pytest.fixture
def invalid_deposit_request(create_account_response: CreateAccountResponse) -> DepositRequest:
    side = random.randint(0, 1)
    if side == 0:
        invalid_amount = round(random.uniform(0.01, 999.99), 2)
    else:
        invalid_amount = round(random.uniform(9000.01, 999_999_999.99), 2)

    return DepositRequest(
        accountId=create_account_response.id,
        amount=invalid_amount
    )


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


@pytest.fixture
def transfer_request(transfer_participants: TransferParticipants) -> TransferRequest:
    transfer_amount = round(random.uniform(500.00, 9000.00), 2)
    return TransferRequest(
        fromAccountId=transfer_participants.sender_account.id,
        toAccountId=transfer_participants.recipient_account.id,
        amount=transfer_amount
    )


@pytest.fixture
def invalid_transfer_request(transfer_participants: TransferParticipants) -> TransferRequest:
    transfer_amount = round(random.uniform(0.01, 499.99), 2)
    return TransferRequest(
        fromAccountId=transfer_participants.sender_account.id,
        toAccountId=transfer_participants.recipient_account.id,
        amount=transfer_amount
    )


@pytest.fixture
def deposit_request_for_transfer(transfer_participants: TransferParticipants) -> DepositRequest:
    deposit_amount = round(9000.00, 2)
    return DepositRequest(
        accountId=transfer_participants.sender_account.id,
        amount=deposit_amount
    )


@pytest.fixture
def credit_account_request(create_credit_account_response: CreateAccountResponse) -> CreditReqRequest:
    random_amount = round(random.uniform(5000.00, 15000.00), 2)
    return CreditReqRequest(
        accountId=create_credit_account_response.id,
        amount=random_amount,
        termMonths=12
    )


@pytest.fixture
def invalid_credit_account_request(create_credit_account_response: CreateAccountResponse) -> CreditReqRequest:
    side = random.randint(0, 1)
    if side == 0:
        invalid_amount = round(random.uniform(0.01, 4999.99), 2)
    else:
        invalid_amount = round(random.uniform(15000.01, 999_999_999.99), 2)

    return CreditReqRequest(
        accountId=create_credit_account_response.id,
        amount=invalid_amount,
        termMonths=12
    )


@pytest.fixture
def credit_request_response(api_manager: ApiManager, create_user_credit_request: CreateUserRequest,
                            credit_account_request: CreditReqRequest) -> CreditReqResponse:
    return api_manager.user_steps.credit_req_positive(create_user_credit_request, credit_account_request)


@pytest.fixture
def credit_repay_request(create_credit_account_response: CreateAccountResponse,
                         credit_request_response: CreditReqResponse) -> CreditRepayRequest:
    return CreditRepayRequest(
        creditId=credit_request_response.creditId,
        accountId=credit_request_response.id,
        amount=credit_request_response.amount
    )


@pytest.fixture
def invalid_credit_repay_request(create_credit_account_response: CreateAccountResponse,
                                 credit_request_response: CreditReqResponse) -> CreditRepayRequest:
    repay_amount = round(credit_request_response.amount - 0.01, 2)
    return CreditRepayRequest(
        creditId=credit_request_response.creditId,
        accountId=credit_request_response.id,
        amount=repay_amount
    )
