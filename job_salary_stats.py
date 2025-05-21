from datetime import date, timedelta
from tabulate import tabulate
from dotenv import load_dotenv
import requests
import os


HH_MOSCOW_AREA_ID = 1
SJ_MOSCOW_TOWN_ID = 4


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def get_hh_stats(language):
    url = 'https://api.hh.ru/vacancies'
    all_vacancies = []
    page = 0
    pages_number = 1
    total_vacancies = 0

    while page < pages_number:
        params = {
            'text': f'Программист {language}',
            'area': HH_MOSCOW_AREA_ID,
            'date_from': date.today() - timedelta(days=30),
            'page': page,
            'per_page': 100
        }
        response = requests.get(url, params=params)
        programmer_vacancies_hh = response.json()

        if page == 0:
            total_vacancies = programmer_vacancies_hh.get('found', 0)

        all_vacancies.extend(programmer_vacancies_hh['items'])
        pages_number = programmer_vacancies_hh['pages']
        page += 1

    salaries = []
    for vacancy in all_vacancies:
        salary = vacancy.get('salary')
        if salary and salary['currency'] == 'RUR':
            predicted = predict_salary(salary.get('from'), salary.get('to'))
            if predicted:
                salaries.append(predicted)

    return {
        'vacancies_found': total_vacancies,
        'vacancies_processed': len(salaries),
        'average_salary': int(sum(salaries) / len(salaries)) if salaries else 0
    }


def get_sj_stats(language, token):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {"X-Api-App-Id": token}
    all_vacancies = []
    page = 0
    more = True
    total_vacancies = 0

    while more:
        params = {
            'keyword': f'Программист {language}',
            'town': SJ_MOSCOW_TOWN_ID,
            'count': 100,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)
        programmer_vacancies_superjob = response.json()

        if page == 0:
            total_vacancies = programmer_vacancies_superjob.get('total', 0)

        all_vacancies.extend(programmer_vacancies_superjob['objects'])
        more = programmer_vacancies_superjob.get('more', False)
        page += 1

    salaries = []
    for vacancy in all_vacancies:
        if vacancy.get("currency") == "rub":
            predicted = predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
            if predicted:
                salaries.append(predicted)

    return {
        'vacancies_found': total_vacancies,
        'vacancies_processed': len(salaries),
        'average_salary': int(sum(salaries) / len(salaries)) if salaries else 0
    }


def print_table(title, stats):
    table = [[lang, data['vacancies_found'], data['vacancies_processed'], data['average_salary']]
             for lang, data in stats.items()]
    headers = ['Язык программирования', 'Найдено вакансий', 'Обработано', 'Средняя зарплата']
    print(f'\n{title}')
    print(tabulate(table, headers=headers, tablefmt='grid'))


def main():
    load_dotenv()
    superjob_access_token = os.environ['SUPERJOB_TOKEN']

    languages = ["Python", "Java", "JavaScript", "C", "C++", "C#", "Ruby", "Go", "1С"]
    hh_stats = {lang: get_hh_stats(lang) for lang in languages}
    sj_stats = {lang: get_sj_stats(lang, superjob_access_token) for lang in languages}

    print_table('HeadHunter Moscow', hh_stats)
    print_table('SuperJob Moscow', sj_stats)


if __name__ == '__main__':
    main()
