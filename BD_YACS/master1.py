import json
import sys
from socket import *
import time
import random
import threading
from datetime import datetime
import os
import csv

# dt_object = datetime.fromtimestamp(arrival_time)
'''
arguments are parsed here
'''
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

if(os.path.isfile("logs/job_log.csv") and os.path.isfile("logs/task_log.csv")):
	os.remove("logs/job_log.csv")
	os.remove("logs/task_log.csv")
'''
done
'''
def logger(mssg,what):
	#with open("log.json") as r:
	#	old = json.load(r)
	#old.update(mssg)
	if(what == 'jobs'):
		filename = "logs/job_log.csv"
		column_name = ["algo", "job_id", "map_tasks_done", "reduce_tasks_done", "arrival_time", "end_time", "job_done"]
	else:
		filename = "logs/task_log.csv"
		column_name = ["algo", "job_id", "worker_id", "task_id", "arrival_time", "end_time", "duration", "done"]

	file_exists = os.path.isfile(filename)
	mssg["algo"] = schedule_algo
	with open(filename, 'a') as file:
		writer = csv.DictWriter(file, delimiter=',', lineterminator='\n',fieldnames=column_name)

		if (not file_exists):
			writer.writeheader()

		writer.writerow(mssg)
	file.close()


'''
class definitions
'''

class worker:
	def __init__(self, wid, slot, port):
		self.id = wid
		self.slot = slot
		self.occupied_slots = 0
		self.port = port
		self.mutex = threading.Semaphore(1) # to lock worker information
	def print(self):
		print(self.id, self.slot, self.port, sep=', ')
	def print_slot(self):
		print(f"--> Status of worker\n	worker id: {self.id}, worker total slots: {self.slot}, worker occupied slots: {self.occupied_slots} , worker port: {self.port}")



class task:
	def __init__(self, task_id, duration):
		self.task_id = task_id
		self.duration = duration
		self.done = False
		self.arrival_time = -1
		self.end_time = -1
	def print(self):
		print("task_id: {0} | duration: {1} | status: {2} ".format(self.task_id, self.duration, self.done))
	def to_json(self, job_id, worker_id):
		temp = {"job_id": job_id, "worker_id": worker_id, "task_id": self.task_id, "duration":self.duration, "done":self.done}
		return temp

class job:
	def __init__(self, job_id):
		self.job_id = job_id
		self.map_tasks = []
		self.reduce_tasks = []
		self.map_tasks_done = 0 #count number of map_task.done == True
		self.reduce_tasks_done = 0 #count number of red_task.done == True
		self.job_done = False #true only when (map_tasks_done = True and reduce_tasks_done = True)
		self.arrival_time = datetime.now().timestamp()
		self.end_time = -1
	def print(self):
		print("Job          : ", self.job_id, "\t status: ", self.job_done)
		print("map_tasks    : ", len(self.map_tasks),"       map_task_done: ", self.map_tasks_done)
		print("-------------------------------------------")
		for i in self.map_tasks:
			i.print()
		print("-------------------------------------------")
		print("reduce_tasks : ", len(self.reduce_tasks),"       red_task_done: ", self.reduce_tasks_done)
		print("-------------------------------------------")
		for i in self.reduce_tasks:
			i.print()
		print("-------------------------------------------")
	def to_json(self):
		temp = {"job_id": self.job_id,"map_tasks_done":self.map_tasks_done, "reduce_tasks_done":self.reduce_tasks_done, "arrival_time":self.arrival_time,"end_time":self.end_time,  "job_done":self.job_done}
		return temp
'''
done
'''

'''
global variables are declared here
'''
workers = [] #list of worker objects
worker_dict = {} #key , value where key=> worker_id and value is index in the above workers list
curr_worker_to_send=0
num_workers = 0

jobs = []# list of jobs
jobs_dict = {}# key , value where key=> job id and value is index in the above jobs list
num_jobs = 0
'''
done
'''

'''
all semaphores are declared here
'''
lock_workers=threading.Semaphore(1) # to lock shared variable 'workers'
lock_jobs=threading.Semaphore(1) # to lock the shared variable 'jobs'
'''
done
'''

print('Workers init started......')
work_count = 0
for line in summary['workers']:
	workers.append(worker(line['worker_id'], line['slots'], line['port']))
	worker_dict[line['worker_id']] = work_count #
	work_count += 1

