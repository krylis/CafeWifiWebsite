from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'

db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String)
    coffee_price = db.Column(db.String)


@app.route('/show_cafe/<int:cafe_id>')
def show_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    return render_template('cafe.html', cafe=cafe)


@app.route('/')
def index():
    cafes = Cafe.query.order_by(Cafe.name)
    return render_template('index.html', cafes=cafes)


if __name__ == '__main__':
    app.run(debug=True)
