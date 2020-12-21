FROM python:3.7-alpine
# Optional and depreciated
MAINTAINER alperakbas Analytica Advisory Group 


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt 


RUN mkdir /app
WORKDIR /app
COPY ./app /app

# We dont want to give root access to everyone
RUN adduser -D user
USER user
