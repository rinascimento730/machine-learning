# coding: utf-8
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

data_file = '../../BuildingMachineLearningSystemsWithPython/ch01/data/web_traffic.tsv'
graph_file = '../../output/web-trafic.png'

def join(path):
	base = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(base, path))

def get_web_trafic(data_path):
	file = join(data_path)
	data = sp.genfromtxt(file, delimiter="\t")

	print(data[:10])
	print(data.shape)

	x = data[:,0]
	y = data[:,1]
	x = x[~sp.isnan(y)]
	y = y[~sp.isnan(y)]

	return x, y

def make_graph(x, y, graph_path):
	plt.scatter(x, y, s=5)
	plt.title("Web traffic over the last month")
	plt.xlabel("Time")
	plt.ylabel("Hits / hour")
	plt.xticks([w*7*24 for w in range(10)],
	['week %i'%w for w in range(10)])
	plt.autoscale(tight=True)
	plt.grid()
	plt.show()

	filename = join(graph_path)
	plt.savefig(filename)

def main():
	x, y = get_web_trafic(data_file)
	make_graph(x, y, graph_file)

if __name__ == "__main__":
	main()