# base image: Ubuntu
FROM ubuntu:latest

# Install package
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    vim \
    git

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