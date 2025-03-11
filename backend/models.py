from app import db

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