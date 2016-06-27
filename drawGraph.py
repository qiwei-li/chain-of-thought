import networkx as nx
import pickle
import community
import collections
import matplotlib.pyplot as plt
from matplotlib import cm
import pygraphviz as pgv


def loadData(infile):
	return pickle.load(open(infile, "rb"))


def getYear(date_str):
        year = int(date_str.split(' ')[-1])
        return year


def community_keywords(data, partition):
	num_of_communities = sorted(partition.values(), reverse=True)[0] + 1
	keywords = {}
	community_index = 0
	while(community_index < num_of_communities):
		nodes_lst = [node for node in data if partition.get(node) == community_index]
	 	tmp = []
		for node in nodes_lst:
			tmp += [k for k in data[node]['ieee_terms']]
			#tmp += [k for k in data[node]['keywords']]
		counter = collections.Counter(tmp)
		keywords[community_index] = ' '.join([k[0] for k in counter.most_common(1)])
		community_index += 1
	return keywords


def community_distance(G, partition, seed, community):
	community_nodes_lst = [k for k in G.nodes() if partition.get(k) == community]
	distance = 0
	for node in community_nodes_lst:
		distance += nx.shortest_path_length(G, seed, node)
	return distance / float(len(community_nodes_lst))


def community_direct_connectivity(G, partition, c1, c2):
	c1_nodes_lst = [k for k in G.nodes() if partition.get(k) == c1]
	c2_nodes_lst = [k for k in G.nodes() if partition.get(k) == c2]
	
	for n1 in c1_nodes_lst:
		for n2 in c2_nodes_lst:
			if nx.has_path(G, n1, n2):
				for path in nx.all_shortest_paths(G, n1, n2):
					if set(path).issubset(set(c1_nodes_lst + c2_nodes_lst)):
						return True
	return False

	
def community_connectivity(G, partition, c1, c2):
	c1_nodes_lst = [k for k in G.nodes() if partition.get(k) == c1]
	c2_nodes_lst = [k for k in G.nodes() if partition.get(k) == c2]

	for n1 in c1_nodes_lst:
		for n2 in c2_nodes_lst:
			if nx.has_path(G, n1, n2):
				return True
	return False 		

				
def saveSeedCommunity(nodes_lst, outfile):
	with open(outfile, 'wb') as ff:
		pickle.dump(nodes_lst, ff)


