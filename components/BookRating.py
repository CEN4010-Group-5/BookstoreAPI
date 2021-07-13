from __main__ import db, ma, app


# product Class/model
class Rating(db.Model):

    # Product Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ('id', 'name', 'rate', 'comment', 'book')

    # Init schema
    product_schema = productSchema(strict=True)

    products_schema = productSchema(many=True, strict=True)

    id= db.Column(db.Integer,primary_key=True)
    book= db.Column(db.String)
    name = db.Column(db.String)
    rate = db.Column(db.Integer)
    comment = db.Column(db.String)
    def __init__(self,book,name, rate, comment):

        self.book = book
        self.name = name
        self.rate = rate
        self.comment = comment










