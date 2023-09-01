from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/api/books', methods=['GET'])
def get_books():
    books = [
        {'title': 'Book 1', 'author': 'Author 1'},
        {'title': 'Book 2', 'author': 'Author 2'},
        {'title': 'Book 3', 'author': 'Author 3'},
    ]
    return jsonify(books)

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = {'title': 'Book 1', 'author': 'Author 1'}
    return jsonify(book)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    return f'Hello, {name}'

if __name__ == '__main__':
    app.run(debug=True)