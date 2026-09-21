import pytest
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=1500.0)
        response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        assert response.balance == 1500.0

    def test_deposit_account_below_min(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=999)
        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)


    def test_deposit_account_above_max(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositAccountRequest(account_id=account_response.id, amount=9001)
        api_manager.user_steps.deposit_account_invalid(deposit_request, create_user_request)






