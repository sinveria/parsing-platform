from flask import request, render_template, redirect, url_for, flash
import requests
from models import db, Vacancy, VacancyData

def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            db.drop_all()
            db.create_all()

            vacancy_filter = request.form.get('vacancy', '').lower()
            experience_filter = request.form.get('experience', '').lower()
            employment_filter = request.form.get('employment', '').lower()

            response = requests.get('https://api.hh.ru/vacancies')
            if response.status_code == 200:
                all_vacancies = response.json()['items']
                filtered_vacancies = []
                for vacancy in all_vacancies:
                    name = vacancy['name']
                    experience = vacancy['experience']['name']
                    employment = vacancy['employment']['name']
                    area = vacancy['area']['name']

                    if (vacancy_filter in name.lower() and 
                        experience_filter in experience.lower() and 
                        employment_filter in employment.lower()):
                        new_vacancy = Vacancy(name=name)
                        db.session.add(new_vacancy)
                        db.session.commit()

                        new_vacancy_data = VacancyData(
                            vacancy_id=new_vacancy.id,
                            experience=experience,
                            employment=employment,
                            area=area
                        )
                        db.session.add(new_vacancy_data)
                        db.session.commit()

                        filtered_vacancies.append({
                            'name': name,
                            'experience': experience,
                            'employment': employment,
                            'area': area
                        })
                
                if filtered_vacancies:
                    return redirect(url_for('results'))
                else:
                    flash('Ничего не найдено')
                    return render_template('index.html')
        return render_template('index.html')

    @app.route('/allvacancies')
    def results():
        vacancies = Vacancy.query.join(VacancyData).all()
        results_data = [{
            'name': vacancy.name,
            'experience': vacancy.vacancy_data.experience,
            'employment': vacancy.vacancy_data.employment,
            'area': vacancy.vacancy_data.area
        } for vacancy in vacancies]
        return render_template('vacancies.html', vacancies=results_data)