FROM python:3.9-buster

RUN pip install --no-cache-dir websearch-python

CMD python -m websearch 0.0.0.0 $PORT