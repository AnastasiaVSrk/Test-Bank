import allure
from typing import Callable, Any

class DbAllureStep:
    @staticmethod
    def run(step_name: str, query: Callable[[], Any]) -> Any:
        with allure.step(step_name):
            result = query()
            allure.attach(str(result), 'DB result', allure.attachment_type.TEXT)
            return result
