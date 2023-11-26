import psycopg2
from utils import get_employer, get_vacancies
from config import config


class DBManager:
    par = config()

    def __init__(self):
        con = psycopg2.connect(dbname='postgres', **self.par)
        con.autocommit = True
        cur = con.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS hhparser")
        cur.execute(f"CREATE DATABASE hhparser")
        con.close()
        self.con = psycopg2.connect(dbname='hhparser', **self.par)

    def create_tables(self):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS employees(
                        employer_id VARCHAR PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        description TEXT,
                        area TEXT,
                        vacancies_url TEXT)""")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies(
                        vacancy_id VARCHAR PRIMARY KEY,
                        employer_id VARCHAR REFERENCES employees(employer_id),
                        name VARCHAR NOT NULL,
                        alternate_url VARCHAR,
                        area VARCHAR,
                        salary_from INT,
                        salary_to INT,
                        requirement TEXT,
                        responsibility TEXT,                    
                        published_at TIMESTAMP)""")

    def fill_vacancies(self):
        with self.con as con:
            with con.cursor() as cur:
                data_vacancies = get_vacancies()
                for employer in data_vacancies:
                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                ([emp for emp in employer]))

    def fill_employees(self):
        with self.con as con:
            with con.cursor() as cur:
                data_employees = get_employer()
                for employer in data_employees:
                    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s)",
                                ([emp for emp in employer]))

    def get_count_employees_vacancies(self):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT employees.name AS company, count(vacancies.*) AS vacancy_count
                FROM vacancies join employees using (employer_id)
                GROUP BY employees.name""")
                result = cur.fetchall()
                for item in result:
                    print(item)

    def get_all_vacancies(self):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT employees.name, vacancies.name, salary_from, salary_to, alternate_url FROM employees, vacancies
                ORDER BY salary_from, employees.name""")
                result = cur.fetchall()
                for item in result:
                    print(item)

    def get_avg_salary(self):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute("""SELECT AVG (salary_from) as avg_salary FROM vacancies""")
                result = cur.fetchone()
                print(result)

    def get_vacancies_with_higher_salary(self):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT employees.name, vacancies.name, salary_from, salary_to, alternate_url FROM vacancies, employees
                WHERE salary_from > (SELECT AVG (salary_from) FROM vacancies)
                ORDER BY salary_from""")
                result = cur.fetchall()
                for item in result:
                    print(item)

    def get_vacancies_with_keyword(self, keyword):
        with self.con as con:
            with con.cursor() as cur:
                cur.execute(f"""
                SELECT employees.name, vacancies.name, salary_from, salary_to, alternate_url FROM vacancies, employees
                WHERE vacancies.name LIKE '%{keyword[1:]}%'""")
                result = cur.fetchall()
                for item in result:
                    print(item)
