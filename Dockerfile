# Use Alpine Linux with Python as the base image
FROM python:3.8-alpine

# Install Git
RUN apk update
RUN apk add git

# Install Python package
ADD requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r /tmp/requirements.txt

# Clone src from GitHub
WORKDIR /web
RUN git clone https://github.com/wakky927/flaskML flaskML

# Launch flask app
# ENV FLASK_APP /web/flaskML/app.py
# CMD flask run -h 0.0.0.0 -p $PORT