import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.amount_generator import RandomAmountGenerator as AmountGen
from src.main.api.generators.amount_limits import AmountLimits
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.receiving_credit_request import ReceivingCreditRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_credit_secret_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = 'ROLE_CREDIT_SECRET'
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_account_credit_secret_response(api_manager, create_user_credit_secret_request):
    account_response = api_manager.user_steps.create_account(create_user_credit_secret_request)
    return account_response

@pytest.fixture
def create_account_response(api_manager, create_user_request):
    user_response = api_manager.user_steps.create_account(create_user_request)
    return user_response

@pytest.fixture
def create_second_account_response(api_manager, create_user_request):
    user_response = api_manager.user_steps.create_account(create_user_request)
    return user_response

@pytest.fixture
def deposit_account_response(api_manager, create_user_request, create_account_response):
    deposit_request = DepositAccountRequest(account_id=create_account_response.id, amount=AmountGen.generate_valid_amount(AmountLimits.DEPOSIT))
    deposit_response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)
    return deposit_response

@pytest.fixture
def receiving_credit_response(api_manager, create_user_credit_secret_request, create_account_credit_secret_response):
    receiving_credit_request = ReceivingCreditRequest(
        account_id=create_account_credit_secret_response.id,
        amount=AmountGen.generate_valid_amount(AmountLimits.CREDIT),
        term_months=AmountGen.generate_valid_term_months(AmountLimits.TERM_MONTHS)
    )
    receiving_credit_response = api_manager.user_steps.receiving_credit(receiving_credit_request, create_user_credit_secret_request)
    return receiving_credit_response