for  i in workers:
	worker.print(i)
print(worker_dict)
num_workers = len(workers)
print('Workers init ended......')

'''
function definitions
'''
def scheduling_algo():

	if schedule_algo == 'RANDOM':
		while True:
			# print("Here bitch")
			# listen_updates()
			# lock_workers.acquire()
			i = random.randrange(0, len(workers))
			if workers[i].occupied_slots < workers[i].slot:
				return workers[i].id
			# lock_workers.release()

	if schedule_algo == 'RR':
		# workers_sorted = sorted(workers, key=lambda worker: worker.id)
		# num_workers = len(workers)
		# i = 0
		while True:
			if workers[curr_worker_to_send].occupied_slots < workers[curr_worker_to_send].slot:
				return workers[curr_worker_to_send].id
			curr_worker_to_send = (curr_worker_to_send + 1)%(num_workers)

	if schedule_algo == 'LL':
		while True:
			least_loaded = sorted(workers, key = lambda worker: worker.slot - worker.occupied_slots, reverse=True)
			if least_loaded[0].occupied_slots < least_loaded[0].slot:
				for idx in range(len(workers)):
					if least_loaded[0] == workers[idx]:
						return workers[idx].id

			# time.sleep(1)

def send_task_to_worker(task,job_id):
	#call this under listen_to_worker since they are in the same thread
	print("Sending task to worker...")
	i = scheduling_algo()
 	#eventually do this
	# need to decrement the slot of worker
	#port = 4000

	lock_workers.acquire()
	port = workers[worker_dict[i]].port
	workers[worker_dict[i]].occupied_slots += 1
	workers[worker_dict[i]].print_slot()
	lock_workers.release()

	with socket(AF_INET, SOCK_STREAM) as s:
		# workers[i].print_slot()
		s.connect(("localhost", port))
		send_task = task.to_json(job_id, i)
		message=json.dumps(send_task)
		s.send(message.encode())
	# workers[i].mutex.release()


def listen_to_requests():
	#opening this will make port 5000 active and recieve requests from requests.py
	request = socket(AF_INET,SOCK_STREAM) #init a TCP socket
	request.bind(('',5000)) #listen on port 5000, from requests.py
	request.listen(3)
	print("Master ready to recieve job requests from requests.py")
	job_count = 0
	while True:
		connectionSocket, addr = request.accept()
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		# print("Received job request from requests.py : ", addr)
		mssg = json.loads(message)
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close()

		j = job(mssg['job_id']) #init a job
		for maps_i in mssg['map_tasks']:
			j.map_tasks.append(task(maps_i['task_id'], maps_i['duration'])) #append all map_tasks of a job, by initing task
		for reds_i in mssg['reduce_tasks']:
			j.reduce_tasks.append(task(reds_i['task_id'], reds_i['duration']))#append all red_tasks of a job, by initing task

		lock_jobs.acquire()
		jobs.append(j) #add to list of jobs
		jobs_dict[mssg['job_id']] = job_count
		job_count += 1
		lock_jobs.release()

		for t in j.map_tasks:
			# sender_thread = threading.Thread(target=send_task_to_worker,args=(t,j.job_id,))
			# sender_thread.start()
			# sender_thread.join()
			send_task_to_worker(t,j.job_id)

	request.close()

# def scheduler():
# 	while True:
# 		for j in jobs:
# 			if j.map_tasks_done!=len(j.map_tasks):
# 				for map_task in j.map_tasks:
# 					if map_task.done !=True:
# 						send_task_to_worker(map_task,j.job_id)

