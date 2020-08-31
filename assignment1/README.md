# Plane Carrier 

Dataset ---> [link](https://drive.google.com/drive/folders/10xfNXqxSpF_aHyhoo8dizGXUAxhOw_Va)

### Python Execution
```
python3 map2.py < plane_carriers.ndjson > test.txt  
python3 reduce2.py < test.txt
```

### Whats left !?
- [ ] Hadoop streaming 
- [ ] Taking in variables from cmd line (not hardcoding)
- [x] Verify if eucledian dist func, is implemented the way they want it
- [ ] Fix True/False o/p from reducer1
- [ ] Sort the o/p  of reducer2
- [ ] Verify bad record function
