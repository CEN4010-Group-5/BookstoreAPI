import requests
import json
from time import sleep


def addBookRequest(name, desc, price, author, genre, pub, year, sold):
    """Send post request to url with a json"""
    # Name must be unique for every entry. If not, it might return error 500

    # Route
    url = "http://localhost:5050/admin/books"

    data = {
        "Name": name,
        "Description": desc,
        "Price": price,
        "Author": author,
        "Genre": genre,
        "Publisher": pub,
        "YearPublished": year,
        "Sold": sold,
    }

    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    # Send POST request
    DATA_R = requests.post(url, data=json.dumps(data), headers=headers)

    print(DATA_R.status_code)
    print(DATA_R.json())


def getAllBooks():
    """Returns a json with all the books in the DB"""
    url = "http://localhost:5050/admin/books"
    return requests.get(url).json()


def getAllAuthors():
    """Returns a json with all the authors in the DB"""
    url = "http://localhost:5050/authors"
    return requests.get(url).json()


def getBookByISBN(ISBN):
    """Return a json of the book using a specific ISBN"""

    # Route
    url = "http://localhost:5050/books/" + str(ISBN)

    return requests.get(url).json()


def createAuthor(FirstName, LastName, Biography, Publisher):
    """Send post request to url with a json to create an author"""
    # Route
    url = "http://localhost:5050/admin/createAuthor"

    data = {
        "FirstName": FirstName,
        "LastName": LastName,
        "Biography": Biography,
        "Publisher": Publisher,
    }

    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    # Send POST request
    DATA_R = requests.post(url, data=json.dumps(data), headers=headers)

    print(DATA_R.status_code)
    print(DATA_R.json())


if __name__ == "__main__":
    # Basic data fields template
    Booksdata = {
        "Name": "Dragon Book ",
        "Description": "The Dragon Book",
        "Price": 369.0,
        "Author": "JamesBond",
        "Genre": "Compilers",
        "Publisher": "JamesBondInc",
        "YearPublished": 1968,
        "Sold": 399,
    }

    AuthorData = {
        "FirstName": "Johnny",
        "LastName": "Depp",
        "Biography": "Johnny Depp was born in Owensboro",
        "Publisher": "JohnnyDeppInc",
    }

    # Add 5 books to the DB with different names
    for x in range(5):
        addBookRequest(
            Booksdata["Name"] + str(x + 1),
            Booksdata["Description"],
            Booksdata["Price"],
            Booksdata["Author"],
            Booksdata["Genre"],
            Booksdata["Publisher"],
            Booksdata["YearPublished"],
            Booksdata["Sold"],
        )

    # Print pretty json Books
    print(json.dumps(getAllBooks(), indent=4))

    # Get an array of dicts of every book in the database
    booksjson = [json.loads(json.dumps(getAllBooks()[x])) for x in range(5)]

    # Print all of them
    print("All the books:\n", booksjson)

    # To access each, index them
    print("\nThe first book:\n", booksjson[0])

    # To get their values
    print("\nThe first book's author: ", booksjson[0].get("Author"))

    # Get book by ISBN
    print(getBookByISBN(1))

    # Create author
    createAuthor(
        AuthorData["FirstName"],
        AuthorData["LastName"],
        AuthorData["Biography"],
        AuthorData["Publisher"],
    )

    # Print all authors
    print(json.dumps(getAllAuthors(), indent=4))
