from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateField, DateTimeField
from wtforms.validators import DataRequired
from flaskext.mysql import MySQL

app = Flask(__name__)


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'aieng'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'esres'
app.config['WTF_CSRF_ENABLED'] = False

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/api/books', methods=['GET'])
def get_books():
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return jsonify(books)

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    return f'Hello, {name}'

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

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
    publication_date = DateField('publication_date')
    price = DecimalField('price')
    created_at = DateTimeField('created_at') 
    updated_at = DateTimeField('updated_at')
    submit = SubmitField('submit')

@app.route('/api/books', methods=['POST'])
def create_book():
    form = BookForm(request.form)
    if form.validate():
        title = form.title.data
        author = form.author.data
        publication_date = form.publication_date.data or None
        price = form.price.data or None
        created_at = form.created_at.data or None
        updated_at = form.updated_at.data or None
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO BOOKS
                (title, author, publication_date, price, created_at, updated_at)
            VALUES 
                (%s,%s,%s,%s,%s,%s)
            """,
        [title, author, publication_date, price, created_at, updated_at])
        db.commit()
        return jsonify({'message': 'Book created successfully'}), 201
    else:
        error = {'error': 'Invalid data'}
        return jsonify({**error, **form.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)