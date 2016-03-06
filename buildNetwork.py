import collections
import pickle
from getRefCiteSim import getRefs, getCites, getSimls

class buildNetwork(object):
	""" A citation/reference graph class
	
	Attributes: 
		data: A dictionary of article information
	"""	

	def __init__(self, MAX_ITERS, MAX_NODES):
		self.data = {}
		# max number of iterations
		self.MAX_ITERS = MAX_ITERS
		# max number of nodes at each iteration
		self.MAX_NODES = MAX_NODES	
	
	
	def saveData(self, outfile):
		pickle.dump(self.data, open(outfile, "wb"))


	def fillEntry(self, arnumber, layer):
		if not arnumber in self.data:
			self.data[arnumber] = {}
			self.data[arnumber]['refs'] = getRefs(arnumber)
			self.data[arnumber]['layer'] = layer


	def getNextLayer(self, curr_layer_lst):
		tmp = []
		for num in curr_layer_lst:
			for ref in self.data[num]['refs']:
				tmp.append(ref)
	
		counter = collections.Counter(tmp)
		next_layer_lst = [k[0] for k in counter.most_common(self.MAX_NODES)]		
		return next_layer_lst


	def createRefGraph(self, arnumber):
		layer = 0
		self.fillEntry(arnumber, layer)
		curr_layer_lst = self.data[arnumber]['refs']
		layer = 1

		while(layer < self.MAX_ITERS):
			print "current layer nodes: ", curr_layer_lst
			for num in curr_layer_lst:
				self.fillEntry(num, layer)
			
			curr_layer_lst = self.getNextLayer(curr_layer_lst)
			layer += 1
			
		
			




