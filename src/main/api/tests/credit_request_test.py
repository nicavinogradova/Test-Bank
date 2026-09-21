import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_req_request import CreditReqRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_positive(self, api_manager: ApiManager,
                                     create_user_credit_request: CreateUserRequest,
                                     credit_account_request: CreditReqRequest,
                                     db_session: Session
                                     ):
        response = api_manager.user_steps.credit_req_positive(create_user_credit_request, credit_account_request)

        assert response.amount == credit_account_request.amount, 'Сумма кредита не равна запрошенной сумме'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId, 'ID кредитного счета не найден в БД, ошибка'
        assert credit_from_db.balance is not None, 'Поле баланса для кредитного счета отсутствует в БД'

    def test_credit_request_negative(self,
                                     api_manager: ApiManager,
                                     create_user_credit_request: CreateUserRequest,
                                     invalid_credit_account_request: CreditReqRequest,
                                     db_session: Session
                                     ):
        api_manager.user_steps.credit_req_negative(create_user_credit_request, invalid_credit_account_request)

        credit_from_db = Credit.get_credit_by_id(db_session, invalid_credit_account_request.accountId)
        assert credit_from_db is None, 'Кредитный счет найден в БД, ошибка'
