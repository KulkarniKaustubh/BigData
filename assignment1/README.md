# Plane Carrier 

Dataset ---> [link](https://drive.google.com/drive/folders/10xfNXqxSpF_aHyhoo8dizGXUAxhOw_Va)

### Python Execution
``` 
python3 map1.py aircraft\ carrier < plane_carriers.ndjson  > test.txt  
python3 reduce1.py < test.txt  
python3 map2.py 'aircraft carrier' 100 < plane_carriers.ndjson > test.txt  
python3 reduce2.py < test.txt  
bin/hadoop jar '/home/sriram/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar'  -mapper 'python3 /home/sriram/BIG_DATA_FILES/map_t1.py airplane' -reducer 'python3 /home/sriram/BIG_DATA_FILES/red_t1.py' -input input/plane_carriers.ndjson -output output
```

### Whats left !?
- [ ] Hadoop streaming 
- [x] Taking in variables from cmd line (not hardcoding)
- [x] Verify if eucledian dist func, is implemented the way they want it
- [ ] Fix True/False o/p from reducer1
- [ ] Sort the o/p  of reducer2
- [ ] Verify bad record function
