import logging
import threading
import random
import time
import copy
import time


class sharedResource:
  def __init__(self):
    self.store = []
    self.rLock = threading.Lock()
    self.wLock = threading.Lock()
    self.numReaders = 0
    self.numWriters = 0

  def getRLock(self):
    with self.rLock:
      self.numReaders+=1
      if (self.numReaders==1):
        self.wLock.acquire()

  def releaseRLock(self):
    with self.rLock:
      self.numReaders-=1
      if (self.numReaders==0):
        self.wLock.release()
  
  def getWLock(self):
    self.wLock.acquire()

  def releaseWLock(self):
    self.wLock.release()
  
  def readStore(self):
    self.getRLock()
    retval = copy.deepcopy(self.store)
    self.releaseRLock()
    return retval

  def writeStore(self,item:int):
    self.getWLock()
    self.store.append(item)
    self.releaseWLock()

def reader(resource:sharedResource):
  time.sleep(random.random())
  logging.info("reader {} trying to read resouce".format(threading.current_thread().getName()))
  print(resource.readStore())

def writer(resource:sharedResource):
  time.sleep(random.random())
  logging.info("writer trying to append {} to resource".format(threading.current_thread().getName()))
  resource.writeStore(time.time())

if __name__=="__main__":
  format = "%(asctime)s %(message)s"
  logging.basicConfig(format=format,datefmt="%H:%M:%S",level=logging.INFO)
  resource = sharedResource()
  logging.info("spawning reader threads")
  for i in range(0,10):
    num = random.randint(0,100)
    if (num%2==0):
      t = threading.Thread(target=reader, args=(resource,))
      t.setName("reader_"+str(i))
    else:
      t = threading.Thread(target=writer, args=(resource,))
      t.setName("writer_"+str(i))
    t.start()
    t.join()
