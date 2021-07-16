from __main__ import db, ma, app


class wishList(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("Title", "Books")

    # Create DB fields
    Title = db.Column(db.String(300), primary_key=True)
    Books = db.Column(db.String())

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Title, Books):
        self.Title = Title
        self.Books = Books