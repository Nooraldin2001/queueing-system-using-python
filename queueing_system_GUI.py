import tkinter as tk
from tkinter import ttk
import numpy as np
import queue
import copy
import matplotlib.pyplot as plt


class QueueSimulationApp:
    def __init__(self, master):
        self.master = master
        master.title("Queue Simulation")

        self.total_time_label = ttk.Label(master, text="Enter time for simulation (Hours):")
        self.total_time_label.grid(row=0, column=0, sticky="w")
        self.total_time_entry = ttk.Entry(master)
        self.total_time_entry.grid(row=0, column=1)

        self.arrival_rate_label = ttk.Label(master, text="Enter Job Arrival Rate (/Hour):")
        self.arrival_rate_label.grid(row=1, column=0, sticky="w")
        self.arrival_rate_entry = ttk.Entry(master)
        self.arrival_rate_entry.grid(row=1, column=1)

        self.service_rate_label = ttk.Label(master, text="Enter Job Service Rate (/Hour):")
        self.service_rate_label.grid(row=2, column=0, sticky="w")
        self.service_rate_entry = ttk.Entry(master)
        self.service_rate_entry.grid(row=2, column=1)

        self.simulate_button = ttk.Button(master, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=3, column=0, columnspan=2)

        self.plot_wait_button = ttk.Button(master, text="Plot Wait Times", command=self.plot_wait_times)
        self.plot_wait_button.grid(row=4, column=0, columnspan=2)

        self.plot_delay_button = ttk.Button(master, text="Plot Delay Times", command=self.plot_delay_times)
        self.plot_delay_button.grid(row=5, column=0, columnspan=2)

        self.wait_times = []
        self.delay_times = []

    def simulate(self):
        total_time = int(self.total_time_entry.get())
        job_arrival_rate = int(self.arrival_rate_entry.get())
        job_service_rate = int(self.service_rate_entry.get())

        job_queue = queue.Queue()
        current_process = None
        inter_arrival_time = []
        service_time = []
        arrival_time = []
        wait_time = []
        server_busy = False

        num_processes = int(np.random.poisson(job_arrival_rate) * total_time)
        num_processes_served = 0

        for i in range(num_processes):
            temp = int(np.random.exponential(1/job_arrival_rate) * 60 * 60)
            if i == 0:
                inter_arrival_time.append(0)
            else:
                inter_arrival_time.append(temp)
                
        while not len(service_time) == num_processes:
            temp = int(np.random.exponential(1/job_service_rate) * 60 * 60)
            if not temp < 1:
                service_time.append(temp)

        service_time_copy = copy.deepcopy(service_time)

        for i in range(num_processes):
            if i == 0:
                arrival_time.append(0)    
            else:
                arrival_time.append(arrival_time[i-1] + inter_arrival_time[i])
            wait_time.append(0)

        for i in range(total_time * 60 * 60):    
            if server_busy:
                for item in list(job_queue.queue):
                    wait_time[item] = wait_time[item] + 1
                service_time[current_process] -= 1
                if service_time[current_process] == 0:
                    server_busy = False
                    num_processes_served = num_processes_served + 1

            for j in range(num_processes):
                if i == arrival_time[j]:
                    job_queue.put(j)

            if not server_busy and not job_queue.empty():
                current_process = job_queue.get()
                server_busy = True

            sum_wait = 0
            sum_delay = 0

            for i in range(num_processes_served):
                sum_wait = sum_wait + wait_time[i]
                sum_delay = sum_delay + wait_time[i] + service_time_copy[i]
            
            if num_processes_served == 0:
                self.wait_times.append(0)
                self.delay_times.append(0)
            else:
                self.wait_times.append(sum_wait / (num_processes_served * 60 * 60))  
                self.delay_times.append(sum_delay / (num_processes_served * 60 * 60))

    def plot_wait_times(self):
        plt.plot([i+1 for i in range(len(self.wait_times))], self.wait_times)
        plt.ylabel("Average Wait Times")
        plt.xlabel("Time In Seconds")
        plt.show()

    def plot_delay_times(self):
        plt.plot([i+1 for i in range(len(self.delay_times))], self.delay_times)
        plt.ylabel("Average Delay Times")
        plt.xlabel("Time In Seconds")
        plt.show()

def main():
    root = tk.Tk()
    app = QueueSimulationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
