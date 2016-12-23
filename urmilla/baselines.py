import analyze_event
import nltk
import os
import xml.etree.ElementTree as ET

from constants import EVENT_TYPES_TO_SUBTYPES
from nltk.stem.wordnet import WordNetLemmatizer

WNL = WordNetLemmatizer()

def _init_type_count_map():
	event_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_map[event_type] = 0
	return event_map

def _init_type_anchor_map():
	event_map = {}
	for event_type in EVENT_TYPES_TO_SUBTYPES:
		event_map[event_type] = set()
	return event_map

def _init_subtype_map():
	event_map = {}
	for event_subtype in EVENT_TYPES_TO_SUBTYPES.values():
		for s in event_subtype:
			event_map[s] = 0
	return event_map

def _get_type_counts(path, print_results=False):
	tree = ET.parse(path) 
	root = tree.getroot()

	event_map = _init_type_count_map()
	for event_el in root: 
		event_type = event_el.attrib.get("TYPE").lower()
		event_map[event_type] += 1

	return event_map

def _get_subtype_counts(path, print_results=False):
	tree = ET.parse(path) 
	root = tree.getroot()

	event_map = _init_subtype_map()
	for event_el in root: 
		event_type = event_el.attrib.get("SUBTYPE").lower()
		event_map[event_type] += 1

	return event_map

def _get_most_freq_type(print_intermediate):
	train_counts = _get_type_counts(analyze_event.TRAIN_FILE, print_results=print_intermediate)
	max_event = max(train_counts, key=lambda i: train_counts[i])

	if print_intermediate:
		for e,c in train_counts.items():
			print(e + ": " + str(c))
		print("Most frequent type: " + max_event)

	return max_event


def most_frequent_type_baseline(print_intermediate=False):
	max_event = _get_most_freq_type(print_intermediate)

	correct = 0
	incorrect = 0
	test_counts = _get_type_counts(analyze_event.TEST_FILE, print_results=print_intermediate)
	for event, count in test_counts.items():
		if event == max_event:
			correct += count
		else:
			incorrect += count
	total = correct + incorrect

	print("----------MOST FREQ EVENT TYPE RESULTS----------")
	print("Correct: " + str(correct) + "/" + str(total) + " = " + str(correct/total))
	print("Incorrect: " + str(incorrect) + "/" + str(total) + " = " + str(incorrect/total))

def _get_most_freq_subtype(print_intermediate):
	train_counts = _get_subtype_counts(analyze_event.TRAIN_FILE, print_results=print_intermediate)
	max_event = max(train_counts, key=lambda i: train_counts[i])

	if print_intermediate:
		for e,c in train_counts.items():
			print(e + ": " + str(c))
		print("Most frequent subtype: " + max_event)

	return max_event

def most_frequent_subtype_baseline(print_intermediate=False):
	max_event = _get_most_freq_subtype(print_intermediate)

	correct = 0
	incorrect = 0
	test_counts = _get_subtype_counts(analyze_event.TEST_FILE, print_results=print_intermediate)
	for event, count in test_counts.items():
		if event == max_event:
			correct += count
		else:
			incorrect += count
	total = correct + incorrect

	print("----------MOST FREQ EVENT SUBTYPE RESULTS----------")
	print("Correct: " + str(correct) + "/" + str(total) + " = " + str(correct/total))
	print("Incorrect: " + str(incorrect) + "/" + str(total) + " = " + str(incorrect/total))

def _lemmatize(anchor):
	# Get lemmatized form of anchor if it exists, else keep original anchor
	tags = nltk.pos_tag(anchor.split())

	lemmatized = ""
	for word, tag in tags:
		if tag[0] == 'N' or tag[0] == 'V':
			word = WNL.lemmatize(word, tag[0].lower())
		lemmatized += " " + word

	return lemmatized.strip()

def _build_anchor_dict(path, print_intermediate):
	tree = ET.parse(path) 
	root = tree.getroot()

	anchor_dict = {}
	for event_el in root: 
		event_type = event_el.attrib.get("TYPE").lower()
		anchor = event_el.find("event_mention").find("anchor").find("charseq").text.lower()

		lemmatized = _lemmatize(anchor)

		# Count the type classification for each anchor type
		if lemmatized in anchor_dict:
			event_map = anchor_dict[lemmatized]
			if event_type in event_map: 
				event_map[event_type] += 1
			else:
				event_map[event_type] = 1

		else:
			anchor_dict[lemmatized] = {}
			anchor_dict[lemmatized][event_type] = 1

	if print_intermediate:
		for anchor, event_map in anchor_dict.items():
			print(anchor + ": " + str(event_map.keys()))


	return anchor_dict

def _get_anchor_type_pairs(path):
	tree = ET.parse(path) 
	root = tree.getroot()

	pairs_list = []
	for event_el in root: 
		event_type = event_el.attrib.get("TYPE").lower()
		anchor = event_el.find("event_mention").find("anchor").find("charseq").text.lower()
		pairs_list.append((anchor, event_type))

	return pairs_list


def verb_lookup_and_frequency_baseline(print_intermediate=False):
	anchor_dict = _build_anchor_dict(analyze_event.TRAIN_FILE, print_intermediate)
	max_event = _get_most_freq_type(False)
	pairs_list= _get_anchor_type_pairs(analyze_event.TEST_FILE)

	correct = 0
	incorrect = 0
	num_lookup_matches = 0
	num_lookup_matches_correct = 0

	# Predict based on anchor, follow up with most frequent type
	for anchor, true_type in pairs_list:
		looked_up = False
		predicted_type = max_event

		lemmatized = _lemmatize(anchor)

		if lemmatized in anchor_dict:
			event_map = anchor_dict[lemmatized]
			predicted_type = max(event_map, key=lambda i: event_map[i])
			num_lookup_matches += 1
			looked_up = True

		if predicted_type == true_type:
			correct += 1
			if looked_up:
				num_lookup_matches_correct += 1
		else:
			incorrect += 1
	total = correct + incorrect

	print("----------LOOKUP + MOST FREQ EVENT TYPE RESULTS----------")
	print("Correct: " + str(correct) + "/" + str(total) + " = " + str(correct/total))
	print("Incorrect: " + str(incorrect) + "/" + str(total) + " = " + str(incorrect/total))
	print("Num lookups: " + str(num_lookup_matches) + ", Num correct lookups: " + str(num_lookup_matches_correct))

def main():
	most_frequent_type_baseline(print_intermediate=False)
	most_frequent_subtype_baseline(print_intermediate=False)
	verb_lookup_and_frequency_baseline(print_intermediate=False)

if __name__ == "__main__":
	main()