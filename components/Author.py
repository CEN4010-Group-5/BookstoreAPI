from __main__ import db, ma, app


class Author(db.Model):
    """This class represents a book author"""

    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "FirstName",
                "LastName",
                "Biography",
                "Publisher",
            )

    # Create DB fields
    FirstName = db.Column(db.Integer, unique=True, primary_key=True)
    LastName = db.Column(db.Integer, unique=True, primary_key=True)
    Biography = db.Column(db.String(1000))
    Publisher = db.Column(db.String(300))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, FirstName, LastName, Biography, Publisher):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Biography = Biography
        self.Publisher = Publisher
