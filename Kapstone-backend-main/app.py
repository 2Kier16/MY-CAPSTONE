from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os


app = Flask(__name__)

basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite') 


db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String, nullable=False)
    zodiac = db.Column(db.String, nullable=False)
    book = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


    def __init__(self, interest, zodiac, book, author, description):
        self.interest = interest
        self.zodiac = zodiac
        self.book = book
        self.author = author
        self.description = description


class InterestSchema(ma.Schema):
    class Meta:
        fields = ("id",'interest', 'zodiac', 'book', 'author', 'description')    

interest_schema = InterestSchema()
interests_schema = InterestSchema(many=True)

@app.route("/interest/add", methods=['POST'])
def add_interests():
    interest = request.json.get("interest")
    zodiac = request.json.get("zodiac")
    book = request.json.get("book")
    author = request.json.get("author")
    description = request.json.get("description")

    record = Interests(interest, zodiac, book, author, description)
    db.session.add(record)
    db.session.commit()

    return jsonify(interest_schema.dump(record))


@app.route("/interests", methods=["Get"])
def get_all_interests():
    all_interests = Interests.query.all()
    return jsonify(interests_schema.dump(all_interests))


if __name__ == "__main__":
    app.run(debug=True)