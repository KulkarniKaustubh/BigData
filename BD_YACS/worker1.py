import json
import sys
from socket import *
import time
import threading
from datetime import datetime


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
        self.worker_id = worker_id
        self.job_id = job_id
        self.task_id = task_id
        self.duration = duration
        self.done = False
        self.arrival_time = datetime.now().timestamp()
        self.end_time = -1

    def print(self):
        #print("job_id: ",self.job_id, "worker_id: ", self.worker_id, "task_id: ", self.task_id, "  duration: ", self.duration, "  done: ", self.done)
        print("job_id: ", self.job_id, "worker_id: ", self.worker_id, "task_id: ", self.task_id, "arrival: ",
              self.arrival_time, "end: ", self.end_time, " duration: ", self.duration, "  done: ", self.done)

    def to_json(self):
        temp = {"job_id": self.job_id, "worker_id": self.worker_id, "task_id": self.task_id,
                "arrival_time": self.arrival_time, "end_time": self.end_time, "duration": self.duration, "done": self.done}
        return temp


""" class definitions are over """


""" Shared variable definitions """
exe_pool = []
""" done """


""" initialising TCP socket """
# task_in_socket = socket(AF_INET,SOCK_STREAM) #init a TCP socket
# task_in_socket.bind(('',port)) #listen on port 5000, from requests.py
# task_in_socket.listen(3)
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


def task_in(port):
    thread_dict = {}
    task_in_socket = socket(AF_INET, SOCK_STREAM)  # init a TCP socket
    task_in_socket.bind(('', port))  # listen on port 5000, from requests.py
    task_in_socket.listen(3)
    while True:
        connectionSocket, addr = task_in_socket.accept()
        message = connectionSocket.recv(2048)  # recieve max of 2048 bytes
        # connectionSocket.shutdown(SHUT_RDWR)
        # connectionSocket.close()
        print()
        mssg = json.loads(message)
        # this will apend the task to exe pool
        received_task = Task(
            mssg['task_id'], mssg['duration'], mssg['job_id'], mssg['worker_id'])

        print(f"Received task {received_task.task_id} from : ", addr)

        # lock.acquire()
        # exe_pool.append(received_task)
        thread_dict[f"{received_task.task_id}"] = threading.Thread(
            target=task_out, args=(received_task,))
        thread_dict[f"{received_task.task_id}"].start()
        # thread_dict[f"{received_task.task_id}"].join()
        # lock.release()

        # sample_test.print()
        # this is a dummy line to mimic completion of the task
        """sample_test.done = True
		sample_test.print()"""
        # task_exec()
        # need to add task to exe pool and do the execution


"""listener code ends"""


"""updater code"""


def task_out(task):  # take a task as input to send it through .send
    # lock.acquire()
    time.sleep(task.duration)
    task.duration = 0
    task.end_time = datetime.now().timestamp()
    task.done = True
    task.print()
    send_task = Task.to_json(task)
    message = json.dumps(send_task)
    s=socket()
    print("created socket")
    try:
        print("In try")
        s.connect(('127.0.0.1',5001))
        s.send(message.encode())
    except:
        print("could not connect")
    print(f"Sent task {task.task_id} completed...")
    s.close()

"""updater code ends"""


''' Running worker'''
listening_thread = threading.Thread(target=task_in, args=(port,))
listening_thread.start()
listening_thread.join()
