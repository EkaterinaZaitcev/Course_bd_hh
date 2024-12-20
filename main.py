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
    db_manager = DBManager(params)
print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"0 - Выход из программы")

while True:
        user_input = input('Введите номер запроса\n')
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")

        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}\n")

        elif user_input == '0':
            break


if __name__ == '__main__':
    main()

