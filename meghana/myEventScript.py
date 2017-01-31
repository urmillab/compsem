import xml.etree.ElementTree as ET
import os
from sets import Set

event_dict = {}

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
        

    # # my code
    # event_type = event_el.attrib.get("TYPE")
    # event_subtype = event_el.attrib.get("SUBTYPE")
    # event_anchor = info
    # if event_dict.has_key(event_type):
    #     temp_dict = event_dict[event_type]
    #     if temp_dict.has_key(event_subtype): 
    #         temp_set = temp_dict[event_subtype]
    #         temp_set.add(event_anchor)
    #         (event_dict[event_type])[event_subtype] = temp_set
    #     else: 
    #         temp_set = Set([event_anchor])
    #         (event_dict[event_type])[event_subtype] = temp_set
    # else: 
    #     temp_dict = {}
    #     temp_set = Set([event_anchor])
    #     temp_dict[event_subtype] = temp_set 
    #     event_dict[event_type] = temp_dict 
    # # end of my code 

    return retv

def analyze_charseq(charseq_el):
    retv = { }
    retv["START"] = charseq_el.attrib.get("START")
    retv["END"] = charseq_el.attrib.get("END")
    retv["content"] = charseq_el.text

    return retv
    
def print_events_in_file(filename):
    tree = ET.parse(filename) # root: source_file
    root = tree.getroot() # child of root: document
    document_el = root[0]

    #children of "document" include those with tag "event"
    for anno in document_el: 
        if anno.tag == "event":
            info = analyze_event(anno)


            # my code
            # event_type = info["TYPE"]
            # event_subtype = info["SUBTYPE"]
            # event_anchor = info["anchor"]
            # if event_dict.has_key(event_type):
            #     temp_dict = event_dict[event_type]
            #     if temp_dict.has_key(event_subtype): 
            #         temp_set = temp_dict[event_subtype]
            #         temp_set.add(event_anchor)
            #         (event_dict[event_type])[event_subtype] = temp_set
            #     else: 
            #         temp_set = Set([event_anchor])
            #         (event_dict[event_type])[event_subtype] = temp_set
            # else: 
            #     temp_dict = {}
            #     temp_set = Set([event_anchor])
            #     temp_dict[event_subtype] = temp_set 
            #     event_dict[event_type] = temp_dict 
                # end of my code 



            print(info["anchor"] + " - " + info["TYPE"] + " - " +  info["phrase"]) 
            # print("type", info["TYPE"], "subtype", info["SUBTYPE"], "anchor", info["anchor"])
            # print("\t", info["phrase"])
            # for info_arg in info["arguments"]:
                # print("\t", "role", info_arg["ROLE"], info_arg["content"])

for dirpath, dirnames, filenames in os.walk("../resources/ace2005/ace2005/data/English_adj"):
    for basename in filenames:
        if basename.endswith(".apf.xml"):
            print("doc break")
            # this is the type of files we want to analyze
            print_events_in_file(os.path.join(dirpath, basename))
            

# for event in event_dict: 
#     print ("EVENT: ") 
#     print (event)
#     print("    SUBEVENTS:")

#     for subevent in event_dict[event]: 
#         print ("    " + subevent)
#         print ("        ANCHORS:")
#         for anchor in event_dict[event][subevent]: 
#             print ("        " + anchor)






















