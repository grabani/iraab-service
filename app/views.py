import json
import os

import convert_numbers
from flask import jsonify, request

from app import app

with open(os.path.join(app.static_folder, 'out.json'), 'r', encoding='utf-8') as f:
    quran = json.load(f)

@app.route('/')
def home():
    return "hello world!"

@app.route('/irreb',methods=['GET'])
def irreb():
    # curl -X GET -H "Content-type: application/json" -d "{\"surah\" : \"10\", \"ayah\" : \"1\", \"word\" : \"1\"}" "localhost:56733/irreb"
    response_json = {}
    global quran
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        try:
            surah = convert_numbers.english_to_arabic(json["surah"])
            ayah = convert_numbers.english_to_arabic(json["ayah"])
            word = convert_numbers.english_to_arabic(json["word"])
            ayah_text = quran[surah][ayah][0]
            irrabs = quran[surah][ayah][1]
            return jsonify({'ayah': quran[surah][ayah]})
        except KeyError as e:
            print(e)
            return "Please enter valid keys (surah,ayah,word)"
        return jsonify(response_json)
    else:
        return 'Content-Type not supported!'