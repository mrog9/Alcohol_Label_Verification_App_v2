from flask import Flask, request, render_template
import requests
from utils import *

app = Flask(__name__)

# Replace with your actual service URLs
PREPROCESS_URL = "http://preprocess-service:5000/preprocess"
OCR_URL = "http://ocr-service:5000/ocr"

@app.route("/", methods=["GET", "POST"])
def upload_file():

    brand = request.form['brand'].lower()
    prod = request.form['product'].lower()
    alc = request.form['content'].lower()
    net = request.form['net'].lower()
    file = request.files["file"]

    comment_str, brand_nm_list, prod_nm_list = validate_form(brand, prod, alc, net, file)

    results = None


    if not comment_str:

        
        try:

            # Step 1: Send to Preprocessing service
            preprocess_resp = requests.post(PREPROCESS_URL, files={"file": file})
            processed_image = preprocess_resp.content

            # Step 2: Send processed image to OCR service
            ocr_resp = requests.post(OCR_URL, files={"file": processed_image})
            results = ocr_resp.json()
            text = results['results']

            comment_str = validate_labels(brand_nm_list, prod_nm_list, alc, net, text)

        except Exception as e:

            comment_str = comment_str + str(e)

    return render_template("form.html", submission=comment_str, text = results)

if __name__ == "__main__":
    app.run(debug=True)



