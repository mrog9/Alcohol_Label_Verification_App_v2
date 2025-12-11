from flask import Flask, request, render_template
from utils import *
import os

# global variables

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# "home" page

@app.route("/")
def index():

    return render_template("form.html")


# when file is uploaded, the form is validated and rectangles drawn around mismatched labels.
# If no comment is added. Then, the label is validated
# with the form with the comment "SUCCESS!". The homepage is rendered with the extracted text and comment included

@app.route("/upload", methods=["GET", "POST"])
def upload_file():

    text, comment, filepath = None, None, None

    delete_any_files(UPLOAD_FOLDER)

    if request.method == "POST":

        comment, file_obj, img, text = getComments()
        filepath = save_image(app, file_obj, img)
        
      
    return render_template("form.html", text = text, comment = comment, filepath = filepath)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)