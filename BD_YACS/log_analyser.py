from docx import Document
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
def mean_median_dump(log_dict, where):
    duration = [x1 - x2 for (x1, x2) in zip(log_dict['end_time'].values(), log_dict['arrival_time'].values())]
    mean_time = np.mean(duration)
    median_time = np.median(duration)

    str1 = "\t1. Mean Completion Time : " + '{:.4f}'.format(mean_time) + " seconds\n" 
    str2 = "\t2. Median Completion Time : " + '{:.4f}'.format(median_time) + " seconds\n"

    if(where == 1):
        str3 = 'Job Analysis\n'
    else:
        str3 = 'Task Analysis\n'
    
    p_object = document.add_paragraph("\n" + str3)
    p_object.add_run(str1)
    p_object.add_run(str2)

    str3 = 'Plot'
    if(where != 1):
        p_object = document.add_paragraph(str3)
        


    


def plotter(log_dict):
    imgname = log_dict['algo'][0] # Getting the name of the algorithm
    imgname += "_plot_image.png" # obtaining the appropriate name to save the plot later
    imgname = "img/" + imgname
    doc_name = log_dict['algo'][0] + "_Logs_Analysis.docx"
    info = [] # list of tuples [('arrival_time', 'worker_id')] in order to sort in ascending order of 'arrival time'
    unique_worker_set = set()
    check_if_done = dict()
    end_time_list = []

    for i, j in zip(log_dict['arrival_time'].values(), log_dict['worker_id'].values()):
        info.append((i, j)) # populating the list of tuples
        unique_worker_set.add(j)

    for i, j in zip(log_dict['end_time'].values(), log_dict['worker_id'].values()):
        check_if_done[i] = j
        end_time_list.append(i)

    graph_dict = dict()
    graph_dict['time'] = list()
    for i in unique_worker_set:
        graph_dict[i] = list()           # dictionary to store the number of tasks assigned to each worker every time a task arrives for scheduling

    info.sort(key = lambda x : x[0]) # sorting the list of tuples
    for j, i in info:
        worker_list = list(unique_worker_set) # set of all the workers
        graph_dict['time'].append(j) # keying in the arrival time of each task

        if graph_dict[i] == []:
            graph_dict[i] = [1] # when the first task of the job comes in, we initialize the task count of the worker that is alloted this task
        else:
            top = len(graph_dict[i]) - 1
            graph_dict[i].append(graph_dict[i][top] + 1) # updating the task count for the worker that was alloted this task
        
        worker_list.remove(i) # remove the worker that was alloted this task from the list of all workers
        for k in worker_list:
            top = len(graph_dict[k]) - 1
            if top == -1:
                graph_dict[k].append(0)
            else:
                graph_dict[k].append(graph_dict[k][top]) #keeping the new task count of the other workers same as the previously updated task count
        
        for end_time in end_time_list:
            if end_time <= j:
                worker_id = check_if_done[end_time]
                top = len(graph_dict[worker_id]) - 1
                graph_dict[worker_id][top] = graph_dict[worker_id][top] - 1
                end_time_list.remove(end_time)

        
    # plotting the graph
    x_axis = list(range(1, len(info) + 1))
    legend_text_list = []
    for i in graph_dict.keys():
        if i != 'time':
            plt.plot(x_axis, graph_dict[i])
            legend_text_list.append('Worker ' + str(i))

    plt.xlabel('Arrival time of a task')
    plt.ylabel('Number of tasks scheduled for each worker') 
    # plt.legend(['worker 0', 'worker 1', 'worker 2'])
    plt.legend(legend_text_list)
    plt.title('Number of tasks scheduled on each machine against time')
    plt.savefig(imgname)
    plt.show(block=False)
    plt.close()
    document.add_picture(imgname)
    document.save(doc_name)


document = Document()

# Analysing logs/job_logs.csv
df = pd.read_csv("logs/job_log.csv")
if not df.empty: 
    # Converting the dataframe 'df' into a dictonary 'job_log_dict'
    job_log_dict = df.to_dict()
    doc_heading = job_log_dict['algo'][0] + " Scheduling Algorithm Analysis"
    document.add_heading(doc_heading,0)
    mean_median_dump(job_log_dict, 1)


# Analysing logs/task_logs.csv
df = pd.read_csv("logs/task_log.csv")
if not df.empty:
    # Converting the dataframe 'df' into a dictonary 'task_log_dict'
    task_log_dict = df.to_dict()
    mean_median_dump(task_log_dict, 2)
    plotter(task_log_dict)

