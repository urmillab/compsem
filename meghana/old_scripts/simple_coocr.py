from bs4 import BeautifulSoup
import itertools
import xml.etree.ElementTree as ET
import os
import math
import numpy as np
from scipy import spatial
from xml.dom import minidom
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_TRAIN_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/train")
PATH_TO_TEST_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/test")
PATH_TO_ALL_DATA = os.path.join(os.getcwd(), "../resources/ace2005/ace2005/data/English_adj")

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

	# event_mention has child extent, which contains the whole phrase marked as an event
	extent = emention_el.find("extent")
	info = analyze_charseq(extent.find("charseq"))
	retv["phrase"] = info["content"]

	# event_mention has children event_mention_argument
	retv["arguments"] = [ ]
	for arg in emention_el.findall("event_mention_argument"):
		retv["arguments"].append(arg.attrib.get("ROLE"))

	return retv

#method description
def analyze_charseq(charseq_el):
    retv = { }
    retv["START"] = charseq_el.attrib.get("START")
    retv["END"] = charseq_el.attrib.get("END")
    retv["content"] = charseq_el.text

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

def find_coocr(PATH_TO_DATA):
	#create dictionary of coocr possibilites:
	#(life, movement, transaction, businesses, conflict, contact, personnel, justice) - so 8^8 possibilities 
	coocr_dict = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		coocr_dict[event_type] = {}
		for event_type_rep in EVENT_TYPES_TO_SUBTYPES:
			coocr_dict[event_type][event_type_rep] = 0

	# for e1 in coocr_dict: 
	# 	for e2 in coocr_dict[e1]: 
	# 		print (e1 + " - " + e2)
	# 		print(coocr_dict[e1][e2])
	
	#make a list of all sgm documents we want to analyze 
	xml_docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"): # this is the type of files we want to analyze
				xml_docs.append(os.path.join(dirpath, basename))

	
	for xml in xml_docs:
		event1 = None 
		event2 = None 
		fresh_doc = True 
		#xml info extraction
		event_anno_list = get_all_info(xml)
		for event in event_anno_list:
			e_info = analyze_event(event)
			e_type = e_info["type"].lower() 
			e_anchor = e_info["anchor"]
			e_phrase = e_info["phrase"]

			print(e_type + " - " + e_anchor + " - " +  e_phrase) 

			if fresh_doc: 
				event1 = e_type
				fresh_doc = False  
			else: 
				event2 = e_type 
				coocr_dict[event1][event2] += 1 
				event1 = event2 

		for e1 in coocr_dict: 
			for e2 in coocr_dict[e1]: 
				print (e1 + " - " + e2)
				print(coocr_dict[e1][e2])

	# for e1 in coocr_dict: 
	# 	for e2 in coocr_dict[e1]: 
	# 		print (e1 + " - " + e2)
	# 		print(coocr_dict[e1][e2])
	
if __name__ == '__main__':
	find_coocr(PATH_TO_ALL_DATA)
	
