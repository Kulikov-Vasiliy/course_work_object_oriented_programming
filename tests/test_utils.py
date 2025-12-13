import pytest
from unittest.mock import MagicMock, patch

from src.vacancy import Vacancy
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)


class TestFilterVacancies:

    def test_filter_with_match(self, sample_vacancies_list_objects):
        """Проверка фильтрации, когда слова совпадают"""
        filter_words = "Python Java"
        filtered = filter_vacancies(sample_vacancies_list_objects, filter_words)
        assert len(filtered) == 2
        titles = [v.title for v in filtered]
        assert "Python Developer (Mid)" in titles
        assert "Java Developer (Senior)" in titles

    def test_filter_no_match(self, sample_vacancies_list_objects):
        """Проверка фильтрации, когда совпадений нет"""
        filter_words = "C++"
        filtered = filter_vacancies(sample_vacancies_list_objects, filter_words)
        assert len(filtered) == 0

    def test_filter_case_insensitivity(self, sample_vacancies_list_objects):
        """Проверка, что фильтр не чувствителен к регистру"""
        filter_words = "qa"
        filtered = filter_vacancies(sample_vacancies_list_objects, filter_words)
        assert len(filtered) == 1
        assert filtered.title == "QA Engineer (Junior)"

    def test_filter_empty_words(self, sample_vacancies_list_objects):
        """Проверка обработки пустой строки фильтра"""
        filtered = filter_vacancies(sample_vacancies_list_objects, "")
        assert len(filtered) == 0


class TestGetVacanciesBySalary:

    def test_filter_salary_range_match_full_range(self, sample_vacancies_list_objects):
        """Фильтрация по полному диапазону, который охватывает несколько вакансий"""
        salary_range = "100000 - 160000"
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)

        # Ожидаем Python (100-150) и DevOps (130-160). Java (120-180) не попадает из-за верхней границы 180 > 160
        assert len(filtered) == 2
        titles = sorted([v.title for v in filtered])
        assert titles == ['DevOps Engineer (Lead)', 'Python Developer (Mid)']

    def test_filter_salary_range_match_from_only(self, sample_vacancies_list_objects, actual_titles):
        """Фильтрация по нижней границе диапазона пользователя (от 80k и выше)"""
        salary_range = "80000 - 0"  # u_salary_to == 0 (интерпретируется как "от 80k и выше")
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)
        # Ожидаемые вакансии:
        # Sales Manager (80k)
        # Python Developer (100k)
        # Java Developer (120k)
        # DevOps Engineer (130k)
        assert len(filtered) == 4
        expected_titles = sorted([
            "Sales Manager",
            "DevOps Engineer (Lead)",
            "Java Developer (Senior)",
            "Python Developer (Mid)"
        ])
        # Сравниваем полученный список заголовков с ожидаемым списком
        assert actual_titles == expected_titles

    def test_filter_salary_range_match_to_only(self, sample_vacancies_list_objects):
        """Фильтрация по верхней границе диапазона пользователя"""
        salary_range = "0 - 40000"  # u_salary_from == 0
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)

        # Ожидаем Cleaner (0k-40k), т.к. 40k >= 40k.
        assert len(filtered) == 1
        assert filtered[0].title == "Cleaner"

    def test_filter_salary_range_no_match(self, sample_vacancies_list_objects):
        """Фильтрация по диапазону, которому ни одна вакансия не соответствует"""
        salary_range = "200000 - 300000"
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)
        assert len(filtered) == 0

    def test_filter_salary_invalid_input(self, sample_vacancies_list_objects):
        """Обработка некорректного формата строки зарплаты - должен вернуть исходный список"""
        salary_range = "abc - def"
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)
        assert len(filtered) == len(sample_vacancies_list_objects)

    def test_filter_salary_zero_ranges(self, sample_vacancies_list_objects):
        """
        Проверка поведения при нулевых диапазонах (ввод пользователя 0-0).
        Функция возвращает исходный список.
        """
        salary_range = "0 - 0"
        filtered = get_vacancies_by_salary(sample_vacancies_list_objects, salary_range)
        assert len(filtered) == len(sample_vacancies_list_objects)


class TestSortVacancies:

    def test_sort_ascending(self, sample_vacancies_list_objects):
        """Сортировка по возрастанию минимальной зарплаты"""
        sorted_list = sort_vacancies(sample_vacancies_list_objects, ascending=True)
        # Ожидаемый порядок по минимальной ЗП: Junior (0), Cleaner (0, min is 0), QA (50k), Sales (80k), Python (100k), Java (120k), DevOps (130k)
        assert sorted_list[0].title == "Junior Intern"
        assert sorted_list[1].title == "Cleaner"
        assert sorted_list[-1].title == "DevOps Engineer (Lead)"

    def test_sort_descending(self, sample_vacancies_list_objects):
        """Сортировка по убыванию минимальной зарплаты"""
        sorted_list = sort_vacancies(sample_vacancies_list_objects, ascending=False)
        # Обратный порядок
        assert sorted_list[0].title == "DevOps Engineer (Lead)"
        assert sorted_list[-1].title == "Cleaner"


class TestPrintVacancies:
    """Тестирование функции вывода требует перехвата стандартного вывода (stdout)"""

    @patch('sys.stdout')
    def test_print_vacancies_output_format(self, mock_stdout, sample_vacancies_list_objects):
        """Проверка, что функция печати вызывает print с ожидаемым форматом"""
        # Берем одну вакансию для простоты проверки: Python Developer (100k-150k)
        vacancy_to_print = sample_vacancies_list_objects[0]
        print_vacancies([vacancy_to_print])

        # Convert the calls to a single string for easier assertion, simulating the output
        # Используем mock_stdout.write для захвата при использовании print() в Python 3+
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)

        assert "Вакансия: Python Developer (Mid)" in output
        assert "Зарплата: 100000" in output
        assert "Зарплата: 150000" in output
        assert "URL: url1" in output
        assert "=" * 40 in output

    @patch('sys.stdout')
    def test_print_vacancies_empty_list(self, mock_stdout):
        """Проверка вывода при пустом списке вакансий"""
        print_vacancies([])
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "Нет вакансий для отображения." in output
