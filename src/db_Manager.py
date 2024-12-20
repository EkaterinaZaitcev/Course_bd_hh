import psycopg2

class DBManager:
    """Класс для получения ифнормации о вакансиях из базы данных"""

    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hhdb', **params)
        self.cur = self.conn.cursor()


    def get_companies_and_vacancies_count(self) -> list[str]:
        """Возвращает список работадателей и количество вакансий"""
        self.cur.execute(
                """SELECT employers.employer_name, COUNT(vacancy.employer_id)
                FROM employers
                JOIN vacancy USING (employer_id)
                GROUP BY employers.employer_name
                ORDER BY COUNT DESC"""
            )

        return self.cur.fetchall()

    def get_all_vacancies(self):
        """список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию."""
        self.cur.execute("""
                    SELECT employers.employer_name, vacancy_name, salary, vacancy_url
                    FROM vacancy
                    JOIN employers USING (employer_id)
                    ORDER BY salary desc""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""
        self.cur.execute("""
                    SELECT AVG(salary)
                    FROM vacancy
            """)

        return self.cur.fetchall()


    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        self.cur.execute(
            """
            SELECT vacancy_name, salary
            FROM vacancy
            GROUP BY vacancy_name, salary
            having salary > (SELECT AVG(salary) FROM vacancy)
            ORDER BY salary DESC"""
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        request_sql = """
                SELECT * FROM vacancy
                WHERE LOWER (vacancy_name) LIKE %s
                """
        self.cur.execute(request_sql, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()
