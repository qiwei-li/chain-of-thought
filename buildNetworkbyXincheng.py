import collections
import pickle
from getRefCiteSim import getRefs, getCites, getSimls
import operator
from keywordsModule import index_term as index

class buildNetwork(object):
	""" A citation/reference graph class
	
	Attributes: 
		data: A dictionary of article information
	"""	

	def __init__(self, layer_ref,nodes_ref,layer_cite,nodes_cite):
		self.data = {}
		# number of layers in ref direction
		self.layer_ref = layer_ref
		# number of ref papers in each layer
		self.nodes_ref = nodes_ref
		# number of layers in cite direction
		self.layer_cite = layer_cite
		# number of cite papers in each layer
		self.nodes_cite = nodes_cite
		self.training_data = {}

	def saveData(self, outfile):
		pickle.dump(self.data, open(outfile, "wb"))

	def saveTraningData(self,outfile):
		pickle.dump(self.training_data, open(outfile, "wb"))


	def fillEntry_ref(self, arnumber, layer):
		if not arnumber in self.data:
			self.data[arnumber] = {}
			self.data[arnumber]['refs'] = getRefs(arnumber)
			self.data[arnumber]['keywords'] = index(arnumber)
			#index function return "IEEE TERMS" of paper ID arnumber
			self.data[arnumber]['layer'] = layer

	def fillEntry_cite(self, arnumber, layer):
		if not arnumber in self.data:
			self.data[arnumber] = {}
			self.data[arnumber]['cites'] = getCites(arnumber)
			self.data[arnumber]['keywords'] = index(arnumber)
			self.data[arnumber]['layer'] = layer


	def getNextLayer_ref(self, curr_layer_lst):
		tmp = {}
		for num in curr_layer_lst:
			print "%d is processed"%(num)
			for ref in self.data[num]['refs']:
				print "    refer paper %d is accessed"%(ref)
				if not ref in self.data:
					if not ref in tmp:
						citation = len(getCites(ref))
						if citation > 1:
							tmp[ref] = {}
							tmp[ref]['citation'] = citation
							tmp[ref]['keywords'] = index(ref)
							tmp[ref]['similarity'] = len(set(self.data[num]['keywords'])&set(tmp[ref]['keywords']))
							tmp[ref]['repeat'] = 1
					else:
						siml = len(set(self.data[num]['keywords'])&set(tmp[ref]['keywords']))
						tmp[ref]['similarity'] = max(tmp[ref]['similarity'],siml)
						tmp[ref]['repeat'] += 1
		score = {}
		training_data = []
		print len(tmp)
		for ref in tmp:
			score[ref] = tmp[ref]['similarity']*tmp[ref]['citation']*tmp[ref]['repeat']
			# Candidate ref papers are given scores by similarity * citation * # of citations from last layer
			training_data.append([tmp[ref]['similarity'],tmp[ref]['citation'],tmp[ref]['repeat']])
		score = sorted(score.iteritems(), key=operator.itemgetter(1),reverse = True)
		maxIteration = min(len(score),self.nodes_ref)
		result = [0]*maxIteration
		for i in xrange(maxIteration):
			result[i] = score[i][0]
			print result[i]
			print tmp[result[i]]['similarity'],tmp[result[i]]['citation'],tmp[result[i]]['repeat']
		# Top nodes_ref papers are chosen for next layer
		return result,training_data

	def getNextLayer_cite(self, curr_layer_lst):
		tmp = {}
		for num in curr_layer_lst:
			for cite in self.data[num]['cites']:
				if not cite in self.data:
					if not cite in tmp:
						citation = len(getCites(cite))
						if citation > 10:
							tmp[cite] = {}
							tmp[cite]['citation'] = citation
							tmp[cite]['keywords'] = index(cite)
							tmp[cite]['similarity'] = len(set(self.data[num]['keywords'])&set(tmp[cite]['keywords']))
							tmp[cite]['repeat'] = 1
					else:
						siml = len(set(self.data[num]['keywords'])&set(tmp[cite]['keywords']))
						tmp[cite]['similarity'] = max(tmp[cite]['similarity'],siml)
						tmp[cite]['repeat'] += 1
		score = {}
		for cite in tmp:
			score[cite] = tmp[cite]['similarity']*tmp[cite]['citation']*tmp[cite]['repeat']
		score = sorted(score.iteritems(), key=operator.itemgetter(1),reverse = True)
		maxIteration = min(len(score),self.nodes_cite)
		result = [0]*maxIteration
		for i in xrange(maxIteration):
			result[i] = score[i][0]
			print result[i]
			print tmp[result[i]]['similarity'],tmp[result[i]]['citation'],tmp[result[i]]['repeat']
		return result

	def createRefGraph(self, seed):
		#seed is a list, though we usually start from a single paper
		layer = 0
		curr_layer_lst = seed
		while(layer < self.layer_ref):
			print("current layer nodes: ", curr_layer_lst)
			for num in curr_layer_lst:
				self.fillEntry_ref(num, layer)

			tmp_list = self.getNextLayer_ref(curr_layer_lst)
			curr_layer_lst = tmp_list[0]
			self.training_data[layer] = tmp_list[1]
			print tmp_list[1]
			layer += 1
			if layer == 1:
				layer_one_lst = curr_layer_lst
		for num in curr_layer_lst:
			self.fillEntry_ref(num, layer)
		layer = 0
		curr_layer_lst = seed
		for num in curr_layer_lst:
			self.data[num]['cites'] = getCites(num)
		while(layer>-self.layer_cite):
			layer -= 1
			curr_layer_lst = self.getNextLayer_cite(curr_layer_lst)
			for num in curr_layer_lst:
				self.fillEntry_cite(num,layer)
		for key, value in self.training_data.iteritems():
			print value

network = buildNetwork(7,7,0,5)
network.createRefGraph([6547194])
network.saveData("test3.p")
network.saveTraningData("trainingData.p")







