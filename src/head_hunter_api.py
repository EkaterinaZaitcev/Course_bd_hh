from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """Родительский класс get-запросов"""

    @abstractmethod
    def load_vacancies(self, keyword):
        """Метод отправки get-запроса на сайт Head Hunter"""
        pass


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def load_vacancies(self, keyword: str) -> list:
        """Получение вакансий по ключевому слову"""
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            if response:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
                print(vacancies)
            else:
                break
        vacancies_list = []
        if self.__vacancies:
            """Получение списка словарей с ключами"""
            for vacancy in self.__vacancies:
                name = vacancy.get("name")
                url = vacancy.get("alternate_url")
                requirement = vacancy.get("snippet").get("requirement")
                responsibility = vacancy.get("snippet").get("responsibility")
                if vacancy.get("salary"):
                    if vacancy.get("salary").get("to"):
                        salary = vacancy.get("salary").get("to")
                    elif vacancy.get("salary").get("from"):
                        salary = vacancy.get("salary").get("from")
                else:
                    salary = 0
                vac = {
                    "name": name,
                    "url": url,
                    "requirement": requirement,
                    "responsibility": responsibility,
                    "salary": salary,
                }
                vacancies_list.append(vac)
        return vacancies_list
