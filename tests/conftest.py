import json

import pytest

from src.json_class import JSONSaver
from src.Vacancy import Vacancy


@pytest.fixture
def temp_json_file(tmpdir):
    """Создает временный файл JSON и возвращает путь к нему."""
    file_path = tmpdir.join("test_vacancies.json")
    # Инициализируем файл пустым списком
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    return str(file_path)

# Фикстура для создания экземпляра JSONSaver
@pytest.fixture
def json_saver(temp_json_file):
    """Возвращает экземпляр JSONSaver, использующий временный файл."""
    return JSONSaver(filename=temp_json_file)

# Фикстура для создания тестовых объектов Vacancy
@pytest.fixture
def sample_vacancies():
    """Возвращает список тестовых объектов Vacancy."""
    return [
        Vacancy("Python Developer", "http://url1.com", "100000 - 150000 RUB", "RUB", "Req1", "Resp1"),
        Vacancy("QA Engineer", "http://url2.com", "80000 RUB", "RUB", "Req2", "Resp2"),
        Vacancy("Data Scientist", "http://url3.com", "150000 - 200000 USD", "USD", "Req3", "Resp3"),
    ]