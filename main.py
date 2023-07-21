#!/bin/python

# AUTHOR: WESTY
# This python script generates and clusters points on a line (For now) TODO: Process in 2D space.


from random import *
import numpy as np

class Point(object):
	def __init__(self,value, x, y):
		self.title = None
		self.value = randint(0,1)
		self.x = x
		self.y = y # 2d space
		self.is_cluster = False
		self.asigned_cluster = None

	def get_cluster(self): #get asigned cluster of this point
		return self.asigned_cluster

	def asign_to_cluster(self, cluster): #asign this point to a cluster
		self.asigned_cluster = cluster

	def set_as_cluster(self): #to make a point a cluster
		self.is_cluster = True

	def __str__(self):
		if(self.value > 0):
			return f"p_index: {self.x} val={self.value}  clus_index: {None if self.asigned_cluster == None else self.asigned_cluster.x} {'Cluster!' if self.is_cluster else ''}"
		else:
			return f"p_index: {self.x}---------------------- {'Cluster!' if self.is_cluster else ''}"

	def reset(self):
		self.asigned_cluster = None
		self.is_cluster = False


class KCluster(object):
	def __init__(self):
		self.clustering = True
		#generate an array fo random points
		self.line = [Point(randint(0,1),x,0) for x in range(60)]

		#select k random points = The selected points represent clusters


		self.k = 5 #TODO Calculate the value of K
		

		self.selected = choices(population=[p for p in self.line if p.value >0],k=self.k)

		for x in range(len(self.selected)):
			self.line[self.selected[x].x].set_as_cluster()

	def dif(self,p1, p2):
		return p1.x-p2.x if p1.x >=p2.x else p2.x-p1.x

	#asign each point in line to their nearest cluster/
	def asign_clusters(self):
		for x in range(len(self.line)):
			self.line[x].reset() #reset  all points
			if self.line[x].value == 1: #check point is set
				#compare point distance form all clusters and asign to nearest cluster.
				map={}
				for clus in self.selected:
					map[self.dif(self.line[x],clus)] = clus
				d = min(list(map)) #index of new cluster
				nearest_cluster = map[d] #get new cluster
				self.line[x].asign_to_cluster(cluster=self.line[nearest_cluster.x]) #asign point to new cluster
		return self.center_clusters()

	# print results
	def do_print(self):
		print("\n")
		for x in range(len(self.line)):
			print(self.line[x])
		print("\n")

	#adjust cluster by mean
	def center_clusters(self):
		new_selected = []
		for x in range(len(self.selected)):

			#create a new array of p indicies asigned to clus
			temp = [] #a list of cluster indices

			for p in self.line:
				if p.asigned_cluster != None:
					if p.asigned_cluster.x == self.selected[x].x: #check if p is under current cluster
						temp.append(p.x) #list of p=point under a cluster

			#calculate mean and re-position cluster
			i = int(round(np.mean(temp)))
			self.line[i].set_as_cluster() #get nearest cluster to p=point
			new_selected.append(self.line[i]) #update new_clusters

		#stop loop when there is no variation
		var = 0 #count new different cluster positions
		for i in range(len(new_selected)):
			if new_selected[i].x != self.selected[i].x:
				var += 1
		self.selected = new_selected
		return True if var > 0 else False

	def  loop(self):
		print("*"*5,"start","*"*5)
		self.do_print()

		while self.asign_clusters():
			self.do_print()
		self.do_print()
		print("*"*5,"end","*"*5)


if __name__ == "__main__":
	process = KCluster()
	process.loop()
