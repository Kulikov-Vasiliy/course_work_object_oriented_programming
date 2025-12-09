class Vacancy:
    """Класс для обработки вакансиями"""

    # [no-untyped-def]
    def __init__(
        self,
        title: str,
        url: str,
        salary: str,
        currency: str | None,
        requirement: str = "Требования не указаны",
        responsibility: str = "Обязанности не указаны",
    ) -> None:
        self.title = title
        self.url = url
        self.salary = salary
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility

    @staticmethod
    def cast_to_object_list(json_data: dict) -> list:
        vacancies_list = []
        for item in json_data.get("items", []):
            title = item.get("name")
            url = item.get("alternate_url")
            salary_info = item.get("salary")
            salary_str = "0"
            currency = None
            if salary_info:
                from_salary = salary_info.get("from", "")
                to_salary = salary_info.get("to", "")
                currency = salary_info.get("currency", "")
                salary_str = (
                    f"{from_salary} - {to_salary} {currency}"
                    if from_salary and to_salary
                    else f"{from_salary or to_salary} {currency}"
                )
            snippet = item.get("snippet")
            # print(f"Полученные данные: {snippet}")

            if snippet:
                requirement = snippet.get("requirement", "Требования не указаны")
                responsibility = snippet.get("responsibility", "Обязанности не указаны")
            else:
                requirement = "Требования не указаны"
                responsibility = "Обязанности не указаны"
            # print(f"Требования: {requirement}, Обязанности: {responsibility}")
            vacancies_list.append(Vacancy(title, url, salary_str, currency, requirement, responsibility))

        return vacancies_list

    def __repr__(self):  # type: ignore[no-untyped-def]
        return (
            f"Vacancy(title='{self.title}', "
            f"url='{self.url}', "
            f"salary='{self.salary} currency={self.currency}', "
            f"requirement={self.requirement[:]}, "
            f"responsibility={self.responsibility[:]})"
        )

    def __str__(self):  # type: ignore[no-untyped-def]
        return (
            f"Вакансия: {self.title}\nЗарплата: {self.salary}\nURL: {self.url}\n"
            f"Требования: {self.requirement[:]}\nОбязанности: {self.responsibility[:]}\n" + "=" * 40
        )
