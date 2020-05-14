
import subprocess
import threading
from matplotlib import pyplot as plt

class Graph(threading.Thread):
   def __init__(self,x,y):
       threading.Thread.__init__(self)
       self.x = x
       self.y = y


   def run(self):
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.plot(self.x, self.y)  # Plot some data on the axes.
        ax.set_xlabel('x Time ')  # Add an x-label to the axes.
        ax.set_ylabel('y Car life time')  # Add a y-label to the axes.
        ax.set_title("Simple Plot")  # Add a title to the axes.
        ax.grid()
        plt.show()

#thread = Graph()
#thread.start()