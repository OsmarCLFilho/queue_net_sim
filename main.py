import numpy as np
import functools as fnt
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import networkx as nx

rng = np.random.default_rng()

class Queue:
    def __init__(self, service_time_gen):
        self.time_gen = service_time_gen
        self.waiting_count = 0

    def generate_time(self):
        return self.time_gen()


class EntryPoint(Queue):
    def __init__(self, arrival_time_gen, target):
        self.time_gen = arrival_time_gen
        self.target = target

def arg_min(arr): # Optional return
    arg_min = None
    min_val = None

    for (i, v) in enumerate(arr):
        if v == None:
            continue

        if min_val == None:
            arg_min = i
            min_val = v

        elif v < min_val:
            arg_min = i
            min_val = v

    return (arg_min, min_val)

class Network:
    def __init__(self):
            self.queue_list = []
            self.queue_adj = []
            self.entry_points = []

    def add_queue(self, service_time_gen):
        q = Queue(service_time_gen)
        self.queue_list.append(q)

        self.queue_adj.append([])

        return len(self.queue_list) - 1

    def add_route(self, origin, target):
        self.queue_adj[origin].append(target)

    def add_entry_point(self, arrival_time_gen, target):
        ep = EntryPoint(arrival_time_gen, target)
        self.entry_points.append(ep)

        return len(self.entry_points) - 1

    def nearest_event(self, queue_countdown, entry_point_countdown):
        (q_id, q_countdown) = arg_min(queue_countdown) # Optional
        (ep_id, ep_countdown) = arg_min(entry_point_countdown)

        if q_id == None or ep_countdown < q_countdown:
            return (ep_id, ep_countdown, 0) # 0 -> entry_point
        
        return (q_id, q_countdown, 1) # 1 -> queue

    def simulate(self, time_limit):
        curr_time = 0

        for i in range(len(self.queue_list)):
            self.queue_list[i].waiting_count = 0

        # Queues only countdown when not empty
        queue_countdown = [None for _ in range(len(self.queue_list))]
        entry_point_countdown = [0 for _ in range(len(self.entry_points))]

        for i in range(len(entry_point_countdown)):
            entry_point_countdown[i] = self.entry_points[i].generate_time()

        queues_history = []
        timestamps = []

        while curr_time < time_limit:
            (nearest_event_id, nearest_countdown, event_type) = self.nearest_event(queue_countdown, entry_point_countdown)

            # Walk forth in time
            for i in range(len(queue_countdown)):
                if queue_countdown[i] != None:
                    queue_countdown[i] -= nearest_countdown

            for i in range(len(entry_point_countdown)):
                entry_point_countdown[i] -= nearest_countdown

            curr_time += nearest_countdown

            # Operate on event
            if event_type == 0: # 0 -> entry_point
                ep_id = nearest_event_id
                entry_point_countdown[ep_id] = self.entry_points[ep_id].generate_time()

                target_id = self.entry_points[nearest_event_id].target
                self.queue_list[target_id].waiting_count += 1

                # Queue not empty anymore -> generate time
                if queue_countdown[target_id] == None:
                    queue_countdown[target_id] = self.queue_list[target_id].generate_time()

            else: # 1 -> queue
                queue_id = nearest_event_id
                self.queue_list[queue_id].waiting_count -= 1
                
                # Queue became empty -> remove time
                if self.queue_list[queue_id].waiting_count == 0:
                    queue_countdown[queue_id] = None

                else:
                    queue_countdown[queue_id] = self.queue_list[queue_id].generate_time()

                targets = self.queue_adj[queue_id]
                if len(targets) != 0:
                    target_id = targets[rng.integers(0, len(targets))]

                    self.queue_list[target_id].waiting_count += 1
                    if queue_countdown[target_id] == None:
                        queue_countdown[target_id] = self.queue_list[target_id].generate_time()

            waiting_counts = []
            for q in self.queue_list:
                waiting_counts.append(q.waiting_count)

            queues_history.append(waiting_counts)
            timestamps.append(curr_time)

        return (queues_history, timestamps)


if __name__ == "__main__":
    print("Hello, PC!")

    # Create a network of queues
    queue_net = Network()

    # Add queues with a given distribution for the service time
    queue_id1 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))
    queue_id2 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))
    queue_id3 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))

    # Add entry points with a given distribution for arrival time and a target queue
    queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), queue_id1)
    queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), queue_id3)

    # Add routes between queues
    queue_net.add_route(queue_id1, queue_id2)
    queue_net.add_route(queue_id3, queue_id2)

    # Simulate up until a given time limit
    (queues_history, timestamps) = queue_net.simulate(100)

    fig, ax = plt.subplots()
    graph = nx.DiGraph([(1,2), (3,2)])
    pos = nx.shell_layout(graph)

    def update(frame):
        ax.clear()

        nx.draw_networkx(
                graph,
                pos,
                node_color=queues_history[frame],
                node_size=[100 + 50*i for i in queues_history[frame]]
                )

        plt.draw()

    animation = ani.FuncAnimation(
            fig,
            update,
            frames=len(queues_history),
            interval=10,
            repeat=True
            )

    # animation.save("2expo_into_1expo.mp4")

    plt.show()