def listen_updates():
	#opening this will make port 5001 active and recieve updates from worker.py
	update = socket(AF_INET, SOCK_STREAM) #init a TCP socket
	update.bind(('', 5001))
	update.listen(3)
	print("Master ready to recieve task updates from worker.py")

	while True:

		connectionSocket, addr = update.accept()
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		mssg = json.loads(message)
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close()
		# lock.acquire()
		# taking in the necessary values inorder to increase the slot count and to check if a job has finished executing.
		print("\n\n")
		print(mssg)
		task_id = mssg['task_id']
		worker_id = mssg['worker_id']
		done_flag = mssg['done']
		arrival_time = mssg['arrival_time']
		end_time = mssg['end_time']

		if done_flag == False:
			if '_M' in task_id:
				print("\nMap task with taskid ", task_id, " has failed.",end = '\n')
				break
			else:
				print("\nReduce task with taskid ", task_id, " has failed.",end = '\n')
				break

		job_id = task_id.split('_')[0]


		if '_M' in task_id: # The task that got completed is a map task

			job = jobs[jobs_dict[job_id]]
			for m_task in job.map_tasks:
				if m_task.task_id == task_id:

					lock_jobs.acquire()
					m_task.done = True # Updating the map task's done is True
					m_task.arrival_time = arrival_time
					m_task.end_time = end_time
					jobs[jobs_dict[job_id]].map_tasks_done += 1 # Incrementing the number of map tasks completed for that particular job
					lock_jobs.release()

					# workers[worker_dict[worker_id]].print_slot()
					print(f"Recieved task from worker: {worker_id}...")

					lock_workers.acquire()
					workers[worker_dict[worker_id]].occupied_slots -= 1
					workers[worker_dict[worker_id]].print_slot()
					lock_workers.release()
					logger(mssg, 'tasks')
					break

			#this is to send reduce tasks if all map tasks wer completed
			if((jobs[jobs_dict[job_id]].map_tasks_done == len(jobs[jobs_dict[job_id]].map_tasks)) and (jobs[jobs_dict[job_id]].job_done == False)):
				# send_task_to_worker(t, j.job_id)
				for t in jobs[jobs_dict[job_id]].reduce_tasks:
					# sender_thread1 = threading.Thread(target=send_task_to_worker,args=(t,job.job_id,))
					# sender_thread1.start()
					# sender_thread1.join()
					send_task_to_worker(t,jobs[jobs_dict[job_id]].job_id)
			# jobs[jobs_dict[job_id]].print() #added this to check i real task.done is getting updated

		else:

			job = jobs[jobs_dict[job_id]]
			for r_task in job.reduce_tasks:
				if r_task.task_id == task_id:

					lock_jobs.acquire()
					r_task.done = True #  Checking if the reduce task's done is True
					r_task.arrival_time = arrival_time
					r_task.end_time = end_time
					jobs[jobs_dict[job_id]].reduce_tasks_done += 1 # Incrementing the number of reduce tasks completed for that particular job
					lock_jobs.release()

					# workers[worker_dict[worker_id]].print_slot()
					print(f"Recieved task from worker: {worker_id}...")
					# workers[worker_dict[worker_id]].mutex.acquire()

					lock_workers.acquire()
					# print("\nlock acquired\n")
					workers[worker_dict[worker_id]].occupied_slots -= 1
					workers[worker_dict[worker_id]].print_slot()
					lock_workers.release()

					# print("\nlock released\n")
					# workers[worker_dict[worker_id]].mutex.release()
					logger(mssg, 'tasks')
					if( (len(jobs[jobs_dict[job_id]].map_tasks) == jobs[jobs_dict[job_id]].map_tasks_done) and (len(jobs[jobs_dict[job_id]].reduce_tasks) == jobs[jobs_dict[job_id]].reduce_tasks_done)): # To check if the entire job is done
						lock_jobs.acquire()
						jobs[jobs_dict[job_id]].job_done = True # Updating the job's done to True
						#job.end_time = datetime.fromtimestamp(r_task.end_time)
						jobs[jobs_dict[job_id]].end_time = r_task.end_time
						lock_jobs.release()
						temp = jobs[jobs_dict[job_id]].to_json()
						logger(temp,'jobs')
						print('Job ', job_id, ' was processed successfully', end = '\n')
						print("Arrival: {0}    End: {1}".format(jobs[jobs_dict[job_id]].arrival_time, jobs[jobs_dict[job_id]].end_time))
					break

			# jobs[jobs_dict[job_id]].print()

		# lock.release()
	update.close()
'''
done
'''

'''
running master
'''

listening_requests = threading.Thread(target = listen_to_requests)
listening_worker = threading.Thread(target = listen_updates)


listening_requests.start()
listening_worker.start()

num_jobs = len(jobs)
for i in range(num_jobs):
	print('---------------------------------')
	jobs[i].print()

time.sleep(10)
