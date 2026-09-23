import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.receiving_credit_request import ReceivingCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

@pytest.mark.api
class TestReceivingCredit:
    def test_receiving_credit(self, db_session: Session, api_manager: ApiManager, create_user_credit_secret_request: CreateUserRequest):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=5000.0, term_months=12 )
        receiving_credit_response = api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)

        assert receiving_credit_response.balance == 5000.0, 'Сумма кредита не выдана'

        receiving_credit_from_db = Credit.get_credit_by_account_id(db_session, receiving_credit_response.account_id)
        assert receiving_credit_from_db.amount == 5000.0, 'Сумма кредита в БД не обновилась'
        assert receiving_credit_from_db.balance == -5000.0, 'Долг по кредиту в БД не назначен'
        assert receiving_credit_from_db.term_months == 12, 'Срок кредита в БД не назначен'

    def test_receiving_second_credit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_credit_secret_request: CreateUserRequest):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=5000.0, term_months=12)
        api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)
        api_manager.user_steps.receiving_second_credit_invalid(receiving_credit_request, create_user_credit_secret_request)

        receiving_credit_from_db = Credit.get_count_credit_by_account_id(db_session, account_response.id)
        assert receiving_credit_from_db == 1, 'Количество кредитов на счете в БД не равно 1'




