# Plane Carrier

Dataset ---> [link](https://drive.google.com/drive/folders/10xfNXqxSpF_aHyhoo8dizGXUAxhOw_Va)


### Python Execution
```sh
$ python3 map1.py aircraft\ carrier < plane_carriers.ndjson  > test.txt  
$ python3 reduce1.py < test.txt  
$ python3 map2.py 'aircraft carrier' 100 < plane_carriers.ndjson > test.txt  
$ python3 reduce2.py < test.txt  
```

- Create 'user' dir  ```$ bin/hdfs dfs -mkdir /user ```
- Create 'username' dir under 'user' ```$ bin/hdfs dfs -mkdir /user/<username>```
- Create input dir  ```$ bin/hdfs dfs -mkdir input```
- Create output dir  ```$ bin/hdfs dfs -mkdir output```
- View dir under hadoop ```$ bin/hadoop fs -ls```
- Copy data file into HDFS ```$ bin/hdfs dfs -put /home/<...>/plane_carriers.ndjson input ```
- (Optional), add ```export HADOOP_STREAM=/home/<...>/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar``` to your ```~/.bashrc``` file in the end.


### Hadoop Execution 
```sh
$ bin/hadoop jar $HADOOP_STREAM -mapper 'python3 /home/<....>/BigData/assignment1/map1.py airplane' -reducer 'python3 /home/<....>/BigData/assignment1/reduce1.py' -input input/plane_carriers.ndjson -output output/task1_1

$ bin/hadoop jar $HADOOP_STREAM -mapper 'python3 /home/<....>/BigData/assignment1/map2.py airplane 100' -reducer 'python3 /home/<....>/BigData/assignment1/reduce2.py' -input input/plane_carriers.ndjson -output output/task2_1  

$ bin/hadoop jar $HADOOP_STREAM -mapper "python3 /home/<....>/BigData/assignment1/map1.py 'aircraft carrier'" -reducer 'python3 /home/<....>/BigData/assignment1/reduce1.py' -input input/plane_carriers.ndjson -output output/task1_2  

$ bin/hadoop jar $HADOOP_STREAM -mapper "python3 /home/<....>/BigData/assignment1/map2.py 'aircraft carrier' 100" -reducer 'python3 /home/<....>/BigData/assignment1/reduce2.py' -input input/plane_carriers.ndjson -output output/task2_2 
```


- To view o/p in browser open ```http://localhost:9870/explorer.html#/``` and navigate to your output dir.
- To delete the o/p file ```$ bin/hadoop fs -rm -r output/task1```
- start ```sbin/start-dfs.sh```, stop ```sbin/stop-dfs.sh```, view ```jps```

### Whats left !?
- [x] Hadoop streaming
- [x] Taking in variables from cmd line (not hardcoding)
- [x] Verify if eucledian dist func, is implemented the way they want it
- [x] Fix True/False o/p from reducer1 (automatically taken care)
- [x] Sort the o/p  of reducer2 (automatically taken care)
- [ ] Verify bad record function
- [ ] Cross verify outputs

