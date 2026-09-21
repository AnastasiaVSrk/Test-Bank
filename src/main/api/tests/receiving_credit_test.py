import pytest
from src.main.api.models.receiving_credit_request import ReceivingCreditRequest

@pytest.mark.api
class TestReceivingCredit:
    def test_receiving_credit(self, api_manager, create_user_credit_secret_request):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=5000.0, term_months=12 )
        receiving_credit_response = api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)

        assert receiving_credit_response.balance == 5000.0

    def test_receiving_second_credit_invalid(self, api_manager, create_user_credit_secret_request):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=5000.0, term_months=12)
        api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)
        api_manager.user_steps.receiving_second_credit_invalid(receiving_credit_request, create_user_credit_secret_request)



