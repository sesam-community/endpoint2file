FROM python:3-alpine

LABEL maintainer="Geir Atle Hegsvold geir.hegsvold@sesam.io"

RUN apk update

RUN pip install --upgrade pip

COPY ./service/requirements.txt /service/requirements.txt
RUN pip install -r /service/requirements.txt
COPY ./service /service

EXPOSE 5555

CMD ["python3", "-u", "./service/endpoint2file.py"]
