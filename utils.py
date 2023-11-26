from datetime import datetime

import requests

employees_id = [740, 2180, 3805, 4352, 23427, 78638, 1095544, 1122462, 2071925, 5385759]


def get_vacancies():
    data = []
    for employer_id in employees_id:
        params = {"only_with_salary": True,
                  "per_page": 100}
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}', params).json()['items']
        for item in response:
            vacancy_id = item['id']
            name = item['name']
            alternate_url = item['alternate_url']
            area = item['area']['name']
            salary_from = item['salary']['from']
            salary_to = item['salary']['to']
            requirement = item['snippet']['requirement']
            responsibility = item['snippet']['responsibility']
            published_at = item['published_at']
            data.append([vacancy_id, employer_id, name, alternate_url, area, salary_from,
                         salary_to, requirement, responsibility, published_at])
    return data


def get_employer():
    data = []
    for employer_id in employees_id:
        params = {"only_with_vacancies": True,
                  "per_page": 1}
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}', params).json()
        name = response['name']
        area = response['area']['name']
        description = response['description']
        vacancies_url = response['vacancies_url']
        bad_words = ['</strong>', '<strong>', '<p>', '</p>', '&laquo;', '&raquo;', '&nbsp;', '<em>', '</em>', '<br />',
                     '\xa0', '\r', '\n', '</u>', '<u>', '\ufeff', '</li>', '<li>', '&quot;', '<ul>', '</ul>']
        for word in bad_words:
            if word in description:
                description = description.replace(word, ' ')
        data.append([employer_id, name, description, area, vacancies_url])
    return data
