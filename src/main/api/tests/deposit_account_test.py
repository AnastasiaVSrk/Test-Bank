import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=1500.0)
        response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        assert response.balance == 1500.0, 'Баланс не обновлен после внесения депозита'

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == 1500.0, 'Баланс в БД не обновился после внесения депозита'


    def test_deposit_account_below_min(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=999)
        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == 0, 'Баланс в БД обновлен, депозит внесен'


    def test_deposit_account_above_max(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=9001)
        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == 0, 'Баланс в БД обновлен, депозит внесен'






