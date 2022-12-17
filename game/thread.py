import typing
import threading


class myThread(threading.Thread):
   """
   Allow to execute a function f in a thread
   """

   def __init__(self, name:str, f:typing.Callable) -> None:
      """Initialise the thread

      :param str name: The name of the thread
      :param typing.Callable f: The function to execute in the thread
      """
      threading.Thread.__init__(self)
      self.name = name
      self.f = f

   def run(self) -> None:
      """Launch the thread
      """
      self.f()
