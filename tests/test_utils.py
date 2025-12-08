import unittest
import io
from unittest.mock import patch

from src.Vacancy import Vacancy
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)


class TestUtilsFunctions(unittest.TestCase):
    """Тестирование утилитарных функций с использованием импортированных модулей"""

    def setUp(self):
        # Подготовка фиктивных данных (список объектов Vacancy)
        self.vacancies_list = [
            Vacancy("Python Developer (Junior)", url='url1', salary="50000 - 70000 RUB", currency="RUB"),
            Vacancy("Senior Python Engineer", url='url2', salary="150000 - 200000 RUB", currency="RUB"),
            Vacancy("Data Scientist", url='url3', salary="100000 - 130000 RUB", currency="RUB"),
            Vacancy("QA Engineer", url='url4', salary="0", currency=None),
            Vacancy("Java Developer", url='url5', salary="80000 - 120000 RUB", currency="RUB"),
        ]

    def test_filter_vacancies_empty_filter_words(self):
        """Проверка фильтрации с пустым списком слов"""
        result = filter_vacancies(self.vacancies_list, [])
        self.assertEqual(len(result), 0)

    def test_filter_vacancies_basic_match(self):
        """Базовая проверка фильтрации по одному слову"""
        result = filter_vacancies(self.vacancies_list, ["Python"])
        self.assertEqual(len(result), 2)
        self.assertIn("Python Developer (Junior)", [v.title for v in result])


    def test_filter_vacancies_no_match(self):
        """Тестирование, когда ни одно слово из списка не найдено"""
        filter_words = ["GoLang", "C++"]
        filtered = filter_vacancies(self.vacancies_list, filter_words)
        self.assertEqual(len(filtered), 0)


    def test_get_vacancies_by_salary_range_match(self):
        """Проверка фильтрации по корректному диапазону ЗП"""
        salary_range = "90000 - 140000"
        filtered = get_vacancies_by_salary(self.vacancies_list, salary_range)
        self.assertEqual(len(filtered), 2)
        # Обращение к первому элементу списка
        self.assertEqual(filtered[0].title, "Data Scientist", "Java Developer")

    def test_get_vacancies_by_salary_skip_zero_salary(self):
        """Проверка, что вакансии с ЗП '0' пропускаются"""
        salary_range = "0 - 1000000"
        filtered = get_vacancies_by_salary(self.vacancies_list, salary_range)
        # Ожидаем все вакансии, кроме QA Engineer с ЗП 0
        self.assertEqual(len(filtered), 4)
        self.assertNotIn("QA Engineer", [v.title for v in filtered])

    def test_sort_vacancies_ascending(self):
        """Проверка сортировки по возрастанию ЗП"""
        sorted_list = sort_vacancies(self.vacancies_list, ascending=True)

        # Так как ЗП QA Engineer = 0, он должен идти первым.
        # Проверяем, что первый элемент - QA Engineer.
        self.assertEqual(sorted_list[0].title, "QA Engineer")
        self.assertEqual(sorted_list[-1].title, "Senior Python Engineer")

    def test_get_top_vacancies_standard(self):
        """Стандартная проверка получения топа"""
        top_list = get_top_vacancies(self.vacancies_list, 2)
        self.assertEqual(len(top_list), 2)
        self.assertEqual(top_list[0].title, "Python Developer (Junior)")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_vacancies_standard_output(self, mock_stdout):
        """Проверка стандартного вывода одной вакансии"""
        print_vacancies(self.vacancies_list[:1])
        output = mock_stdout.getvalue()
        self.assertIn("Вакансия: Python Developer (Junior)", output)
        self.assertIn("Зарплата: 50000 - 70000 RUB", output)
        self.assertIn("URL: url1", output)
