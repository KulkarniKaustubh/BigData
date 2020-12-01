#!/bin/sh

log_dir="logs"
img_dir="img"
[ ! -d "$log_dir" ] && mkdir -p "$log_dir"
[ ! -d "$img_dir" ] && mkdir -p "$img_dir"

gnome-terminal -- python3 worker1.py 4000 1
gnome-terminal -- python3 worker1.py 4001 2
gnome-terminal -- python3 worker1.py 4002 3

gnome-terminal -- python3 master1.py config.json LL

gnome-terminal -- python3 requests.py 10
