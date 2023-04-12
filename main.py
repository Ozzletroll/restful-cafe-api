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


@app.route("/all", methods=["GET", "POST"])
def all_cafes():
    if request.method == "GET":
        cafes = db.session.query(Cafe).all()
        cafe_list = []
        for cafe in cafes:
            cafe_list.append(cafe.convert_to_dict())
        return jsonify(all_cafes=cafe_list)

    pass


# This route searches the database for all cafes that match the given location parameters.
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        search_params = request.args.get("location").title()
        cafe_search = db.session.query(Cafe).filter_by(location=search_params).all()
        if len(cafe_search) > 0:
            return jsonify(search_results=[cafe.convert_to_dict() for cafe in cafe_search])
        else:
            return jsonify(error={"Not found": "There are no cafes at this location."})
        pass

    pass


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":

        cafe_to_add = Cafe(name=request.args.get("name"),
                           map_url=request.args.get("map_url"),
                           img_url=request.args.get("img_url"),
                           location=request.args.get("location"),
                           seats=request.args.get("seats"),
                           has_toilet=request.args.get("has_toilet"),
                           has_sockets=request.args.get("sockets"),
                           can_take_calls=request.args.get("can_take_calls"),
                           coffee_price=request.args.get("coffee_price"),
                           )

        # db.session.add(cafe_to_add)
        # db.session.commit()
        return jsonify(response={"success": "Successfully added cafe to database."})

    pass


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_coffee_price = request.args.get("new_price")

    cafe_to_update = db.session.get(Cafe, cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_coffee_price
        db.session.commit()
    else:
        return jsonify(response={"failure": "No cafe matching that id found."})

    return jsonify(response={"success": "Successfully updated cafe price."})

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
