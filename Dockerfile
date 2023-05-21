FROM python:3

WORKDIR /work

COPY requirements.txt requirements.txt

RUN /usr/local/bin/pip3 install --no-cache-dir -r requirements.txt

ENV TRANSMISSION_PROTOCOL "http"
ENV TRANSMISSION_HOST "127.0.0.1"
ENV TRANSMISSION_USER "admin"
ENV TRANSMISSION_PASSWORD "password"
ENV TRANSMISSION_PORT "9091"
ENV TRANSMISSION_PATH "/transmission/rpc"
ENV TRANSMISSION_TIMEOUT "60"
ENV TRANSMISSION_UPDATE_TYPE "all"
ENV TRANSMISSION_UPDATE_INTERVAL "360"
ENV TRANSMISSION_UPDATE_INTERVAL_TRACKER_LIST "21600"
ENV TRANSMISSION_TRACKER_LIST_URL "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt"
ENV TRANSMISSION_TRACKER_LIST ""

COPY update.py /work/update.py

CMD ["/work/update.py", "/work/config.yml"]
