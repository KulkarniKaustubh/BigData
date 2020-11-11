# YACS - Yet Another Centralized Scheduler

### Execution
Run on 2 diff terminals  

```sh
python3 master.py config.json RR
python3 requests.py 3 
```

###Ports 
```
5000 - requests.py ->  master.py  
4001 - master.py   ->  worker.py 4001 1  
4002 - master.py   ->  worker.py 4002 2  
4003 - master.py   ->  worker.py 4003 3
5001 - worker.py   ->  master.py
```  

#### Whats left!?
- [ ] 1. job_id being searched through list O(n). Implement a dictionary to get it in O(1) - later
- [ ] 2. Round Robin schedule algo
- [ ] 3. Random schedule algo
- [ ] 4. Least Loaded schedule algo
- [x] 5. Port 5000
- [ ] 6. Port 5001, currently code implemented on master
- [ ] # 7. Usage of threads?? IMPORTANT 
