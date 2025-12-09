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

    text = ""
    comment = ""
    filepath = ""
    img = None

    if request.method == "POST":

        brand = request.form['brand'].lower()
        prod = request.form['product'].lower()
        alc = request.form['content'].lower().replace(" ","")
        net = request.form['net'].lower().replace(" ","")
        file = request.files["file"]

        comment = validate_form_input(brand, prod, alc, net, file)

        if not comment:

            text, comment, img = get_text_from_image(file)

        if not text and not comment:

            comment += "Take clearer picture. No text could be recognized."

        if not comment:

            comment, img = validate_label(img, brand, prod, alc, net)
            
        if not comment:

            comment = "SUCCESS!"


        raw_path = save_file(app, file, img)
        filepath = raw_path.replace('static/', "")
        filepath = filepath.replace("\\", "/")
      
    return render_template("form.html", text = text, comment = comment, filepath = filepath)

if __name__ == "__main__":
    app.run(debug=True)