from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestCreditRepay:
    def test_credit_repay_positive(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest,
                                   credit_repay_request: CreditRepayRequest, db_session: Session):
        response = api_manager.user_steps.credit_repay_positive(create_user_credit_request, credit_repay_request)

        credit_repay_from_db = Transaction.make_transaction_by_credit_id(db_session, response.creditId)
        assert credit_repay_from_db.credit_id == response.creditId, 'ID кредитного счета не найден в БД, ошибка'
        assert credit_repay_from_db.id is not None, 'Транзакция погашения кредита отсутствует в БД'

    def test_credit_repay_negative(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest,
                                   invalid_credit_repay_request: CreditRepayRequest, db_session: Session):
        api_manager.user_steps.credit_repay_negative(create_user_credit_request, invalid_credit_repay_request)

        credit_repay_from_db = Transaction.make_transaction_by_credit_id(db_session,
                                                                         invalid_credit_repay_request.creditId)
        assert credit_repay_from_db is None, 'Транзакция погашения кредита найдена в БД, ошибка'
