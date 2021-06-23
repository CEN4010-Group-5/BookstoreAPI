from flask import Flask, request, jsonify
from BookstoreAPI import db, ma
from sqlalchemy import exists
from BookstoreAPI import app


# Template class: [4] Book Details
class Book(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "ISBN",
                "Name",
                "Description",
                "Price",
                "Author",
                "Genre",
                "Publisher",
                "YearPublished",
                "Sold",
            )

    # Create DB fields
    ISBN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(300), unique=True)
    Description = db.Column(db.String(2000))
    Price = db.Column(db.Float)
    Author = db.Column(db.String(300))
    Genre = db.Column(db.String(300))
    Publisher = db.Column(db.String(300))
    YearPublished = db.Column(db.Integer)
    Sold = db.Column(db.Integer)

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Name, Desc, Price, Auth, Genre, Pub, Year, Sold):
        self.Name = Name
        self.Description = Desc
        self.Price = Price
        self.Author = Auth
        self.Genre = Genre
        self.Publisher = Pub
        self.YearPublished = Year
        self.Sold = Sold


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
