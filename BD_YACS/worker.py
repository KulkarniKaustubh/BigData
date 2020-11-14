import json
import sys
from socket import *
import time
import threading



""" parsing arguments"""
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
""" done"""



""" class definitions """

class Task:
	def __init__(self, task_id, duration, job_id, worker_id):
		self.task_id = task_id
		self.duration = duration
		self.done = False
		self.job_id = job_id
		self.worker_id = worker_id
	def print(self):
		print("job_id: ",self.job_id, "worker_id: ", self.worker_id, "task_id: ", self.task_id, "  duration: ", self.duration, "  done: ", self.done)
	def to_json(self):
		temp = {"job_id": self.job_id, "worker_id": self.worker_id, "task_id": self.task_id, "duration":self.duration, "done":self.done}
		return temp
""" class definitions are over """



""" Shared variable definitions """
exe_pool = []
""" done """


""" initialising TCP socket """
task_in_socket = socket(AF_INET,SOCK_STREAM) #init a TCP socket
task_in_socket.bind(('',port)) #listen on port 5000, from requests.py
task_in_socket.listen(3)
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

	while True:
		connectionSocket, addr = task_in_socket.accept()
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		print()
		mssg = json.loads(message)
		#this will apend the task to exe pool
		received_task = Task(mssg['task_id'], mssg['duration'], mssg['job_id'], mssg['worker_id'])

		print(f"Received task {received_task.task_id} from : ", addr)

		# lock.acquire()
		# exe_pool.append(received_task)
		thread_dict[f"{received_task.task_id}"] = threading.Thread(target = task_exec, args = (received_task,))
		thread_dict[f"{received_task.task_id}"].start()
		# lock.release()

		#sample_test.print()
		#this is a dummy line to mimic completion of the task
		"""sample_test.done = True
		sample_test.print()"""
		#task_exec()
		#need to add task to exe pool and do the execution

"""listener code ends"""




"""updater code"""
def task_out(task): # take a task as input to send it through .send
	with socket(AF_INET, SOCK_STREAM) as s:
		s.connect(("localhost", 5001))

		print(f"Sending {task.task_id} completed to master")
		#generalise the below line

		send_task=Task.to_json(task)

		message = json.dumps(send_task)
		s.send(message.encode())

		print(f"Sent task {task.task_id} completed...")

	# with socket(AF_INET, SOCK_STREAM) as s:
	# 	s.connect(("localhost", 5001))
	# 	print("Sending update to master")
	# 	#generalise the below line
	# 	task = Task.to_json(exe_pool[0])      ### won't work as of now ...till master is ready to accept updates.
	# 	message=json.dumps(send_task)
	# 	s.send(message.encode())
	# 	print('done...')
"""updater code ends"""




"""executor code"""
def task_exec(task):
	while not task.done and task.duration != 0:
		time.sleep(1)
		task.duration -= 1
		if task.duration == 0:
			task.done=True

	#lock.acquire()
	task_out(task)
	#lock.release()


	# while True:
	# 	for task in exe_pool:
	# 		# print('-'*60)
	# 		print(f"Executing task with id {task.task_id}")
	#
	# 		lock.acquire()
	# 		task.duration-=1
	# 		task.print()
	# 		if task.duration==0:
	# 			print(f"Task {task.task_id} has finished execution")
	# 			#task_out(send_task)
	# 			task.done = True
	# 			updater_thread=threading.Thread(target=task_out,args=(task,))
	# 			updater_thread.start()
	#
	# 			updater_thread.join()
	# 			exe_pool.remove(task)
	# 		lock.release()
	#
	# 		print("")
	# 		print('-'*60)

"""executor code ends"""



''' Running worker'''
listening_thread = threading.Thread(target = task_in)
# executing_thread = threading.Thread(target=task_exec)
#task_in()
listening_thread.start()

# executing_thread.start()
#time.sleep(10)
