import re


def filter_vacancies(vacancies_list: list[dict], filter_words: list[str]) -> list[dict]:
    """Фильтрует вакансии по ключевым словам"""
    words = filter_words
    result = []

    for vacancy in vacancies_list:
        title = vacancy.title.lower()
        if any(re.search(word, title, re.IGNORECASE) for word in words):
            result.append(vacancy)

    return result


def get_vacancies_by_salary(filtered_vacancies: list[dict], salary_range: str) -> list[dict]:
    """Фильтрует вакансии по зп"""
    result = []
    salary_from, salary_to = map(int, salary_range.split(' - '))

    for vacancy in filtered_vacancies:
        parts = vacancy.salary.split(' currency=')

        # Берём первую часть, которая содержит зарплатный диапазон
        salary_clean = parts[0]
        if not salary_clean or salary_clean == '0':
            continue  # Пропускаем вакансии без указания зарплаты

        salary_info = salary_clean.replace(' - ', ' ').split()
        salary_values = [int(val) for val in salary_info if val.isdigit()]

        if len(salary_values) == 1:  # Только "от" зарплата
            salary_from_vacancy = salary_values[0]
            if salary_from <= salary_from_vacancy <= salary_to:
                result.append(vacancy)
        elif len(salary_values) == 2:  # Диапазон зарплат
            salary_from_vacancy, salary_to_vacancy = salary_values
            if salary_from <= salary_to_vacancy and salary_to >= salary_from_vacancy:
                result.append(vacancy)

    return result


def sort_vacancies(ranged_vacancies: list[dict], ascending: bool=True) -> list[dict]:
    """Сортировка фильтрованных вакансий"""
    return sorted(ranged_vacancies, key=lambda vacancy: int(vacancy.salary.split()[0]), reverse=not ascending)


def get_top_vacancies(sorted_vacancies: list[dict], top_n: int) -> list[dict]:
    """Получение топа вакансий в заданном количестве"""
    return sorted_vacancies[:top_n]


def print_vacancies(top_vacancies):
    """Вывод желаемого количества вакансий в человекочитаемом виде"""
    for vacancy in top_vacancies:
        print(f"Вакансия: {vacancy.title}\nЗарплата: {vacancy.salary}\nURL: {vacancy.url}\n"
                f"Требования: {vacancy.requirement[:]}\nОбязанности: {vacancy.responsibility[:]}\n" + "=" * 40)
    return
