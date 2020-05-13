import matplotlib.pyplot as plt
import multiprocessing

class Graph:

    def __init__(self):
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.plot([0,3,6,7], [0,3,6,7])  # Plot some data on the axes.
        ax.set_xlabel('x Time ')  # Add an x-label to the axes.
        ax.set_ylabel('y Car life time')  # Add a y-label to the axes.
        ax.set_title("Simple Plot")  # Add a title to the axes.
        ax.grid()
        plt.show() #I think the code in the child will stop here until the graph is closed


    def multi_p(self):
        job_for_another_core = multiprocessing.Process(target=plot_a_graph,args=())
        job_for_another_core.start()

#the follow print statement will also be modified to demonstrate that it comes from the parent process, and should happen without substantial delay as another process performs the plotting operation:
        print(multiprocessing.current_process().name, "The main process is continuing while another process deals with plotting.")
