import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.amount_generator import RandomAmountGenerator as AmountGen
from src.main.api.generators.amount_limits import AmountLimits
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account(self,
                             db_session: Session,
                             api_manager: ApiManager,
                             create_user_request: CreateUserRequest,
                             create_account_response: CreateAccountResponse
                             ):
        deposit_request = DepositAccountRequest(
            account_id=create_account_response.id,
            amount=AmountGen.generate_valid_amount(AmountLimits.DEPOSIT)
        )
        response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        assert response.balance == deposit_request.amount, 'Баланс не обновлен после внесения депозита'

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == deposit_request.amount, 'Баланс в БД не обновился после внесения депозита'


    def test_deposit_account_below_min(self,
                                       db_session: Session,
                                       api_manager: ApiManager,
                                       create_user_request: CreateUserRequest,
                                       create_account_response: CreateAccountResponse
                                       ):

        deposit_request = DepositAccountRequest(
            account_id=create_account_response.id,
            amount=AmountGen.generate_below_min(AmountLimits.DEPOSIT)
        )

        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == 0, 'Баланс в БД обновлен, депозит внесен'


    def test_deposit_account_above_max(self,
                                       db_session: Session,
                                       api_manager: ApiManager,
                                       create_user_request: CreateUserRequest,
                                       create_account_response: CreateAccountResponse
                                       ):
        deposit_request = DepositAccountRequest(
            account_id=create_account_response.id,
            amount=AmountGen.generate_above_max(AmountLimits.DEPOSIT)
        )

        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)

        deposit_from_db = Account.get_account_by_id(db_session, deposit_request.account_id)
        assert deposit_from_db.balance == 0, 'Баланс в БД обновлен, депозит внесен'






