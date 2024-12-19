from src.head_hunter_api import HH
from src.config import config
from src.db_Manager import DBManager
from src.db_creater import create_db, save_data_to_database

def main():
    """Функция для работы с программой"""
    params = config()
    data_employer = HH().get_employers()
    data_vacancies = HH().get_vacancies()
    create_db('hh_db', params)
    save_data_to_database(data_employer, data_vacancies, 'hh_db', params)
    db_manager = DBManager(params)

    print("""Введите цифру для получения нужной Вам информации
            1 - получает список всех компаний и количество вакансий у каждой компаний.
            2 - получает список всех вакансий с указанием названия компании,
            названия вакансии, зарплаты и ссылки на вакансию.
            3 - получает среднюю зарплату по вакансиям.
            4 - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
            5 - получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
            0 - Завершить программу""")
    while True:
        user_input = input()
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print("Cписок всех компаний и количество вакансий у каждой компаний:")
            for i in companies_and_vacancies_count:
                print(i)
            print("Введите цифру для получения нужной Вам информации")
        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("""
                    список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию:
                    """)
            for i in all_vacancies:
                print(i)
            print("Введите цифру для получения нужной Вам информации")
        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print("средняя зарплату по вакансиям:")
            print(avg_salary)
            print("Введите цифру для получения нужной Вам информации")
        elif user_input == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
            for i in vacancies_with_higher_salary:
                print(i)
            print("Введите цифру для получения нужной Вам информации")
        elif user_input == "5":
            user_word = input("Введите ключ слово\n").lower()
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_word)
            print("список всех вакансий, в названии которых содержатся переданные в метод слова:")
            for i in vacancies_with_keyword:
                print(i)
            print("Введите цифру для получения нужной Вам информации")
        elif user_input == "0":
            print("Программа завершила работу")
            break

if __name__ == '__main__':
    main()

