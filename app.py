from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/add_cafe', methods=["POST", "GET"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe()
        new_cafe.name = request.form['name']
        new_cafe.map_url = request.form['map']
        new_cafe.seats = request.form['seats']
        new_cafe.img_url = request.form['img']
        new_cafe.location = request.form['location']
        new_cafe.coffee_price = request.form['coffee']

        if request.form.get('sockets'):
            new_cafe.has_sockets = True
        else:
            new_cafe.has_sockets = False

        if request.form.get('wifi'):
            new_cafe.has_wifi = True
        else:
            new_cafe.has_wifi = False

        if request.form.get('calls'):
            new_cafe.can_take_calls = True
        else:
            new_cafe.can_take_calls = False

        if request.form.get('toilets'):
            new_cafe.has_toilet = True
        else:
            new_cafe.has_toilet = False

        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    try:
        db.session.delete(cafe)
        db.session.commit()
    except:
        return "There was a problem deleting this cafe."

    return render_template('delete.html', cafe=cafe)


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
