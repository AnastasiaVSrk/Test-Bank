import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.deposit_user_request import DepositUserRequest


@pytest.mark.api
class TestDepositUser:

    def test_deposit_user(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositUserRequest(account_id=account_response.id, amount=1500.0)
        response = api_manager.user_steps.deposit_user(deposit_request, create_user_request)

        assert response.balance == 1500.0

    def test_deposit_user_below_min(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositUserRequest(account_id=account_response.id, amount=999)
        response = api_manager.user_steps.deposit_user_invalid(deposit_request, create_user_request)


    def test_deposit_user_above_max(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositUserRequest(account_id=account_response.id, amount=9001)
        response = api_manager.user_steps.deposit_user_invalid(deposit_request, create_user_request)






