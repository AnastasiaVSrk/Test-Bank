import pytest
from src.main.api.models.receiving_credit_request import ReceivingCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self, api_manager, create_user_credit_secret_request):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=5000.0, term_months=12)
        receiving_credit_response = api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)

        repay_credit_request = RepayCreditRequest(credit_id=receiving_credit_response.credit_id, account_id=receiving_credit_request.account_id, amount=5000.0)
        repay_credit_response = api_manager.user_steps.repay_credit(repay_credit_request, create_user_credit_secret_request)

        assert repay_credit_response.amount_deposited == 5000.0

    def test_repay_credit_invalid_insufficient_funds(self, api_manager, create_user_credit_secret_request):
        account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)

        receiving_credit_request = ReceivingCreditRequest(account_id=account_response.id, amount=10000.0, term_months=12)
        receiving_credit_response = api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)

        repay_credit_request = RepayCreditRequest(credit_id=receiving_credit_response.credit_id, account_id=receiving_credit_request.account_id, amount=15000.0)
        api_manager.user_steps.repay_credit_invalid_insufficient_funds(repay_credit_request, create_user_credit_secret_request)
