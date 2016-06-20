import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def show_map(map_matrix, clean=False):
	"""Just plot the map matrix"""
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.tick_params(axis='both', which='both', length=0)
	plt.imshow(map_matrix, cmap="gray", origin='upper', interpolation='none', vmin=-3, vmax=1)
	if clean:
		plt.axis('off')
	else:
		plt.grid('on', linestyle='dotted', linewidth=1, which='major')


def show_path(path, **kwargs):
	params = {
		'color': 'k',
		'lw': 1,
		'markersize':3
	}
	params.update(kwargs)
	if path[-1] == (0,0):
		path = path[:-1]
	xs = [p[0] for p in path]
	ys = [p[1] for p in path]
	plt.plot(xs, ys, 'o-', **params)#color=color, lw=1, markersize=3, **kwargs)


def show_views(paths, M, title=True, size=3, plotsize=1):
	"""
	Displays an array of views given a path and the map.

	Arguments:
		paths: a list of paths (lists of (x,y) coordinates)
		M: the map matrix
		title (bool): show a title for every view?
		size: the size of the view (default 3x3)
		plotsize: scale the output plot
	"""

	num_cols = 6
	num_rows = len(paths) // num_cols + 1
	hspace = 1 if title else .2

	plt.figure(figsize = (num_cols*plotsize, num_rows*plotsize))
	grid = gridspec.GridSpec(num_rows, num_cols)
	grid.update(wspace=.2/plotsize, hspace=hspace/plotsize) # set the spacing between axes. 

	for i, p in enumerate(paths):
		ax = plt.subplot(grid[i])

		# Hide ticks
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		ax.tick_params(axis='both', which='both', length=0)

		# Plot the views
		view = get_view(p, M, size=size)
		plt.plot([(size-1)/2], [(size-1)/2], 'o', color='r', markersize=3)
		ax.matshow(view, cmap="gray", origin='upper', interpolation='none', vmin=-3, vmax=1)
		if title:
			ax.set_title('({x}, {y})'.format(i=i, x=p[0], y=p[1]), 
				fontsize=9, horizontalalignment="center")


def load_map(map_fn, border=1):
	"""
	Read out the map from a CSV file exported from google docs

	Arguments:
		map_fn: the filename of a csv map
		border: the width of the border (will be added automatically). Default 1.

	Returns a numpy array
	"""
	matrix = []
	with open(map_fn, 'r') as data_f:
		parse_cell = lambda cell: int(cell != "")
		for line in data_f:
			line = line.replace("\n", "").replace("\r","")
			matrix.append(map(parse_cell, line.split(",")))
	
	# Add rows of zeros to the right and column of zeros to the bottom
	M = np.array(matrix)
	M = np.pad(M, border, 'constant', constant_values=(0))
	return M

def read_map(map_fn, **kwargs):
	return load_map(map_fn, **kwargs)

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
	if Map[y,x] == 0:
		print("Error: invalid initial position")
		raise

	xs, ys = [x], [y]
	for i in range(length - 1):

		# Find all possible next positions 
		candidates = []
		for d in np.array([[-1,0], [1,0], [0,-1], [0,1]]):
			cand_x, cand_y = (x, y) + d

			# Don't walk across boundaries and never go back
			if (Map[cand_y, cand_x] != 0
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

def get_view((x,y), Map, size=3):
	if (x, y) == (0, 0):
		return np.zeros((size, size))
	delta = (size-1) / 2
	return Map[y-delta:y+delta+1, x-delta:x+delta+1]
