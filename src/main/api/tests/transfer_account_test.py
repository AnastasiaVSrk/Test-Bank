import pytest
from pytest import approx
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.amount_generator import RandomAmountGenerator as AmountGen
from src.main.api.generators.amount_limits import AmountLimits, AmountRange


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account(self,
                              db_session: Session, api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              create_second_account_response: CreateAccountResponse,
                              deposit_account_response: DepositAccountResponse
                              ):

        transfer_amount = AmountGen.generate_valid_amount(AmountRange(
            AmountLimits.TRANSFER.min_value,
            min(deposit_account_response.balance, AmountLimits.TRANSFER.max_value)
        ))

        transfer_request = TransferAccountRequest(
            from_account_id=create_account_response.id,
            to_account_id=create_second_account_response.id,
            amount=transfer_amount
        )

        transfer_response = api_manager.user_steps.transfer_account(transfer_request, create_user_request)

        assert transfer_response.from_account_id_balance == approx(deposit_account_response.balance - transfer_request.amount), 'Баланс не изменен, перевод не выполнен'

        first_account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        second_account_from_db = Account.get_account_by_id(db_session, create_second_account_response.id)
        assert first_account_from_db.balance == approx(deposit_account_response.balance - transfer_request.amount), 'Баланс не обновлен в БД, списание не выполнено'
        assert second_account_from_db.balance == transfer_request.amount, 'Баланс не обновлен в БД, пополнение не выполнено'

    def test_transfer_account_invalid(self,
                              db_session: Session, api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              create_second_account_response: CreateAccountResponse,
                              ):

        transfer_request = TransferAccountRequest(
            from_account_id=create_account_response.id,
            to_account_id=create_second_account_response.id,
            amount=AmountGen.generate_valid_amount(AmountLimits.TRANSFER)
        )

        api_manager.user_steps.transfer_account_invalid(transfer_request, create_user_request)

        first_account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        second_account_from_db = Account.get_account_by_id(db_session, create_second_account_response.id)
        assert first_account_from_db.balance == 0, 'Баланс обновлен в БД, списание выполнено'
        assert second_account_from_db.balance == 0, 'Баланс обновлен в БД, средства зачислены'





