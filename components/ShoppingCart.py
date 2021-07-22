from BookstoreAPI import db, ma


class ShoppingCart(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "User",
                "Books",
            )

    # Create DB fields
    User = db.Column(db.String(300), primary_key=True)
    Books = db.Column(db.String(300))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, User, Books):
        self.User = User
        self.Books = Books
