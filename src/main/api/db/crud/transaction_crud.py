from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def make_transaction_by_id(db: Session, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=to_account_id).order_by(Transaction.id.desc()).first()

    def make_transaction_by_credit_id(db: Session, credit_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id).order_by(Transaction.id.desc()).first()
