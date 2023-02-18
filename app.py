from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

db_path = 'C:\\Users\\Emily\\Documents\\Codecademy\\projects_js\\SpotifyPlaylistMaker\\books.db'

books = [ 
            {'id': 0, 
            'title': 'A Fire Upon the Deep', 
            'author': 'Vernor Vinge', 
            'first_sentence': 'The coldsleep itself was dreamless.', 
            'year_published': '1992'},
            
            {'id': 1, 
            'title': 'The Ones Who Walk Away From Omelas', 
            'author': 'Ursula K. Le Guin', 
            'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.', 
            'published': '1973'},

            {'id': 2, 
            'title': 'Dhalgren', 
            'author': 'Samuel R. Delany', 
            'first_sentence': 'to wound the autumnal city.', 
            'published': '1975'} 
        ]

@app.route('/', methods=['GET'])
def home():
	return "<h1>JAime es un tipazo</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


# GET Display all the books
@app.route('/api/v1/resources/books/all', methods=['GET']) 
def api_all():
    return jsonify(books)
    #return books

# GET ?id=x -> Display the book with specified id
@app.route('/api/v1/resources/books', methods=['GET']) 
def api_id():

    if request.method == 'GET':
        if 'id' in request.args: 
            id = int(request.args['id']) 
        else: 
            return "Error: No id field provided. Please specify an id." 
    
        results = [] 
        for book in books: 
            if book['id'] == id: 
                results.append(book) 
    
        return jsonify(results)
    
@app.route('/api/v1/resources/books/<string:title>', methods=['GET'])
def get_by_title(title):
    results = []
    for book in books:
        if book['title'] == title:
            return jsonify(book)
    return jsonify({'message': 'Book not found'})

# POST {id:, title:, author:, fist_sentence:, published:} -> Create this book
@app.route('/api/v2/resources/books', methods=['POST']) 
def post_book():
    data = request.get_json() 
    books.append(data) 
    return jsonify(data)

@app.route('/api/v1/resources/books/sql/all', methods=['GET']) 
def get_all(): 
    # connection = sqlite3.connect('books.db') 
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor() 
    cursor.execute(''' CREATE TABLE IF NOT EXISTS testing (column_1 integer PRIMARY KEY, column_2 text )''')
    cursor.execute(''' INSERT INTO testing (column_1, column_2) VALUES (3, "This is cool")''')
    tables = cursor.execute("""SELECT name FROM sqlite_schema WHERE type ='table'""").fetchall()
    try:
        select_books = "SELECT * FROM books" 
        result = cursor.execute(select_books).fetchall() 
        connection.close() 
 
        return jsonify({'books': result})  
    except:
        return cursor.execute('''select * from testing''').fetchall() 

@app.route('/age/finder/<firstName>', methods=['GET'])
def get_age(firstName):
    urlPath = f"https://api.agify.io?name={firstName}"
    r = requests.get(urlPath)
    age = r.json()
    return age

@app.route('/ads/db', methods=['GET'])
def get_ads():
    #adsPath = "C:\\Users\\Emily\\Documents\\Codecademy\\projects_js\\SpotifyPlaylistMaker\\04-Industrializacion\\1-Routing_APIs\\ejercicios\\Modelo_Clase\\model\\advertising.sqlite"
    #adsPath = "C:\\Users\\Emily\\Documents\\TheBridge2022\\Copy_Repo\\02-Data_analysis\\My_project\\Project_houses\\HouseDB.sqlite"
    adsPath = "C:\\Users\\Emily\\Documents\\TheBridge2022\\Copy_Repo\\04-Industrializacion\\1-Routing_APIs\\Solved\\adsDB.sqlite"
    connection = sqlite3.connect(adsPath) 
    cursor = connection.cursor() 
    tables = cursor.execute("""SELECT name FROM sqlite_schema WHERE type ='table'""").fetchall()
    answer = cursor.execute('SELECT * FROM "ads_train"').fetchall()
    connection.close()
    return answer

@app.route('/predict-message', methods=['GET'])
def pred_msg():
    return "I will make a sales prediction!"

app.run(port=5000)