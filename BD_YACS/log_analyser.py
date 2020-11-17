import pandas as pd
import numpy as np

def mean_median_dump(log_dict, where, FILE):
    duration = [x1 - x2 for (x1, x2) in zip(log_dict['end_time'].values(), log_dict['arrival_time'].values())]
    mean_time = np.mean(duration)
    median_time = np.median(duration)
    
    s = "*" * 25
    if(where == 1):
        a = "JOB"
    else:
        a = "TASK"
    FILE.write("{} {} {}\n\n".format(s, a, s))
    FILE.write("Mean {} Completion time : {} seconds\n".format(a, mean_time))
    FILE.write("Median {} Completion time : {} seconds\n".format(a, median_time))
    FILE.write("\n{} END {}\n\n\n\n".format(s, s))
    


# Analysing job_logs.csv
df = pd.read_csv("job_log.csv")
if not df.empty: 
    # Converting the dataframe 'df' into a dictonary 'job_log_dict'
    job_log_dict = df.to_dict()
    # Create the scheduling algorith specific file to store the analysis obtained
    filename = job_log_dict['algo'][0]
    filename += "_logs_analysis.txt"
    FILE = open(filename, "w")
    mean_median_dump(job_log_dict, 1, FILE)

# Analysing task_logs.csv
df = pd.read_csv("task_log.csv")
if not df.empty:
    # Converting the dataframe 'df' into a dictonary 'task_log_dict'
    task_log_dict = df.to_dict()
    mean_median_dump(task_log_dict, 2, FILE)
FILE.close()