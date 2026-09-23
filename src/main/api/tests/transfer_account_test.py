import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        first_account_response = api_manager.user_steps.create_account(create_user_request)
        second_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=first_account_response.id, amount=1500.0)
        api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        transfer_request = TransferAccountRequest(from_account_id=first_account_response.id, to_account_id=second_account_response.id, amount=1300.0)
        transfer_response = api_manager.user_steps.transfer_account(transfer_request, create_user_request)

        assert transfer_response.from_account_id_balance == 200.0, 'Баланс не изменен, перевод не выполнен'

        first_account_from_db = Account.get_account_by_id(db_session, first_account_response.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account_response.id)
        assert first_account_from_db.balance == 200.0, 'Баланс не обновлен в БД, списание не выполнено'
        assert second_account_from_db.balance == 1300.0, 'Баланс не обновлен в БД, пополнение не выполнено'

    def test_transfer_account_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        first_account_response = api_manager.user_steps.create_account(create_user_request)
        second_account_response = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferAccountRequest(from_account_id=first_account_response.id, to_account_id=second_account_response.id, amount=1300.0)
        api_manager.user_steps.transfer_account_invalid(transfer_request, create_user_request)

        first_account_from_db = Account.get_account_by_id(db_session, first_account_response.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account_response.id)
        assert first_account_from_db.balance == 0, 'Баланс обновлен в БД, списание выполнено'
        assert second_account_from_db.balance == 0, 'Баланс обновлен в БД, средства зачислены'





