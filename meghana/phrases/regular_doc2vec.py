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
from constants import EVENT_TYPES
from constants import GC_FILE_LIST
from real_name_to_gc_name_dict import REAL_TO_GC_NAMES_DICT
from real_name_to_gc_name_dict import GC_NAMES_TO_REAL

PATH_TO_APNEWS_MODEL = ('../../resources/doc2vec.bin')
PATH_TO_DATA = os.path.join(os.getcwd(), "../../resources/ace2005/ace2005/data/English_adj")
MIN_EVENT_TYPES = 2
TOP_K = 10

boolean_gc_file_list = GC_FILE_LIST

def create_documents(standard):
	docs = []
	files = []
	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".sgm"):
				name = os.path.splitext(basename)[0]

				if not name in REAL_TO_GC_NAMES_DICT:
					continue



				f = open(os.path.join(dirpath, basename))
				soup = BeautifulSoup(f.read(), 'html.parser')
				f.close()

				# print ("BODY ******************************")
				# print(soup.find('body'))
				# print ("END ******************************")

				text = soup.find('body').text.lower().split()
				# sentences = split_into_sentences(text)

				
				# sentences = nltk.sent_tokenize(text)

				# print ("SENT ******************************")
				# print(sentences)
				# print ("END ******************************")
				
				for i, w in enumerate(text):
					text[i] = ''.join(c for c in w if c not in punctuation)   

				# print ("TEXT ******************************")
				# print(text)
				# print ("END ******************************")
				docs.append(models.doc2vec.LabeledSentence(text, tags=[name]))
				files.append(name)

	return docs, files

def count_events(filename, counts):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]
    print (filename)
    #children of "document" include those with tag "event"
    all_events = []
    for anno in document_el: 
        if anno.tag == "event":
        	print("event found")
        	e_type = anno.attrib.get("TYPE")
        	counts[EVENT_TYPES[e_type.lower()]] += 1
        	all_events.append(e_type.lower())
    return counts, all_events


def load_gold_standard():
	""" Load dict of all documents and events contained in that document. """
	standard = {}

	for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
		for basename in filenames:
			if basename.endswith(".apf.xml"):
				counts = numpy.array(numpy.zeros(len(EVENT_TYPES)))
				counts, all_events = count_events(os.path.join(dirpath, basename), counts)
				
				""" Excluse all documents with less than 2 event types """
				if numpy.sum(counts) < MIN_EVENT_TYPES:
					continue

				name = os.path.splitext(os.path.splitext(basename)[0])[0]
				standard[name] = (counts, all_events)

	print("Loaded documents: " + str(len(standard)))
	return standard

def generate_model(docs):
	print("building")
	model = models.Doc2Vec(alpha=.025, min_alpha=.025, min_count=1, dm=0)
	model.build_vocab(docs)

	for epoch in range(10):
	    model.train(docs)
	    model.alpha -= 0.002  # decrease the learning rate`
	    model.min_alpha = model.alpha  # fix the learning rate, no decay

	model.save('doc2vec.model')


def precision_score_candidate_match(standard, selected_types, candidate_docs):
	""" Choose MIN_EVENT_TYPES random events to query. """
	score = 0
	for cdoc in candidate_docs:
		counts, all_events = standard[cdoc]

		event_match = True
		for event_type in selected_types:
			if counts[EVENT_TYPES[event_type]] == 0:
				event_match = False

		if event_match:
			score += 1

	assert(score <= TOP_K), str(score)
	return score

def recall_score_candidate_match(standard, selected_types, candidate_docs):
	relevant_docs = []
	for doc in standard:
		counts, all_events = standard[doc]

		event_match = True
		for event_type in selected_types:
			if counts[EVENT_TYPES[event_type]] == 0:
				event_match = False

		if event_match:
			relevant_docs.append(doc)

	candidate_relevant_docs = len([c for c in candidate_docs if c in relevant_docs])
	return candidate_relevant_docs/float(len(relevant_docs))



def score_doc2vec_model(override=False):
	""" Use doc2vec to analyze document similarity. """
	standard = load_gold_standard()
	docs, files = create_documents(standard)

	if override or not os.path.isfile('doc2vec.model'):
		generate_model(docs)

	model = models.Doc2Vec.load('doc2vec.model')
	
	precision_score = 0.0
	recall_score = 0.0
	for f in files:
		counts, all_events = standard[f]
		random.shuffle(all_events)
		selected_types = all_events[:MIN_EVENT_TYPES]

		candidate_docs = [c for c, _ in model.docvecs.most_similar([f], topn=TOP_K)]
		
		precision_score += precision_score_candidate_match(standard, selected_types, candidate_docs)
		recall_score += recall_score_candidate_match(standard, selected_types, candidate_docs)

	print("Doc2Vec precision: " + str(precision_score/len(files)))
	print("Doc2Vec recall: " + str(recall_score/len(files)))

def score_random():
	standard = load_gold_standard()
	docs, files = create_documents(standard)
	
	precision_score = 0.0
	recall_score = 0.0
	for i, f in enumerate(files):
		counts, all_events = standard[f]
		
		random.shuffle(all_events)
		selected_types = all_events[:MIN_EVENT_TYPES]

		idxs = random.sample([x for x in range(len(files)) if x != i], TOP_K)
		candidate_docs = [files[i] for i in idxs]

		precision_score += precision_score_candidate_match(standard, selected_types, candidate_docs)
		recall_score += recall_score_candidate_match(standard, selected_types, candidate_docs)

	print("Random precision: " + str(precision_score/len(files)))
	print("Random recall: " + str(recall_score/len(files)))



score_doc2vec_model(False)
score_random()

	