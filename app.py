from flask import Flask, request, jsonify
import sqlite3
import requests
from datetime import datetime
import sklearn
import pickle
import numpy as np

app = Flask(__name__)
app.config['DEBUG'] = True

book_path = 'C:\\Users\\Emily\\Documents\\TheBridge2022\\Copy_Repo\\04-Industrializacion\\1-Routing_APIs\\Solved\\api-demo\\books.sqlite'
ads_path = "C:\\Users\\Emily\\Documents\\TheBridge2022\\Copy_Repo\\04-Industrializacion\\1-Routing_APIs\\Solved\\api-demo\\adsDB.sqlite"
model_path = "C:\\Users\\Emily\\Documents\\TheBridge2022\\Copy_Repo\\04-Industrializacion\\1-Routing_APIs\\Solved\\api-demo\\advertising.model"

model = pickle.load(open(model_path, 'rb'))

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
    for book in books:
        if book['title'] == title:
            return jsonify(book)
    return jsonify({'message': 'Book not found'})

@app.route('/api/v2/resources/books', methods=['POST']) 
def post_book():
    data = request.get_json() 
    books.append(data) 
    return jsonify(data)

@app.route('/api/v1/resources/books/sql/all', methods=['GET']) 
def get_all(): 
    connection = sqlite3.connect(book_path)
    cursor = connection.cursor() 
    try:
        select_books = "SELECT * FROM books" 
        result = cursor.execute(select_books).fetchall() 
        connection.close() 
        return jsonify({'books': result})  
    except Exception as e:
        print(e)
        return 'oops'

@app.route('/age/finder/<firstName>', methods=['GET'])
def get_age(firstName):
    urlPath = f"https://api.agify.io?name={firstName}"
    r = requests.get(urlPath)
    age = r.json()
    return age

@app.route('/ads/db', methods=['GET'])
def get_ads():
    connection = sqlite3.connect(ads_path) 
    cursor = connection.cursor() 
    # tables = cursor.execute("""SELECT name FROM sqlite_schema WHERE type ='table'""").fetchall()
    answer = cursor.execute('SELECT * FROM "ads_train"').fetchall()
    connection.close()
    return answer

@app.route('/predict-message', methods=['GET'])
def pred_msg():
    return "I will make a sales prediction!"

@app.route('/check-model', methods=['GET'])
def check_model():
    try: 
        pred = model.predict([[23.8,35.1,65.9]])[0]
        pred = str(pred)
        #coefs = model.coef_
        return pred
    except Exception as e:
        print(e)
        return 'model not found'

@app.route('/predict-from-model', methods=['POST'])
def get_predict():
    result = []
    # Get current time for the PREDICTIONS table
    str_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    conn = sqlite3.connect(ads_path)
    crs = conn.cursor()
    data = request.get_json()
    result.append(data) 
    tv = data.get("TV",0)
    radio = data.get("radio",0)
    newspaper = data.get("newspaper",0)

    # Model prediction
    pred = model.predict(np.array([[tv, radio, newspaper]]))[0]
    print(pred)
    # Save prediction in PREDICTIONS table
    crs.execute(''' INSERT INTO predictions(pred_date,TV,radio,newspaper,prediction)
                    VALUES(?,?,?,?,?) ''', (str_time, tv, radio, newspaper, pred))
    conn.commit()
    conn.close()
    return str(pred), 200

@app.route('/review_predicts', methods=['GET'])
def return_predicts():
    conn = sqlite3.connect(ads_path)
    crs = conn.cursor()
    query = "SELECT * FROM PREDICTIONS"
    resultado = jsonify(crs.execute(query).fetchall())

    conn.close()
    return resultado, 200

app.run(port=5000)