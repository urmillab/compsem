import os
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml.dom import minidom

result_path = 'annotated_texts_by_chains.txt'
MIN_EVENTS = 2

def annotate_chain(sgm, xml, result_path, document_number, chain_number, event_id_group):
	result = open(result_path, 'a')
	result.write('---------------------------DOCUMENT (' + str(document_number) + '), CHAIN (' + str(chain_number) +')---------------------------\n')
	chain_xml = open(os.path.join(os.getcwd(), 'chain_xmls', str(document_number) +  "_" + str(chain_number) + ".xml"), 'w')

	# Parse the sgm for event anchor data
	tree = ET.parse(xml) 
	root = tree.getroot()
	document_el = root[0]
	chain_root = ET.Element('root')

	start_idxs = {}
	end_idxs = {}
	eid = 0
	for anno in document_el: 
		if anno.tag == "event":
			if eid in event_id_group:
				chain_root.append(anno)
				e_type = anno.attrib.get("TYPE").upper()

				# event element has child event_mention
				emention_el = anno.find("event_mention")
				anchor = emention_el.find("anchor")
				charseq_el = anchor.find("charseq")
				start_idx = int(charseq_el.get("START"))
				end_idx = int(charseq_el.get("END"))

				result.write("[" + str(eid) + "] " + e_type + " - " + charseq_el.text + "\n")
				start_idxs[start_idx] = eid
				end_idxs[end_idx] = e_type

			eid += 1

	result.write("\n")
	

	soup = BeautifulSoup(open(sgm).read(), 'html.parser')
	raw_text = soup.find('doc').text

	annotated_text = []

	offset = 0
	if "CNN_CF_" in sgm or "CNN_IP_" in sgm:
		offset = 1
	else:
		offset = 0

	for cidx, c in enumerate(raw_text):
		if cidx + offset in start_idxs:
			result.write("[" + str(start_idxs[cidx + offset]) + "] *** " + c)
		elif cidx + offset in end_idxs:
			result.write(c + " *** (" + end_idxs[cidx + offset] + ")")
		else:
			result.write(c)

	result.write('\f')
	result.close()

	# Write out annotations to xml
	chain_xml.write(minidom.parseString(ET.tostring(chain_root, 'utf-8')).toprettyxml())


def main(args):
	if len(args) <= 1:
		print("Must input event group source document.")
		sys.exit()

	sgms = open('annotated_file_paths.txt', 'r').readlines()
	xmls = []

	for path in sgms:
		xmls.append(os.path.splitext(path)[0] + ".apf.xml")

	event_group_file = args[1]
	try:
		all_groups = open(event_group_file).readlines()
	except FileNotFoundError:
		print("File specified not found.")

	# Clear out result file
	open(result_path, 'w').close()

	for line in all_groups:
		groups = line.split()
		doc_id = int(groups[0])

		xml_path = xmls[doc_id - 1].strip()
		sgm_path = sgms[doc_id - 1].strip()

		chain_num = 1
		for i in range(1, len(groups)):	
			g = [int(idx) for idx in groups[i].split(',')]

			if len(g) >= MIN_EVENTS:
				annotate_chain(sgm_path, xml_path, result_path, doc_id, chain_num, g)
				chain_num += 1





if __name__ == "__main__":
	main(sys.argv)