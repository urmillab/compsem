import xml.etree.ElementTree as ET
import os
import math
import numpy as np
from scipy import spatial
from xml.dom import minidom
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_TRAIN_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/train")
PATH_TO_TEST_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/test")

#returns dictionary of information about the event 
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

#returns a list containing all annotations of type 'event' in the document 
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

def get_event_type_counts(PATH_TO_DATA):
	#create dictionary of event types:
	#(life, movement, transaction, businesses, conflict, contact, personnel, justice)
	event_count_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_count_map[event_type] = 0

	#make a list of all the xml documents we want to analyze
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"): # this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	for document in docs:
		#get all event annotations from document 
		event_anno_list = get_all_info(document)
		for event in event_anno_list: 
			e_info = analyze_event(event) #dict of information about event 
			e_type = e_info['type'].lower()
			#counting num of occurences of each event type 
			event_count_map[e_type] += 1

	return event_count_map 
	
	#code to print out count results 	
	# total_num_e = 0
	# for e_type, count in event_count_map.items():
	# 	print(str(e_type) + ": " + str(count))
	# 	total_num_e += count
	# print("Total: " + str(total_num_e))


if __name__ == '__main__':
	train_event_counts = get_event_type_counts(PATH_TO_TRAIN_DATA)
	test_event_counts = get_event_type_counts(PATH_TO_TEST_DATA)
	#event of highest frequency in training data 
	highest_freq_e = [] 
	counter = 0 
	for e_type, count in train_event_counts.items(): 
		if count == counter: 
			highest_freq_e.append(e_type)
		elif count > counter: 
			del highest_freq_e[:]
			highest_freq_e.append(e_type)
			counter = count

	#analyze test data 
	if len(highest_freq_e) == 1: 
		test_total_num_e = 0
		for e_type, count in test_event_counts.items():
			test_total_num_e += count 

		num_correct = test_event_counts[highest_freq_e[0]]
		num_wrong = test_total_num_e - num_correct
		print ("Prediction: " + str(test_total_num_e) + "/" + str(test_total_num_e) + " of type " + highest_freq_e[0])
		print ("Actual: " + str(num_correct) + "/" + str(test_total_num_e) + " of type " + highest_freq_e[0])
		print (str(num_wrong) + " predicted wrong")
		print ("Accuracy: " + str(num_correct/float(test_total_num_e)))
	
	else:
		print("multiple event types of higeset frequency. Do calclations by hand for now")
		for e_type in highest_freq_e: 
			print(e_type)


