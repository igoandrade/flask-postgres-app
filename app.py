from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
app.config['SECRET_KEY'] = "sakjdfhsjfjsfdjfhjnffnfhiue"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/cars_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap4(app)

from models import *

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars', methods=['POST', 'GET'])
def get_cars():
    cars = CarsModel.query.order_by(CarsModel.id).all()
    return render_template('cars.html', cars=cars)


@app.route('/cars/new', methods=['POST'])
def insert_car():
    name = request.form.get('name')
    model = request.form.get('model')
    doors = int(request.form.get('doors'))
    car = CarsModel(name=name, model=model, doors=doors)
    db.session.add(car)
    db.session.commit()
    flash("success#Data entered successfully!!")
    return redirect(url_for('get_cars'))

@app.route('/cars/update/car/<int:car_id>', methods=['POST'])
def update_car(car_id):
    name = request.form.get('name')
    model = request.form.get('model')
    doors = int(request.form.get('doors'))
    car = CarsModel.query.filter_by(id=car_id).first()
    car.name = name
    car.model=model
    car.doors = doors
    db.session.commit()
    flash("success#Data updated successfully!!")
    return redirect(url_for('get_cars'))

@app.route('/cars/delete/car/<int:car_id>')
def delete_car(car_id):
    car = CarsModel.query.filter_by(id=car_id).first()
    db.session.delete(car)
    db.session.commit()
    flash("success#Data deleted successfully!!")
    return redirect(url_for('get_cars'))


"""
@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method=='POST':
        if request.is_jason:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method=='GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]

    return {"count": len(results), "cars": results}
"""



if __name__=="__main__":
    app.run(debug=True)