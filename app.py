from flask import Flask, jsonify, request
from transformers import pipeline
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
CORS(app)
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# db details
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# db connection
app.config["MYSQL_HOST"]= db_host
app.config["MYSQL_USER"]= db_user
app.config["MYSQL_PASSWORD"]= db_password
app.config["MYSQL_DB"]= db_name

mysql = MySQL(app)

@app.route("/transcribe_voice")
def transcribeVoiceHandler():
    text = pipe("shirt.mp3")
    print(text["text"])
    return jsonify(
        {"status": "Success", "message": "Voice Transcribed Successfully", 'data': text["text"]}
    ), 200


@app.route("/upload", methods=['POST'])
def uploadHandler():
    print(request.json)
    result = pipe(request.json['url'])
    print(result['text'])
    return result['text']

@app.route("/fetch_products", methods=['POST'])
def fetchProductsHandler():
    lstStrings = request.json['text'].split()
    format_strings = ','.join(['%s'] * len(lstStrings))
    
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM products WHERE category IN ({format_strings})"
    cur.execute(query, lstStrings)
    products = cur.fetchall() # returns tuple of tuples
    
    column_names = [desc[0] for desc in cur.description]
    product_list = [dict(zip(column_names, product)) for product in products]
    
    return jsonify(product_list)
    
@app.route("/")
def testHandler():
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
