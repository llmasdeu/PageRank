#!/opt/local/bin/python2.7
# -*- coding: utf-8 -*-

# Mineria de Dades
# Exercici 1: PageRank
# Lluís Masdeu (lluis.masdeu)
# 19/10/2019

import argparse
import sys
import re
from scipy.sparse import coo_matrix
import numpy
import time

def pagerank(graph, beta=0.85, epsilon=1.0e-8):
	# Fill the initializations
	inlink_map=[]
	
	for j in xrange(graph.shape[0]):
		print >>sys.stderr,"Making in-link map of %d\r"%(j),
		inlink_map.append(graph.getcol(j).nonzero()[0])

	# Computes the number of output links each link has
	out_degree=numpy.array(graph.sum(axis=1))
	
	print >>sys.stderr,"\nLink-map done!"

	# Computes the initial old rank
	ranks=numpy.ones(graph.shape[0])/graph.shape[0]

	new_ranks = {}
	delta = 1.0
	n_iterations = 0

	# Computes the PageRank of the links
	while delta > epsilon:
		new_ranks = numpy.zeros(graph.shape[0])

		# Do something here!!!!
		# for x in xrange(graph.shape[0]):
		# 	for y in range(len(inlink_map[x])):
		# 		x_temp = inlink_map[x][y]
		# 		temp = out_degree[x_temp][0]
		# 		if temp != 0:
		# 			new_ranks[x] += ((ranks[x_temp] / temp) * beta)
		new_ranks = computeNewRanks(graph.shape[0], inlink_map, out_degree, ranks, new_ranks, beta, 0)

		delta=numpy.sqrt(numpy.sum(numpy.power(ranks-new_ranks,2)))
		ranks,new_ranks=new_ranks,ranks

		print >>sys.stderr,"\nIteration %d has been computed with an delta of %e (epsilon=%e)"%(n_iterations,delta,epsilon)

		n_iterations += 1

	rranks={}

	for i in xrange(ranks.shape[0]):
		rranks[i]=ranks[i]

	return rranks, n_iterations

def computeNewRanks(size, inlink_map, out_degree, ranks, new_ranks, beta, x):
	if x < size:
		new_ranks[x] = computeNewRankX(len(inlink_map[x]), inlink_map[x], out_degree, ranks, 0) * beta

		if x < size - 1:
			return computeNewRanks(size, inlink_map, out_degree, ranks, new_ranks, beta, x + 1)

	return new_ranks

def computeNewRankX(length, inlinks, out_degree, ranks, y):
	new_rank = 0

	if y < length:
		in_temp = inlinks[y]
		out_temp = out_degree[in_temp][0]

		if out_temp != 0:
			new_rank = ranks[in_temp] / out_temp

		return new_rank + computeNewRankX(length, inlinks, out_degree, ranks, y + 1)

	return new_rank

def processInput(filename):
	webs={}
	rows=numpy.array([],dtype='int8')
	cols=numpy.array([],dtype='int8')
	data=numpy.array([],dtype='float32')

	# For each line of the file, we store the information
	for line in open(filename,'r'):
		line=line.rstrip()
		m=re.match(r'^n\s([0-9]+)\s(.*)',line)

		if m:
			webs[int(m.groups()[0])]=m.groups()[1]
			continue

		m=re.match(r'^e\s([0-9]+)\s([0-9]+)',line)

		if m:
			rows=numpy.append(rows,int(m.groups()[0]))
			cols=numpy.append(cols,int(m.groups()[1]))
			data=numpy.append(data,1)
			
	graph=coo_matrix((data,(rows,cols)),dtype='float32',shape=(max(webs.keys())+1,max(webs.keys())+1))

	return (webs,graph)

if __name__ == "__main__":
	# Setting the recursion limit
	sys.setrecursionlimit(9000000)

	# Parsing the arguments of the program
	parser = argparse.ArgumentParser(description="Analyze web data and output PageRank")
	parser.add_argument("file", type=str, help="file to be processed")
	parser.add_argument("--beta", type=float, help="β value to be considered",default=0.8)
	args = parser.parse_args()

	# Process the file with the list of websites
	webs,graph=processInput(args.file)

	# Computes the PageRank
	start = time.time()
	ranks,n_iterations=pagerank(graph,args.beta)
	end = time.time()

	print >>sys.stderr,"It took %f seconds to converge"%(end - start)

	# Organizes the information to display
	keys=map(lambda x: ranks.keys()[x],numpy.argsort(ranks.values())[-1::-1])
	values=map(lambda x: ranks.values()[x],numpy.argsort(ranks.values())[-1::-1])

	# Displays the information
	for p,(k,v) in enumerate(zip(keys,values)):
		print "[%d] %s:\t%e"%(p,webs[k],v)