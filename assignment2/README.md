# Page Rank Algorithm implementation with Map Reduce

### Execution
Ensure that you have a input, output dir under /user/(username). The same can be achieved by :
```sh
$ $HADOOP_HOME/bin/hdfs dfs -mkdir /user
$ $HADOOP_HOME/bin/hdfs dfs -mkdir /user/(desired username)
$ $HADOOP_HOME/bin/hdfs dfs -mkdir input
$ $HADOOP_HOME/bin/hdfs dfs -mkdir output
```
After this fix all paths in iterate-hadoop.sh.
You may have to modify the commands if in case the same commands doesn't work for the hadoop version you have installed.
Then run :
```sh
$ sh iterate-hadoop.sh
```
Open <b>localhost:9870</b> to browse hdfs and see o/p.


### Whats left !?
- [x] Basic outline of task1 and task2
- [x] Hadoop streaming of task1 and task2
- [x] Take care of key error
- [x] Run the hadoop script, successfully
- [ ] Verify output, number of iterations


