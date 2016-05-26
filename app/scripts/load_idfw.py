import json
from pymongo import MongoClient

json_file = open('../data/idfw.json')
json_str = json_file.read()
json_data = json.loads(json_str)

#clean data to insert
for key in json_data:
	if '.' in key:
		new_key = key.replace('.', '')
		json_data[new_key] = json_data.pop(key)


for key, value in json_data.iteritems():
	if value['count'] == 0:
		value['IDF'] = 0.0

#convert dict to list of dicts
data = []
for key, value in json_data.iteritems():
	data.append({"name" : key, "count" : value['count'], "IDF" : value['IDF']})

#insert
client = MongoClient('localhost', 27017)

db = client.app

collection = db.idfw

collection.insert_many(data)
