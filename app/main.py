from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId


#find keywords from text
def keywords(text):
	#open dictionary file and read all terms
	terms_file = open('./data/Dictionary.txt', 'r')
	terms = terms_file.readlines()

	#clean
	terms = [t.rstrip('\n') for t in terms]
	terms = [t.lower() for t in terms]

	#clean text to compare
	words = word_tokenize(text)
	words = [w.lower() for w in words]
	lmtzr = WordNetLemmatizer()
	words = [str(lmtzr.lemmatize(w)) for w in words]

	#create bigrams and trigrams from words
	words_bigrams = [words[i:i+2] for i in xrange(len(words)-2)]
	words_trigrams = [words[i:i+3] for i in xrange(len(words)-3)]

	#convert list of lists to list of strings
	words_bigrams = [w[0] + ' ' + w[1] for w in words_bigrams]
	words_trigrams = [w[0] + ' ' + w[1] + ' ' + w[2] for w in words_trigrams]

	#combine all lists
	words = words + words_bigrams + words_trigrams

	#find common terms
	common_terms = set(terms) & set(words)
	common_terms = list(common_terms)

	#remove smaller keywords from larger keywords
	for term in common_terms:
		if ' ' in term:
			for t in common_terms:
				if (t in term and t != term):
					common_terms.remove(t)

	return common_terms


#find similarity between two words
def compare_words(word1, word2):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.sim

	if (collection.find_one({'name':word1}) and collection.find_one({'name':word2})):
		data = collection.find_one({'name':word1}, {'_id':0, 'similarity.'+word2:1})
		score = data['similarity'][word2]
	else:
		score = 0
	return score


#compare units
#get content from db, Description or LO (Learning Outcomes)
def get_content_from_db(unit, content):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.utasunits

	data = collection.find_one({'name':unit}, {'_id':0, content:1})
	return data[content]


def get_idfw(term, field):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.idfw

	data = collection.find_one({'name':term})
	return data[field]


def get_sim_score(source, target):
	values = []
	idfw = []
	sim_keywords = []
	results = []
	for word in source:
		max_sim = 0.0
		temp = []
		if word in target:
			max_sim = 1.0
			temp.append(max_sim)
		else:
			for t in target:
				temp.append(compare_words(word, t))

		if temp:
			max_sim = max(temp)
		else:
			max_sim = 0
		if max_sim > 0:
			sim_keywords.append(word)
		idf_wt = 0.0
		if get_idfw(word, 'count') is not 0:
			idf_wt = get_idfw(word, 'IDF')

		max_sim = max_sim * idf_wt
		values.append(max_sim)
		idfw.append(idf_wt)
	if sum(idfw) == 0:
		sim = 0
	else:
		sim = sum(values) / sum(idfw)

	return (sim, sim_keywords)


def compare_units(unit1, unit2, content):
	unit1_content = get_content_from_db(unit1, content)
	kw_unit1 = keywords(unit1_content)
	kw_unit2 = keywords(unit2)

	#get similarity scores
	sim_1 = get_sim_score(kw_unit1, kw_unit2)
	sim_2 = get_sim_score(kw_unit2, kw_unit1)
	sim_1_2 = sim_1[0]
	sim_2_1 = sim_2[0]
	#scale down similarity based on number of keywords
	if kw_unit2:
        	ratio1 = len(kw_unit1) / float(len(kw_unit2))
    	else:
        	ratio1 = 0

    	if kw_unit1:
        	ratio2 = len(kw_unit2) / float(len(kw_unit1))
    	else:
        	ratio2 = 0

    	if ratio1 < 0.2:
        	sim = (ratio1 * sim_1_2 + sim_2_1) / 2
    	elif ratio2 < 0.2:
        	sim = (sim_1_2 + ratio2 * sim_2_1) / 2
    	else:
        	sim = (sim_1_2 + sim_2_1) / 2

    	return (sim, sim_2[1])

#recommendation on the basis of similarity score and level of units
def get_recommendation(utasunit, level, description, lo):
	if utasunit == 'KIT101':
		sim_tup = compare_units('KIT101', description, 'Description')
		sim_score = sim_tup[0]
		if sim_score < 0.6093:
			sim = 0  #NOt similar
		else:
			if level == '2':
				sim = 2 #Similar
			elif level == '1':
				if sim_score > 0.6406:
					sim = 2
				else:
					sim = 1  #Cannot decide
	elif utasunit == 'KIT205':
		sim_tup = compare_units('KIT205', description, 'Description')
		sim_score = sim_tup[0]
		if level == '1':
			sim = 0  #Not similar
		elif level == '2':
			if sim_score < 0.6061:
				sim = 0
			elif sim_score > 0.67:
				sim = 2
			else:
				sim = 1

	return (sim_score, sim, sim_tup[1])

############ Database methods ###################

def save_history(utasunit, description, result, message, uni, code, lo, lo_keywords):
	data = {}
	data['Unit'] = utasunit
	data['Description'] = description
	data['Result'] = result
	data['Institute'] = uni
	data['Code'] = code
	data['Time'] = datetime.now()
	data['Message'] = message
	data['LO'] = lo
	data['lo_keywords'] = lo_keywords
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.history

	collection.insert(data)



def get_history():
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.history

	all_data = collection.find({})
	return all_data


def get_history_by_id(id):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.history

	data = collection.find_one({'_id':ObjectId(id)})
	return data

def delete_history_by_id(id):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.history

	collection.remove({'_id':ObjectId(id)})

def save_unit(utasunit, description, result, message, uni, code, lo, lo_keywords):

	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.units

	if collection.find({"Code" : code, "Institute" : uni}).count() == 0:
		data = {}
		data['Unit'] = utasunit
		data['Description'] = description
		data['Result'] = result
		data['Institute'] = uni
		data['Code'] = code
		data['Time'] = datetime.now()
		data['Message'] = message
		data['LO'] = lo
		data['lo_keywords'] = lo_keywords


		collection.insert(data)

def get_units():
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.units

	all_data = collection.find({})
	return all_data

def get_unit_by_id(id):
        client = MongoClient('localhost', 27017)
        db = client.app
        collection = db.units
        data = collection.find_one({'_id':ObjectId(id)})
        return data

def delete_unit_by_id(id):
	client = MongoClient('localhost', 27017)
	db = client.app
	collection = db.units

	collection.remove({'_id':ObjectId(id)})
