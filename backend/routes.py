from flask import request, render_template, redirect, url_for, flash
import requests
from models import db, Vacancy, VacancyData

def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            reset_database()
            filters = get_filters_from_request()
            vacancies = fetch_vacancies_from_api()
            filtered_vacancies = filter_vacancies(vacancies, filters)
            
            if filtered_vacancies:
                save_vacancies_to_db(filtered_vacancies)
                return redirect(url_for('results'))
            else:
                flash('Ничего не найдено')
        
        return render_template('index.html')

    @app.route('/allvacancies')
    def results():
        vacancies = get_all_vacancies_from_db()
        return render_template('vacancies.html', vacancies=vacancies)

    def reset_database():
        db.drop_all()
        db.create_all()

    def get_filters_from_request():
        return {
            'vacancy': request.form.get('vacancy', '').lower(),
            'experience': request.form.get('experience', '').lower(),
            'employment': request.form.get('employment', '').lower()
        }

    def fetch_vacancies_from_api():
        response = requests.get('https://api.hh.ru/vacancies')
        if response.status_code == 200:
            return response.json()['items']
        return []

    def filter_vacancies(vacancies, filters):
        filtered_vacancies = []
        for vacancy in vacancies:
            name = vacancy['name']
            experience = vacancy['experience']['name']
            employment = vacancy['employment']['name']
            area = vacancy['area']['name']

            if (filters['vacancy'] in name.lower() and 
                filters['experience'] in experience.lower() and 
                filters['employment'] in employment.lower()):
                filtered_vacancies.append({
                    'name': name,
                    'experience': experience,
                    'employment': employment,
                    'area': area
                })
        return filtered_vacancies

    def save_vacancies_to_db(vacancies):
        for vacancy in vacancies:
            new_vacancy = Vacancy(name=vacancy['name'])
            db.session.add(new_vacancy)
            db.session.commit()

            new_vacancy_data = VacancyData(
                vacancy_id=new_vacancy.id,
                experience=vacancy['experience'],
                employment=vacancy['employment'],
                area=vacancy['area']
            )
            db.session.add(new_vacancy_data)
            db.session.commit()

    def get_all_vacancies_from_db():
        vacancies = Vacancy.query.join(VacancyData).all()
        return [{
            'name': vacancy.name,
            'experience': vacancy.vacancy_data.experience,
            'employment': vacancy.vacancy_data.employment,
            'area': vacancy.vacancy_data.area
        } for vacancy in vacancies]