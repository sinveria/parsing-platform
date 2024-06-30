from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__, template_folder='/app/frontend', static_folder='/app/frontend')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:hisamo3485043@127.0.0.1:3306/platform?charset=utf8mb4')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

class Vacancy(db.Model):
    __tablename__ = 'vacancies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)

class VacancyData(db.Model):
    __tablename__ = 'vacancies_data'
    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancies.id'), nullable=False)
    experience = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    employment = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    area = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)

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
    vacancies = Vacancy.query.all()
    results_data = []
    for vacancy in vacancies:
        vacancy_data = VacancyData.query.filter_by(vacancy_id=vacancy.id).first()
        results_data.append({
            'name': vacancy.name,
            'experience': vacancy_data.experience,
            'employment': vacancy_data.employment,
            'area': vacancy_data.area
        })
    return render_template('vacancies.html', vacancies=results_data)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)