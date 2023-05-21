#!/usr/bin/env python3
import requests
from transmission_rpc import Client
import time
import os
import sys

def signal_handler(sig, frame):
    print('SIGTERM received. Exiting...')
    sys.exit(0)

transmission_protocol = os.environ.get('TRANSMISSION_PROTOCOL', 'http')
transmission_host = os.environ.get('TRANSMISSION_HOST', 'http')
transmission_user = os.environ.get('TRANSMISSION_USER', 'admin')
transmission_password = os.environ.get('TRANSMISSION_PASSWORD', 'password')
transmission_port = int(os.environ.get('TRANSMISSION_PORT', 9091))
transmission_path = os.environ.get('TRANSMISSION_PATH', '/transmission/rpc')
transmission_timeout = int(os.environ.get('TRANSMISSION_TIMEOUT', '60'))
transmission_update_type = os.environ.get('TRANSMISSION_UPDATE_TYPE', 'all') # ‘check pending’, ‘checking’, ‘downloading’, ‘download pending’, ‘seeding’, ‘seed pending’ or ‘stopped’ or all (default)
transmission_update_interval = int(os.environ.get('TRANSMISSION_UPDATE_INTERVAL', '360'))
transmission_update_interval_tracker_list = int(os.environ.get('TRANSMISSION_UPDATE_INTERVAL_TRACKER_LIST', '21600'))
transmission_tracker_list_url = os.environ.get('TRANSMISSION_TRACKER_LIST_URL', 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt')
transmission_tracker_list = os.environ.get('TRANSMISSION_TRACKER_LIST', '')

cold_start = True

def create_transmission_client(transmission_protocol, transmission_host, transmission_port, transmission_user, transmission_password, transmission_path, transmission_timeout):
    tr = Client(protocol=transmission_protocol, host=transmission_host, port=transmission_port, path=transmission_path, username=transmission_user, password=transmission_password, timeout=transmission_timeout)
    return tr

def get_all_torrents(tr, update_type):
    all_torrents = []
    if update_type == "all" or update_type == "":
        all_torrents = tr.get_torrents()
    else:
        torrents = tr.get_torrents()
        for torrent in torrents:
            if torrent.status == update_type:
                all_torrents += torrent
    return all_torrents

def replace_tracker_list(tr, torrent, tracker_list):
    current_list = torrent.tracker_list
    new_list = set(current_list + tracker_list)
    tr.change_torrent(torrent.id, tracker_list = [new_list])

def update_all_torrents(tr, update_type, tracker_list):
    for torrent in get_all_torrents(tr, update_type):
        print(f"update torrent - {torrent.id} - {torrent.name}")
        replace_tracker_list(tr, torrent, tracker_list)

def update_tracker_list(tracker_list_url, tracker_list):
    tracker_list_by_url = []
    tracker_list_by_user = []
    if tracker_list_url != "":
        new_tracker_list_by_url = requests.get(tracker_list_url)
        if new_tracker_list_by_url.status_code == 200:
            print(f"Getting new list {tracker_list_url} ok {new_tracker_list_by_url.status_code}")
            for tracker in new_tracker_list_by_url.text.split("\n"):
                if tracker.strip():
                    tracker_list_by_url.append(tracker)

    if tracker_list != "":
        tracker_list_by_user = transmission_tracker_list.split(',')

    return_list = tracker_list_by_url + tracker_list_by_user
    print("New list of trackers")
    print(f"{return_list}")
    return return_list


if __name__ == "__main__":
    update_tracker_flag = False
    update_tracker_timer = transmission_update_interval_tracker_list
    if cold_start:
        tracker_list = update_tracker_list(transmission_tracker_list_url, transmission_tracker_list)

    while True:
        tr = create_transmission_client(transmission_protocol, transmission_host, transmission_port, transmission_user, transmission_password, transmission_path, transmission_timeout)
        if update_tracker_flag:
            tracker_list = update_tracker_list(transmission_tracker_list_url, transmission_tracker_list)
            update_tracker_timer = transmission_update_interval_tracker_list
            update_tracker_flag = False

        update_all_torrents(tr, transmission_update_type, tracker_list)
        update_tracker_timer = update_tracker_timer - transmission_update_interval
        print(f"Time before update trackers - {update_tracker_timer}")
        if update_tracker_timer <= 0:
            print("Run update trackers next_time")
            update_tracker_flag = True

        print(f"Sleeping before next update {transmission_update_interval}s")
        time.sleep(transmission_update_interval)

