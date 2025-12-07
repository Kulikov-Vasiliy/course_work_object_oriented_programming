from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv
from enum import Enum, auto
import os


load_dotenv()
CURRENCY_API = os.getenv("API_KEY_CURRENCY")


class Experience(Enum):
    NO_EXPERIENCE = "Без опыта"
    LESS_THAN_1 = "Менее 1 года"
    ONE_TO_THREE = "от 1 года до 3 лет"
    THREE_TO_SIX = "от 3 до 6 лет"
    MORE_THAN_SIX = "Более 6 лет"

class Employment(Enum):
    CIVIL_CONTRACT = "ГПХ"
    SELF_EMPLOYED = "Самозанятость"
    OFFICIAL_EMPLOYMENT = "Официальное трудоустройство"
    SERVICE_CONTRACT = "Договор подряда"

class Currency(Enum):
    EUR = "Eur"
    RUB = "Rub"
    USD = "Usd"

# Создайте словарь для сопоставления значений образования
EDUCATION_LEVELS = {
    "Не требуется или не указано": "not_required_or_not_specified",
    "Среднее-специальное": "special_secondary",
    "Высшее": "higher"
}


class AbstractAPI(ABC):
    """Абстрактный класс для работы с апи"""

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(AbstractAPI):
    """
    Класс для работы с платформой hh.ru:
    должен уметь подключаться к API и получать вакансии
    """
    search_query: str
    only_with_salary: bool
    no_magic: bool


    def __init__(
            self, search_query:str, currency: str = "RUR",
            only_with_salary:bool=False,
            no_magic:bool=True,
    ):
        self.text = search_query if search_query != "" else "Введите запрос"
        self.only_with_salary = only_with_salary if only_with_salary is True else False
        self.currency = currency
        self.no_magic = no_magic

    def get_vacancies(self):
        """Подключение к api и получение вакансий с фильтрацией"""

        try:
            url = "https://api.hh.ru/vacancies"
            payload = {
                "text": self.text, "only_with_salary": self.only_with_salary,
                "no_magic": self.no_magic
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()
            result = response.json()

            for item in result.get('items', []):
                salary_info = item.get('salary', {})
                salary = salary_info.get('from', 0) or salary_info.get('to', 0)  # Если отсутствует, вернёт 0
                currency = salary_info.get('currency', '')  # Если отсутствует, вернёт пустую строку

            return result

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                return "400\nПараметры переданы с ошибкой"
            elif e.response.status_code == 403:
                return "403\nТребуется ввести капчу"
            elif e.response.status_code == 404:
                return "404\nУказанная вакансия не существует"
            else:
                return f"Произошла ошибка: {e}"
