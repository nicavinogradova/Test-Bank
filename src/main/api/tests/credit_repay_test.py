from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_req_request import CreditReqRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestCreditRepay:
    def test_credit_repay_positive(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest,
                                   create_credit_account_response: CreateAccountResponse, db_session: Session):
        credit_acc_request = CreditReqRequest(accountId=create_credit_account_response.id, amount=6000.20,
                                              termMonths=12)

        create_user_credit_response = api_manager.user_steps.credit_req_positive(create_user_credit_request,
                                                                                 credit_acc_request)

        credit_repay_request = CreditRepayRequest(
            creditId=create_user_credit_response.creditId,
            accountId=create_user_credit_response.id,
            amount=6000.20
        )

        response = api_manager.user_steps.credit_repay_positive(create_user_credit_request, credit_repay_request)

        credit_repay_from_db = Transaction.make_transaction_by_credit_id(db_session, response.creditId)
        assert credit_repay_from_db.credit_id == response.creditId, 'ID кредитного счета не найден в БД, ошибка'
        assert credit_repay_from_db.id is not None, 'Транзакция погашения кредита отсутствует в БД'

    def test_credit_repay_negative(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest,
                                   create_credit_account_response: CreateAccountResponse, db_session: Session):
        credit_acc_request = CreditReqRequest(accountId=create_credit_account_response.id, amount=6000.20,
                                              termMonths=12)

        create_user_credit_response = api_manager.user_steps.credit_req_positive(create_user_credit_request,
                                                                                 credit_acc_request)

        credit_repay_request = CreditRepayRequest(
            creditId=create_user_credit_response.creditId,
            accountId=create_user_credit_response.id,
            amount=4000.20
        )

        api_manager.user_steps.credit_repay_negative(create_user_credit_request, credit_repay_request)

        credit_repay_from_db = Transaction.make_transaction_by_credit_id(db_session,
                                                                         create_user_credit_response.creditId)
        assert credit_repay_from_db is None, 'Транзакция погашения кредита найдена в БД, ошибка'
