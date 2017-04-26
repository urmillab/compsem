import os
import numpy
import xml.etree.ElementTree as ET
from constants import EVENT_TYPES
from scipy import spatial
from scipy.stats import spearmanr
from scipy.stats import pearsonr

GOLD_STANDARD = 'annotated_file_paths.txt'
SCORES = 'doc_scores.npy'
THRESHOLD = 0.1


def _get_ranking_matrix():
	# Initialize rank matrix
	score_matrix = numpy.load('ratings_complete.npy')
	num_docs = len(score_matrix)
	ranking_matrix = numpy.zeros((num_docs, num_docs))

	# Calculate the rankings across all event groups
	for ridx in range(num_docs):
		rscores = score_matrix[ridx]
		sorted_idxs = [i[0] for i in sorted(enumerate(rscores), key=lambda x:x[1], reverse=True)]
		ranking_matrix[ridx] = sorted_idxs
	
	numpy.save('rankings.npy', ranking_matrix)


def score_correlation(score_matrix):
	ratings_matrix = numpy.load('ratings_complete.npy')

	if len(ratings_matrix) != len(score_matrix) or len(ratings_matrix[0]) != len(score_matrix[0]):
		print("ERROR: Different shaped matrices")
		return

	num_groups = len(ratings_matrix)
	ratings_vector = ratings_matrix.reshape(num_groups**2)
	score_vector = score_matrix.reshape(num_groups**2)
	
	spearman, p = spearmanr(ratings_vector, score_vector)
	return spearman, p