"""
Title: Module 2 Case Study.py
Author: Neal Vander Does
Date: 11/16/2024
Class: SDEV220-50P-IO-202420-I-82X
GitHub Link: 
Description: CRUD API for Books. Heavily based on https://www.youtube.com/watch?v=qbLc5a9jdXo
"""

# Imports
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# A few variables for less typing and a config for the database.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Book(db.Model):
    """
    Creates the database in an Object Relational Model (ORM) layer.
    Creates 4 columns, "id", "book_name", "author", and "publisher".
    Id is the primary key and book's MUST have a name and be unique.
    """
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.id} - {self.book_name} - {self.author} - {self.publisher}"

@app.route("/books")
def get_books():
    """
    Function used to Read data. "R" in CRUD.
    Allows a person to see every book within the database.
    """
    books = Book.query.all()
    output = []
    for book in books: # Iterates through every book in the database and appends it to the output list.
        book_data = {"id": book.id, "name": book.book_name, "author": book.author, "publisher": book.publisher}
        output.append(book_data)
    return {"books": output}

@app.route("/books/<id>")
def get_book(id):
    """
    Function used to Read data. "R" in CRUD.
    Allows a person to query a specific book using it's unique id.
    If the book doesn't exist an error page shows up instead.
    """
    book = Book.query.get_or_404(id) # Shows the book page if it exists, an error page if not.
    return {"id": book.id, "name": book.book_name, "author": book.author, "publisher": book.publisher}


@app.route("/books", methods=["POST"])
def add_book():
    """
    Function used to Create data. "C" in CRUD.
    Allows a person to create their own book using something like Postman
    as long as its formatted in json and the variables are used correctly.
    It is then added to the database and saved.
    """
    book = Book(id=request.json["id"], book_name=request.json["book_name"], 
                author=request.json["author"], publisher=request.json["publisher"])
    db.session.add(book)
    db.session.commit()
    return {"id": book.id}

@app.route("/books/<id>", methods=["DELETE"])
def delete_book(id):
    """
    Function used to Delete data. "D" in CRUD.
    Allows a person to delete an entry if they enter the correct URL 
    and id using something like Postman then commits the change. 
    If the id doesn't exist, returns a message saying error: "Book not found".
    """
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"Deleted": book}       

@app.route("/books/<id>", methods=["PUT"])
def update_book(id):
    """
    Function used to "Update" data. "U" in CRUD.
    Allows a person to update the data of a specific book based on its id
    using something like Postman. Returns an error if the id doesn't exist.
    There is probably a better way to do this, but I couldn't figure that way out.
    """
    book = Book.query.get(id)
    if book is None:
        return {"error": "Invalid id"}
    else: 
        db.session.delete(book) # Deletes the book that is being updated
        updated_book = Book(id=request.json["id"], book_name=request.json["book_name"],
                            author=request.json["author"], publisher=request.json["publisher"])
        db.session.add(updated_book) # Adds the updated book information
        db.session.commit() 
        return {"Updated": updated_book.id}   

# Creates the initial books inside of the database.
with app.app_context(): 
    db.create_all()
    
    book1 = Book(id=1, book_name="The Weirdstone of Brisingamen", author="Alan Garner", publisher="Publisher1")
    book2 = Book(id=2, book_name="Perdido Street Station", author="China Mieville", publisher="Publisher2")
    book3 = Book(id=3, book_name="Thud!", author="Terry Pratchett", publisher="Publisher3")
    book4 = Book(id=4, book_name="The Spellman Files", author="Lisa Lutz", publisher="Publisher4")
    book5 = Book(id=5, book_name="Small Gods", author="Terry Pratchett", publisher="Publisher5")

# Creates a session to communicate with the database and adds the initial books

    db.session.add_all([book1, book2, book3, book4, book5]) # Calls the book variables from above and adds the information to the database

# Starts the program
if __name__ == "__main__":
    app.run(debug=True)
