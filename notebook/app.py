from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import io
import base64
import os

app = Flask(__name__)

model = load_model("data/digit_cnn.h5")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    img = None

    if "image" in request.files:
        file = request.files["image"]
        img = Image.open(file).convert("L")

    elif request.is_json and "imageBase64" in request.json:
        data = request.json["imageBase64"]
        image_bytes = base64.b64decode(data.split(",")[1])
        img = Image.open(io.BytesIO(image_bytes)).convert("L")

    else:
        return jsonify({"error": "No image provided"}), 400

    img = ImageOps.invert(img)
    img = img.resize((28, 28))

    img_array = np.array(img).astype("float32") / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    preds = model.predict(img_array)
    pred_class = int(np.argmax(preds, axis=1)[0])

    return jsonify({"prediction": pred_class})

if __name__ == "__main__":
    app.run(debug=True)