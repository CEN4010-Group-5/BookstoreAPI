from __main__ import db, ma, app
from components.BookDetails import Book


class Wishlist(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("Title", "Books")

    # Create DB fields
    Title = db.Column(db.String(300), primary_key=True)
    Books = db.Column(db.String(300))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, Title, Books):
        self.Title = Title
        self.Books = Books

    def addBookToWish(self, ISBN):
        self.Books = self.Books + ISBN
        return "Book " + Book.query.get(int(ISBN)).Name + " has been added"

    def addWishBookToShoppingCart(self, ISBN):
        self.Books = self.Books + ISBN
        return Book.query.get(int(ISBN)).Name + "was added"

    def removeBookInList(self, ISBN):
        newList = ""
        for book in self.Books:
            if book != ISBN:
                newList = newList + book
        if newList == self.Books:
            return "Book was not found"
        else:
            self.Books = newList
            return Book.query.get(int(ISBN)).Name + " has been deleted"
