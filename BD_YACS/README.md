# YACS - Yet Another Centralized Scheduler

### Execution
Run on 3+2 diff terminals  

```sh
python3 worker.py 4001 1
python3 master.py config.json RANDOM
python3 requests.py 3 
```
or just execute(as of for now, script tested on ubuntu)  

```sh
sh run.sh
```

### Ports 
```
5000 - requests.py ->  master.py  
4001 - master.py   ->  worker.py 4001 1  
4002 - master.py   ->  worker.py 4002 2  
4003 - master.py   ->  worker.py 4003 3
5001 - worker.py   ->  master.py
```  

#### Whats left!?
- [ ] ~~job_id being searched through list O(n). Implement a dictionary to get it in O(1) - later~~
- [x] Schedule algos
- [x] Port 5000
- [x] Port 5001
- [ ] Usage of threads
- [ ] Updation of slots, after and before worker allocation
- [ ] Plot graphs for logging purposes
