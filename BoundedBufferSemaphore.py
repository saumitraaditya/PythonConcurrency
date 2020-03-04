import logging
import threading
import random
import time



class BoundedBuffer:
	def __init__(self,capacity):
		self.store = [0 for i in range(capacity)]
		print(self.store)
		self.cap = capacity
		self.rF =0;
		self.wT =0;
		self.freeSlots = self.cap
		self.lock = threading.Lock()
		self.rSem = threading.Semaphore()
		self.wSem = threading.Semaphore(self.freeSlots)
		self.rSem.acquire()

	def read(self,readerT):
		logging.info("reader: %s attempting to read",readerT)
		self.rSem.acquire()
		logging.info("reader: %s successfully acquired read semaphore",readerT)
		self.lock.acquire()
		logging.info("reader: %s successfully acquired store lock",readerT)
		readIndex = self.rF%self.cap
		message = self.store[readIndex]
		logging.info("reader: %s successfully read from index %d value %d",readerT,self.rF,message)
		self.rF+=1
		self.wSem.release()
		self.lock.release()
		return message

	def write(self,writerT, data):
		logging.info("writer: %s attempting to write value %d",writerT,data)
		self.wSem.acquire()
		logging.info("writer: %s successfully acquired write semaphore",writerT)
		self.lock.acquire()
		writeIndex = self.wT%self.cap
		self.store[writeIndex]=data
		logging.info("writer: %s successfully wrote value %d at index %d",writerT,data,writeIndex)
		self.wT+=1
		self.rSem.release()
		self.lock.release()


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
