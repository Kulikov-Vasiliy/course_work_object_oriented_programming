# Функция для взаимодействия с пользователем
from src.api_class import HeadHunterAPI
from src.Vacancy import Vacancy
from src.utils import (filter_vacancies, get_vacancies_by_salary,
                        sort_vacancies, get_top_vacancies, print_vacancies)
from src.json_class import JSONSaver, DATA_PATH

path_file = DATA_PATH


def user_interaction():
    platforms = ["HeadHunter"]
    # search_query = input("Введите поисковый запрос: ")
    search_query = "Python-разработчик"
    # with_salary = input("Показывать вакансии только с указанной зарплатой? Yes/No ").strip().upper()[0]
    with_salary = "Y"
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_n = 3
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filter_words = "Python Django"
    # salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
    salary_range = "100000 - 300000"

    # Пример использования HeadHunterAPI
    hh_api = HeadHunterAPI(search_query=search_query, only_with_salary= True if with_salary == "Y" else False)
    hh_vacancies_json = hh_api.get_vacancies()

    if isinstance(hh_vacancies_json, str):
        print(hh_vacancies_json)
        return

    # Преобразование набора данных из JSON в список объектов
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_json)
    for vac in vacancies_list[:top_n]:
        print(vac)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    # print(filtered_vacancies)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    # print(ranged_vacancies)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

    # Сохранение информации о вакансиях в файл
    json_saver = JSONSaver(filename=path_file)
    json_saver.add_vacancy(vacancies_list)
    json_saver.delete_vacancy(vacancies_list)


if __name__ == "__main__":
    user_interaction()