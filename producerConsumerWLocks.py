import threading
import logging
import random
import time


'''
Single producer consumer with simple locks.
'''

sentinel = object()

class Pipeline:
	def __init__(self):
		self.message=0
		self.producer_lock = threading.Lock()
		self.consumer_lock = threading.Lock()
		self.consumer_lock.acquire()

	def setMessage(self,message,tName):
		self.producer_lock.acquire()
		logging.info("Producer: %s is going to set the message.",tName)
		self.message = message
		logging.info("Producer: %s finished setting message.",tName)
		self.consumer_lock.release()

	def getMessage(self,tName):
		logging.info("Consumer: %s is going to read message",tName)
		self.consumer_lock.acquire()
		message = self.message
		logging.info("Consumer: %s finished reading message",tName)
		self.producer_lock.release()
		return message

def producer(pipeline,tName):
	for index in range(10):
		message = random.randint(1,101)
		logging.info("Producer got message %s",message)
		pipeline.setMessage(message,tName)
	pipeline.setMessage(sentinel,tName)

def consumer(pipeline,tName):
	message =0
	while message is not sentinel:
		message = pipeline.getMessage(tName)
		if message is not sentinel:
			logging.info("Consumer storing message %s",message)

if __name__=="__main__":
	format = "%(asctime)s %(message)s"
	logging.basicConfig(format=format,datefmt="%H:%M:%S",level=logging.INFO)
	pipeline = Pipeline()
	producerThread = threading.Thread(target=producer,args=(pipeline,"producer",))
	consumerThread = threading.Thread(target=consumer,args=(pipeline,"consumer",))
	producerThread.start()
	consumerThread.start()
	producerThread.join()
	consumerThread.join()
	logging.info("Main thread finished!!")