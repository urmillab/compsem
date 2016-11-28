import xml.etree.ElementTree as ET
import os

PATH_TO_DATA = os.path.join(os.getcwd(), "ace2005/ace2005/data/")

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
            print(ET.dump(anno))
            print('\n')
            info = analyze_event(anno)
            print("type", info["TYPE"], "subtype", info["SUBTYPE"], "anchor", info["anchor"])
            print("\t", info["phrase"])
            for info_arg in info["arguments"]:
                print("\t", "role", info_arg["ROLE"], info_arg["content"])

print PATH_TO_DATA
for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
    for basename in filenames:
        if basename.endswith(".apf.xml"):
            print(basename)
            # this is the type of files we want to analyze
            print_events_in_file(os.path.join(dirpath, basename))
            break


        
