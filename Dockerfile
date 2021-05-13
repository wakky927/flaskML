# Use Alpine Linux with Python as the base image
FROM python:3.8-alpine

# Install Git
RUN apk update
RUN apk add git

# Install Python package
ADD requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# Clone src from GitHub
WORKDIR /web
RUN git clone https://github.com/wakky927/flaskML flaskML

# Launch flask app
# ENV FLASK_APP /web/flaskML/app.py
# CMD flask run -h 0.0.0.0 -p $PORT