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
	def print(self):
		print("taskid: ", self.taskid, "  duration: ", self.duration)

class job:
	def __init__(self, jobid):
		self.jobid = jobid
		self.map_tasks = []
		self.reduce_tasks = []
	def print(self):
		print("Job          : ", self.jobid)
		print("map_tasks    : ")
		for i in self.map_tasks:
			i.print()
		print("reduce_tasks : ")
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


num_jobs = len(jobs)
for i in range(num_jobs):
	print('---------------------------------')
	jobs[i].print()
