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


if __name__ == '__main__':
    main()

