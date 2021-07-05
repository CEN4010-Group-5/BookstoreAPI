
from __main__ import db, ma, app


class Profile(db.Model):
    """This class represents a book author"""

    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "id",
                "UserName",
                "Password",
                "Name",
                "HomeAddress",
                "CreditCards"
            )

    # Create DB fields
    id = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(300), unique = True)
    Password = db.Column(db.String(300))
    Name = db.Column(db.String(1000))
    HomeAddress = db.Column(db.String(300))
    cards = db.relationship('CreditCards', backref = 'owner')


    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, UserName, Password, Name, HomeAddress):
        self.UserName = UserName
        self.Password = Password
        self.Name = Name
        self.HomeAddress = HomeAddress

class CreditCards(db.Model):
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "cardNumber",
                "expirationDate",
                "cvs",
                "ownerId"
            )

    
    cardNumber = db.Column(db.String(300), primary_key = True)
    expirationDate = db.Column(db.String(10))
    cvs = db.Column(db.String(5))
    ownerId = db.Column(db.String(300), db.ForeignKey('profile.UserName'))

    def __init__(self, cardNumber, expirationDate, cvs):
        self.cardNumber = cardNumber
        self.expirationDate = expirationDate
        self.cvs = cvs

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)