import unittest
from src.Vacancy import Vacancy

class TestVacancy(unittest.TestCase):

    def setUp(self):
        # Подготовка данных для тестов
        self.vacancy = Vacancy(
            title="Разработчик Python",
            url="http://example.com/vacancy/1",
            salary="100000 - 150000 RUB",
            currency="RUB",
            requirement="Опыт работы с Python от 3 лет",
            responsibility="Разработка бэкенда"
        )
        self.json_data_full = {
            'items': [
                {
                    'name': 'Аналитик данных',
                    'alternate_url': 'http://example.com/vacancy/2',
                    'salary': {
                        'from': 80000,
                        'to': 120000,
                        'currency': 'RUR'
                    },
                    'snippet': {
                        'requirement': 'Опыт работы с SQL',
                        'responsibility': 'Анализ данных'
                    }
                }
            ]
        }
        self.json_data_partial = {
            'items': [
                {
                    'name': 'Менеджер проектов',
                    'alternate_url': 'http://example.com/vacancy/3',
                    'salary': None,
                    'snippet': None
                }
            ]
        }
        self.json_data_empty = {'items': []}

    def test_init(self):
        """Тестирование инициализации объекта Vacancy"""
        self.assertEqual(self.vacancy.title, "Разработчик Python")
        self.assertEqual(self.vacancy.url, "http://example.com/vacancy/1")
        self.assertEqual(self.vacancy.salary, "100000 - 150000 RUB")
        self.assertEqual(self.vacancy.currency, "RUB")
        self.assertEqual(self.vacancy.requirement, "Опыт работы с Python от 3 лет")
        self.assertEqual(self.vacancy.responsibility, "Разработка бэкенда")

    def test_init_defaults(self):
        """Тестирование инициализации с значениями по умолчанию для требований и обязанностей"""
        v = Vacancy("Тестировщик", "http://example.com/vacancy/4", "50000 RUR", "RUR")
        self.assertEqual(v.requirement, "Требования не указаны")
        self.assertEqual(v.responsibility, "Обязанности не указаны")

    def test_str_representation(self):
        """Тестирование метода __str__"""
        expected_str_start = "Вакансия: Разработчик Python\nЗарплата: 100000 - 150000 RUB\nURL: http://example.com/vacancy/1\n"
        self.assertTrue(str(self.vacancy).startswith(expected_str_start))
        self.assertIn("Требования: Опыт работы с Python от 3 лет", str(self.vacancy))

    def test_repr_representation(self):
        """Тестирование метода __repr__"""
        expected_repr_start = "Vacancy(title='Разработчик Python', url='http://example.com/vacancy/1', salary='100000 - 150000 RUB currency=RUB'"
        self.assertTrue(repr(self.vacancy).startswith(expected_repr_start))

    def test_cast_to_object_list_full_data(self):
        """Тестирование cast_to_object_list с полными данными"""
        vacancies = Vacancy.cast_to_object_list(self.json_data_full)
        self.assertEqual(len(vacancies), 1)
        v = vacancies[0]
        self.assertIsInstance(v, Vacancy)
        self.assertEqual(v.title, 'Аналитик данных')
        self.assertEqual(v.salary, '80000 - 120000 RUR')
        self.assertEqual(v.requirement, 'Опыт работы с SQL')
        self.assertEqual(v.responsibility, 'Анализ данных')

    def test_cast_to_object_list_partial_data(self):
        """Тестирование cast_to_object_list с неполными данными (проверка значений по умолчанию)"""
        vacancies = Vacancy.cast_to_object_list(self.json_data_partial)
        self.assertEqual(len(vacancies), 1)
        v = vacancies[0]
        self.assertEqual(v.title, 'Менеджер проектов')
        self.assertEqual(v.salary, '0')
        self.assertIsNone(v.currency)
        self.assertEqual(v.requirement, 'Требования не указаны')
        self.assertEqual(v.responsibility, 'Обязанности не указаны')

    def test_cast_to_object_list_empty_data(self):
        """Тестирование cast_to_object_list с пустым списком вакансий"""
        vacancies = Vacancy.cast_to_object_list(self.json_data_empty)
        self.assertEqual(len(vacancies), 0)