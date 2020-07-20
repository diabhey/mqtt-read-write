FROM jfloff/alpine-python

RUN apk add --no-cache openrc mosquitto 

COPY . app/

RUN  pip3 install -r app/requirements.txt

CMD [ "mosquitto" ]