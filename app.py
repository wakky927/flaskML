from flask import Flask, render_template, request

import torch
import torch.nn as nn
import torch.nn.functional as functional

from torchvision import transforms

from PIL import Image, ImageOps
from datetime import datetime


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, (5, 5), (1, 1))
        self.conv2 = nn.Conv2d(20, 50, (5, 5), (1, 1))
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = functional.relu(self.conv1(x))
        x = functional.max_pool2d(x, 2, 2)
        x = functional.relu(self.conv2(x))
        x = functional.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = functional.relu(self.fc1(x))
        x = self.fc2(x)
        return functional.log_softmax(x, dim=1)


device = torch.device("cpu")
model = Net().to(device)

# training static load
model.load_state_dict(
    torch.load("/web/flaskML/mnist_cnn.pt", map_location=lambda storage, loc: storage)
)

model = model.eval()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # temporary save
        f = request.files["file"]
        filepath = "/web/flaskML/static/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        f.save(filepath)

        # read img
        image = Image.open(filepath)

        # Preprocessing(binaries, resize, normalize, add-dimension)
        image = ImageOps.invert(image.convert("L")).resize((28, 28))
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )
        image = transform(image).unsqueeze(0)

        # prediction
        output = model(image)
        _, prediction = torch.max(output, 1)
        result = prediction[0].item()

        return render_template("index.html", filepath=filepath, result=result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
