import logging
import threading
import random
import time

'''
with python condition variables we did not need to use the store lock
reference: https://docs.python.org/3/library/threading.html#condition-objects
'''

class BoundedBuffer:
	def __init__(self,capacity):
		self.store = [0 for i in range(capacity)]
		print(self.store)
		self.cap = capacity
		self.rF =0;
		self.wT =0;
		self.freeSlots = self.cap
		self.lock = threading.Lock()
		self.cvLock = threading.Lock()
		self.rCV = threading.Condition(self.cvLock)
		self.wCV = threading.Condition(self.cvLock)
		self.cvLock.acquire()
		self.wCV.notify_all()
		self.cvLock.release()

	def read(self,readerT):
		logging.info("reader: %s attempting to read",readerT)
		with self.rCV:
			logging.info("reader: %s successfully acquired cv lock",readerT)
			self.rCV.wait_for(self.canRead)
			# self.lock.acquire()
			logging.info("reader: %s successfully acquired store lock",readerT)
			readIndex = self.rF%self.cap
			message = self.store[readIndex]
			logging.info("reader: %s successfully read from index %d value %d",readerT,self.rF,message)
			self.rF+=1
			self.freeSlots+=1
			# self.lock.release()
			self.wCV.notify_all()
		return message

	def write(self,writerT, data):
		logging.info("writer: %s attempting to write value %d",writerT,data)
		with self.wCV:
			logging.info("writer: %s successfully acquired cv lock",writerT)
			self.wCV.wait_for(self.canWrite)
			# self.lock.acquire()
			writeIndex = self.wT%self.cap
			self.store[writeIndex]=data
			self.freeSlots-=1
			logging.info("writer: %s successfully wrote value %d at index %d",writerT,data,writeIndex)
			self.wT+=1
			# self.lock.release()
			self.rCV.notify_all()

	def canWrite(self):
		return self.freeSlots>0

	def canRead(self):
		return self.freeSlots!=self.cap


def writer(boundedBuffer,threadName):
	for i in range(1,101):
		boundedBuffer.write(threadName,i)

def reader(boundedBuffer,threadName):
	message = 0
	recvd_messages = []
	while (1):
		message = boundedBuffer.read(threadName)
		recvd_messages.append(message)
		if (message==100):
			logging.info("reader received all messages, as shown below")
			break
	logging.info(recvd_messages)



if __name__=="__main__":
	format = "%(asctime)s %(message)s"
	logging.basicConfig(format=format,datefmt="%H:%M:%S",level=logging.INFO)
	boundedBuffer = BoundedBuffer(5)
	readerT = threading.Thread(target=reader,args=(boundedBuffer,"reader"))
	writerT = threading.Thread(target=writer,args=(boundedBuffer,"writer"))
	readerT.start()
	writerT.start()
	readerT.join()
	writerT.join()
	logging.info("Main is going to finish now !!!")
