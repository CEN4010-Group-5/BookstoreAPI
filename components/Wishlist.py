class Wishlist(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("Title")

    # Create DB fields
    Title = db.Column(db.String(300), primary_key=True)
    Books = db.Column(db.String())

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Title):
        self.Title = Title

class Wishbooks(db.Model):
    """This class represents a book author"""

    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("bookName")

    # Create DB fields
    
    bookName = db.Column(db.String(300), unique=True)

    product_schema= ProductSchema()
    products_schema= ProductSchema(many = True)

    def __init__(self, bookName):
        self.bookName = bookName
    
