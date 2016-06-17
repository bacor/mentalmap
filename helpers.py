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

def generate_path(init, length, Map):
	"""Get a random walk through the map given an initial position,
	a length and the actual map. The path can never go back, so 
	can only go forward, right or left.

	Arguments: 
	init: a pair (x, y) of initial coordinates
	length: the maximum length of the path
	Map: the map matrix

	Returns:
	path: a list of (x,y) coordinates
	"""

	# Check if the initial position is valid (i.e. not on a boundary)
	x, y = init
	if Map[x,y] == 0:
		print("Error: invalid initial position")
		raise

	xs, ys = [x], [y]
	for i in range(length - 1):

		# Find all possible next positions 
		candidates = []
		for d in np.array([[-1,0], [1,0], [0,-1], [0,1]]):
			cand_x, cand_y = (x, y) + d

			# Don't walk across boundaries and never go back
			if (Map[cand_x, cand_y] != 0
				and not (len(xs) > 1 and ((xs[-2], ys[-2]) == (cand_x, cand_y)))):
				candidates.append((cand_x, cand_y))

		# Stop if there are no futher options
		if len(candidates) == 0: break

		# And otherwise, randomly pick a next position
		index = np.random.randint(len(candidates))
		x, y = candidates[index]
		xs.append(x)
		ys.append(y)

	return list(zip(xs, ys))
