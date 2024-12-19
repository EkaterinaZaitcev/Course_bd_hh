import requests

class HH():
    """Класс для работы с API HeadHunter вакансии"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}

    def get_response(self) -> bool:
        """Метод подключения к API"""
        response = requests.get(
            self.__url, headers=self.__headers, params=self.__params
        )
        status_code = response.status_code
        print(status_code)
        if status_code == 200:
            return True
        else:
            return False

    def get_employers(self) -> list[dict]:
        """Метод для получения данных о работодателе"""
        employers = []
        if self.get_response():
            self.__url = "https://api.hh.ru/employers"
            self.__params["sort_by"] = "by_vacancies_open"
            self.__params["per_page"] = 10
        for employer in employers:
            self.__params["text"] = employer
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            data = response.json()
            print(f'инфо из компаний: {data}')
            if data.get("items"):
                for employer_data in data["items"]:
                    if employer_data.get("name") == employer:
                        id_ = employer_data.get("id")
                        name = employer_data.get("name")
                        url = employer_data.get("alternate_url")
                        employers.append(
                            {
                                "employer_id": id_,
                                "employer_name": name,
                                "company_url": url,
                            }
                        )
            else:
                employers.append(
                    {"employer_name": employer, "error": "Данные отсутствуют"}
                )
        return employers

    def get_vacancies(self, employer_id: str) -> list[dict]:
        """Метод для получения данных о вакансиях по id компании"""
        vacancies = []
        self.__params["employer_id"] = employer_id
        self.__params["per_page"] = 10
        if self.get_response():
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            data = response.json().get("items", [])
            print(f'инфо из вакансий: {data}')
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies

    @classmethod
    def change_data(cls, vacancy: dict) -> dict:
        """Метод для преобразования вакансии в подходящий формат"""
        salary = 0
        if type(vacancy.get("salary")) == dict:
            from_ = vacancy["salary"].get("from", 0)
            to = vacancy["salary"].get("to", 0)
            if (from_ is not None and from_ != 0) and (to is not None and to != 0):
                salary = (from_ + to) // 2
            elif from_ is not None and from_ != 0:
                salary = from_
            elif to is not None and to != 0:
                salary = to
        transformed_vacancy = {
            "vacancy_id": vacancy["id"],
            "employer_id": vacancy["employer"]["id"],
            "vacancy_name": vacancy["name"],
            "salary": salary,
            "vacancy_url": vacancy.get("alternate_url", ""),
        }
        return transformed_vacancy

if __name__ == "__main__":
    my_api = HH()
    response = my_api.get_employers()
    print(response)