from flask import Flask, request, render_template
import requests

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

@app.route('/', methods=['GET', 'POST'])
def index():
    vacancies = None
    if request.method == 'POST':
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
                    filtered_vacancies.append({
                        'name': name,
                        'experience': experience,
                        'employment': employment,
                        'area': area
                    })
            vacancies = filtered_vacancies
    
    return render_template('index.html', vacancies=vacancies)

if __name__ == '__main__':
    app.run(debug=True)