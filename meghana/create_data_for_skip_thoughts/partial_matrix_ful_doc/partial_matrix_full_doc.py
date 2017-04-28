import os
import numpy
import random
import scipy.spatial
import xml.etree.ElementTree as ET
import nltk 
import nltk.data
import re 

from gensim import models
from bs4 import BeautifulSoup
from string import punctuation
from constants import EVENT_TYPES, GC_FILE_LIST
from real_name_to_gc_name_dict import REAL_TO_GC_NAMES_DICT, GC_NAMES_TO_REAL
from top_ten_gc import TOP_TEN
from man_scores import MAN_SCORES
from sklearn.utils import shuffle


PATH_TO_APNEWS_MODEL = ('../../../resources/doc2vec.bin')
PATH_TO_XMLS = os.path.join(os.getcwd(), "../../../urmilla/chain_xmls")
PATH_TO_SGMS = os.path.join(os.getcwd(), "../../../resources/ace2005/ace2005/data/English_adj")
MIN_EVENT_TYPES = 2
TOP_K = 10
counter = 0 

def create_documents(standard):
	docs = []
	files = []

	list_all_sent = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_SGMS):
		for basename in filenames:
			if basename.endswith(".sgm"):
	
				name = os.path.splitext(basename)[0]

				if not name in REAL_TO_GC_NAMES_DICT:
					continue
				
				list_xmls = REAL_TO_GC_NAMES_DICT[name]
				for xml in list_xmls:

					# file_path = ("../../../urmilla/chain_xmls/" + xml)
					
					# print(os.path.join(dirpath, basename))
					f = open(os.path.join(dirpath, basename))
					soup = BeautifulSoup(f.read(), 'html.parser')
					f.close()

					text = soup.find('body').text.lower().split()
					new_text = ""
					# print(text)
					for (i, w) in enumerate(text):
						new_text += w + " "
					
					list_all_sent.append(new_text)

				
					# new_name = xml[:-4]
					# docs.append(models.doc2vec.LabeledSentence(text, tags=[new_name]))
					# files.append(new_name)

	return list_all_sent #docs, files

def count_events(filename, counts):
	# print(filename)
	tree = ET.parse(filename) # root: source_file

	root = tree.getroot() # child of root: document
	# ET.dump(root)
	# print(root)
	document_el = root[0]

	all_events = []
	for anno in root: 
		# print ("anno found")
		if anno.tag == "event":
			# print("found event")
			e_type = anno.attrib.get("TYPE")
			counts[EVENT_TYPES[e_type.lower()]] += 1
			all_events.append(e_type.lower())
	return counts, all_events


def load_wanted_files():
	""" Load dict of all documents and events contained in that document. """
	standard = {}
	for dirpath, dirnames, filenames in os.walk(PATH_TO_XMLS):
		for basename in filenames:
			if basename.endswith(".xml"):
				counts = numpy.array(numpy.zeros(len(EVENT_TYPES)))
				counts, all_events = count_events(os.path.join(dirpath, basename), counts)
			
				""" Excluse all documents with less than 2 event types """
				if numpy.sum(counts) < MIN_EVENT_TYPES:
					continue

				name = os.path.splitext(basename)[0]
				# name = os.path.splitext(os.path.splitext(basename)[0])[0]
				standard[name] = (counts, all_events)

	print("Loaded documents: " + str(len(standard)))
	return standard

# def generate_model(docs):
# 	print("building")
# 	model = models.Doc2Vec(alpha=.025, min_alpha=.025, min_count= 10, dm=0)
# 	model.build_vocab(docs)

# 	for epoch in range(10):
# 	    model.train(docs)
# 	    model.alpha -= 0.002  # decrease the learning rate`
# 	    model.min_alpha = model.alpha  # fix the learning rate, no decay

# 	model.save('doc2vec.model')


def precision_score_candidate_match(f, candidate_docs):
	""" Choose MIN_EVENT_TYPES random events to query. """
	score = 0
	target = f + ".xml"
	for cdoc in candidate_docs:
		cdoc = cdoc + ".xml"
		if cdoc in TOP_TEN[target]: 
			score += 1 
	# print (score/10)
	return (score/10.0) 

def load_info(override=True):
	""" Use doc2vec to analyze document similarity. """
	standard = load_wanted_files()
	list_all_sent = create_documents(standard)

	sentA = ""
	sentB = []
	scoresAB = []

	#compute pairs for each doc 
	for index in range(0, 74): #we won't have to compute a pair for row 73 because it will all be done 
		manual_scores = MAN_SCORES[index]
		#make sure we don't compute duplicates
		sentA = list_all_sent[index]
		for nrep in range(0, 74):
			sentB.append(list_all_sent[nrep])
			scoresAB.append(manual_scores[nrep])	#currently ints, convert to strings


		sentB, scoresAB = shuffle(sentB, scoresAB, random_state=1234)
		filename = str(index) + "_SICK_test_annotated.txt"
		file = open(filename, 'w')
		file.write("pair_ID\tsentence_A\tsentence_B\trelatedness_score\tentailment_judgement\n")
		for x in range(0, 74):
			file.write(str(x) + "\t" + sentA + "\t" + sentB[x] + "\t" + str(scoresAB[x]*1.0) + "\tblep\n")
		file.close()

load_info(True)


	