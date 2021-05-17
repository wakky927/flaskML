import base64
import re

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import torch
from torchvision import transforms

import cv2
import numpy as np

from PIL import Image, ImageOps
from datetime import datetime

from ai.cnn import Cnn


cnn = Cnn()

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        ans = get_answer(request)
        return jsonify({'ans': ans})


def get_answer(req):
    img_str = re.search(r'base64,(.*)', req.form['img']).group(1)
    nparr = np.fromstring(base64.b64decode(img_str), np.uint8)
    img_src = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_negaposi = 255 - img_src
    img_gray = cv2.cvtColor(img_negaposi, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_gray, (28, 28))
    cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)

    # prediction
    image = Image.fromarray(img_resize)
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
    )
    image = transform(image).unsqueeze(0)
    cnn.data_load(image=image)
    result = cnn.predict()

    return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
