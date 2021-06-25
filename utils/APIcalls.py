import requests
import json
from time import sleep

# Route
url = "http://localhost:5050/books"


def addBookRequest(name, desc, price, author, genre, pub, year, sold):
    """Send post request to url with a json"""
    # Name must be unique for every entry. If not, it might return error 500
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
    """Returns a json with all the items in the DB"""
    return requests.get(url).json()


if __name__ == "__main__":
    # Basic data fields template
    data = {
        "Name": "Dragon Book ",
        "Description": "The Dragon Book",
        "Price": 369.0,
        "Author": "JamesBond",
        "Genre": "Compilers",
        "Publisher": "JamesBondInc",
        "YearPublished": 1968,
        "Sold": 399,
    }

    # Add 5 books to the DB with different names
    for x in range(5):
        addBookRequest(
            data["Name"] + str(x + 1),
            data["Description"],
            data["Price"],
            data["Author"],
            data["Genre"],
            data["Publisher"],
            data["YearPublished"],
            data["Sold"],
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
