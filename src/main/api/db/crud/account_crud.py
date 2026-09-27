from sqlalchemy.orm import Session
from src.main.api.db.models.account_table import Account
from src.main.api.db.db_allure_step import DbAllureStep

class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return DbAllureStep.run(
            f'DB: Получить Account по id={account_id}',
            lambda: db.query(Account).filter_by(id=account_id).first()
        )

