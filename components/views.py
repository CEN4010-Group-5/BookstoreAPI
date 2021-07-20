from flask import Flask, request, jsonify
from sqlalchemy import exists
from components.BookDetails import Book
from components.Author import Author
from components.Wishlist import Wishlist
from components.Profile import Profile
from components.Profile import CreditCards
from __main__ import db, app

"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.

It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""


# ******************** [4] Book Details ********************
@app.route("/admin/books", methods=["POST"])
def addBook():
    """Handles adding a book to the database"""
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


@app.route("/admin/books", methods=["GET"])
def getBooks():
    """Returns a json with all the books in the database"""
    # Query
    all_books = Book.query.all()

    result = Book.products_schema.dump(all_books)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/authors", methods=["GET"])
def getAuthors():
    """Returns a json with all the books in the database"""
    # Query
    all_authors = Author.query.all()

    result = Author.products_schema.dump(all_authors)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/admin/createAuthor", methods=["POST"])
def createAuthor():
    """Handles adding an author to the database"""
    # Fetch the POST request's fields
    FName = request.json["FirstName"]
    LName = request.json["LastName"]
    Biography = request.json["Biography"]
    Publisher = request.json["Publisher"]

    # Check if the book exists in the DB
    dupFName = db.session.query(exists().where(Author.FirstName == FName)).scalar()
    dupLName = db.session.query(exists().where(Author.LastName == LName)).scalar()

    if dupFName and dupLName:
        return jsonify("Author is already in the database.")

    # Create new book with fetched fields
    new_author = Author(FName, LName, Biography, Publisher)

    # Only add book if it's unique
    db.session.add(new_author)
    db.session.commit()

    # Return new_book as json
    return new_author.product_schema.jsonify(new_author)


@app.route("/books/<ISBN>", methods=["GET"])
def getBookByISBN(ISBN):
    """Returns the book requested by the specific ISBN route"""
    book = Book.query.get(ISBN)

    if book is None:
        return jsonify(None)

    return Book.product_schema.jsonify(book)


@app.route("/books/author/<AUTHOR>", methods=["GET"])
def getBooksByAuthor(AUTHOR):
    """Retrieve a list of books associated with an author"""
    # Get all books
    all_books = Book.query.all()

    # Append the book's name if its author was specified on the URL
    byAuthor = [book.Name for book in all_books if book.Author == AUTHOR]

    # Check that the author has books in the database. If no books are found
    # by the author, return a json message saying so, and suggest authors.
    all_authors = Author.products_schema.dump(Author.query.all())
    if len(byAuthor) == 0:
        return jsonify(
            "No books written by this author in the database.",
            "Here is a list of authors recorded: ",
            all_authors,
        )

    # Returns all the DB items as json
    return jsonify(byAuthor)


# ******************** [4] Book Details ********************

# ******************** [2] Profile Management ********************
@app.route("/profile/createUser", methods=["POST"])
def addUser():
    """Handles creating a user profile in the databse"""
    # Fetch the POST request's fields
    UserName = request.json["UserName"]
    Password = request.json["Password"]
    Name = request.json["Name"]
    HomeAddress = request.json["HomeAddress"]

    # Check if the username already exists in the DB
    duplicate = db.session.query(exists().where(Profile.UserName == UserName)).scalar()

    if duplicate:
        return jsonify("Username already in use")

    # Create new user with fetched fields
    new_user = Profile(UserName, Password, Name, HomeAddress)

    # Only add user if it's unique
    db.session.add(new_user)
    db.session.commit()

    # Return new_user as json
    return new_user.product_schema.jsonify(new_user)


@app.route("/profile/<userName>", methods=["GET"])
def getUserByUsername(userName):
    """Returns the searched user requested using the username"""
    user = Profile.query.filter_by(UserName=userName).first()

    if user is None:
        return jsonify(None)

    return Profile.product_schema.jsonify(user)


@app.route("/profile/<userName>", methods=["PUT"])
def updateUser(userName):
    """Update a user's information"""
    user = Profile.query.filter_by(UserName=userName).first()
    # Fetch the PUT request's fields

    Password = request.json["Password"]
    Name = request.json["Name"]
    HomeAddress = request.json["HomeAddress"]

    user.Password = Password
    user.Name = Name
    user.HomeAddress = HomeAddress

    db.session.commit()

    # Update user fields
    return user.product_schema.jsonify(user)


@app.route("/profile/<userName>/creditcards", methods=["POST"])
def addCards(userName):
    """Add credit cards by user"""
    someOwner = Profile.query.filter_by(UserName=userName).first()

    cardNumber = request.json["cardNumber"]
    expirationDate = request.json["expirationDate"]
    cvs = request.json["cvs"]

    newCard = CreditCards(cardNumber, expirationDate, cvs)
    newCard.ownerId = someOwner.id

    db.session.add(newCard)
    db.session.commit()

    return newCard.product_schema.jsonify(newCard)


