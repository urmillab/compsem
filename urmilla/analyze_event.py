import xml.etree.ElementTree as ET
from itertools import izip_longest
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist
import os
import numpy as np
from scipy import spatial

PATH_TO_DATA = os.path.join(os.getcwd(), "ace2005/ace2005/data/")
WNL = WordNetLemmatizer()
BATCH_SIZE = 6
OUTPUT = "breakdown.txt"

# Event roles
EVENT_ROLES = {
	"person" : 0,
	"place" : 1,
	"buyer" : 2,
	"seller" : 3,
	"beneficiary" : 4,
	"price" : 5,
	"artifact" : 6, 
	"origin" : 7,
	"destination" : 8,
	"giver" : 9,
	"recipient" : 10,
	"money" : 11,
	"org" : 12,
	"agent" : 13,
	"victim" : 14,
	"instrument" : 15,
	"entity" : 16,
	"attacker" : 17,
	"target" : 18,
	"defendant" : 19,
	"adjudicator" : 20,
	"prosecutor" : 21,
	"plaintiff" : 22,
	"crime" : 23,
	"position" : 24,
	"sentence" : 25,
	"vehicle" : 26,
	"time-after" : 27,
	"time-before" : 28,
	"time-at-beginning" : 29,
	"time-at-end" : 30,
	"time-starting" : 31,
	"time-ending" : 32,
	"time-holds" : 33,
	"time-within" : 34,
}

EVENT_TYPES_TO_SUBTYPES = {
	"life": ["be-born", "marry", "divorce", "injure", "die"],
	"movement" : ["transport"],
	"transaction" : ["transfer-ownership", "transfer-money"],
	"business" : ["start-org", "merge-org", "declare-bankruptcy", "end-org"],
	"conflict":  ["attack", "demonstrate"],
	"contact" : ["meet", "phone-write"],
	"personnel" : ["start-position", "end-position", "nominate", "elect"],
	"justice" : ["arrest-jail", "release-parole", "trial-hearing", "charge-indict", \
	 "sue", "convict", "sentence", "fine", "execute", "extradite", "acquit", "appeal",
	 "pardon"]
}

def _grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

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
    	print(arg.attrib.get("ROLE"))
        retv["arguments"].append(arg.attrib.get("ROLE"))

    return retv

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

            print(event_type, arguments)
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
	
	for event_type, count in event_map.items():
		print str(event_type) + " " + str(count)

def analyze_event_args():
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
		max_val = 0.0
		for comp_event, comp_vector in arg_dist_map.items():
			if curr_event == comp_event:
				continue

			result = 1 - spatial.distance.cosine(curr_vector, comp_vector)
			if result >= max_val:
				max_event = comp_event
				max_val = result

		print str(curr_event) + ": " + str(max_event)
		

if __name__ == '__main__':
	analyze_events()