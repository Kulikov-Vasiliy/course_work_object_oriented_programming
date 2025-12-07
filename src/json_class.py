from abc import ABC, abstractmethod
import json

import os

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "vacancies.json")


class AbstractJSONSaver(ABC):
    """Абстрактный класс для сохранения данных о вакансиях в файл и работы с ними"""

    @abstractmethod
    def add_vacancy(self, vacancy_data: dict | list):
        """Метод для добавления вакансий в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict) -> list:
        """Метод для получения данных из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, criteria: dict):
        """Метод для удаления информации о вакансиях из файла."""
        pass


class JSONSaver(AbstractJSONSaver):
    """Класс для сохранения вакансий в json-файл и их удаления из него"""

    def __init__(self, filename: str = DATA_PATH) -> None:
        self.filename = filename
        # Убедимся, что файл существует или создан с пустым списком
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            self.__write_data([])

    def __read_data(self) -> list:
        """Внутренний метод для чтения данных из файла."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __write_data(self, data: list) -> None:
        """Внутренний метод для записи данных в файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy_list: list) -> None:
        """Логика добавления списка объектов Vacancy в файл."""
        data = self.__read_data()
        # Преобразуем объекты Vacancy в словари перед сохранением
        vac_dicts = [self.__vacancy_to_dict(vac) for vac in vacancy_list]
        data.extend(vac_dicts)
        self.__write_data(data)
        print(f"Добавлено {len(vacancy_list)} вакансий в {self.filename}")

    def get_vacancies(self, criteria: dict = None) -> list:
        """Получение данных из файла по указанным критериям."""
        data = self.__read_data()
        if criteria is None:
            return data

        # Простая фильтрация по критериям
        filtered_data = [
            item for item in data
            if all(item.get(key) == value for key, value in criteria.items())
        ]
        return filtered_data

    def delete_vacancy(self, criteria: dict):
        """Удаление информации о вакансиях из файла по критериям (например, по названию)."""
        data = self.__read_data()
        initial_count = len(data)

        # Оставляем только те элементы, которые НЕ соответствуют критериям удаления
        filtered_data = [
            item for item in data
            if not all(item.get(key) == value for key, value in criteria.items())
        ]

        self.__write_data(filtered_data)
        deleted_count = initial_count - len(filtered_data)
        print(f"Удалено {deleted_count} вакансий из {self.filename}")

    def delete_vacancy_by_object(self, vacancy_list: list):
        """Удаление списка объектов Vacancy из файла по URL в качестве уникального идентификатора."""
        data = self.__read_data()
        urls_to_delete = {vac.url for vac in vacancy_list}

        filtered_data = [item for item in data if item.get('url') not in urls_to_delete]

        self.__write_data(filtered_data)
        deleted_count = len(data) - len(filtered_data)
        print(f"Удалено {deleted_count} вакансий из {self.filename} по списку объектов.")

    def __vacancy_to_dict(self, vacancy_obj):
        """Преобразует объект Vacancy в словарь для записи в JSON."""
        return {
            'title': vacancy_obj.title,
            'url': vacancy_obj.url,
            'salary': vacancy_obj.salary,
            'currency': vacancy_obj.currency,
            'requirement': vacancy_obj.requirement,
            'responsibility': vacancy_obj.responsibility,
        }

    #
    # def __init__(self, filename: str = DATA_PATH) -> None:
    #     self.filename = filename
    #     # Убедимся, что файл существует или создан с пустым списком
    #     if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
    #         with open(self.filename, 'w', encoding='utf-8') as f:
    #             json.dump([], f, ensure_ascii=False, indent=4)
    #
    # def __read_data(self) -> list:
    #     """Внутренний метод для чтения данных из файла."""
    #     with open(self.filename, 'r', encoding='utf-8') as f:
    #         return json.load(f)
    #
    # def __write_data(self, data: list) -> None:
    #     """Внутренний метод для записи данных в файл."""
    #     with open(self.filename, 'w', encoding='utf-8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)
    #
    # def add_vacancy(self, vacancy_list: list) -> None:
    #     """Логика добавления списка вакансий в файл."""
    #     data = self.__read_data()
    #     # Преобразуем объекты Vacancy в словари перед сохранением
    #     vac_dicts = [self.__vacancy_to_dict(vac) for vac in vacancy_list]
    #     data.extend(vac_dicts)
    #     self.__write_data(data)
    #     print(f"Добавлено {len(vacancy_list)} вакансий в {self.filename}")
    #
    # def get_vacancies(self, criteria: dict = None) -> list:
    #     """Получение данных из файла по указанным критериям."""
    #     data = self.__read_data()
    #     if criteria is None:
    #         return data
    #
    #     # Простая фильтрация по критериям (можно расширить)
    #     filtered_data = [
    #         item for item in data
    #         if all(item.get(key) == value for key, value in criteria.items())
    #     ]
    #     return filtered_data
    #
    # def del_vacancy(self, criteria:dict):
    #     """Удаление информации о вакансиях из файла по критериям."""
    #     data = self.__read_data()
    #     initial_count = len(data)
    #
    #     # Оставляем только те элементы, которые НЕ соответствуют критериям удаления
    #     filtered_data = [
    #         item for item in data
    #         if not all(item.get(key) == value for key, value in criteria.items())
    #     ]
    #
    #     self.__write_data(filtered_data)
    #     deleted_count = initial_count - len(filtered_data)
    #     print(f"Удалено {deleted_count} вакансий из {self.filename}")
    #
    # def __vacancy_to_dict(self, vacancy_obj):
    #     """Преобразует объект Vacancy в словарь для записи в JSON."""
    #     return {
    #         'title': vacancy_obj.title,
    #         'url': vacancy_obj.url,
    #         'salary': vacancy_obj.salary,
    #         'currency': vacancy_obj.currency,
    #         'requirement': vacancy_obj.requirement,
    #         'responsibility': vacancy_obj.responsibility,
    #     }
