from constants import CHAINS
from constants import INDEX_TO_CHAIN
from list_manual_ratings import LIST_MANUAL_RATINGS

def generate_index_to_chains_dict():
	index_to_chains_dict = {}
	counter = 0
	for chain in CHAINS:
		chain_tuple = chain.split(",")
		doc_num = chain_tuple[0].strip()
		group_num = chain_tuple[1].strip()
		file_name = doc_num + "_" + group_num + ".xml"
		
		#create dictionary entry 
		index_to_chains_dict[counter] = file_name
		counter += 1

	for entry in index_to_chains_dict: 
		print (str(entry) + ": \"" + index_to_chains_dict[entry] +"\",")

def generate_dictionary_of_manual_ratings(): 
	file_to_rating_list_dict = {}

	# bfile = open("old_ratings.txt", "w")
	# for chain in LIST_MANUAL_RATINGS:
	# 	bfile.write("CHAIN: \n")
	# 	bfile.write(str(chain) + "\n\n")
	# bfile.close()

	# for chain in LIST_MANUAL_RATINGS:
	# 	print ("CHAIN: " + str(chain))

	counter_bottom = 0 
	counter_top = 73
	for x in range(0, 37):
		
		if(counter_bottom == 0 and counter_top == 0): 
			file_bottom = INDEX_TO_CHAIN[counter_bottom]
			file_top = INDEX_TO_CHAIN[counter_top]

			file_to_rating_list_dict[file_bottom] = LIST_MANUAL_RATINGS[counter_bottom]
			file_to_rating_list_dict[file_top] = LIST_MANUAL_RATINGS[counter_top]

			counter_bottom += 1
			counter_top -= 1
		else: 
			ratings_bottom = LIST_MANUAL_RATINGS[counter_bottom]
			ratings_top = LIST_MANUAL_RATINGS[counter_top]

			new_bottom_ratings = []
			new_top_ratings = []

			file_bottom = INDEX_TO_CHAIN[counter_bottom]
			file_top = INDEX_TO_CHAIN[counter_top]

			for y in range (0, 74):
				
				if (ratings_bottom[y] == 0):
					corresponding_list = LIST_MANUAL_RATINGS[y]
					replacement_value = corresponding_list[counter_bottom]
					new_bottom_ratings.append(replacement_value)
				else:
					new_bottom_ratings.append(ratings_bottom[y])

				if (ratings_top[y] == 0):
					corresponding_list = LIST_MANUAL_RATINGS[y]
					replacement_value = corresponding_list[counter_top]
					new_top_ratings.append(replacement_value)
				else: 
					new_top_ratings.append(ratings_top[y])

			file_to_rating_list_dict[file_bottom] = new_bottom_ratings
			file_to_rating_list_dict[file_top] = new_top_ratings

			counter_bottom += 1
			counter_top -= 1 

	#manually making changes for the 5 scores urmilla and I disagreed on 
	file_to_rating_list_dict["3_1.xml"][70] = 4
	file_to_rating_list_dict["52_1.xml"][3] = 4
	file_to_rating_list_dict["3_3.xml"][68] = 3
	file_to_rating_list_dict["50_1.xml"][5] = 3
	file_to_rating_list_dict["12_2.xml"][56] = 2
	file_to_rating_list_dict["41_1.xml"][17] = 2
	file_to_rating_list_dict["20_1.xml"][48] = 2
	file_to_rating_list_dict["38_3.xml"][25] = 2
	file_to_rating_list_dict["32_1.xml"][37] = 4
	file_to_rating_list_dict["33_1.xml"][36] = 4

	# for chain in file_to_rating_list_dict: 
	# 	rl = file_to_rating_list_dict[chain]
	# 	print (chain + ":   ")
	# 	print (str(rl))

	# afile = open("updated_ratings.txt", "w")
	# for x in range(0,74): 
	# 	rl = file_to_rating_list_dict[INDEX_TO_CHAIN[x]]
	# 	afile.write(INDEX_TO_CHAIN[x] + ":   \n")
	# 	afile.write(str(rl) + "\n\n")
	# afile.close()

	return file_to_rating_list_dict 

def generate_top_ten(): 
	top_ten_dict = {}
	file_to_rating_list_dict = generate_dictionary_of_manual_ratings()

	for x in range(0, 74):
		file = INDEX_TO_CHAIN[x]
		ratings = file_to_rating_list_dict[file]

		num_top_docs = 0 
		names_top_docs = []
		rating_value = 5 
		while (num_top_docs < 10):
			for y in range (0, 74):
				if (ratings[y] == rating_value):
					if (INDEX_TO_CHAIN[y] == file): 
						continue
					names_top_docs.append(INDEX_TO_CHAIN[y])
					num_top_docs += 1
			rating_value -= 1

		# USEFULL INFO -> might want to reduce it to TOP 5 
		# print (file)
		# print ("number of top docs: " + str(num_top_docs))
		# print ("rating_value: " + str(rating_value + 1))
		# print ("\n")
		
		top_ten_dict[file] = names_top_docs

 	afile = open("top_10.txt", "w")
 	for e in range (0, 74):
	# for e in top_ten_dict:
		afile.write("\"" + INDEX_TO_CHAIN[e] + "\"" + ":\n" )
		afile.write(str(top_ten_dict[INDEX_TO_CHAIN[e]]) + ",\n\n")
		# print ("\n")
	afile.close()

generate_top_ten()

		










#generate_index_to_chains_dict()
generate_dictionary_of_manual_ratings()