from flask import Flask, jsonify, request
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
generator = pipeline("text-generation", model="gpt2")
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

@app.route("/generate_text")
def generateTextHandler():
    example_query = "what is blue?"
    answer = generator(example_query, max_length=30)
    print(answer[0]["generated_text"])
    return jsonify({"status": "Success", "message": "Text Generation Successfull"}), 200


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
    result = pipe(request.json['img'])
    print(result['text'])
    return result['text']
    
    
@app.route("/")
def testHandler():
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
