from __main__ import db, ma, app


@app.route("/wishList/createWishList", methods=["POST"])
def addWishlist():
    # Fetch the POST request's fields
    Title = request.json["Title"]

    # Check if the wishlist title already exists
    duplicate = db.session.query(exists().where(wishList.Title == Title)).scalar()

    if duplicate: 
        return jsonify("Wishlist tile already in use.")

    new_Wish = wishList(Title)
    
    db.session.add(new_Wish)
    db.session.commit()

    return new_Wish.product_schema.jsonify(new_Wish)

@app.route("/wishList/<title>", methods=["POST"])
def addBook(title):
    """Handles adding a book to the wishlist."""
    # Fetch the POST request's fields
    Name = request.json["Name"]
    Description = request.json["Description"]
    Price = request.json["Price"]
    Author = request.json["Author"]
    Genre = request.json["Genre"]
    Pub = request.json["Publisher"]
    Year = request.json["YearPublished"]
    Sold = request.json["Sold"]

    someList = wishList.query.filter_by(Title=title).first()


   
    # Create new book with fetched fields
    new_book = Book(Name, Description, Price, Author, Genre, Pub, Year, Sold)
    new_book.ownerId = someList.id
    # Only add book if it's unique
    db.session.add(new_book)
    db.session.commit()

    # Return new_book as json
    return new_book.product_schema.jsonify(new_book)    

@app.route("/wishList/<title>", methods=["GET"])
def getBookInList(title):
    """Returns the books requested from a wishlist."""
    wish = wishList.query.filter_by(Title=title).first()


    if wish is None:
        return jsonify(None)

    return wishList.product_schema.jsonify(wish)