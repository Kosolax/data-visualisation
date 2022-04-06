FROM python:3.7

COPY ./collector.py /home
COPY ./requirements.txt /
COPY ./private.pem /home
COPY ./automaton.py /home
COPY ./unit.py /home
RUN pip install -r requirements.txt