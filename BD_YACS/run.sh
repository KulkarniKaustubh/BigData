#!/bin/sh

gnome-terminal -- python3 worker.py 4001 1
gnome-terminal -- python3 master.py config.json RR
gnome-terminal -- python3 requests.py 3
