import pandas as pd

# Analysing job_logs.csv

df = pd.read_csv("job_log.csv")

if not df.empty: 

    # Converting the dataframe 'df' into a dictonary 'job_log_dict'
    job_log_dict = df.to_dict()
    
    # will consist of the differences in arrival_time and end_time for each of the jobs
    duration = list() 

    # first appends the end times of each job to duration
    for i in job_log_dict.keys():
        if i == 'end_time':
            for j in job_log_dict[i].values():
                duration.append(j)

    # subtracts the arrival_time from the end_time for each of the jobs 
    k = 0
    for i in job_log_dict.keys():
        if i == 'arrival_time':
            for j in job_log_dict[i].values():
                duration[k] -= j
                k += 1



    mean_time = 0
    median_time = 0

    duration.sort()

    # Adding up the durations of each job and dividing by the number of jobs to obtain mean completion time
    for i in duration:
        mean_time += i
    
    mean_time /= len(duration)

    # Depending on the number of jobs, the median time of completion is obtained appropriately
    if len(duration) % 2 == 0:
        median_time = (duration[int(len(duration) / 2)] + duration[int(len(duration) / 2) + 1]) / 2
    else:
        median_time = duration[int(len(duration) / 2)]

    # Create the scheduling algorith specific file to store the analysis obtained
    filename = job_log_dict['algo'][0]
    filename += "_logs_analysis.txt"

    # Appending the analysis obtained to the file
    FILE = open(filename, "W")
    s = "*" * 25
    FILE.write("{} JOB {}\n\n".format(s, s))
    FILE.write("Mean Job Completion time : {} seconds\n".format(mean_time))
    FILE.write("Median Job Completion time : {} seconds\n".format(median_time))
    FILE.write("\n{} END {}\n\n\n\n".format(s, s))
    FILE.close()




# Analysing task_logs.csv

df = pd.read_csv("task_log.csv")

if not df.empty:

    # Converting the dataframe 'df' into a dictonary 'task_log_dict'
    task_log_dict = df.to_dict()
    
    # will consist of the differences in arrival_time and end_time for each of the tasks
    duration = list()

    # first appends the end times of each task to duration
    for i in task_log_dict.keys():
        if i == 'end_time':
            for j in task_log_dict[i].values():
                duration.append(j)

    # subtracts the arrival_time from the end_time for each of the tasks
    k = 0
    for i in task_log_dict.keys():
        if i == 'arrival_time':
            for j in task_log_dict[i].values():
                duration[k] -= j
                k += 1


    mean_time = 0
    median_time = 0

    duration.sort()

    # Adding up the durations of each task and dividing by the number of tasks to obtain mean completion time
    for i in duration:
        mean_time += i
    
    mean_time /= len(duration)

    # Depending on the number of tasks, the median time of completion is obtained appropriately
    if len(duration) % 2 == 0:
        median_time = (duration[int(len(duration) / 2)] + duration[int(len(duration) / 2) + 1]) / 2
    else:
        median_time = duration[int(len(duration) / 2)]

    # Open the scheduling algorith specific file to store the analysis obtained
    filename = task_log_dict['algo'][0]
    filename += "_logs_analysis.txt"

    # Appending the analysis obtained to this file
    FILE = open(filename, "a")
    s = "*" * 25
    FILE.write("{} TASK {}\n\n".format(s, s))
    FILE.write("Mean Task Completion time : {} seconds\n".format(mean_time))
    FILE.write("Median Task Completion time : {} seconds\n".format(median_time))
    FILE.write("\n{} END {}\n\n".format(s, s))
    FILE.close()
