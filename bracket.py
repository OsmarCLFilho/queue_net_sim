import numpy as np
import matplotlib.pyplot as plt
import functools as fnt
from main import *

rng = np.random.default_rng()

queue_net = Network()

q1 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))
q2 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))
q3 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))
q4 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))

r1 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1/2))
r2 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1))

s1 = queue_net.add_queue(fnt.partial(rng.exponential, scale=1/4))

ep1 = queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), q1)
ep2 = queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), q2)
ep3 = queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), q3)
ep4 = queue_net.add_entry_point(fnt.partial(rng.exponential, scale=1), q4)

queue_net.add_route(q1, r1)
queue_net.add_route(q2, r1)
queue_net.add_route(q3, r2)
queue_net.add_route(q4, r2)

queue_net.add_route(r1, s1)
queue_net.add_route(r2, s1)

(queues_history, timestamps) = queue_net.simulate(100)

fig, ax = plt.subplots()

def draw_line_plot():
    ax.plot(timestamps, [i[0] for i in queues_history])
    ax.plot(timestamps, [i[1] for i in queues_history])
    ax.plot(timestamps, [i[2] for i in queues_history])
    ax.plot(timestamps, [i[3] for i in queues_history])
    ax.plot(timestamps, [i[4] for i in queues_history])
    ax.plot(timestamps, [i[5] for i in queues_history])
    ax.plot(timestamps, [i[6] for i in queues_history])

def draw_graph_plot():
    edges = [
        (q1, r1),
        (q2, r1),
        (q3, r2),
        (q4, r2),
        (r1, s1),
        (r2, s1)
    ]
    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(queues_history[0])))
    graph.add_edges_from(edges)

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

    return animation

# animation = draw_graph_plot()
# animation.save("bracket.mp4")

draw_line_plot()

plt.show()
