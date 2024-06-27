import threading
import time

# Create a stop event
stop_event = threading.Event()

def heavy_calculation(name, stop_event):
    sum_squares = 0
    for i in range(1, 100000000):  # A large number for heavy computation
        if stop_event.is_set():
            print(f"Thread {name} received stop signal")
            break
        sum_squares += i * i
        # Simulate checking the stop event periodically
        if i % 100000 == 0:
            print(f"Thread {name} processed {i} numbers")
    print(f"Thread {name} is stopping with sum_squares = {sum_squares}")

# Create and start the thread
thread = threading.Thread(target=heavy_calculation, args=("Test", stop_event))
thread.start()

# Let the thread run for a specified time (e.g., 2 seconds)
time.sleep(2)

# Signal the thread to stop
stop_event.set()

# Wait for the thread to finish
thread.join()
