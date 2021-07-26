from __main__ import db, ma
from components.BookDetails import Book

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
    
    def addBookToShoppingCart(self, ISBN):
        self.Books = self.Books + ISBN
        return "Book " + Book.query.get(int(ISBN)).Name + " has been added"

    def deleteBookFromShoppingCart(self, ISBN):
        newListAfterDeletion = ""
        for book in self.Books:
            if book != ISBN:
                newListAfterDeletion = newListAfterDeletion + book
        if newListAfterDeletion == self.Books:
            return "Book to be deleted was not found in shopping cart"
        else:
            self.Books = newListAfterDeletion
            return "Book " + Book.query.get(int(ISBN)).Name + " has been deleted"

