import json
import sys
from socket import * 
import time

try:
	port = int(sys.argv[1])
except IndexError:
	print("Worker port not given")
	print("Exiting ......")
	exit()

try:
	work_id = sys.argv[2]
except IndexError:
	print("Worker id not passed")
	print("Exiting ......")
	exit()


class task:
	def __init__(self, taskid, duration, jobid, workerid):
		self.taskid = taskid
		self.duration = duration
		self.done = False
		self.jobid = jobid
		self.workerid = workerid
	def print(self):
		print("jobid: ",self.jobid, "workerid: ", self.workerid, "taskid: ", self.taskid, "  duration: ", self.duration, "  done: ", self.done)


exe_pool = []
task_in_socket = socket(AF_INET,SOCK_STREAM) #init a TCP socket
task_in_socket.bind(('',port)) #listen on port 5000, from requests.py
task_in_socket.listen(3)
print("Worker ready to recieve tasks from master.py")

def task_in():
	while(1):
		connectionSocket, addr = task_in_socket.accept() 
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		print("Received job request from: ", addr)
		mssg = json.loads(message)
		#this will apend the task to exe pool
		sample_test = task(mssg['taskid'], mssg['duration'], mssg['jobid'], mssg['workerid'])
		exe_pool.append(sample_test)
		sample_test.print()
		#this is a dummy line to mimic completion of the task
		sample_test.done = True
		sample_test.print()
		#need to add task to exe pool and do the execution

def task_out():#take a task as input to send it through .send
	with socket(AF_INET, SOCK_STREAM) as s:
		s.connect(("localhost", 5001))
		send_task = task.to_json(jobs[0].map_tasks[0])
		message=json.dumps(send_task)
		s.send(message.encode())

task_in()

time.sleep(10)
