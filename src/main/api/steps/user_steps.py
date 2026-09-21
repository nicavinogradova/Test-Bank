from requests import Response

from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_req_request import CreditReqRequest
from src.main.api.models.credit_req_response import CreditReqResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.foundation.endpoint import Endpoint


class UserSteps(BaseSteps):
    def create_account(self, user: CreateUserRequest | CreateUserResponse) -> CreateAccountResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_positive(self, create_user_request: CreateUserRequest,
                         deposit_request: DepositRequest) -> DepositResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        return response

    def deposit_negative(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest) -> Response:
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)

    def credit_req_positive(self, create_user_credit_request: CreateUserRequest,
                            credit_acc_request: CreditReqRequest) -> CreditReqResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_request.username,
                                      password=create_user_credit_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_acc_request)

        return response

    def credit_req_negative(self, create_user_credit_request: CreateUserRequest,
                            credit_acc_request: CreditReqRequest) -> Response:
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_request.username,
                                      password=create_user_credit_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(credit_acc_request)

    def transfer_positive(self, create_user_request: CreateUserRequest,
                          transfer_acc_request: TransferRequest) -> TransferResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_acc_request)
        return response

    def transfer_negative(self, create_user_request: CreateUserRequest,
                          transfer_acc_request: TransferRequest) -> Response:
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer_acc_request)

    def credit_repay_positive(self, create_user_credit_request: CreateUserRequest,
                              credit_repay_request: CreditRepayRequest) -> CreditRepayResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_request.username,
                                      password=create_user_credit_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def credit_repay_negative(self, create_user_credit_request: CreateUserRequest,
                              credit_repay_request: CreditRepayRequest) -> Response:
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_request.username,
                                      password=create_user_credit_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
