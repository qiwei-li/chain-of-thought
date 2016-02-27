import pickle
import matplotlib.pyplot as plt
import networkx as nx

data = pickle.load(open("data_200.p", 'rb'))
G = nx.Graph()

for key, value in data.iteritems():
    for item in value['refs']:
        G.add_edge(item, key);

G.number_of_nodes()
G.number_of_edges()

nx.draw(G, with_labels=False, node_size=50)
plt.show()