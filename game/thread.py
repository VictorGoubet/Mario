import threading

class myThread(threading.Thread):
   """
   Allow to execute a function f in a thread
   """

   def __init__(self, name, f):
      threading.Thread.__init__(self)
      self.name = name
      self.f = f
      
   def run(self):
      self.f()