def createGraph(infile, seed, flag):
	data = loadData(infile)
	DG = nx.DiGraph()
	for node in data:
		DG.add_node(node)
		DG.node[node]['layer'] = data[node]['layer']
	
	for node in data:
		edges = [(node, ref) for ref in data[node]['refs'] if ref in data]
		DG.add_edges_from(edges)

	### Plot graph, assigning each layer a different color	
	outfile = "test_layer_{0}.png".format(flag)
	pos = nx.pygraphviz_layout(DG)
	colors = [DG.node[node]['layer'] for node in DG.nodes()]
	size_cm = 90
        size_sp = 180
        sizes = [size_cm + size_sp*(node==seed) for node in DG.nodes()]

	nx.draw_networkx(DG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size=sizes, with_labels=False)
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
	outfile = "test2_{0}.png".format(flag)
	A.draw(outfile, prog='dot')	 									

	### Find Communities
	#seed = 7037476
	G = DG.to_undirected()
	partition = community.best_partition(G)
	num_of_communities = sorted(partition.values(), reverse=True)[0] + 1
	print "number of communities: ", num_of_communities

	# number of nodes in each communites
	values = [partition.get(node) for node in G.nodes()]
	seed_community = partition.get(seed)
	print "seed belongs to community ", seed_community
	seed_community_lst = [node for node in G.nodes() if partition.get(node) == seed_community]
	saveSeedCommunity(seed_community_lst, 'seed_community.p')
	counter = collections.Counter(values)
	print "number of nodes in each community: ", counter.most_common(num_of_communities)

	outfile = "test_communities_{0}.png".format(flag)
	pos = nx.pygraphviz_layout(DG)
	colors = [partition.get(node) for node in DG.nodes()]
	size_cm = 90
	size_sp = 180
	sizes = [size_cm + size_sp*(node==seed) for node in DG.nodes()]
	
	nx.draw_networkx(DG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size = sizes, with_labels=False)
	#nx.draw_networkx_nodes(G, pos, nodelist=[seed], node_size=size_sp, node_color = [partition.get(seed)], with_labels=False)
	plt.savefig(outfile)
	plt.clf()

	
	### Draw community graph (each community is denoted as one node)
	CG = nx.DiGraph()
	keywords = community_keywords(data, partition)
	for i in range(num_of_communities):
		CG.add_node(i)
		CG.node[i]['keywords'] = keywords[i]	

	for i in range(num_of_communities):
		if i == partition.get(seed):
			CG.node[i]['distance'] = 0
		else:
			CG.node[i]['distance'] = community_distance(DG, partition, seed, i) 	

	print nx.get_node_attributes(CG, 'distance')
	nodes_distance_lst = sorted(CG.nodes(), key = lambda x: CG.node[x]['distance'], reverse=True)
	for i in range(len(nodes_distance_lst)):
                target = nodes_distance_lst[i]
                for j in range(i+1, len(nodes_distance_lst)):
                        source = nodes_distance_lst[j]
                        if community_direct_connectivity(DG, partition, source, target):
                                CG.add_edge(source, target)
	"""
	for source in CG.nodes():
		for target in CG.nodes():
			if source != target and community_connectivity(DG, partition, source, target):
				CG.add_edge(source, target)

	for e in CG.edges():
		for k in CG.nodes():
			if e[0] != k and (e[0], k) in CG.edges() and (k, e[1]) in CG.edges():
				CG.remove_edge(e[0], e[1])
				break
	"""

	print CG.edges() 
	outfile = "test_concentrate_{0}.png".format(flag)
        pos = nx.pygraphviz_layout(CG)
        colors = [node for node in CG.nodes()]
        size_cm = 180
        size_sp = 270
        sizes = [size_cm + size_sp*(node==partition.get(seed)) for node in CG.nodes()]

        nx.draw_networkx(CG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size = sizes, with_labels=False)
        nx.draw_networkx_labels(CG, pos, labels = keywords)
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
		#tmp = sorted(nodes_lst, key = lambda x:degreeCentl[x], reverse=True)[0:1]
		print tmp
		representatives += tmp
		community_index += 1
	# add the seed node
	representatives.append(seed)

	# community representative graph
	RG = nx.DiGraph()
	for node in representatives:
		RG.add_node(node)
	
	nodes_time_lst = sorted(RG.nodes(), key = lambda x: getYear(data[x]['date']))
	for i in range(len(nodes_time_lst)):
		target = nodes_time_lst[i]
		for j in range(i+1, len(nodes_time_lst)):
			source = nodes_time_lst[j]
			if nx.has_path(DG, source, target):
				RG.add_edge(source, target)
				break
		
	# add direct reference edge
	#for node in nodes_time_lst:
	#	tmp = [k for k in data[node]['refs'] if k in nodes_time_lst]
	#	for ref in tmp:
	#		RG.add_edge(node, ref)
	"""						
	for source in representatives:
		for target in representatives:
			if source != target and nx.has_path(DG, source, target):
				RG.add_edge(source, target)
	
	edge_lst = RG.edges()
	for e in RG.edges():
		for k in representatives:
			if e[0] != k and (e[0], k) in RG.edges() and (k, e[1]) in RG.edges():
				RG.remove_edge(e[0], e[1])
				break
	"""	
	outfile = "representative_graph_{0}.png".format(flag)
	pos = nx.spring_layout(RG)
	size_cm = 180
	size_sp = 270
	colors = [partition.get(node) for node in RG]
	sizes = [size_cm + size_sp*(node==seed) for node in RG]
	nx.draw_networkx(RG, pos, node_color = colors, cmap=plt.get_cmap('jet'), node_size = sizes, with_labels = True)
	plt.savefig(outfile)
	plt.clf() 	
	
	# draw the "important" papers layer-by-layer
	layer = 0
	RG.node[seed]['layer'] = layer
	curr_layer = [seed]
	while(len(curr_layer) > 0):
		next_layer = list(set([e[1] for e in RG.edges() if e[0] in curr_layer]))
		layer += 1
		for node in next_layer:
			RG.node[node]['layer'] = layer
		curr_layer = next_layer
				
	A = nx.to_agraph(RG)
	layer = 0
	layer_of_nodes = [k for k in RG.nodes() if RG.node[k]['layer'] == layer]
	while (len(layer_of_nodes) > 0):
		A.add_subgraph(layer_of_nodes, rank='same')
		layer += 1
		layer_of_nodes = [k for k in RG.nodes() if RG.node[k]['layer'] == layer]
	outfile = "test3_{0}.png".format(flag)
	A.draw(outfile, prog='dot')
	"""
	# draw the "important" papers layer-by-layer
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
	"""


if __name__ == "__main__":
	pass

createGraph("refs_7037476_20_5.p",	7037476)