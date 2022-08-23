from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = "sakjdfhsjfjsfdjfhjnffnfhiue"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *

@app.route('/')
def index():
    return {"Hello": "World!"}

if __name__=="__main__":
    app.run(debug=True)