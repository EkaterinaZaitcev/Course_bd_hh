import requests

class HH():
    """Класс для работы с API HeadHunter вакансии"""

    def __init__(self):
        self.__url = "https://api.hh.ru/"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {'per_page': 100, 'page': 0, 'only_with_salary': True}

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
        employers = [9140614, 5775464, 4748227, 605490, 10609539, 78638, 1740, 1473866, 39305, 2748]
        if self.get_response():
            self.__url = "https://api.hh.ru/employers/"
            self.__params["sort_by"] = "only_with_salary"
            self.__params["per_page"] = 100

        for employer in employers:
            self.__params["text"] = employer
            response = requests.get(
                self.__url+str(employer), headers=self.__headers)
            data = response.json()
            print(f'инфо из компаний: {data}')

        return employers

    def get_vacancies(self, id: str) -> list[dict]:
        """Метод для получения данных о вакансиях по id компании"""
        vacancies = []
        self.__params["employer_id"] = id
        self.__params["per_page"] = 100
        if self.get_response():
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            data = response.json().get("items", [])
            print(f'инфо из вакансий: {data}')
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies

if __name__ == "__main__":
    my_api = HH()
    response = my_api.get_employers()
    result = my_api.get_vacancies(1740)
    print(response, result)