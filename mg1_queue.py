import numpy as np
import matplotlib.pyplot as plt
import functools as fnt
from main import *

rng = np.random.default_rng()

queue_net = Network()

# queue_id = queue_net.add_queue(fnt.partial(rng.uniform, low=2, high=4))
queue_id = queue_net.add_queue(lambda: abs(rng.normal(loc=0, scale=1)))
queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), queue_id)

(queues_history, timestamps) = queue_net.simulate(10)

for i in range(len(queues_history)):
    print(timestamps[i], queues_history[i])

fig, ax = plt.subplots()

ax.plot(timestamps, [i[0] for i in queues_history])

plt.show()
