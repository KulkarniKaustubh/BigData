import json
import sys
from socket import * 

try:
	config_path = sys.argv[1]
except IndexError:
	print("Config path not passed as arg")
	print("Exiting ......")
	exit()

try:
	schedule_algo = sys.argv[2]
except IndexError:
	print("Scheduling algorithm not specified - [RANDOM, RR, LL]")
	print("Exiting ......")
	exit()

with open(config_path) as f:
	summary = json.load(f)
f.close()



class worker:
	def __init__(self, wid, slot, port):
		self.id = wid
		self.slot = slot
		self.port = port
	def print(self):
		print(self.id, self.slot, self.port, sep=', ')


class task:
	def __init__(self, taskid, duration):
		self.taskid = taskid
		self.duration = duration
		self.done = False
	def print(self):
		print("taskid: ", self.taskid, "  duration: ", self.duration, "   status: ", self.done)

class job:
	def __init__(self, jobid):
		self.jobid = jobid
		self.map_tasks = []
		self.reduce_tasks = []
		self.map_tasks_done = False #true when all map_tasks don
		self.reduce_tasks_done = False #Truse when all reduce tasks done
		self.job_done = False #true only when (map_tasks_done = True and reduce_tasks_done = True)
	def print(self):
		print("Job          : ", self.jobid, "    status: ", self.job_done)
		print("map_tasks    : ", len(self.map_tasks),"       status: ", self.map_tasks_done)
		for i in self.map_tasks:
			i.print()
		print("reduce_tasks : ", len(self.reduce_tasks),"       status: ", self.reduce_tasks_done)
		for i in self.reduce_tasks:
			i.print()

workers = [] #list of worker objects
num_workers = 0

jobs = []
num_jobs = 0


print('Workers init started......')
for line in summary['workers']:
	workers.append(worker(line['worker_id'], line['slots'], line['port']))

for  i in workers:
	worker.print(i)
num_workers = len(workers)
print('Workers init ended......')

'''
#opening this will make port 5000 active and recieve requests from requests.py
request = socket(AF_INET,SOCK_STREAM) #init a TCP socket
request.bind(('',5000)) #listen on port 5000, from requests.py
request.listen(3)
print("Master ready to recieve job requests from requests.py")
k = 0 #as of for now only 3, dont know how to take as many as needed

while(k!=3):
	connectionSocket, addr = request.accept() 
	message = connectionSocket.recv(2048) # recieve max of 2048 bytes
	print("Received job request from: ", addr)
	mssg = json.loads(message)

	j = job(mssg['job_id']) #init a job
	for maps_i in mssg['map_tasks']:
		j.map_tasks.append(task(maps_i['task_id'], maps_i['duration'])) #append all map_tasks of a job, by initing task
	for reds_i in mssg['reduce_tasks']:
		j.reduce_tasks.append(task(reds_i['task_id'], reds_i['duration']))#append all red_tasks of a job, by initing task
	jobs.append(j) #add to list of jobs
	k += 1

request.close()
'''


#bruteforce
i = '{"job_id": "0", "map_tasks": [{"task_id": "0_M0", "duration": 2}, {"task_id": "0_M1", "duration": 4}, {"task_id": "0_M2", "duration": 3}, {"task_id": "0_M3", "duration": 4}], "reduce_tasks": [{"task_id": "0_R0", "duration": 1}]}'
mssg = json.loads(i) 
j = job(mssg['job_id']) #init a job
for maps_i in mssg['map_tasks']:
	j.map_tasks.append(task(maps_i['task_id'], maps_i['duration'])) #append all map_tasks of a job, by initing task
for reds_i in mssg['reduce_tasks']:
	j.reduce_tasks.append(task(reds_i['task_id'], reds_i['duration']))#append all red_tasks of a job, by initing task
jobs.append(j)
#bruteforce



num_jobs = len(jobs)
for i in range(num_jobs):
	print('---------------------------------')
	jobs[i].print()

