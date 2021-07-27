import datetime
import re
from sqlalchemy import func
from flask import Flask, request, jsonify
from sqlalchemy import exists
from components.BookDetails import Book
from components.Author import Author
from components.Wishlist import Wishlist
from components.Profile import Profile
from components.Profile import CreditCards
from components.Rate import Rate
from __main__ import db, app

"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.

It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""


@app.route("/books/rate", methods=['POST'])
def createBookRating():
    """Create a rating and comment on a book"""
    book_isbn = request.json["isbn"]
    rating = request.json['rating']
    comment = request.json['comment']
    username = request.json['username']
    user = Profile.query.filter_by(UserName=username).first()
    if user is None:
        return jsonify(None)
    curr_time = datetime.datetime.now()
    new_rating = Rate(book_isbn, username, rating, comment, curr_time)
    db.session.add(new_rating)
    db.session.commit()
    return new_rating.product_schema.jsonify(new_rating)


@app.route("/books/topRating", methods=["GET"])
def getBooksTopRating():
    """Returns a json with all books ordered by rating"""

    # Query
    top_rating_books = Rate.query.order_by(Rate.rating.desc())

    result = Rate.products_schema.dump(top_rating_books)

    # Returns X books in the DB as json
    return jsonify(result)


@app.route("/book/<ISBN>/averageRating", methods=["GET"])
def getAverageRating(ISBN):
    """Returns a average rating json with book given ISBN """

    # Query
    avg_rating_books = db.session.query(func.avg(Rate.rating)).filter_by(isbn=ISBN).first()

    # Returns X books in the DB as json
    return jsonify({"rating": avg_rating_books[0]})
