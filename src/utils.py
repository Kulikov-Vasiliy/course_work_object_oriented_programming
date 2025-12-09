def filter_vacancies(vacancies_list: list[dict], filter_words: str) -> list[dict]:
    """Фильтрует вакансии по ключевым словам"""
    if not filter_words:
        return []

    result = []

    for vacancy in vacancies_list:
        title = vacancy.title.lower()  # type: ignore[attr-defined]
        if any(word.lower() in title for word in filter_words if word):
            result.append(vacancy)

    return result


def get_vacancies_by_salary(filtered_vacancies: list[dict], salary_range: str) -> list[dict]:
    """Фильтрует вакансии по зп"""
    if not filtered_vacancies or not salary_range:
        return []

    result = []  # type: ignore[var-annotated]
    try:
        salary_from, salary_to = map(int, salary_range.split(" - "))
    except (ValueError, AttributeError):
        return filtered_vacancies

    result = []

    for vacancy in filtered_vacancies:
        if not vacancy.salary or vacancy.salary == "0":  # type: ignore[attr-defined]
            continue

            # Извлекаем зарплату из строки
        salary_str = vacancy.salary  # type: ignore[attr-defined]

        # Если есть 'currency=', убираем эту часть
        if "currency=" in salary_str:
            salary_str = salary_str.split(" currency=")[0]

        # Извлекаем числа из строки
        numbers = []
        for part in salary_str.replace("-", " ").replace("—", " ").split():
            try:
                numbers.append(int(part))
            except ValueError:
                continue

        if not numbers:
            continue

        if len(numbers) == 1:  # Только "от"
            vacancy_salary = numbers[0]
            if salary_from <= vacancy_salary <= salary_to:
                result.append(vacancy)
        elif len(numbers) >= 2:  # Диапазон
            vacancy_from = numbers[0]
            vacancy_to = numbers[1]
            if not (vacancy_to < salary_from or vacancy_from > salary_to):
                result.append(vacancy)

    return result


def sort_vacancies(ranged_vacancies: list[dict], ascending: bool = True) -> list[dict]:
    """Сортировка фильтрованных вакансий"""
    if not ranged_vacancies:
        return []

    def get_salary(vacancy):  # type: ignore[no-untyped-def]
        """Извлекает минимальную зарплату из строки"""
        if not vacancy.salary:
            return 0

        salary_str = vacancy.salary
        if "currency=" in salary_str:
            salary_str = salary_str.split(" currency=")[0]

        # Ищем первое число в строке
        numbers = []
        for part in salary_str.replace("-", " ").replace("—", " ").split():
            try:
                numbers.append(int(part))
                break  # Берем первое найденное число
            except ValueError:
                continue

        return numbers[0] if numbers else 0

    return sorted(ranged_vacancies, key=get_salary, reverse=not ascending)


def get_top_vacancies(sorted_vacancies: list[dict], top_n: int) -> list[dict]:
    """Получение топа вакансий в заданном количестве"""
    if not sorted_vacancies or top_n <= 0:
        return []

    return sorted_vacancies[:top_n]


def print_vacancies(top_vacancies):  # type: ignore[no-untyped-def]
    """Вывод желаемого количества вакансий в человекочитаемом виде"""
    if not top_vacancies:
        print("Нет вакансий для отображения.")
        return

    for vacancy in top_vacancies:
        print(f"Вакансия: {vacancy.title}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"URL: {vacancy.url}")

        # Обрезаем длинный текст
        req = vacancy.requirement if hasattr(vacancy, "requirement") else "Не указаны"
        if len(req) > 150:
            req = req[:150] + "..."
        print(f"Требования: {req}")

        resp = vacancy.responsibility if hasattr(vacancy, "responsibility") else "Не указаны"
        if len(resp) > 150:
            resp = resp[:150] + "..."
        print(f"Обязанности: {resp}")

        print("=" * 40)
