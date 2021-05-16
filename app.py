from flask import Flask, render_template, request

from torchvision import transforms

from PIL import Image, ImageOps
from datetime import datetime

from ai.cnn import Cnn


cnn = Cnn()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # temporary save
        f = request.files["file"]
        filepath = "static/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        f.save(filepath)

        # read img
        image = Image.open(filepath)

        # Preprocessing(binaries, resize, normalize, add-dimension)
        image = ImageOps.invert(image.convert("L")).resize((28, 28))
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
        )
        image = transform(image).unsqueeze(0)

        # prediction
        cnn.data_load(image=image)
        result = cnn.predict()

        return render_template("index.html", filepath=filepath, result=result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
