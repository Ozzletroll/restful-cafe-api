from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from sqlalchemy.sql.expression import func
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # Convert Cafe object into dictionary, ready to be jsonified.
    def convert_to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


# Get a random café from the database
@app.route("/random", methods=["GET", "POST"])
def random_cafe():
    if request.method == "GET":
        cafes = db.session.query(Cafe).all()
        cafe_choice = random.choice(cafes)

        return jsonify(cafe=cafe_choice.convert_to_dict())

        # This code is only if we need to have absolute control over the json response.

        # return jsonify(cafe={"name": cafe_choice.name,
        #                      "map_url": cafe_choice.map_url,
        #                      "img_url": cafe_choice.img_url,
        #                      "location": cafe_choice.location,
        #                      "has_sockets": cafe_choice.has_sockets,
        #                      "has_toilets": cafe_choice.has_toilet,
        #                      "has_wifi": cafe_choice.has_wifi,
        #                      "can_take_calls": cafe_choice.can_take_calls,
        #                      "seats": cafe_choice.seats,
        #                      "coffee_price": cafe_choice.coffee_price
        #                      })



    pass


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
