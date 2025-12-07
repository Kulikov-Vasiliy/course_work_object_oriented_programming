import unittest
import re
import io
from unittest.mock import patch
from src.Vacancy import Vacancy
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies



class TestVacancyClass(unittest.TestCase):
    """Тестирование методов класса Vacancy и статического метода cast_to_object_list"""

    def setUp(self):
        self.vacancy = Vacancy(
            title="Разработчик Python", url="e.com", salary="100000 RUB",
            currency="RUB", requirement="Опыт от 3 лет", responsibility="Разработка"
        )
        self.json_data_full = {
            'items': [{
                'name': 'Аналитик',
                'alternate_url': 'e.com',
                'salary': {'from': 80000, 'to': 120000, 'currency': 'RUR'},
                'snippet': {'requirement': 'SQL', 'responsibility': 'Анализ'}
            }]
        }
        self.json_data_partial = {
            'items': [{
                'name': 'Менеджер',
                'alternate_url': 'e.com',
                'salary': None,
                'snippet': None
            }]
        }
        self.json_data_empty = {'items': []}

    def test_init(self):
        self.assertEqual(self.vacancy.title, "Разработчик Python")
        self.assertEqual(self.vacancy.requirement, "Опыт от 3 лет")
        self.assertEqual(self.vacancy.currency, "RUB")

    def test_init_defaults(self):
        v = Vacancy("Title", "url", "salary", "RUR")
        self.assertEqual(v.requirement, "Требования не указаны")
        self.assertEqual(v.responsibility, "Обязанности не указаны")

    def test_str_representation(self):
        expected_start = "Вакансия: Разработчик Python\nЗарплата: 100000 RUB\nURL: e.com\n"
        self.assertTrue(str(self.vacancy).startswith(expected_start))

    def test_repr_representation(self):
        expected_start = "Vacancy(title='Разработчик Python'"
        self.assertTrue(repr(self.vacancy).startswith(expected_start))

    def test_cast_to_object_list_full_data(self):
        vacancies = Vacancy.cast_to_object_list(self.json_data_full)
        self.assertEqual(len(vacancies), 1)
        v = vacancies[0]
        self.assertIsInstance(v, Vacancy)
        self.assertEqual(v.title, 'Аналитик')
        self.assertEqual(v.salary, '80000 - 120000 RUR')
        self.assertEqual(v.requirement, 'SQL')

    def test_cast_to_object_list_partial_data(self):
        vacancies = Vacancy.cast_to_object_list(self.json_data_partial)
        self.assertEqual(len(vacancies), 1)
        v = vacancies[0]
        self.assertEqual(v.title, 'Менеджер')
        self.assertEqual(v.salary, '0')
        self.assertIsNone(v.currency)
        self.assertEqual(v.requirement, 'Требования не указаны')

    def test_cast_to_object_list_empty_data(self):
        vacancies = Vacancy.cast_to_object_list(self.json_data_empty)
        self.assertEqual(len(vacancies), 0)


class TestUtilsFunctions(unittest.TestCase):
    """Тестирование утилитарных функций (filter, sort, top_n, print)"""

    def setUp(self):
        # Фиктивные данные для тестов utils
        self.vacancies_list = [
            Vacancy("Python Developer (Junior)", "url1", "50000 - 70000 RUB", "RUB"), # Python (1)
            Vacancy("Senior Python Engineer", "url2", "150000 - 200000 RUB", "RUB"), # Python (2)
            Vacancy("Data Scientist (Python/R)", "url3", "100000 - 130000 RUB", "RUB"), # Python (3)
            Vacancy("QA Engineer", "url5", "0", None),
            Vacancy("Python Team Lead", "url6", "220000 RUB", "RUB"), # Python (4)
        ]

    def test_filter_vacancies_single_word(self):
        """Проверка фильтрации по одному слову (без учета регистра)"""
        filter_words = "Python"
        filtered = filter_vacancies(self.vacancies_list, filter_words)
        self.assertEqual(len(filtered), 4)
        self.assertTrue(all("python" in v.title.lower() for v in filtered))

    def test_get_vacancies_by_salary_range(self):
        """Проверка фильтрации по диапазону ЗП"""
        salary_range = "90000 - 140000"
        filtered = get_vacancies_by_salary(self.vacancies_list, salary_range)
        self.assertEqual(len(filtered), 1)
        v = filtered[0]
        self.assertEqual(v.title, "Data Scientist (Python/R)")

    def test_sort_vacancies_descending(self):
        """Проверка сортировки по убыванию (по первой цифре зарплаты)"""
        sorted_list = sort_vacancies(self.vacancies_list, ascending=False)
        self.assertEqual(sorted_list[0].title, "Python Team Lead")
        self.assertEqual(sorted_list[-1].title, "QA Engineer")


    def test_get_top_vacancies(self):
        """Проверка получения заданного количества топа вакансий"""
        top_n = 2
        top_list = get_top_vacancies(self.vacancies_list, top_n)
        self.assertEqual(len(top_list), 2)
        self.assertEqual(top_list[0].title,
                         "Python Developer (Junior)")
