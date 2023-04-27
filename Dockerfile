FROM python:3.9

ARG LAT 
ARG LONG 
ARG API_KEY 

ENV LAT = value1
ENV LONG = value2
ENV API_KEY = value3

COPY wrapper.py ./

RUN pip3 install requests
CMD ["sh", "-c", "python3 ./wrapper.py ${LAT} ${LONG} ${API_KEY}"]