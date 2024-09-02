import threading
import time

def worker(num):
    print(f"Thread {num} started")
    time.sleep(2)
    print(f"Thread {num} finished")

# Create multiple threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
start = time.time()
# Start all threads
for t in threads:
    t.start()

# Check if all threads are alive
for i, t in enumerate(threads):
    print(f"Is thread {i} alive? {t.is_alive()}")

# Wait for all threads to complete
for t in threads:
    t.join()
print(time.time()-start)
print("All threads have finished.")
