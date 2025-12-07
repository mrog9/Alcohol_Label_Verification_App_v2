from flask import Flask, request, send_file
import numpy as np
import cv2
import io

app = Flask(__name__)

@app.route("/preprocess", methods=["POST"])
def preprocess():
    file = request.files["file"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Example preprocessing: grayscale + resize
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (640, 480))

    # Encode back to JPEG
    _, buffer = cv2.imencode(".jpg", resized)
    return send_file(
        io.BytesIO(buffer.tobytes()),
        mimetype="image/jpeg"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
