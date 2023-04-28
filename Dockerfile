FROM python:3.9

ARG LAT 
ARG LONG 
ARG API_KEY 

ENV LAT = value1
ENV LONG = value2
ENV API_KEY = value3

WORKDIR /app
COPY wrapper.py ./

RUN pip3 install --no-cache-dir requests==2.7.0

CMD ["sh", "-c", "python3 ./wrapper.py ${LAT} ${LONG} ${API_KEY}"]