import queue
import requests

jobs = queue.Queue(maxsize=1000)


jobs.put(1)
jobs.put(2)
jobs.put(3)
jobs.put(4)


for n in list(jobs.queue):
    print(n)
    
print(jobs.get())

print("  ")
for n in list(jobs.queue):
    print(n)

