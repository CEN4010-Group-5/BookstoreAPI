from __main__ import db, ma, app


class Wishlist(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("Title")

    # Create DB fields
    Title = db.Column(db.String(300), primary_key=True)
    
    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Title):
        self.Title = Title
        

class WishBooks(db.Model):
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("Books", "listId")

    Books = db.Column(db.String(300), unique=True)
    listId =db.Column(db.String(300), db.ForeignKey("wishList.Title"))

    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Books):
        self.Books = Books
        
