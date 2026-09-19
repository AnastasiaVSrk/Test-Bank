import pytest

from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account(self, api_manager, create_user_request):
        first_account_response = api_manager.user_steps.create_account(create_user_request)
        second_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=first_account_response.id, amount=1500.0)
        api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        transfer_request = TransferAccountRequest(from_account_id=first_account_response.id, to_account_id=second_account_response.id, amount=1300.0)
        transfer_response = api_manager.user_steps.transfer_account(transfer_request, create_user_request)

        assert transfer_response.from_account_id_balance == 200.0

    def test_transfer_account_invalid(self, api_manager, create_user_request):
        first_account_response = api_manager.user_steps.create_account(create_user_request)
        second_account_response = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferAccountRequest(from_account_id=first_account_response.id, to_account_id=second_account_response.id, amount=1300.0)
        api_manager.user_steps.transfer_account_invalid(transfer_request, create_user_request)





