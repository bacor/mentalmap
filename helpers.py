import numpy as np
import matplotlib.pyplot as plt


def show_map(map_matrix):
	"""Just plot the map matrix"""
	plt.imshow(map_matrix.T, cmap="gray", origin='upper', interpolation='none')

def read_map(map_fn):
	"""Read out the map from a CSV file exported from google docs"""
	matrix = []
	with open(map_fn, 'r') as data_f:
		parse_cell = lambda cell: int(cell != "")
		for line in data_f:
			line = line.replace("\n", "").replace("\r","")
			matrix.append(map(parse_cell, line.split(",")))
	
	# Add rows of zeros to the right and column of zeros to the bottom
	M = np.array(matrix).T
	M = np.concatenate((M, np.zeros((M.shape[0],1))), axis=1)
	M = np.concatenate((M, np.zeros((1,M.shape[1]))), axis=0)
	return M

def generate_path(init, length, Map, next_step):
	"""Get a random walk through the map given an initial position,
	a length and a function that returns the next step"""
	path = [init]
	x, y = init
	if Map[x,y] == 0:
		print("Error: invalid initial position")
		raise

	for i in range(length -1):
		x, y = next_step(x, y, Map)
		path.append((x,y))
	return path