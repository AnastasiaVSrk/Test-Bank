from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit
from src.main.api.db.db_allure_step import DbAllureStep


class CreditCrudDb:
    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return DbAllureStep.run(
            f'Получить Credit по account_id={account_id}',
            lambda: db.query(Credit).filter_by(account_id=account_id).first())

    @staticmethod
    def get_count_credit_by_account_id(db: Session, account_id: int) -> int:
        return DbAllureStep.run(
            f'Получить количество Credit по account_id={account_id}',
            lambda: db.query(Credit).filter_by(account_id=account_id).count()
        )