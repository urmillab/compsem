import os
import numpy
import random
import scipy.spatial
import xml.etree.ElementTree as ET
import pickle 
import nltk.data 

from nltk import tokenize 
from gensim import models
from bs4 import BeautifulSoup
from string import punctuation
# from constants import EVENT_TYPES
from real_name_to_gc_name_dict import REAL_TO_GC_NAMES_DICT
from real_name_to_gc_name_dict import GC_NAMES_TO_REAL

PATH_TO_APNEWS_MODEL = ('../../resources/doc2vec.bin')
PATH_TO_XMLS = os.path.join(os.getcwd(), "../../../urmilla/chain_xmls")
PATH_TO_SGMS = os.path.join(os.getcwd(), "../../../resources/ace2005/ace2005/data/English_adj")

doc_to_event_sentences_dict = {}

def write_to_file(): 
	with open("doc_to_event_sentences_dict.pik", "wb") as f: 
		pickle.dump([doc_to_event_sentences_dict], f, -1)

def analyze_charseq(charseq_el):
    retv = { }
    retv["START"] = charseq_el.attrib.get("START")
    retv["END"] = charseq_el.attrib.get("END")
    retv["content"] = charseq_el.text

    return retv

def analyze_event(event_el):
	retv = { }
	retv["TYPE"] = event_el.attrib.get("TYPE")
	retv["SUBTYPE"] = event_el.attrib.get("SUBTYPE")

    # event element has child event_mention
	emention_el = event_el.find("event_mention")
    
    # event_mention has child anchor, which contains the predicate
	anchor = emention_el.find("anchor")
	info = analyze_charseq(anchor.find("charseq"))
	retv["anchor"] = info["content"]
	retv["anchorSTART"] = info["START"]
	retv["anchorEND"] = info["END"]

    # event_mention has child extent, which contains the whole phrase marked as an event
	extent = emention_el.find("extent")
	info = analyze_charseq(extent.find("charseq"))
	retv["phrase"] = info["content"]
	retv["phraseSTART"] = info["START"]
	retv["phraseEND"] = info["END"]

    # event_mention has children event_mention_argument
	retv["arguments"] = [ ]
	for arg in emention_el.findall("event_mention_argument"):
		retv_arg = { }
		retv_arg["ROLE"] = arg.attrib.get("ROLE")
		info = analyze_charseq(arg.find("extent").find("charseq"))
		retv_arg["content"] = info["content"]
		retv_arg["contentSTART"] = info["START"]
		retv_arg["contentEND"] = info["END"]
		retv["arguments"].append(retv_arg)

	return retv 

def get_event_sentences(doc_to_sentences_dict):
	for dirpath, dirnames, filenames in os.walk(PATH_TO_XMLS):
		for basename in filenames:
			if basename.endswith(".xml"):

				name = os.path.splitext(basename)[0]
				file_version_name = name + ".xml"

				tree = ET.parse(os.path.join(dirpath, basename))
				root = tree.getroot()
				document_el = root[0]

				event_sent_list = [] 

				for anno in root: 
					if anno.tag == "event":
						info = analyze_event(anno)

						e_phrase = info["phrase"]
						sent_list = doc_to_sentences_dict[GC_NAMES_TO_REAL[file_version_name]]


						for sent in sent_list: 
							if e_phrase in sent: 
								event_sent_list.append(sent)

				doc_to_event_sentences_dict[name] = event_sent_list


def get_all_sentences():
	doc_to_sentences_dict = {} 

	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

	for dirpath, dirnames, filenames in os.walk(PATH_TO_SGMS):
		for basename in filenames:
			if basename.endswith(".sgm"):
				

				name = os.path.splitext(basename)[0]
				

				if name not in REAL_TO_GC_NAMES_DICT:
					continue
				# print(name)
				f = open(os.path.join(dirpath, basename))
				soup = BeautifulSoup(f.read(), 'html.parser')
				f.close()

				text = soup.find('body').text #.lower()
				sentence_list = tokenize.sent_tokenize(text)

				doc_to_sentences_dict[name] = sentence_list
	return doc_to_sentences_dict

def print_stuff(): 
	for entry in doc_to_event_sentences_dict: 
		sent_list = doc_to_event_sentences_dict[entry]
		print ("DOCUMENT NAME: " + entry)
		for sent in sent_list:
			print("		SENTENCE: " + sent)

def create_dict():
	doc_to_sentences_dict = get_all_sentences()
	get_event_sentences(doc_to_sentences_dict)
	write_to_file() 
	print_stuff()

create_dict()




	