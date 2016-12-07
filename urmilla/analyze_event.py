import xml.etree.ElementTree as ET
from itertools import zip_longest
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist
import os
import numpy as np
from scipy import spatial
from sklearn.metrics import jaccard_similarity_score
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_DATA = os.path.join(os.getcwd(), "../resources/ace2005/ace2005/data/English_adj")
PATH_TO_RESULT = os.path.join(os.getcwd(), "data")
WNL = WordNetLemmatizer()
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

def get_source(filename):
	tree = ET.parse(filename) # root: source_file
	root = tree.getroot() # child of root: document

	return root.attrib["SOURCE"]

def get_all_sources():
	
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
			sources[s] = 0

	for source, count in sources.items():
		print(source + ", " + str(count))

def generate_feature_file():
	docs = {}
	for t in DOCUMENT_TYPES:
		docs[t] = []

	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				f = os.path.join(dirpath, basename)
				s = get_source(f)
				
				#print(basename)
				# this is the type of files we want to analyze
				docs[s].append(os.path.join(dirpath, basename))

	event_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_map[event_type] = 0

	for t, doclist in docs.items():
		for d in doclist:
			filename, ext = os.path.splitext(os.path.basename(d))

			result_path = os.path.join(PATH_TO_RESULT, t, filename + ".xml")

			info_list = get_all_info(d)
			for i in info_list:
				info = analyze_event(i)
				e_type = info['type'].lower()
				event_map[e_type] += 1
		

	for e_type, count in event_map.items():
		print(str(e_type) + ": " + str(count))





			#root = ET.Element('root')
			#for info in info_list:
			#	root.append(info)

			#ET.ElementTree(root).write(result_path)



if __name__ == '__main__':
	generate_feature_file()