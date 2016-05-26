import json
import os
from pymongo import MongoClient

path = '../data/sim'
files = []
for file in os.listdir(path):
	files.append(file)

files = [os.path.join(path, file) for file in files]

client = MongoClient('localhost', 27017)
db = client.app
collection = db.sim

for fp in files:
	json_file = open(fp)
	json_str = json_file.read()
	json_data = json.loads(json_str)


	for key in json_data:
	        if '.' in key:
        	        new_key = key.replace('.', '')
                	json_data[new_key] = json_data.pop(key)

	for key, value in json_data.iteritems():
		for k, v in value.iteritems():
			if '.' in k:
				new_k = k.replace('.', '')
				value[new_k] = value.pop(k)
	data = []
	for key, value in json_data.iteritems():
		data.append({"name" : key, "similarity" : value})


	collection.insert_many(data)
