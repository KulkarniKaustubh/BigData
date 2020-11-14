#!/bin/sh

gnome-terminal -- python3 worker.py 4000 1
gnome-terminal -- python3 worker.py 4001 2
gnome-terminal -- python3 worker.py 4002 3

gnome-terminal -- python3 master.py config.json RANDOM

gnome-terminal -- python3 requests.py 3
