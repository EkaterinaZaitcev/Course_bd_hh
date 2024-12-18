from typing import Any

import psycopg2

class DBManager:
    """Класс для получения ифнормации о вакансиях из базы данных"""

    def __init__(self, db_name:str, params: dict[str, Any]) -> None:
        """Инициализатор класса DBManager"""
        self.db_name = db_name
        self.__params = params

    def connect_database(self):
        """Подключение к базе данных"""
        return psycopg2.connect(dbname=self.db_name, **self.__params)

    def get_companies_and_vacancies_count(self) -> list[str]:
        """Возвращает список работадателей и количество вакансий"""
        conn = self.connect_database()
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_name, COUNT(*)
                FROM vacancies JOIN employers USING(employer_id)
                GROUP BY employers.employer_name;"""
            )
            vacansion_counter = cur.fetchall()

        conn.close()

        return [f'{employer[0]}:{employer[1]} вакансий' for employer in vacansion_counter]

    def get_all_vacancies(self) -> list[str]:
        """Возвращает список всех вакансий"""
        conn = self.connect_database()
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_name, vacancy_name, salary_from, salary_to, vacancies.url
                            FROM vacancies JOIN employers USING(employer_id);"""
            )
            vacantion_data = cur.fetchall()
            conn.close()
            result = []
            for vac in vacantion_data:


