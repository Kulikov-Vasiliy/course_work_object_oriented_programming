import json
import os

import pytest

from src.json_class import AbstractJSONSaver, JSONSaver


def test_initialization(temp_json_file):
    """Проверяет, что файл создается при инициализации."""
    assert os.path.exists(temp_json_file)
    with open(temp_json_file, 'r', encoding='utf-8') as f:
        assert json.load(f) == []


def test_add_vacancy(json_saver, sample_vacancies):
    """Проверяет добавление списка вакансий в файл."""
    json_saver.add_vacancy(sample_vacancies)
    data = json_saver._JSONSaver__read_data()  # Доступ к приватному методу для чтения

    assert len(data) == 3
    assert data[0]['title'] == "Python Developer"
    assert data[2]['currency'] == "USD"


def test_get_vacancies_all(json_saver, sample_vacancies):
    """Проверяет получение всех вакансий из файла."""
    json_saver.add_vacancy(sample_vacancies)
    vacs = json_saver.get_vacancies()
    assert len(vacs) == 3


def test_get_vacancies_with_criteria(json_saver, sample_vacancies):
    """Проверяет получение вакансий по критериям (фильтрацию)."""
    json_saver.add_vacancy(sample_vacancies)

    # Поиск по валюте USD
    usd_vacs = json_saver.get_vacancies(criteria={'currency': 'USD'})
    assert len(usd_vacs) == 1
    assert usd_vacs[0]['title'] == "Data Scientist"

    # Поиск по несуществующему критерию
    non_existent = json_saver.get_vacancies(criteria={'title': 'Non Existent Job'})
    assert len(non_existent) == 0


def test_delete_vacancy_by_criteria(json_saver, sample_vacancies, capsys):
    """Проверяет удаление вакансий по критериям."""
    json_saver.add_vacancy(sample_vacancies)

    # Удаляем все вакансии с валютой RUB
    json_saver.delete_vacancy(criteria={'currency': 'RUB'})

    data = json_saver._JSONSaver__read_data()
    assert len(data) == 1
    assert data[0]['title'] == "Data Scientist"

    captured = capsys.readouterr()
    assert "Удалено 2 вакансий из" in captured.out


def test_delete_vacancy_by_object(json_saver, sample_vacancies, capsys):
    """Проверяет удаление списка объектов с помощью нового метода."""
    json_saver.add_vacancy(sample_vacancies)

    # Удаляем только "QA Engineer" и "Data Scientist"
    to_delete_list = [sample_vacancies[1], sample_vacancies[2]]
    json_saver.delete_vacancy_by_object(to_delete_list)

    data = json_saver._JSONSaver__read_data()
    assert len(data) == 1
    assert data[0]['title'] == "Python Developer"

    captured = capsys.readouterr()
    assert "Удалено 2 вакансий из" in captured.out


def test_abstract_class_instantiation():
    """Проверяет, что абстрактный класс нельзя инстанцировать напрямую."""
    with pytest.raises(TypeError):
        AbstractJSONSaver()