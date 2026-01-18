import requests
from itertools import count
import time
from environs import env
from terminaltables import AsciiTable


def get_response_hhru(prog_language, page):
    hh_url = 'https://api.hh.ru/vacancies/'
    mosсow_id = 1
    professional_role_id = 96
    period_in_days = 30
    payload = {
        'text': prog_language,
        'professional_role': professional_role_id,
        'area': mosсow_id,
        'period': period_in_days,
        'page': page,
    }

    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    return response.json()


def get_response_superjob(prog_language, secret_key, sj_token, page):
    city = 'Москва'
    headers = {
        'X-Api-App-Id': secret_key,
        'Authorization': f'Bearer {sj_token}'
    }
    url_superjob = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'page': page,
        'town': city,
        'keyword': prog_language,
    }
    response = requests.get(url_superjob, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_statistics_hhru(popular_languages):
    vacancies_stats = {}
    for prog_language in popular_languages:
        all_salaries = []
        for page in count(start=0):
            time.sleep(0.5)
            full_response = get_response_hhru(prog_language, page)
            total_vacancies = full_response['found']
            pages = full_response['pages']
            for vacancy in full_response['items']:
                salary = predict_rub_salary_for_hh(vacancy['salary'])
                if salary:
                    all_salaries.append(salary)
            if page >= pages - 1:
                break
        avg_salary = sum(all_salaries) / len(all_salaries) if all_salaries else 0
        vacancies_stats[prog_language] = {
            'Вакансий найдено': total_vacancies,
            'Вакансий обработано': len(all_salaries),
            'Средняя зарплата': int(avg_salary),
        }
    return vacancies_stats


def get_statistics_sj(popular_languages, secret_key, sj_token):
    vacancies_stats = {}
    for prog_language in popular_languages:
        all_salaries = []
        for page in count(start=0):
            time.sleep(0.2)
            full_response = get_response_superjob(prog_language, secret_key, sj_token, page)
            if not page:
                total_vacancies = full_response['total']
            for vacancy in full_response['objects']:
                salary = predict_rub_salary_for_superjob(vacancy)
                if salary:
                    all_salaries.append(salary)
            if not full_response['more']:
                break
        avg_salary = sum(all_salaries) / len(all_salaries) if all_salaries else 0
        vacancies_stats[prog_language] = {
            'Вакансий найдено': total_vacancies,
            'Вакансий обработано': len(all_salaries),
            'Средняя зарплата': int(avg_salary),
        }
    return vacancies_stats


def predict_rub_salary_for_hh(salary):
    if not salary:
        return None
    salary_from = salary['from']
    salary_to = salary['to']
    return calculate_average_salary(salary_from, salary_to)


def predict_rub_salary_for_superjob(salary):
    if not salary or salary['currency'] != 'rub':
        return None
    salary_from = salary['payment_from']
    salary_to = salary['payment_to']
    return calculate_average_salary(salary_from, salary_to)


def calculate_average_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)
    return None


def create_table_with_vacancies(vacancy_statistics, title):
    first_statistic = next(iter(vacancy_statistics.values()))
    headers = ['Язык программирования'] + list(first_statistic.keys())
    rows = [[lang] + list(stats.values()) for lang, stats in vacancy_statistics.items()]
    table = AsciiTable([headers] + rows, title)
    return table.table


def main():
    env.read_env()
    secret_key = env.str('SJ_SECRET_KEY')
    sj_token = env.str('SJ_ACCESS_TOKEN')
    if not secret_key or not sj_token:
        raise ValueError("Не задан SECRET_KEY или ACCESS_TOKEN")
    title_hhru = 'HeadHunter Moscow'
    title_sj = 'SuperJob Moscow'
    popular_languages = [
        'Python',
        'Javascript',
        '1c',
        'ruby',
        'C',
        'C#',
        'C++',
        'PHP'
    ]

    statistics_sj = get_statistics_sj(popular_languages, secret_key, sj_token)
    statistics_hhru = get_statistics_hhru(popular_languages)

    print(create_table_with_vacancies(statistics_sj, title_sj))
    print(create_table_with_vacancies(statistics_hhru, title_hhru))


if __name__ == '__main__':

    main()
