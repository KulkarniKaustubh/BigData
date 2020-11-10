import json
import sys
from socket import * 


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
	def __init__(self, taskid, duration):
		self.taskid = taskid
		self.duration = duration
		self.done = False
	def print(self):
		print("taskid: ", self.taskid, "  duration: ", self.duration, "  done: ", self.done)


task_request = socket(AF_INET,SOCK_STREAM) #init a TCP socket
task_request.bind(('',port)) #listen on port 5000, from requests.py
task_request.listen(3)
print("Worker ready to recieve tasks from master.py")

while(1):
	connectionSocket, addr = task_request.accept() 
	message = connectionSocket.recv(2048) # recieve max of 2048 bytes
	print("Received job request from: ", addr)
	mssg = json.loads(message)
	print(mssg)