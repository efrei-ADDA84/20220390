FROM python:3.9

ARG API_KEY 

ENV API_KEY = value1

WORKDIR /app
COPY wrapperApi.py ./

RUN pip3 install --no-cache-dir requests==2.7.0
RUN pip3 install --no-cache-dir flask==2.3.1

CMD ["sh", "-c", "python3 ./wrapperApi.py ${API_KEY}"]