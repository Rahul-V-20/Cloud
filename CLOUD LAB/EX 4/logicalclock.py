import threading
import time
import random

class Process:
    def __init__(self, pid):
        self.pid = pid  # Process ID
        self.clock = 0  # Logical clock
        self.lock = threading.Lock()  # Lock to ensure safe clock updates in multi-threaded environment

    def send_message(self, receiver):
        # Increment clock before sending a message
        with self.lock:
            self.clock += 1
            print(f"Process {self.pid} sends message to Process {receiver.pid} with timestamp {self.clock}")
        # Send the clock value as the timestamp
        receiver.receive_message(self.clock)

    def receive_message(self, received_time):
        # Adjust clock to max(received_time, local_clock) + 1
        with self.lock:
            self.clock = max(self.clock, received_time) + 1
            print(f"Process {self.pid} received message. Updated timestamp: {self.clock}")

    def perform_event(self):
        # Increment clock for internal events
        with self.lock:
            self.clock += 1
            print(f"Process {self.pid} performs an internal event. Timestamp: {self.clock}")

def process_actions(process, processes):
    # Simulate random internal events and message passing
    for _ in range(3):  # Each process will perform 3 actions for this demo
        # Perform an internal event
        process.perform_event()
        time.sleep(random.uniform(0.1, 0.5))  # Simulate delay between events

        # Select a random other process to send a message to
        receiver = random.choice([p for p in processes if p != process])
        process.send_message(receiver)  # Send a message
        time.sleep(random.uniform(0.1, 0.5))  # Simulate delay

def simulate(num_processes=3):
    # Create a list of processes
    processes = [Process(i) for i in range(1, num_processes + 1)]

    # Create and start a thread for each process
    threads = []
    for process in processes:
        t = threading.Thread(target=process_actions, args=(process, processes))
        threads.append(t)
        

    # Wait for all threads to finish
    for t in threads:
        t.start()
        t.join()

simulate(num_processes=3)  # Simulate with 3 processes