# ******************** [2] Profile Management ********************


# ******************** [1] Book Browsing & Sorting *******************
@app.route("/books/genre/<GENRE>", methods=["GET"])
def getBooksByGenre(GENRE):
    """Handles getting books by genre from the database"""

    # Get books by genre from db
    books = Book.query.filter(Book.Genre == GENRE)

    # Return books by genre as json
    results = Book.products_schema.dump(books)
    return jsonify(results)


@app.route("/books/topSellers", methods=["GET"])
def getBooksByTopSellers():
    """Handles getting books by top sellers from the database"""

    # Get books by top sellers from db
    books = Book.query.order_by(Book.Sold.desc()).limit(10)

    # Return books by top sellers as json
    results = Book.products_schema.dump(books)
    return jsonify(results)


# ******* Relies on rating system to be implemented *****
# @app.route("/books/rating/<RATING>", methods=["GET"])
# def getBooksByRating(RATING):
#     """Handles getting books by a rating or higher from the database"""

#     # Get books by a specific rating or higher from db
#     books = Book.query.filter(Book.Rating >= RATING)

#     # Return books by a specific rating or higher as json
#     results = Book.products_schema.dump(books)
#     return jsonify(results)


@app.route("/books/limit/<LIMIT>", methods=["GET"])
def getBooksByLimit(LIMIT):
    """Returns a json with X books where X is an int in the database"""

    # Query
    all_books = Book.query.order_by(Book.Name.asc()).limit(LIMIT)

    result = Book.products_schema.dump(all_books)

    # Returns X books in the DB as json
    return jsonify(result)


# ******************** [1] Book Browsing & Sorting *******************

# ******************** [4] Wishlist ************************
@app.route("/wishList/createWishList", methods=["POST"])
def addWishlist():
    # Fetch the POST request's fields
    Title = request.json["Title"]
    Books = request.json["Books"]

    # Check if the wishlist title already exists
    duplicate = db.session.query(exists().where(Wishlist.Title == Title)).scalar()

    if duplicate:
        return jsonify("Wishlist tile already in use.")

    new_Wish = Wishlist(Title, Books)

    db.session.add(new_Wish)
    db.session.commit()

    return new_Wish.product_schema.jsonify(new_Wish)


# @app.route("/wishList/<title>", methods=["POST"])
# def addBook(title):
# """Handles adding a book to the wishlist."""
# # Fetch the POST request's fields
# Name = request.json["Name"]
# Description = request.json["Description"]
# Price = request.json["Price"]
# Author = request.json["Author"]
# Genre = request.json["Genre"]
# Pub = request.json["Publisher"]
# Year = request.json["YearPublished"]
# Sold = request.json["Sold"]

# someList = Wishlist.query.filter_by(Title=title).first()

# # Create new book with fetched fields
# new_book = Book(Name, Description, Price, Author, Genre, Pub, Year, Sold)
# new_book.ownerId = someList.id
# # Only add book if it's unique
# db.session.add(new_book)
# db.session.commit()

# # Return new_book as json
# return new_book.product_schema.jsonify(new_book)


@app.route("/wishList/<title>", methods=["GET"])
def getBookInList(title):
    """Returns the books requested from a wishlist."""
    wish = Wishlist.query.filter_by(Title=title).first()

    if wish is None:
        return jsonify(None)

    return Wishlist.product_schema.jsonify(wish)


# ******************** [4] Wishlist ************************

# ******************** [6] Shopping Cart *******************

@app.route("/admin/ShoppingCart", methods=["POST"])
def createShoppingCart():
    """Handles adding a shopping cart to the database"""
    # Fetch the POST request's fields
    User = request.json["User"]
    Books = request.json["Books"]


    # Check if the shopping cart exists in the DB
    duplicate = db.session.query(exists().where(ShoppingCart.User == User)).scalar()

    if duplicate:
        return jsonify("Shopping cart is already in the database")

    # Create new shopping cart with fetched fields
    new_shoppingcart = ShoppingCart(User, Books)

    # Only add shopping cart if it's unique
    db.session.add(new_shoppingcart)
    db.session.commit()

    # Return new_shoppingcart as json
    return new_shoppingcart.product_schema.jsonify(new_shoppingcart)

#@app.route("/admin/ShoppingCart/<User>", methods=["PUT"])
#def addBookToShoppingCart(book):

 #   duplicate = db.session.query(exists().where(ShoppingCart.Books == book)).scalar()

  #  if duplicate:
   #     return jsonify("Book already in shopping cart")
    ##   shoppingCart = ShoppingCart(User, book)
      ## db.commit()

        #return shoppingCart.product_schema.jsonify(shoppingCart)


