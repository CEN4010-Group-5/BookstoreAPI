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

@app.route("/admin/ShoppingCart/id", methods=["PUT"])
def addBookToShoppingCart(book):

    # check if book is already in shopping cart
    duplicate = db.session.query(exists().where(ShoppingCart.Books == book)).scalar()

    if duplicate:
        return jsonify("Book is already in shopping cart")
