import threading
import logging
import time
import random


class FakeDB:
	def __init__(self,value):
		self.value = value
		self.lock = threading.Lock()

	def update(self,name):
		logging.info("Thread %s: starting update",name)
		local_copy = self.value
		local_copy+=1
		time.sleep(random.random())
		self.value = local_copy
		logging.info("Thread %s: finished update",name)

	def atomic_update(self,*args,**kwargs):
		name = args[0]
		family = args[1]
		dbname = kwargs["dbname"]
		logging.info("passed parameters are name %s family %s dbname %s",name,family,dbname)
		self.lock.acquire()
		logging.info("Thread %s: starting update",name)
		local_copy = self.value
		local_copy+=1
		time.sleep(random.random())
		self.value = local_copy
		logging.info("Thread %s: finished update",name)
		self.lock.release()



def thread_func(*args,**kwargs):
	name = args[0]
	logging.info("Thread %s: starting",name)
	time.sleep(random.random())
	logging.info("Thread %s: finishing",name)

if __name__=="__main__":
	format = "%(asctime)s %(message)s"
	logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
	threads = list()
	numThreads = 5
	myDb = FakeDB(0)
	logging.info("Main: before running thread.")
	logging.info("Setting up threads")
	for i in range(0,numThreads):
		threads.append(threading.Thread(target=myDb.atomic_update,args=(i+1,"atomic",),kwargs={"dbname":"myDb"}))
	for i in range(0,numThreads):
		threads[i].start()
	for thread in threads:
		thread.join()
	logging.info("Check myDb value: value is %d",myDb.value)
	logging.info("Main: all done!")
