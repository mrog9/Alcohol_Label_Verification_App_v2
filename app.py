from flask import Flask, request, render_template, jsonify, session
from utils import *
from dotenv import load_dotenv
import json
import os

# ---------------------------------------------------

# global variables

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()
ENV = os.getenv("ENV", "deploy")

# ----------------------------------------------------


# "home" page

@app.route("/", methods=["GET", "POST"])
def index():


    return render_template("form.html")

# -----------------------------------------------------------

# the image is previewed and while the rest of the form is being filled out
# the image is being processed. returns json

@app.route("/preview_img", methods=["POST"])
def preview_img():

    comment, data_list, label_segs, filepath = None, None, None, None

    if request.method == "POST":

        delete_any_files(UPLOAD_FOLDER)

        file = request.files["file"]

        comment, data_list, label_segs, filepath = get_label_info(app, file)

    return jsonify({"comment":comment, "data":data_list, 'label':label_segs, "filepath":filepath})

# ------------------------------------------------------------------

# when the form is submitted, all the processed image information and the form info
# is sent to this route. the info is extracted and sent through the getComments method
# where the image is validated with the form information. it will return json

@app.route("/validate", methods=["POST"])
def upload_file():

    text, comment, filepath = None, None, None

    if request.method == "POST":

        data = request.get_json()
        form_data = json.loads(data['form'])

        image_data = json.loads(data['image'])

        b = form_data['brand']
        p = form_data['product']
        a = form_data['content']
        n = form_data['net'].replace(" ","").lower()

        c = image_data['comment']
        dl = image_data['data']
        ls = image_data['label']
        fp = image_data['filepath']

        if not c:
    
            comment, filepath, text = getComments(b, p, a, n,dl, ls, fp)


        else:

            comment = c
      
    return jsonify({"text":text,"comment":comment, "filepath":filepath})

# -----------------------------------------------------------------------

if __name__ == "__main__":

    if ENV == "local":

        app.run(debug=True)

    else:

        port = int(os.environ.get("PORT", 8000))
        app.run(host="0.0.0.0", port=port)