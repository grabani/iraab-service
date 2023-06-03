import json
import os
import re

import convert_numbers
from flask import jsonify, request

from app import app

with open(os.path.join(app.static_folder, 'out.json'), 'r', encoding='utf-8') as f:
    quran = json.load(f)


@app.route('/')
def home():
    return "hello world!"


@app.route('/irreb', methods=['GET'])
def irreb():
    # curl -X GET -H "Content-type: application/json" -d "{\"surah\" : \"10\", \"ayah\" : \"1\", \"word\" : \"1\"}" "localhost:56733/irreb"
    response_json = {}
    global quran
    content_type = request.headers.get('Content-Type')
    det_rx = re.compile(r'[\u0621-\u064A \u064B-\u0652]*')
    if (content_type == 'application/json'):
        json = request.json
        try:
            surah = convert_numbers.english_to_arabic(json["surah"])
            ayah = convert_numbers.english_to_arabic(json["ayah"])
            word_number = int(json["word"])
            ayah_text = quran[surah][ayah][0]
            irrabs = quran[surah][ayah][1]
            ayah_count = len(re.findall(det_rx, ayah_text))
            if word_number > ayah_count:
                raise KeyError
            else:
                current_count = 0
                for irab_key, irab_value in irrabs.items():
                    current_count = current_count + len(re.findall(det_rx, irab_key))
                    if word_number <= current_count:
                        return jsonify({'irrab': irab_value})
            return jsonify({'irrab': irrabs})
        except KeyError as e:
            print(e)
            return "Please enter valid keys (surah,ayah,word)"
        return jsonify(response_json)
    else:
        return 'Content-Type not supported!'
