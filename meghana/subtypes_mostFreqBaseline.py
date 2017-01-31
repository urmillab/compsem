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

def get_event_subtype_counts(PATH_TO_DATA):
	#create dictionary of event types:
	#(life, movement, transaction, businesses, conflict, contact, personnel, justice)
	event_count_map = {}
	# type_subtype_dict = EVENT_TYPES_TO_SUBTYPES
	for event_type, subtype_list in EVENT_TYPES_TO_SUBTYPES.items():
		subtype_to_count_dict = {} 
		for subtype in subtype_list:
			subtype_to_count_dict[subtype] = 0 
		event_count_map[event_type] = subtype_to_count_dict

	#make a list of all the xml documents we want to analyze
	docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"): # this is the type of files we want to analyze
				docs.append(os.path.join(dirpath, basename))

	
	#analyze all docs 
	for document in docs:
		print(document)
		#get all event annotations from document 
		event_anno_list = get_all_info(document)
		for event in event_anno_list: 
			e_info = analyze_event(event) #dict of information about event 
			e_type = e_info['type'].lower()
			e_subtype = e_info['subtype'].lower()
			#counting num of occurences of each event type 

			event_count_map[e_type][e_subtype] += 1 

	# return event_count_map 
	
	# code to print out count results 	
	# total_num_e = 0
	# for e_type, subtype_dict in event_count_map.items():
	# 	print(str(e_type).upper())
	# 	for e_subtype, count in subtype_dict.items(): 
	# 		print(str(e_subtype) + ": " + str(count))
	# 		total_num_e += count
	# 	print
	# print("Total: " + str(total_num_e))

	return event_count_map 


if __name__ == '__main__':
	train_event_counts = get_event_subtype_counts(PATH_TO_TRAIN_DATA)
	test_event_counts = get_event_subtype_counts(PATH_TO_TEST_DATA)
	
	#event of highest frequency in training data 
	highest_freq_e = [] 
	counter = 0 
	for e_type, subtype_dict in train_event_counts.items(): 
		for e_subtype, count in subtype_dict.items(): 
			if count == counter: 
				highest_freq_e.append([e_type,e_subtype])
			elif count > counter: 
				del highest_freq_e[:]
				highest_freq_e.append([e_type,e_subtype])
				counter = count

	# #analyze test data 
	if len(highest_freq_e) == 1: 
		test_total_num_e = 0
		for e_type, subtype_dict in test_event_counts.items():
			for e_subtype, count in subtype_dict.items(): 
				test_total_num_e += count 

		pair = highest_freq_e[0]
		etype = pair[0]
		subtype = pair[1]
		type_to_subtype_dict = test_event_counts[etype]
		num_correct = type_to_subtype_dict[subtype]
		#test_event_counts[highest_freq_e[0]][highest_freq_e[1]]
		num_wrong = test_total_num_e - num_correct
		print ("Prediction: " + str(test_total_num_e) + "/" + str(test_total_num_e) + " of subtype " + subtype)
		print ("Actual: " + str(num_correct) + "/" + str(test_total_num_e) + " of subtype " + subtype)
		print (str(num_wrong) + " predicted wrong")
		print ("Accuracy: " + str(num_correct/float(test_total_num_e)))
	
	else:
		print("multiple event types of higeset frequency. Do calclations by hand for now")
		for e_type in highest_freq_e: 
			print(e_type)


