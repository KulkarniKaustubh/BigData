import json
import sys
from socket import * 
import time
import threading

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

"""
All semaphores are defined here
"""
lock=threading.Semaphore(1)

"""
Semaphore definitions end
"""

print("Worker ready to recieve tasks from master.py")


"""
listener code
"""
def task_in():
	while(1):
		connectionSocket, addr = task_in_socket.accept() 
		message = connectionSocket.recv(2048) # recieve max of 2048 bytes
		print("Received job request from: ", addr)
		mssg = json.loads(message)
		#this will apend the task to exe pool
		sample_test = task(mssg['taskid'], mssg['duration'], mssg['jobid'], mssg['workerid'])
		
		lock.acquire()
		exe_pool.append(sample_test)
		lock.release()
		
		#sample_test.print()
		#this is a dummy line to mimic completion of the task
		"""sample_test.done = True
		sample_test.print()"""
		#task_exec()
		#need to add task to exe pool and do the execution

"""listener code ends"""

"""updater code"""
def task_out(send_task):#take a task as input to send it through .send
	'''send_task.done=True
	print("here")						    ### use this as of now
	send_task.print()'''
	with socket(AF_INET, SOCK_STREAM) as s:
		s.connect(("localhost", 5001))
		print("###---sending update to master---###")
		#send_task = task.to_json(jobs[0].map_tasks[0])      ### won't work as of now ...till master is ready to accept updates.
		message=json.dumps(send_task)
		s.send(message.encode())
		print('done...')
"""updater code ends"""

"""executor code"""
def task_exec():
	while 1:
		for task in exe_pool:
			print('-'*60)
			print(f"executing task with id {task.taskid}")
			
			lock.acquire()
			task.duration-=1
			task.print()
			if task.duration==0:
				print(f"Task {task.taskid} has finished execution")
				#task_out(send_task)
				updater_thread=threading.Thread(target=task_out,args=(task,))
				updater_thread.start()
				
				updater_thread.join()
				exe_pool.remove(task)
			lock.release()
			
			print("")
			print('-'*60)
			
"""executor code ends"""

''' Running worker'''
listening_thread=threading.Thread(target=task_in)
executing_thread=threading.Thread(target=task_exec)
#task_in()
listening_thread.start()

executing_thread.start()
#time.sleep(10)



