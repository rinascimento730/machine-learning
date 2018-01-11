# coding: utf-8
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

data_file = '../../BuildingMachineLearningSystemsWithPython/ch01/data/web_traffic.tsv'
graph_file = '../../output/analyze_webstats.png'

# all examples will have three classes in this file
colors = ['g', 'k', 'b', 'm', 'r']
linestyles = ['-', '-.', '--', ':', '-']

def join(path):
	base = os.path.dirname(os.path.abspath(__file__))
	return os.path.normpath(os.path.join(base, path))

def error(f, x, y):
	return sp.sum((f(x)-y)**2)

def get_web_trafic(data_path):
	file = join(data_path)
	data = sp.genfromtxt(file, delimiter="\t")

	#print(data[:10])
	#print(data.shape)

	x = data[:,0]
	y = data[:,1]
	x = x[~sp.isnan(y)]
	y = y[~sp.isnan(y)]

	return x, y

def plot_models(x, y, models, fname, mx=None, ymax=None, xmin=None):
    plt.clf()
    plt.scatter(x, y, s=10)
    plt.title("Web traffic over the last month")
    plt.xlabel("Time")
    plt.ylabel("Hits/hour")
    plt.xticks(
        [w * 7 * 24 for w in range(10)], ['week %i' % w for w in range(10)])

    if models:
        if mx is None:
            mx = sp.linspace(0, x[-1], 1000)
        for model, style, color in zip(models, linestyles, colors):
            # print "Model:",model
            # print "Coeffs:",model.coeffs
            plt.plot(mx, model(mx), linestyle=style, linewidth=2, c=color)

        plt.legend(["d=%i" % m.order for m in models], loc="upper left")

    plt.autoscale(tight=True)
    plt.ylim(ymin=0)
    if ymax:
        plt.ylim(ymax=ymax)
    if xmin:
        plt.xlim(xmin=xmin)
    plt.grid(True, linestyle='-', color='0.75')
    plt.savefig(fname)

def make_polynomial_model(x, y, dim):
	fp, res, rank, sv, rcond = sp.polyfit(x, y, dim, full=True)
	print("Model dimension: %s" % dim)
	#print("Model parameters: %s" % fp)
	print("Error of the model:", res)

	f = sp.poly1d(fp)

	return f

def when_reach_target(target, func, init):
	print(func)
	print(func - target)
	reached_max = fsolve(func - target, init) / (7 * 24)
	print(target + " hits/hour expected at week %f" % reached_max[0])

def main():
	x, y = get_web_trafic(data_file)
	# first look at the data
	plot_models(x, y, None, join("../../output/analyze_webstats_1400_01_01.png"))

	# create and plot models
	f1 = make_polynomial_model(x, y, 1)
	f2 = make_polynomial_model(x, y, 2)
	f3 = make_polynomial_model(x, y, 3)
	f10 = make_polynomial_model(x, y, 10)
	f50 = make_polynomial_model(x, y, 50)

	plot_models(x, y, [f1], join("../../output/analyze_webstats_1400_01_02.png"))
	plot_models(x, y, [f1, f2], join("../../output/analyze_webstats_1400_01_03.png"))
	plot_models(x, y, [f1, f2, f3, f10, f50], join("../../output/analyze_webstats_1400_01_04.png"))

	# fit and plot a model using the knowledge about inflection point
	inflection = int(3.5 * 7 * 24)
	xa = x[:inflection]
	ya = y[:inflection]
	xb = x[inflection:]
	yb = y[inflection:]

	fa = make_polynomial_model(xa, ya, 1)
	fb = make_polynomial_model(xb, yb, 1)

	plot_models(x, y, [fa, fb], join("../../output/analyze_webstats_1400_01_05.png"))

	print("Errors for the complete data set:")
	for f in [f1, f2, f3, f10, f50]:
	    print("Error d=%i: %f" % (f.order, error(f, x, y)))

	print("Errors for only the time after inflection point")
	for f in [f1, f2, f3, f10, f50]:
	    print("Error d=%i: %f" % (f.order, error(f, xb, yb)))

	print("Error inflection=%f" % (error(fa, xa, ya) + error(fb, xb, yb)))

	# extrapolating into the future
	plot_models(
	    x, y, [f1, f2, f3, f10, f50], join("../../output/analyze_webstats_1400_01_06.png"),
	    mx=sp.linspace(0 * 7 * 24, 6 * 7 * 24, 100),
	    ymax=10000, xmin=0 * 7 * 24)

	print("Trained only on data after inflection point")
	fb1 = fb
	fb2 = make_polynomial_model(xb, yb, 2)
	fb3 = make_polynomial_model(xb, yb, 3)
	fb10 = make_polynomial_model(xb, yb, 10)
	fb50 = make_polynomial_model(xb, yb, 50)

	print("Errors for only the time after inflection point")
	for f in [fb1, fb2, fb3, fb10, fb50]:
	    print("Error d=%i: %f" % (f.order, error(f, xb, yb)))

	plot_models(
	    x, y, [fb1, fb2, fb3, fb10, fb50], join("../../output/analyze_webstats_1400_01_07.png"),
	    mx=sp.linspace(0 * 7 * 24, 6 * 7 * 24, 100),
	    ymax=10000, xmin=0 * 7 * 24)

	print("Errors for only the time after inflection point for after inflection model")
	for f in [fb1, fb2, fb3, fb10, fb50]:
	    print("Error d=%i: %f" % (f.order, error(f, x, y)))

	# separating training from testing data
	frac = 0.3
	split_idx = int(frac * len(xb))
	shuffled = sp.random.permutation(list(range(len(xb))))
	test = sorted(shuffled[:split_idx])
	train = sorted(shuffled[split_idx:])
	fbt1 = make_polynomial_model(xb[train], yb[train], 1)
	fbt2 = make_polynomial_model(xb[train], yb[train], 2)
	fbt3 = make_polynomial_model(xb[train], yb[train], 3)
	fbt10 = make_polynomial_model(xb[train], yb[train], 10)
	fbt50 = make_polynomial_model(xb[train], yb[train], 50)

	print("Test errors for only the time after inflection point")
	for f in [fbt1, fbt2, fbt3, fbt10, fbt50]:
	    print("Error d=%i: %f" % (f.order, error(f, xb[test], yb[test])))

	plot_models(
	    x, y, [fbt1, fbt2, fbt3, fbt10, fbt50], join("../../output/analyze_webstats_1400_01_08.png"),
	    mx=sp.linspace(0 * 7 * 24, 6 * 7 * 24, 100),
	    ymax=10000, xmin=0 * 7 * 24)

	# select best model and predict the time to reach 10000 hit/hour
	print(fbt2)
	print(fbt2 - 100000)
	reached_max = fsolve(fbt2 - 100000, 800) / (7 * 24)
	print("100,000 hits/hour expected at week %f" % reached_max[0])

if __name__ == "__main__":
	main()