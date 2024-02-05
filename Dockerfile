FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=main.py

CMD ["gunicorn", "-b", ":5000", "main:app"]

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y