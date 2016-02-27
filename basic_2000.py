import pickle
data = pickle.load(open("data_2000.p", 'rb'))
print(data)

all_node = []
for key, value in data.iteritems():
    all_node.append(key)
    for item1 in value['refs']:
        all_node.append(item1)
    for item2 in value['cites']:
        all_node.append(item2)

print (set(all_node))