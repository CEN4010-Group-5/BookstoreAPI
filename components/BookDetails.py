from __main__ import db, ma, app


# Template class: [4] Book Details
class Book(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "ISBN",
                "Name",
                "Description",
                "Price",
                "Author",
                "Genre",
                "Publisher",
                "YearPublished",
                "Sold",
                "Rating",
            )

    # Create DB fields
    ISBN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(300), unique=True)
    Description = db.Column(db.String(2000))
    Price = db.Column(db.Float)
    Author = db.Column(db.String(300))
    Genre = db.Column(db.String(300))
    Publisher = db.Column(db.String(300))
    YearPublished = db.Column(db.Integer)
    Sold = db.Column(db.Integer)
    Rating = db.Column(db.Integer)

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, ISBN, Name, Desc, Price, Auth, Genre, Pub, Year, Sold, Rating):  # noqa
        self.ISBN = ISBN
        self.Name = Name
        self.Description = Desc
        self.Price = Price
        self.Author = Auth
        self.Genre = Genre
        self.Publisher = Pub
        self.YearPublished = Year
        self.Sold = Sold
        self.Rating = Rating
