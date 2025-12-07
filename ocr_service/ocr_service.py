from flask import Flask, request, jsonify
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])  # load once at startup

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    file = request.files["file"]
    results = reader.readtext(file.read())

    text_list = []

    for (bbox, text, confidence) in results:
        
        text_list.append(text)

    joined_chars = "".join(text_list).lower()


    return jsonify({"results": joined_chars})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




