from bs4 import BeautifulSoup
import itertools
import xml.etree.ElementTree as ET
import os
import math
import numpy as np
# from scipy import spatial
from xml.dom import minidom
from constants import EVENT_ROLES, EVENT_TYPES_TO_SUBTYPES, DOCUMENT_TYPES

PATH_TO_TRAIN_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/train")
PATH_TO_TEST_DATA = os.path.join(os.getcwd(), "../resources/test_train_data_by_genre/test")
PATH_TO_ALL_DATA = os.path.join(os.getcwd(), "../resources/manualanno")

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

def annotate_text(PATH_TO_DATA):
	#create dictionary of event types:
	#(life, movement, transaction, businesses, conflict, contact, personnel, justice)
	event_count_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_count_map[event_type] = 0

	#make a list of all the xml documents we want to analyze
	sgm_docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".sgm"): # this is the type of files we want to analyze
				sgm_docs.append(os.path.join(dirpath, basename))

	#make a list of all sgm documents we want to analyze 
	xml_docs = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"): # this is the type of files we want to analyze
				xml_docs.append(os.path.join(dirpath, basename))
	counter = 1 
	text_file = open("two_precent.txt", "w")
	for xml, sgm in itertools.izip_longest(xml_docs, sgm_docs):
		print("-------------------------------DOC (" + str(counter) + ")  BREAK --------------------------------")
		print(xml)
		print
		text_file.write("-------------------------------DOC (" + str(counter) + ")  BREAK --------------------------------" +"\n")
		text_file.write(xml+"\n")
		text_file.write("\n")
		counter += 1
		#xml info extraction
		event_anno_list = get_all_info(xml)
		for event in event_anno_list:
			e_info = analyze_event(event)
			e_type = e_info["type"].upper() 
			e_anchor = e_info["anchor"]
			e_phrase = e_info["phrase"]
			print(e_type + " - " + e_anchor + " - " +  e_phrase)
			text_file.write(e_type + " - " + e_anchor + " - " +  e_phrase+"\n") 
		
		#sgm info extraction
		# print(sgm)
		sgm_file = open(sgm, 'r')
		soup = BeautifulSoup(sgm_file, "html.parser")
		doc_text_string = soup.get_text()
		# print (doc_text_string)

		# para_list = doc_text_string.split("\n\n")
		# for para in para_list: 
		# 	# print("PARA") 
		# 	print(para) 
		#annotating for for event mentions within document text 
		for event in event_anno_list: 
			e_info = analyze_event(event)
			e_type = e_info["type"].upper() 
			e_anchor = e_info["anchor"]
			e_phrase = e_info["phrase"]

			annotation_anchor = " *** " + e_anchor + " *** (" + e_type + ")"
			annotated_phrase = e_phrase.replace(e_anchor, annotation_anchor)
			doc_text_string = doc_text_string.replace(e_phrase, annotated_phrase)

		print(doc_text_string)
		text_file.write(doc_text_string+"\n")
	
	text_file.close()
if __name__ == '__main__':
	annotate_text(PATH_TO_ALL_DATA)
	
