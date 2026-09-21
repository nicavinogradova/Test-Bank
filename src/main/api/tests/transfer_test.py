import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_participants import TransferParticipants
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransfer:
    def test_transfer_positive(self, api_manager: ApiManager, transfer_participants: TransferParticipants,
                               deposit_request_for_transfer: DepositRequest,
                               transfer_request: TransferRequest, db_session: Session):
        api_manager.user_steps.deposit_positive(transfer_participants.sender_user, deposit_request_for_transfer)

        response = api_manager.user_steps.transfer_positive(transfer_participants.sender_user, transfer_request)

        expected_balance = round(deposit_request_for_transfer.amount - transfer_request.amount, 2)

        assert response.fromAccountIdBalance == expected_balance, 'Некорректный баланс счета после перевода'

        transfer_from_db = Transaction.make_transaction_by_id(db_session, response.toAccountId)
        assert transfer_from_db.to_account_id == response.toAccountId, 'ID счета для пополнения не найден в БД, ошибка'
        assert transfer_from_db.id is not None, 'Транзакция перевода отсутствует в БД'

    def test_transfer_negative(self, api_manager: ApiManager, transfer_participants: TransferParticipants,
                               deposit_request_for_transfer: DepositRequest,
                               invalid_transfer_request: TransferRequest, db_session: Session):
        api_manager.user_steps.deposit_positive(transfer_participants.sender_user, deposit_request_for_transfer)

        api_manager.user_steps.transfer_negative(transfer_participants.sender_user, invalid_transfer_request)

        transfer_from_db = Transaction.make_transaction_by_id(db_session, transfer_participants.recipient_account.id)
        assert transfer_from_db is None, 'Транзакция найдена в БД, ошибка'
