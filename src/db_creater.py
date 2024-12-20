from typing import Any

import psycopg2


def create_db(db_name: str, params: dict[str, Any]) ->None:
    """Создание базы данных с таблицами"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
               CREATE TABLE employers (
                   employer_id INTEGER PRIMARY KEY,
                   employer_name text not null,
                   employer_area TEXT not null,
                   url TEXT,
                   open_vacancies INTEGER
               )
           """)

    with conn.cursor() as cur:
        cur.execute("""
               CREATE TABLE vacancies (
                   vacancy_id INTEGER,
                   vacancy_name VARCHAR,
                   vacancy_area VARCHAR,
                   salary INTEGER,
                   employer_id INTEGER REFERENCES employers(employer_id),
                   vacancy_url VARCHAR
               )
           """)

    conn.commit()
    conn.close()

def save_data_to_database(data_employer: list[dict[str, Any]], data_vacancies: list[dict[str, Any]],
                          db_name: str, params: dict):
    """Сохранение данных в базу"""
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for employer in data_employer:
            cur.execute("""
                    INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                        (employer['id'], employer['name'], employer['area']['name'], employer['alternate_url'],
                         employer['open_vacancies']))
        for vacancy in data_vacancies:  # 'vacancy', не 'vacancies'
            salary_from = vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary'][
                'from'] is not None else 0
            cur.execute("""
                        INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (vacancy.get('id'), vacancy['name'], vacancy['area']['name'], salary_from,
                         vacancy['employer']['id'], vacancy['alternate_url']))

    conn.commit()
    conn.close()
