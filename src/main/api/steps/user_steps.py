from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.receiving_credit_request import ReceivingCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, deposit_account_request: DepositAccountRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self, deposit_account_request: DepositAccountRequest, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_account_request)

    def transfer_account(self, transfer_account_request: TransferAccountRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response

    def transfer_account_invalid(self, transfer_account_request: TransferAccountRequest, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            response_spec=ResponseSpecs.request_insufficient_funds()
        ).post(transfer_account_request)

    def receiving_credit(self, receiving_credit_request: ReceivingCreditRequest, create_user_credit_secret_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_secret_request.username, password=create_user_credit_secret_request.password),
            Endpoint.RECEIVING_CREDIT,
            response_spec=ResponseSpecs.request_created()
        ).post(receiving_credit_request)
        return response

    def receiving_second_credit_invalid(self, receiving_credit_request: ReceivingCreditRequest, create_user_credit_secret_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_secret_request.username, password=create_user_credit_secret_request.password),
            Endpoint.RECEIVING_CREDIT,
            response_spec=ResponseSpecs.request_not_found()
        ).post(receiving_credit_request)

    def repay_credit(self, repay_credit_request: RepayCreditRequest, create_user_credit_secret_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_secret_request.username, password=create_user_credit_secret_request.password),
            Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response

    def repay_credit_invalid_insufficient_funds(self, repay_credit_request: RepayCreditRequest, create_user_credit_secret_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_credit_secret_request.username, password=create_user_credit_secret_request.password),
            Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_insufficient_funds()
        ).post(repay_credit_request)