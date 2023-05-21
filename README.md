# update.py

Script provide automatic update tracker list from public torrent list for all (or filtered by state) torrents.

## usage

```bash
docker build -t update-torrents  .
docker run -ti --rm --name update-torrents \
  -e TRANSMISSION_PROTOCOL="http" \
  -e TRANSMISSION_HOST="127.0.0.1" \
  -e TRANSMISSION_USER="admin" \
  -e TRANSMISSION_PASSWORD="password" \
  -e TRANSMISSION_PORT="9091" \
  -e TRANSMISSION_PATH="/transmission/rpc" \
  -e TRANSMISSION_TIMEOUT="60" \
  -e TRANSMISSION_UPDATE_TYPE="all" \
  -e TRANSMISSION_UPDATE_INTERVAL="360" \
  -e TRANSMISSION_UPDATE_INTERVAL_TRACKER_LIST="21600" \
  -e TRANSMISSION_TRACKER_LIST_URL="https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt" \
  -e TRANSMISSION_TRACKER_LIST="" \
  update-torrents
```

## Variables

|Name|Default|Description|
|-|-|-|
TRANSMISSION_PROTOCOL | http | Connect via `http` or `https`|
TRANSMISSION_HOST | 127.0.0.1 | Hostname with transmission rpc |
TRANSMISSION_USER | admin | Username for connection to transmission rpc|
TRANSMISSION_PASSWORD | password | Password for transmission rpc |
TRANSMISSION_PORT | 9091 | transmission rpc port |
TRANSMISSION_PATH | /transmission/rpc | path for transmission rpc |
TRANSMISSION_TIMEOUT | 60 | Timeout to connect transmission rpc (in seconds) |
TRANSMISSION_UPDATE_TYPE | all | Which status can be udpated, ‘check pending’, ‘checking’, ‘downloading’, ‘download pending’, ‘seeding’, ‘seed pending’ or ‘stopped’ or all (default) |
TRANSMISSION_UPDATE_INTERVAL | 360 | Update tracker list every 360s |
TRANSMISSION_UPDATE_INTERVAL_TRACKER_LIST | 21600 | Update trackers list every 21600 seconds |
TRANSMISSION_TRACKER_LIST_URL | https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt | Url to new-line seperated files with trackers |
TRANSMISSION_TRACKER_LIST | '' | Comma-seprated list with user-specific torrent, example: 'http://retracker.local/announce,https://retracker.local/announce' |

## Export image for Docker (linux/amd64) to file system on Apple Sillicon

```bash
docker buildx build --load --platform linux/amd64 -t update-torrents:latest .
docker image save update-torrents:latest > update-torrents-amd64.tar
```
