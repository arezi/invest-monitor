# docker build -t arezi/invest-monitor .


FROM python:3.7-alpine

LABEL maintainer="fabio.arezi@gmail.com"



ENV TZ America/Sao_Paulo

WORKDIR /monitor

COPY requirements.txt /monitor
COPY run.py /monitor
COPY app /monitor

RUN pip install -r /monitor/requirements.txt

CMD [ "python", "run.py" ]
