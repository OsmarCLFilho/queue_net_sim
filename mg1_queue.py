import numpy as np
import matplotlib.pyplot as plt
import functools as fnt
from main import *

rng = np.random.default_rng()

queue_net = Network()

queue_id = queue_net.add_queue(fnt.partial(rng.uniform, low=2, high=4))
# queue_id = queue_net.add_queue(lambda: abs(rng.normal(loc=0, scale=1)))
queue_net.add_entry_point(fnt.partial(rng.exponential, scale=4), queue_id)

(queues_history, timestamps) = queue_net.simulate(10000)

print("Clients in queue statistics:")
x = [i[0] for i in queues_history]
print("Mean: ", np.mean(x))
print("Variance: ", np.var(x))

from collections import deque
client_count = 0
starting_times = deque([])
waiting_times = []
for i in range(len(queues_history)):
    if queues_history[i][0] > client_count:
        starting_times.append(timestamps[i])

    if queues_history[i][0] < client_count:
        st = starting_times.popleft()
        waiting_times.append(timestamps[i] - st)

    client_count = queues_history[i][0]

print("Waiting time statistics:")
print("Mean: ", np.mean(waiting_times))

fig, ax = plt.subplots()

ax.plot(timestamps, [i[0] for i in queues_history])

plt.show()
