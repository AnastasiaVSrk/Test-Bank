import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.amount_generator import RandomAmountGenerator as AmountGen
from src.main.api.generators.amount_limits import AmountRange, AmountLimits
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.receiving_credit_response import ReceivingCreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self,
                          db_session: Session,
                          api_manager: ApiManager,
                          create_user_credit_secret_request: CreateUserRequest,
                          receiving_credit_response: ReceivingCreditResponse
                          ):

        repay_credit_request = RepayCreditRequest(
            credit_id=receiving_credit_response.credit_id,
            account_id=receiving_credit_response.account_id,
            amount=receiving_credit_response.amount
        )

        repay_credit_response = api_manager.user_steps.repay_credit(repay_credit_request, create_user_credit_secret_request)

        assert repay_credit_response.amount_deposited == receiving_credit_response.amount, 'Ошибка, сумма кредита не внесена'

        repay_credit_from_db = Credit.get_credit_by_account_id(db_session, receiving_credit_response.account_id)
        assert repay_credit_from_db.amount == receiving_credit_response.amount, 'Сумма кредита в БД не обновилась'
        assert repay_credit_from_db.balance == 0, 'Долг в БД не погашен'

    def test_repay_credit_invalid_insufficient_funds(self,
                                                     db_session: Session,
                                                     api_manager: ApiManager,
                                                     create_user_credit_secret_request: CreateUserRequest,
                                                     receiving_credit_response: ReceivingCreditResponse
                                                     ):

        repay_credit_request = RepayCreditRequest(
            credit_id=receiving_credit_response.credit_id,
            account_id=receiving_credit_response.account_id,
            amount=AmountGen.generate_valid_amount(AmountLimits.CREDIT)
        )

        api_manager.user_steps.repay_credit_invalid_insufficient_funds(repay_credit_request, create_user_credit_secret_request)

        repay_credit_from_db = Credit.get_credit_by_account_id(db_session, receiving_credit_response.account_id)
        assert repay_credit_from_db.amount == receiving_credit_response.amount, 'Сумма кредита в БД обновилась, ошибка'
        assert repay_credit_from_db.balance == -receiving_credit_response.amount, 'Долг в БД по кредиту изменен, ошибка'
