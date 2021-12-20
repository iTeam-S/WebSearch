FROM python:3.9-buster

RUN pip install --no-cache-dir websearch-python

CMD ["sh", "-c", "python -m websearch --host 0.0.0.0 --port $PORT"]
