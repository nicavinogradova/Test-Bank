import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestDeposit:

    def test_deposit_positive(self, api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              db_session: Session
                              ):
        deposit_request = DepositRequest(accountId=create_account_response.id, amount=3000.20)

        response = api_manager.user_steps.deposit_positive(create_user_request, deposit_request)

        assert response.balance == deposit_request.amount

        deposit_from_db = Transaction.make_transaction_by_id(db_session, response.id)
        assert deposit_from_db.to_account_id == response.id, 'ID счета для пополнения не найден в БД, ошибка'
        assert deposit_from_db.id is not None, 'Транзакция пополнения счета отсутствует в БД'

    def test_deposit_negative(self, api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              db_session: Session
                              ):
        deposit_request = DepositRequest(accountId=create_account_response.id, amount=300.75)

        api_manager.user_steps.deposit_negative(create_user_request, deposit_request)

        deposit_from_db = Transaction.make_transaction_by_id(db_session, create_account_response.id)
        assert deposit_from_db is None, 'Транзакция не найдена в БД, ошибка'
