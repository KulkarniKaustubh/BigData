import json
import sys
from socket import *
import time
import threading
from datetime import datetime


""" parsing arguments"""
port = int(sys.argv[1])

work_id = sys.argv[2]
""" done"""



""" class definitions """

class Task:
	def __init__(self, task_id, duration, job_id, worker_id):
		self.worker_id = worker_id
		self.job_id = job_id
		self.task_id = task_id
		self.duration = duration
		self.done = False
		self.arrival_time = datetime.now().timestamp()
		self.end_time = -1
	def print(self):
		print("job_id: ",self.job_id, "worker_id: ", self.worker_id, "task_id: ", self.task_id, "arrival: ", self.arrival_time, "end: ",self.end_time ," duration: ", self.duration, "  done: ", self.done)
	def to_json(self):
		temp = {"job_id": self.job_id, "worker_id": self.worker_id, "task_id": self.task_id, "arrival_time": self.arrival_time, "end_time": self.end_time ,"duration": self.duration, "done": self.done}
		return temp

""" class definitions are over """



""" Shared variable definitions """
exe_pool = []
""" done """

"""
All semaphores are defined here
"""
lock = threading.Semaphore(1)
"""
Semaphore definitions end
"""


print(f"Worker {work_id} ready to recieve tasks from master.py")


"""
listener code
"""
def task_in():
	thread_dict = {}
	task_in_socket = socket(AF_INET,SOCK_STREAM) #init a TCP socket
	task_in_socket.bind(('',port)) #listen on port 5000, from requests.py
	task_in_socket.listen(3)
	while True:
		connectionSocket, addr = task_in_socket.accept()
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		#connectionSocket.shutdown(SHUT_RDWR)
		#connectionSocket.close()
		print()
		mssg = json.loads(message)
		#this will apend the task to exe pool
		received_task = Task(mssg['task_id'], mssg['duration'], mssg['job_id'], mssg['worker_id'])

		print(f"Received task {received_task.task_id} from : ", addr)

		# lock.acquire()
		# exe_pool.append(received_task)
		thread_dict[f"{received_task.task_id}"] = threading.Thread(target = task_exec, args = (received_task,))
		thread_dict[f"{received_task.task_id}"].start()
		# thread_dict[f"{received_task.task_id}"].join()
		# lock.release()

"""listener code ends"""




"""updater code"""
def task_out(task): # take a task as input to send it through .send
	# lock.acquire()
	with socket(AF_INET, SOCK_STREAM) as s:
		# s.bind(('',5001+int(task.task_id.split('_')[0])))
		print("created socket")
		s.connect(("localhost", 5001))
		print("connected")

		print(f"Sending {task.task_id} completed to master")
		#generalise the below line

		send_task=Task.to_json(task)

		message = json.dumps(send_task)
		s.send(message.encode())

		print(f"Sent task {task.task_id} completed...")
	#s.close()




"""executor code"""
def task_exec(task):

	while not task.done and task.duration != 0:
		time.sleep(0.1) # time.sleep(1)
		task.duration -= 1
		if task.duration == 0:
			task.end_time = datetime.now().timestamp()
			task.done=True
			task.print()

	'''
	time.sleep(task.duration)
	task.end_time = datetime.now().timestamp()
	task.done=True
	task.duration = 0
	task.print()
	time.sleep(0.1)
	'''
	lock.acquire()
	task_out(task)
	lock.release()
"""executor code ends"""



''' Running worker'''
listening_thread = threading.Thread(target = task_in)
# executing_thread = threading.Thread(target=task_exec)
#task_in()
listening_thread.start()
listening_thread.join()

# executing_thread.start()
#time.sleep(10)
