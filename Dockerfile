FROM python:3.9.10-buster
RUN apt -y update
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt