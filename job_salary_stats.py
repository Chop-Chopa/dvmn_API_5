from datetime import date, timedelta
from tabulate import tabulate
from dotenv import load_dotenv
import requests
import os

API_KEY = "v3.r.139060648.79c692061429e4acb3e97efd8bfb273e1842fb26.1e5a827ffec98cdaedf92bed77d9d9802b2591fa"

def get_hh_stats(language):
    url = 'https://api.hh.ru/vacancies'
    all_vacancies = []
    page = 0
    pages_number = 1

    while page < pages_number:
        params = {
            'text': f'Программист {language}',
            'area': 1,
            'date_from': date.today() - timedelta(days=30),
            'page': page,
            'per_page': 100
        }
        response = requests.get(url, params=params)
        data = response.json()
        all_vacancies.extend(data['items'])
        pages_number = data['pages']
        page += 1

    salaries = []
    for vacancy in all_vacancies:
        salary = vacancy.get('salary')
        if salary and salary['currency'] == 'RUR':
            if salary.get('from') and salary.get('to'):
                avg = (salary['from'] + salary['to']) / 2
            elif salary.get('from'):
                avg = salary['from'] * 1.2
            elif salary.get('to'):
                avg = salary['to'] * 0.8
            else:
                continue
            salaries.append(avg)

    return {
        'vacancies_found': len(all_vacancies),
        'vacancies_processed': len(salaries),
        'average_salary': int(sum(salaries) / len(salaries)) if salaries else 0
    }

def get_sj_stats(language, token):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {"X-Api-App-Id": token}
    all_vacancies = []
    page = 0
    more = True

    while more:
        params = {
            'keyword': f'Программист {language}',
            'town': 4,
            'count': 100,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_vacancies.extend(data['objects'])
        more = data.get('more', False)
        page += 1

    salaries = []
    for vacancy in all_vacancies:
        if vacancy.get("currency") == "rub":
            frm = vacancy.get('payment_from')
            to = vacancy.get('payment_to')
            if frm and to:
                avg = (frm + to) / 2
            elif frm:
                avg = frm * 1.2
            elif to:
                avg = to * 0.8
            else:
                continue
            salaries.append(avg)

    return {
        'vacancies_found': len(all_vacancies),
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
    sj_stats = {lang: get_sj_stats(lang,superjob_access_token) for lang in languages}

    print_table('HeadHunter Moscow', hh_stats)
    print_table('SuperJob Moscow', sj_stats)

if __name__ == '__main__':
    main()
