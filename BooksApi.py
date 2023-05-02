from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def create_db():
    conn = sqlite3.connect('books.db')
    sql_query = """ CREATE TABLE IF NOT EXISTS books(
        id integer PRIMARY KEY,
        title text NOT NULL,
        author text NOT NULL
    ) """
    cursor = conn.cursor()
    cursor.execute(sql_query)

create_db()

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data['title']
    author = data['author']

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book created successfully'})

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    return jsonify({'books': [{'id': book[0], 'title': book[1], 'author': book[2]} for book in books]})

# Get a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    conn.close()

    if book:
        return jsonify({'id': book[0], 'title': book[1], 'author': book[2]})
    else:
        return jsonify({'error': 'Book not found'})

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data['title']
    author = data['author']

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=? WHERE id=?", (title, author, book_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book updated successfully'})

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
