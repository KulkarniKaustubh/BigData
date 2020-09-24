#!/bin/sh
CONVERGE=1
rm v* log*

$HADOOP_HOME/bin/hadoop dfsadmin -safemode leave
$HADOOP_HOME/bin/hadoop fs -rm -r output/output* 

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
-mapper "python3 /home/<**** INSERT PATH ****>/BigData/assignment2/map1.py" \
-reducer "python3 /home/<**** INSERT PATH ****>/BigData/assignment2/reduce1.py '/home/<**** INSERT PATH ****>/BigData/assignment2/v'"  \
-input input/sample.txt \
-output output/output1 #has adjacency list


while [ "$CONVERGE" -ne 0 ]
do
	$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-*streaming*.jar \
	-mapper "python3 /home/<**** INSERT PATH ****>/BigData/assignment2/map2.py '/home/<**** INSERT PATH ****>/BigData/assignment2/v'" \
	-reducer "python3 /home/<**** INSERT PATH ****>/BigData/assignment2/reduce2.py" \
	-input output/output1 \
	-output output/output2
	touch v1
	$HADOOP_HOME/bin/hadoop fs -cat output/output2/* > /home/<**** INSERT PATH ****>/BigData/assignment2/v1
	CONVERGE=$(python3 check_conv.py >&1)
	$HADOOP_HOME/bin/hadoop fs -rm -r output/output2
	echo $CONVERGE

done
