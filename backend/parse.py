from flask import Flask
from backend.config import Config
from backend.models import db
from backend.routes import init_routes

app = Flask(__name__, template_folder='/app/frontend', static_folder='/app/frontend')
app.config.from_object(Config)
db.init_app(app)

init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)