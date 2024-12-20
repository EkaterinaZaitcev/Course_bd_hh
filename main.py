from src.head_hunter_api import get_employee, get_vacancies
from src.config import config
from src.db_Manager import DBManager
from src.db_creater import create_db, save_data_to_database

def main():
    """Функция для работы с программой"""
    params = config()
    data_employer = get_employee()
    data_vacancies = get_vacancies()
    create_db('hhdb', params)
    save_data_to_database(data_employer, data_vacancies,'hhdb', params)
    dbManager = DBManager(params)

    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
          f"0 - Выход из программы")

    while True:
        user_input = input('Введите номер запроса\n')
        if user_input == "1":
            companies_and_vacancies_count = dbManager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")

        elif user_input == "2":
            all_vacancies = dbManager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}\n")

        elif user_input == '3':
            avg_salary = dbManager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}\n")

        elif user_input == "4":
            vacancies_with_higher_salary = dbManager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}\n")

        elif user_input == "5":
            user_input = input('Введите ключевое слово ')
            vacancies_with_keyword = dbManager.get_vacancies_with_keyword(user_input)
            print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")

        elif user_input == '0':
            break


if __name__ == '__main__':
    main()

