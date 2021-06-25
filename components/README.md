# Common Workflow

Each feature will be its own module (file), Eg:
[BookDetails.py](https://github.com/lustered/BookstoreAPI/blob/master/components/BookDetails.py)
for the 4th feature. This will make working on each features easier to debug,
implement into the main app file
([BookstoreAPI.py](https://github.com/lustered/BookstoreAPI/blob/master/BookstoreAPI.py))
and organize each group member's work.

If any API routes with their functions need to be added, it can be done in the
[views.py](https://github.com/lustered/BookstoreAPI/blob/master/components/views.py)
file.

Once you have the feature class, import them to the
[views.py](https://github.com/lustered/BookstoreAPI/blob/master/components/views.py)
file and implement their functionality

    # views.py

    from components.BookDetails import Book

    @app.route("/books", methods=["GET"])
    def getBooks():
        """ Returns a json with all the books in the database """
        # Query
        all_books = Book.query.all()

        result = Book.products_schema.dump(all_books)

        # Returns all the DB items as json
        return jsonify(result)
