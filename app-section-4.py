from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# WTF_CSRF_ENABLED config deals with the following errors
# 1) A secret key is required to use CSRF
# 2) The CSRF token is missing
app.config['WTF_CSRF_ENABLED'] = False

# For status codes, check out
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# https://http.cat/

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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not ever found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(418)
def im_a_teapot(error):
    return jsonify({'error': "I'm a teapot"}), 418

@app.route('/teapot', methods=['GET'])
def teapot():
    return "Let's have another cuppa", 418

class BookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    submit = SubmitField('submit')

@app.route('/api/books', methods=['POST'])
def create_book():
    form = BookForm(request.form)
    if form.validate():
        title = form.title.data
        author = form.author.data
        print(f'Title: {title}\nAuthor: {author}')
        return jsonify({'message': 'Book created successfully'}), 201
    else:
        error = {'error': 'Invalid data'}
        return jsonify({**error, **form.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)