# Base imports
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exists

# Flask app
app = Flask(__name__)
DBPATH = "sqlite:///" + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "db.sqlite"
)

# Set database
app.config["SQLALCHEMY_DATABASE_URI"] = DBPATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Init db
db = SQLAlchemy(app)

# # Init Marshmallow
ma = Marshmallow(app)

# Component imports
"""
We are going to keep classes in separate files. This way it will be easier to
maintain and integrate new features. Please be sure to name classes uniquely.
"""
from components.BookDetails import *  # noqa:402


@app.route("/books", methods=["POST"])
def addBook():
    # Fetch the POST request's fields
    Name = request.json["Name"]
    Description = request.json["Description"]
    Price = request.json["Price"]
    Author = request.json["Author"]
    Genre = request.json["Genre"]
    Pub = request.json["Publisher"]
    Year = request.json["YearPublished"]
    Sold = request.json["Sold"]

    # Check if the book exists in the DB
    duplicate = db.session.query(exists().where(Book.Name == Name)).scalar()

    if duplicate:
        return jsonify("Book name is already in the database")

    # Create new book with fetched fields
    new_book = Book(Name, Description, Price, Author, Genre, Pub, Year, Sold)

    # Only add book if it's unique
    db.session.add(new_book)
    db.session.commit()

    # Return new_book as json
    return new_book.product_schema.jsonify(new_book)


@app.route("/books", methods=["GET"])
def getBooks():
    # Query
    all_books = Book.query.all()

    result = Book.products_schema.dump(all_books)

    # Returns all the DB items as json
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
