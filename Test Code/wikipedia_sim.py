# -*- coding: utf-8-sig -*-
import requests
import json
import os
import keywords_dict
from xml.etree import ElementTree


def compare_words(word1, word2):
    query = 'http://localhost:8080/wikipedia-miner/services/compare?term1=' + word1 + '&term2=' + word2
    result = requests.get(query, headers = {'connection':'close'})
    tree = ElementTree.fromstring(result.content)
    score = 0.0
    response = tree.find('Response')
    if response.keys()[0] == 'relatedness':
        score = float(response.get('relatedness'))

    #print word1 + ' ' + word2 + ' ' + str(score)
    return score

def one_way_sim(unit1, unit2):
    f = open('idfw.json')
    idfw = json.load(f)
    f.close()
    values = []
    idf_wt_v = []
    for word in unit1:
        max_sim = 0.0
        temp = []
        if word in unit2:
            max_sim = 1.0
            temp.append(max_sim)
        else:
            for target in unit2:
                temp.append(compare_words(word, target))
        if temp:
            max_sim = max(temp)
        else:
            max_sim = 0.0
        idf_wt = 0.0
        if idfw[word]['count'] is not 0:
            idf_wt = idfw[word]['IDF']
        max_sim = max_sim * idf_wt
        values.append(max_sim)
        idf_wt_v.append(idf_wt)
    if sum(idf_wt_v) == 0:
        sim = 0
    else:
        sim = sum(values) / sum(idf_wt_v)

    return sim

#similarity between units
def compare_units(unit1, unit2):
    kw_unit1 = keywords_ngrams.keywords(unit1)
    kw_unit2 = keywords_ngrams.keywords(unit2)

    sim_1_2 = one_way_sim(kw_unit1, kw_unit2)
    sim_2_1 = one_way_sim(kw_unit2, kw_unit1)

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
    return sim

def units_sim(path):
    files = []
    result = {}
    count = 0
    for file in os.listdir(path):
        files.append(file)

    files = [os.path.join(path, file) for file in files]
    for file1 in files:
        filename = file1.lstrip(path + '\\').rstrip('.txt')
        result[filename] = {}
        for file2 in files:
            if file1 == file2:
                continue
            else:
                filename2 = file2.lstrip(path + '\\').rstrip('.txt')
                if filename2 in result:
                    if filename in result[filename2]:
                        continue
                else:
                    result[filename][filename2] = compare_units(file1, file2)
                    count += 1
                    print 'Processed: ' + str(count)
    return result

def one_unit(unit, path):
    files = []
    result = {}
    count = 0
    for file in os.listdir(path):
        files.append(file)
    files = [os.path.join(path, file) for file in files]
    for file in files:
        filename = file.lstrip(path + '\\').rstrip('.txt')
        result[filename] = compare_units(unit, file)
        count += 1
        print "Processed: " + str(count)
    return result

#calculate similarity of units in one dir to all units of another directory
def two_dir_sim(source_path, target_path):
    data = {}
    count = 0
    for file in os.listdir(source_path):
        file = os.path.join(source_path, file)
        filename = file.lstrip(source_path + '\\').rstrip('.txt')
        data[filename] = one_unit(file, target_path)
        count += 1
    print "Processed: " + str(count)
    return data
