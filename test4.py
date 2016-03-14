from buildNetwork import buildNetwork
from getRefCiteSim import getRefs, getCites, getSimls
from drawGraph_v2 import drawGraph
import pickle


#arnumber = 260747
#print getRefs(arnumber)

### build reference network
MAX_ITERS = 20
MAX_NODES = 5
g_ref = buildNetwork(MAX_ITERS, MAX_NODES, 'refs')
#arnumber = 7120028
arnumber = 7037476

#g_ref.createRefGraph(arnumber)
outfile = "refs_{0}_{1}_{2}.p".format(arnumber, MAX_ITERS, MAX_NODES)
#g_ref.saveData(outfile)

infile = outfile
plt = drawGraph(infile, arnumber, [], 'refs')
plt.draw()


### build citation network
MAX_ITERS = 10
MAX_NODES = 10
g_ref = buildNetwork(MAX_ITERS, MAX_NODES, 'cites')
arnumber = 7037476
community_nodes = pickle.load(open('seed_community.p', 'rb'))
#g_ref.createCiteGraph(arnumber, community_nodes)
outfile = "cites_{0}_{1}_{2}.p".format(arnumber, MAX_ITERS, MAX_NODES)
#g_ref.saveData(outfile)

#infile = outfile
#plt = drawGraph(infile, arnumber, community_nodes, 'cites')
#plt.draw()
