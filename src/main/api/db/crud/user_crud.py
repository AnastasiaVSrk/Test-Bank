from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User
from src.main.api.db.db_allure_step import DbAllureStep

class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return DbAllureStep.run(
            f'Получение User по username={username}',
            lambda: db.query(User).filter_by(username=username).first()
        )

