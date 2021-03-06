import shutil
import xml.etree.ElementTree as ET
#from itertools import zip_longest
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.probability import FreqDist
import os
import math
import numpy as np
#from scipy import spatial
from xml.dom import minidom
#from sklearn.metrics import jaccard_similarity_score
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_DATA = os.path.join(os.getcwd(), "../resources/ace2005/ace2005/data/English_adj")
PATH_TO_RESULT = os.path.join(os.getcwd(), "../resources/manualanno")
# TRAIN_FILE = os.path.join(os.getcwd(), "../resources/manualanno")
#TEST_FILE = os.path.join(os.getcwd(), "../resources/genre_split/test.xml")
THRESHOLD = 0.02
#WNL = WordNetLemmatizer()
BATCH_SIZE = 6
OUTPUT = "breakdown.txt"



def _grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def analyze_event(event_el):
	retv = { }
	retv["type"] = event_el.attrib.get("TYPE")
	retv["subtype"] = event_el.attrib.get("SUBTYPE")

	# event element has child event_mention
	emention_el = event_el.find("event_mention")

	# event_mention has child anchor, which contains the predicate
	anchor = emention_el.find("anchor")
	charseq_el = anchor.find("charseq")
	retv["anchor"] = charseq_el.text

	# event_mention has children event_mention_argument
	retv["arguments"] = [ ]
	for arg in emention_el.findall("event_mention_argument"):
		retv["arguments"].append(arg.attrib.get("ROLE"))

	return retv

def get_all_info(filename):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]

    #children of "document" include those with tag "event"
    info_list = []
    for anno in document_el: 
        if anno.tag == "event":
            info_list.append(anno)
    return info_list
            
def add_events_to_map(filename, event_map):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]

    #children of "document" include those with tag "event"
    for anno in document_el: 
        if anno.tag == "event":
            info = analyze_event(anno)
            anchor = WNL.lemmatize(info["anchor"]).lower()
            event_type = (info["type"], info["subtype"])

            print(anchor)
            if (event_type in event_map) and anchor:
            	event_map[event_type].add(anchor)
            else:
            	event_map[event_type] = set()
            	event_map[event_type].add(anchor)


def add_events(filename, event_map):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]

    #children of "document" include those with tag "event"
    for anno in document_el: 
        if anno.tag == "event":
            info = analyze_event(anno)
            anchor = WNL.lemmatize(info["anchor"]).lower()
            event_type = (info["type"].lower(), info["subtype"].lower())

            event_map[event_type] += 1

def add_args_to_map(filename, arg_dist_map):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]

    #children of "document" include those with tag "event"
    for anno in document_el: 
        if anno.tag == "event":
            info = analyze_event(anno)
            event_type = (info["type"].lower(), info["subtype"].lower())
            arguments = info["arguments"]

            count_vector = arg_dist_map[event_type]

            for role in arguments:
            	count_vector[EVENT_ROLES[role.lower()]] += 1

def output_latex_format(event_map):
	f = open(OUTPUT, 'w')
	for event_type in event_map:
		etype, stype = event_type
		f.write(etype + " " + stype + ": ")
		for batch in _grouper(BATCH_SIZE, event_map[event_type]):
			for i, anchor in enumerate(batch):
				if not anchor: continue
				if i == 0:
					f.write(anchor)
				else:
					f.write(" & " + anchor)
			f.write(r"\\")
		f.write("\n")
	f.close()

def analyze_event_clusters():
	event_map = {}
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				add_events_to_map(os.path.join(dirpath, basename), event_map)
	
	output_latex_format(event_map)
#
def analyze_events():
	event_map = {}

	for event_type in EVENT_TYPES_TO_SUBTYPES:
		subtypes = EVENT_TYPES_TO_SUBTYPES[event_type]
		for subtype in subtypes:
			event_map[(event_type, subtype)] = 0

	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				add_events(os.path.join(dirpath, basename), event_map)
	
#
def analyze_event_args(jaccard_similarity=True):
	arg_dist_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		subtypes = EVENT_TYPES_TO_SUBTYPES[event_type]
		for subtype in subtypes:
			arg_dist_map[(event_type, subtype)] = np.zeros((len(EVENT_ROLES),), dtype=np.int)

	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				add_args_to_map(os.path.join(dirpath, basename), arg_dist_map)

	for curr_event, curr_vector in arg_dist_map.items():
		max_event = None
		max_val = float("-inf")
		for comp_event, comp_vector in arg_dist_map.items():
			if curr_event == comp_event:
				continue

			result = 1 - spatial.distance.cosine(curr_vector, comp_vector)
			if jaccard_similarity:
				result = jaccard_similarity_score(curr_vector, comp_vector, normalize=True)

			if result >= max_val:
				max_event = comp_event
				max_val = result

		print(curr_event[0] + ", " + curr_event[1] + ": " + max_event[0] + ", " + max_event[1])

#
def get_source(filename):
	tree = ET.parse(filename) # root: source_file
	root = tree.getroot() # child of root: document
	#print root.attrib["SOURCE"]
	return root.attrib["SOURCE"]

#
def _get_all_sources():
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	sources = {}
	for d in docs:
		s = get_source(d)
		if s in sources:
			sources[s] += 1
		else:
			sources[s] = 1

	return sources

#
def get_source_type_counts():
	sources = _get_all_sources()

	total = 0
	for s, count in sources.items():
		print(str(s) + ": " + str(count))
		total += count
	print("Total: " + str(total))

#
def get_event_type_counts():
	event_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_map[event_type] = 0

	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	for d in docs:
		info_list = get_all_info(d)
		for i in info_list:
			info = analyze_event(i)
			e_type = info['type'].lower()
			event_map[e_type] += 1
		
	total = 0
	for e_type, count in event_map.items():
		print(str(e_type) + ": " + str(count))
		total += count
	print("Total: " + str(total))

def generate_split():
	thresholds = _get_all_sources()

	# train = open(TRAIN_FILE, 'w')
	# test = open(TEST_FILE, 'w')

	# Filter sources dict to find threshold
	for s, count in thresholds.items():
		thresholds[s] = math.ceil(THRESHOLD*count)

	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	current_counts = {}
	for s in thresholds:
		current_counts[s] = 0
		print (thresholds[s])

	# train_root = ET.Element('root')
	# test_root = ET.Element('root')
	manual_count = 0
	# test_count = 0
	for doc_path in docs:
		print("docs" + doc_path)
		s = get_source(doc_path)
		print("result of get_source" + s)
		all_events = get_all_info(doc_path)

		if current_counts[s] < thresholds[s]: #training data 
			# shutil.copy(doc_path, "/u/meghanac/Thesis/compsem/resources/manualanno")
			shutil.copy(doc_path, PATH_TO_RESULT)
			manual_count += len(all_events)
			#  add the .sgm file complement - so I can do manipulations 
			doc_path = doc_path[:-8]
			sgm_doc_path = doc_path + ".sgm"
			shutil.copy(sgm_doc_path, PATH_TO_RESULT)

		# else:									#test data 
		# 	shutil.copy(doc_path, "/u/meghanac/Thesis/compsem/resources/test_train_data_by_genre/test")
		# 	test_count += len(all_events)

		current_counts[s] += 1
		
	# train.write(minidom.parseString(ET.tostring(train_root, 'utf-8')).toprettyxml())
	# test.write(minidom.parseString(ET.tostring(test_root, 'utf-8')).toprettyxml())

	print("Manual set: " + str(manual_count))
	# print("Test set: " + str(test_count))

	# train.close()
	# test.close()



if __name__ == '__main__':
	generate_split()
