FROM python:3.9.7

MAINTAINER MAX NOVOSELSKY <relocker121@gmail.com>

RUN apt-get update

COPY . /usr/src/tutoralls

WORKDIR "/usr/src/tutoralls/"

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "tutoralls.wsgi", "--bind", "0.0.0.0"]
