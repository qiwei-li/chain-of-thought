import networkx as nx
import pickle
import community
import collections
import matplotlib.pyplot as plt
from matplotlib import cm
import pygraphviz as pgv


def loadData(infile):
	return pickle.load(open(infile, "rb"))


def createGraph(infile, seed):
	data = loadData(infile)
	DG = nx.DiGraph()
	for node in data:
		DG.add_node(node)
		DG.node[node]['layer'] = data[node]['layer']
	
	for node in data:
		edges = [(node, ref) for ref in data[node]['refs'] if ref in data]
		DG.add_edges_from(edges)
	
	outfile = "test.png"
	pos = nx.pygraphviz_layout(DG)
	colors = [DG.node[node]['layer'] for node in DG]
	nx.draw_networkx(DG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size=90, with_labels=False)
	plt.savefig(outfile)
	plt.clf()

	### Graphviz
	A = nx.to_agraph(DG)
	layer_of_nodes = []
	layer = 0
	
	sorted_nodes = sorted(data.items(), key = lambda x: x[1]['layer'])
	layer_of_nodes = [k[0] for k in sorted_nodes if k[1]['layer'] == layer]
	while (len(layer_of_nodes) > 0):
		A.add_subgraph(layer_of_nodes, rank='same')
		layer += 1
		layer_of_nodes = [k[0] for k in sorted_nodes if k[1]['layer'] == layer]
	outfile = "test2.png"
	A.draw(outfile, prog='dot')	 									

	### Find Communities
	#seed = 7037476
	G = DG.to_undirected()
	partition = community.best_partition(G)
	num_of_communities = sorted(partition.values(), reverse=True)[0] + 1
	print "number of communities: ", num_of_communities

	# number of nodes in each communites
	values = [partition.get(node) for node in G]
	print "seed belongs to community ", partition.get(seed)
	counter = collections.Counter(values)
	print "number of nodes in each community: ", counter.most_common(num_of_communities)
	
	outfile = "test_communities.png"
	pos = nx.pygraphviz_layout(DG)
	colors = [partition.get(node) for node in DG]
	size_cm = 90
	size_sp = 180
	sizes = [size_cm + size_sp*(node==seed) for node in DG]
	
	nx.draw_networkx(DG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size = sizes, with_labels=False)
	#nx.draw_networkx_nodes(G, pos, nodelist=[seed], node_size=size_sp, node_color = [partition.get(seed)], with_labels=False)
	plt.savefig(outfile)
	plt.clf()

	### Find representatives in each community (naive way: based on degree centrality)
	degreeCentl = nx.in_degree_centrality(DG)
	print "representatives in each community: "
	community_index = 0
	representatives = []
	while(community_index < num_of_communities):
		nodes_lst = [node for node in DG if partition.get(node) == community_index]
		tmp = sorted(nodes_lst, key = lambda x:degreeCentl[x], reverse=True)[0:len(nodes_lst)/5]
		print tmp
		representatives += tmp
		community_index += 1
	# add the seed node
	representatives.append(seed)

	# representative graph
	RG = nx.DiGraph()
	for node in representatives:
		RG.add_node(node)

	for source in representatives:
		for target in representatives:
			if source != target and nx.has_path(DG, source, target):
				RG.add_edge(source, target) 
	
	outfile = "representative_graph.png"
	pos = nx.spring_layout(DG)
	size_cm = 180
	size_sp = 270
	colors = [partition.get(node) for node in RG]
	sizes = [size_cm + size_sp*(node==seed) for node in RG]
	nx.draw_networkx(RG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size = sizes, with_labels = True)
	plt.savefig(outfile)
	plt.clf() 															
