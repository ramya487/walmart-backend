from flask import Flask, jsonify, request
from transformers import pipeline
from flask_cors import CORS
from googletrans import Translator


app = Flask(__name__)
CORS(app)
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-medium")


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
    
@app.route("/translate", methods=['POST'])
def translateHandler():
    translator = Translator() 
    translated_text = translator.translate(request.json['text'], src='auto', dest='en').text
    print("translated text: ",translated_text)
    return "success of translation"


@app.route("/")
def testHandler():
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
