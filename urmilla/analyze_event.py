import xml.etree.ElementTree as ET
from itertools import zip_longest
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.probability import FreqDist
import math
import operator
import os
import numpy as np
from random import shuffle
from scipy import spatial
from xml.dom import minidom
#from sklearn.metrics import jaccard_similarity_score
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_DATA = os.path.join(os.getcwd(), "../resources/ace2005/ace2005/data/English_adj")
TRAIN_FILE = os.path.join(os.getcwd(), "../resources/genre_split/train.xml")
TEST_FILE = os.path.join(os.getcwd(), "../resources/genre_split/test.xml")
PATH_TO_TYPE_SPLIT_DATA = os.path.join(os.getcwd(), "type split data")
THRESHOLD = 0.663
PER_TYPE_THRESHOLD = 0.01
#WNL = WordNetLemmatizer()
BATCH_SIZE = 6
OUTPUT = "breakdown.txt"



def _grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def analyze_event(event_el):
	retv = { }
	retv["anno"] = event_el
	retv["type"] = event_el.attrib.get("TYPE")
	retv["subtype"] = event_el.attrib.get("SUBTYPE")


	# event element has child event_mention
	emention_el = event_el.find("event_mention")

	# event_mention has child anchor, which contains the predicate
	anchor = emention_el.find("anchor")
	charseq_el = anchor.find("charseq")
	retv["anchor"] = charseq_el.text

	# event_mention has children event_mention_argument
	retv["arguments"] = []
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

def get_source_type_counts():
	sources = _get_all_sources()

	total = 0
	for s, count in sources.items():
		print(str(s) + ": " + str(count))
		total += count
	print("Total: " + str(total))

def get_event_type_counts(path, print_results=False):
	event_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_map[event_type] = 0

	docs = []
	for dirpath, dirnames, filenames in os.walk(path):
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
	
	if print_results:	
		total = 0
		for e_type, count in event_map.items():
			print(str(e_type) + ": " + str(count))
			total += count
		print("Total: " + str(total))

	return event_map

def get_events_per_document_average():
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	total_events = 0
	max_num_events = (0, None)
	min_num_events = (float("inf"), None)
	for d in docs:
		num_events = len(get_all_info(d))
		total_events += num_events
		if num_events > max_num_events[0]:
			max_num_events = (num_events, d)
		if num_events < min_num_events[0]:
			min_num_events = (num_events, d)
	

	print("Average # events per document: " + str(float(total_events)/len(docs)))
	print("Max # events: " + str(max_num_events[0]) + ", " + max_num_events[1])
	print("Min # events: " + str(min_num_events[0]) + ", " + min_num_events[1])

def generate_split():
	thresholds = _get_all_sources()

	train = open(TRAIN_FILE, 'w')
	test = open(TEST_FILE, 'w')

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

	train_root = ET.Element('root')
	test_root = ET.Element('root')
	train_count = 0
	test_count = 0
	for d in docs:
		s = get_source(d)
		all_events = get_all_info(d)

		if current_counts[s] < thresholds[s]:
			for i in all_events:
				train_root.append(i)
			train_count += len(all_events)
		else:
			for i in all_events:
				test_root.append(i)
			test_count += len(all_events)

		current_counts[s] += 1
		
	train.write(minidom.parseString(ET.tostring(train_root, 'utf-8')).toprettyxml())
	test.write(minidom.parseString(ET.tostring(test_root, 'utf-8')).toprettyxml())

	total = train_count + test_count
	print("Train set: " + str(train_count) + ' ,' + str(train_count/total))
	print("Test set: " + str(test_count) + ' ,' + str(test_count/total))

	train.close()
	test.close()


def count_event_sequences(length, top_n, fine_grain=False):
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	total_sequences = 0
	event_seq_count = {}
	event_seq_instances = {}
	for d in docs:
		events = []
		info_list = get_all_info(d)
		for i in info_list:
			info = analyze_event(i)
			if fine_grain:
				events.append((info["subtype"], info["anchor"]))
			else:
				events.append((info["type"], info["anchor"]))

		
		for i in range(len(events)):
			event_seq = []
			anchor_seq = []

			# Break when the seq length greater than remaining events
			if i + length > len(events):
				break

			# Get the sequence
			for j in range(i, i + length):
				event_seq.append(events[j][0])
				anchor_seq.append(events[j][1])

			# Add to map
			event_seq = tuple(event_seq)
			if event_seq in event_seq_count:
				event_seq_count[event_seq] += 1
			else:
				event_seq_count[event_seq] = 1

			if event_seq in event_seq_instances:
				event_seq_instances[event_seq].append(tuple(anchor_seq))
			else:
				event_seq_instances[event_seq] = [tuple(anchor_seq)]

			total_sequences += 1

	# Print top n event sequences
	sorted_seqs = sorted(event_seq_count.items(), key=operator.itemgetter(1))
	sorted_seqs.reverse()

	for seq, count in sorted_seqs[:top_n]:
		print('-'.join(seq) + ": " + str(count) + ", " + str(float(count)/total_sequences))

	if fine_grain:
		f = open("fg_sequences_" + str(length) + ".txt", 'w')
	else:
		f = open("cg_sequences_" + str(length) + ".txt", 'w')

	for seq, anchor_list in event_seq_instances.items():
		f.write('-'.join(seq) + '\n')
		for anchor in anchor_list:
			f.write(', '.join(anchor))
			f.write('; ')
		f.write('\n\n')
	f.close()

def create_test_sets_for_event_types():
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				# this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	events = {}
	for t in EVENT_TYPES_TO_SUBTYPES:
		events[t] = []

	for d in docs:
		info_list = get_all_info(d)
		for i in info_list:
			info = analyze_event(i)
			events[info["type"].lower()].append(info["anno"])
	
	for t, event_list in events.items():
		size_train_set = 0
		size_test_set = 0

		train_root = ET.Element('root')
		test_root = ET.Element('root')

		size = len(event_list)
		num_train_positive = int(PER_TYPE_THRESHOLD * size) if int(PER_TYPE_THRESHOLD * size) else 1

		print(t)
		print("Train (positive) set: " + str(num_train_positive))

		folder = os.path.join(PATH_TO_TYPE_SPLIT_DATA, t)
		if not os.path.isdir(folder):
			os.mkdir(folder)

		shuffle(event_list)
		for anno in event_list:
			if num_train_positive > 0:
				size_train_set += 1
				train_root.append(anno)
				num_train_positive -= 1
			else:
				size_test_set += 1
				test_root.append(anno)


		for other_t, other_event_list in events.items():
			if other_t == t:
				continue

			for e in other_event_list:
				size_train_set += 1
				train_root.append(e)

		train_set = open(os.path.join(folder,"train.xml"), 'w')
		test_set = open(os.path.join(folder, "test.xml"), 'w')

		train_set.write(minidom.parseString(ET.tostring(train_root, 'utf-8')).toprettyxml())
		test_set.write(minidom.parseString(ET.tostring(test_root, 'utf-8')).toprettyxml())

		
		print("Train (negative) set: " + str(size_train_set - num_train_positive))
		print("Test set: " + str(size_test_set))



if __name__ == '__main__':
	create_test_sets_for_event_types()