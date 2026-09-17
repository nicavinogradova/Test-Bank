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
                               db_session: Session):
        sender_user = transfer_participants.sender_user
        sender_account = transfer_participants.sender_account
        recipient_account = transfer_participants.recipient_account

        deposit_request = DepositRequest(accountId=sender_account.id, amount=5000.25)

        api_manager.user_steps.deposit_positive(sender_user, deposit_request)

        transfer_acc_request = TransferRequest(
            fromAccountId=sender_account.id,
            toAccountId=recipient_account.id,
            amount=1500.25,
        )

        response = api_manager.user_steps.transfer_positive(sender_user, transfer_acc_request)

        assert response.fromAccountIdBalance == 3500.00

        transfer_from_db = Transaction.make_transaction_by_id(db_session, response.toAccountId)
        assert transfer_from_db.to_account_id == response.toAccountId, 'ID счета для пополнения не найден в БД, ошибка'
        assert transfer_from_db.id is not None, 'Транзакция перевода отсутствует в БД'

    def test_transfer_negative(self, api_manager: ApiManager, transfer_participants: TransferParticipants,
                               db_session: Session):
        sender_user = transfer_participants.sender_user
        sender_account = transfer_participants.sender_account
        recipient_account = transfer_participants.recipient_account

        deposit_request = DepositRequest(accountId=sender_account.id, amount=5000.25)

        api_manager.user_steps.deposit_positive(sender_user, deposit_request)

        transfer_acc_request = TransferRequest(
            fromAccountId=sender_account.id,
            toAccountId=recipient_account.id,
            amount=6500.25,
        )

        api_manager.user_steps.transfer_negative(sender_user, transfer_acc_request)

        transfer_from_db = Transaction.make_transaction_by_id(db_session, recipient_account.id)
        assert transfer_from_db is None, 'Транзакция найдена в БД, ошибка'
