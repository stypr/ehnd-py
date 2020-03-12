# coding: utf-8

"""
server.py

Translation Server
"""

import os
import re
import sys
from flask import Flask, request, jsonify
from trans import TransEngineJPKR, TransEngineKRJP

# Load Flask
app = Flask(__name__, static_url_path='/static')

# Check 64bit (Windows XP Support)
if sys.maxsize > 2**32:
    TRANS_DIR = os.path.join(os.environ["ProgramFiles(x86)"], "ChangShinSoft", "ezTrans XP")
else:
    TRANS_DIR = os.path.join(os.environ["ProgramFiles"], "ChangShinSoft", "ezTrans XP")

# Load Translation Engine
TRANS_JPKR = TransEngineJPKR(TRANS_DIR)
TRANS_KRJP = TransEngineKRJP(TRANS_DIR)

def check_language(text):
    """ (str) -> str

    Detects language based on the character boundary
    """
    matches = [
        len(re.findall('[\u30a0-\u30ff\u3040-\u309f\u4e00-\u9fbf]', text)),
        len(re.findall('[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]', text)),
        len(re.findall('[A-Za-z]', text))
    ]

    most_match = matches.index(max(matches))

    matched_result = ""
    if most_match == 0:
        matched_result = "Japanese"
    elif most_match == 1:
        matched_result = "Korean"
    else:
        matched_result = "English"

    return matched_result

@app.route("/")
def index_page():
    """
    Main page to show translator
    """
    return app.send_static_file('index.html')

@app.route("/translate_auto", methods=["POST"])
def translate_auto():
    """
    API which detects language automatically and translates
    """
    src_text = request.form.get('text')

    if check_language(src_text) == "Japanese":
        translated_text = TRANS_JPKR.translate(src_text)
    else:
        translated_text = TRANS_KRJP.translate(src_text)

    return jsonify(translated_text)

@app.route("/translate_jp_kr", methods=["POST"])
def translate_jp_kr():
    """
    API which translates from JP to KR
    """
    src_text = request.form.get('text')
    return jsonify(TRANS_JPKR.translate(src_text))

@app.route("/translate_kr_jp", methods=["POST"])
def translate_kr_jp():
    """
    API which translates from KR to JP
    """
    src_text = request.form.get('text')
    return jsonify(TRANS_KRJP.translate(src_text))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)
