import io
import re
import unittest
from unittest.mock import patch

from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.Vacancy import Vacancy


class Vacancy:
    def __init__(self, title, url=None, salary=None, currency=None, requirement="Требования не указаны",
                 responsibility="Обязанности не указаны"):
        self.title = title
        self.url = url
        self.salary = salary
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility

    def __repr__(self):
        return f"Vacancy(title='{self.title}')"


def filter_vacancies(vacancies_list: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрует вакансии по ключевым словам"""
    words = filter_words
    result = []
    for vacancy in vacancies_list:
        title = vacancy.title.lower()
        if any(re.search(word.lower(), title, re.IGNORECASE) for word in words if
               word):  # Добавлена проверка на пустое слово
            result.append(vacancy)
    return result


class TestFilterVacancies(unittest.TestCase):

    def setUp(self):
        # Подготовка фиктивных данных (список объектов Vacancy)
        self.vacancies_list = [
            Vacancy("Python Developer (Junior)"),  # 1: Python, Developer
            Vacancy("Senior Python Engineer"),  # 2: Python, Engineer
            Vacancy("Data Scientist (Python/R)"),  # 3: Python, Scientist, Data
            Vacancy("QA Engineer"),  # 4: QA, Engineer
            Vacancy("Frontend Developer"),  # 5: Frontend, Developer
            Vacancy("Java Developer"),  # 6: Java, Developer
        ]

    def test_filter_vacancies_multiple_words(self):
        """Тестирование фильтрации по нескольким словам в списке (логика OR)"""
        filter_words = ["Python", "Java"]
        filtered = filter_vacancies(self.vacancies_list, filter_words)

        # Ожидаем 4 вакансии Python + 1 вакансию Java = 5 вакансий
        self.assertEqual(len(filtered), 5)
        titles = [v.title for v in filtered]
        self.assertIn("Java Developer", titles)
        self.assertIn("Senior Python Engineer", titles)

    def test_filter_vacancies_single_word(self):
        """Тестирование фильтрации по списку из одного слова ('QA')"""
        filter_words = ["QA"]
        filtered = filter_vacancies(self.vacancies_list, filter_words)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "QA Engineer")

    def test_filter_vacancies_empty_list(self):
        """Тестирование с пустым списком фильтров"""
        filter_words = []
        filtered = filter_vacancies(self.vacancies_list, filter_words)
        self.assertEqual(len(filtered), 0)

    def test_filter_vacancies_no_match(self):
        """Тестирование, когда ни одно слово из списка не найдено"""
        filter_words = ["GoLang", "C++"]
        filtered = filter_vacancies(self.vacancies_list, filter_words)

        self.assertEqual(len(filtered), 0)

    def test_filter_vacancies_case_insensitivity(self):
        """Тестирование, что регистр слов не имеет значения"""
        filter_words = ["pYtHoN"]
        filtered = filter_vacancies(self.vacancies_list, filter_words)

        self.assertEqual(len(filtered), 4)
