from db_manager import DBManager


def main():
    db_manager = DBManager()
    db_manager.create_tables()
    db_manager.fill_employees()
    db_manager.fill_vacancies()
    print("База данных сформирована\n")

    while True:
        try:
            command = int(input("1. Получить список всех компаний и количество вакансий у каждой компании;\n"
                                "2. Получить список всех вакансий с указанием названия компании, названия вакансии и "
                                "зарплаты и ссылки на вакансию;\n"
                                "3. Получить среднюю зарплату по вакансиям;\n"
                                "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n"
                                "5. Получить список всех вакансий по ключевому слову;\n"
                                "6. Закрыть программу.\n"
                                "Введите команду: "))
        except ValueError:
            print("Команда должна быть цифрой от 1 до 6\n")
            continue

        if command == 1:
            db_manager.get_count_employees_vacancies()
        elif command == 2:
            db_manager.get_all_vacancies()
        elif command == 3:
            db_manager.get_avg_salary()
        elif command == 4:
            db_manager.get_vacancies_with_higher_salary()
        elif command == 5:
            keyword = input("Введите ключевое слово: ")
            db_manager.get_vacancies_with_keyword(keyword)
        elif command == 6:
            break
        else:
            print("Команда должна быть цифрой от 1 до 6\n")
            continue


if __name__ == '__main__':
    main()
