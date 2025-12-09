import unittest
from unittest.mock import patch, Mock
import requests
# Импортируем ваши классы
from src.api_class import AbstractAPI, HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    """Тестирование класса HeadHunterAPI с использованием мокирования requests"""

    def setUp(self):
        # Инициализируем объект API для тестирования
        self.hh_api = HeadHunterAPI(search_query="Python developer", only_with_salary=True)

    def test_init(self):
        """Проверка инициализации приватных атрибутов"""
        # Доступ к приватным атрибутам через манглинг имен
        self.assertEqual(self.hh_api._HeadHunterAPI__text, "Python developer")
        self.assertTrue(self.hh_api._HeadHunterAPI__only_with_salary)
        self.assertEqual(self.hh_api.currency, "RUR")
        self.assertTrue(self.hh_api._HeadHunterAPI__no_magic)

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тестирование успешного получения данных из API с помощью мокирования"""
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

        # Вызываем метод, который мы тестируем
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
        """Тестирование обработки ошибки 404 (Not Found)"""
        mock_response = Mock()
        mock_response.status_code = 404
        # Имитируем исключение HTTPError
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()
        self.assertEqual(result, "404\nУказанная вакансия не существует")

    @patch('requests.get')
    def test_get_vacancies_http_error_403(self, mock_get):
        """Тестирование обработки ошибки 403 (Forbidden/Captcha)"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()
        self.assertEqual(result, "403\nТребуется ввести капчу")

    @patch('requests.get')
    def test_get_vacancies_other_http_error(self, mock_get):
        """Тестирование обработки других HTTP ошибок"""
        mock_response = Mock()
        mock_response.status_code = 500
        http_error_msg = "500 Server Error: Internal Server Error for url: https://api.hh.ru/vacancies"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(http_error_msg, response=mock_response)
        mock_get.return_value = mock_response

        result = self.hh_api.get_vacancies()
        self.assertIn("Произошла ошибка:", result)
        self.assertIn("500 Server Error", result)