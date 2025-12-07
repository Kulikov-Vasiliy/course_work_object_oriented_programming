import unittest
from unittest.mock import patch, Mock
import requests
from abc import ABC, abstractmethod


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

            # Этот цикл for не используется для возврата данных, он просто перебирает элементы
            # для примера тестирования мы можем проигнорировать его эффект на возвращаемое значение
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


class TestHeadHunterAPI(unittest.TestCase):

    def setUp(self):
        self.hh_api = HeadHunterAPI(search_query="Python developer", only_with_salary=True)

    def test_init(self):
        """Тестирование инициализации класса HeadHunterAPI"""
        self.assertEqual(self.hh_api.text, "Python developer")
        self.assertTrue(self.hh_api.only_with_salary)
        self.assertEqual(self.hh_api.currency, "RUR")
        self.assertTrue(self.hh_api.no_magic)

    def test_init_default_query(self):
        """Тестирование значения по умолчанию для пустого запроса"""
        hh_api_default = HeadHunterAPI(search_query="")
        self.assertEqual(hh_api_default.text, "Введите запрос")

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тестирование успешного получения данных из API"""
        # Создаем Mock-объект ответа
        mock_response = Mock()
        mock_response.status_code = 200
        # Определяем, что должен возвращать response.json()
        mock_response.json.return_value = {
            'items': [
                {'name': 'Vacancy 1', 'salary': {'from': 100, 'to': 200, 'currency': 'RUR'}}
            ],
            'found': 1
        }
        # Устанавливаем, что requests.get должен вернуть наш mock-объект
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()

        # Проверяем, что requests.get был вызван с правильными параметрами
        expected_url = "https://api.hh.ru/vacancies"
        expected_params = {
            "text": "Python developer",
            "only_with_salary": True,
            "no_magic": True
        }
        mock_get.assert_called_once_with(expected_url, params=expected_params)

        # Проверяем, что результат соответствует нашим mock-данным
        self.assertEqual(result['found'], 1)
        self.assertEqual(result['items'][0]['name'], 'Vacancy 1')

    @patch('requests.get')
    def test_get_vacancies_http_error_404(self, mock_get):
        """Тестирование обработки ошибки 404"""
        mock_response = Mock()
        mock_response.status_code = 404
        # Имитируем исключение HTTPError
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()
        self.assertEqual(result, "404\nУказанная вакансия не существует")

    @patch('requests.get')
    def test_get_vacancies_http_error_403(self, mock_get):
        """Тестирование обработки ошибки 403 (капча)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()
        self.assertEqual(result, "403\nТребуется ввести капчу")
