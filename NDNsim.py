#!/usr/bin/env python3

#-------------------------------------------
# IMPORTS

import socket, pickle, time, subprocess, argparse, os
import numpy as np
from copy import deepcopy
from threading import Lock, Thread
from scipy.stats import uniform, norm, zipf
#-------------------------------------------

#-------------------------------------------
# GLOBALS

#Socket config
ip = 'localhost'
port = 8080
phone_ip =  '192.168.1.207' #'localhost' #'192.168.1.1'
phone_port = 9095

# Globals
global_topology = [] #for dijkstras
logging = True

#Locks
phone_node_connect_order_counter = 0 # index for mobile consumer location
phone_node_connect_order_counter_lock = Lock() #lock for phone_node_connect_order_counter
node_init = 0 #0 if nodes are not setup, 1 if nodes are setup
node_init_lock = Lock() #lock for updateing the node init
final_data = [] #so we can pull the data from a thread
final_data_lock = Lock() #lock for updating the data
print_lock = Lock() #lock for updating the data
total_packet_counter = 0 #number of total interests out
total_packet_counter_lock = Lock() #lock to track the total number of return packets
packet_drop = [] #number of packets dropped
packet_drop_lock = Lock() #lock for number of packets dropped
num_precache = 0 #number of times precaching occured
num_precache_lock = Lock() #lock for number of times precaching occured
num_cache_hit = 0 #number of cache hits that occured
num_cache_hit_lock = Lock() #lock for number of cache hits that occured 
#-------------------------------------------

#-------------------------------------------
# CLASS OBJECTS

#-------------------------------------------------------------------------------
# Hybrid name
# contains some redundant fields (hierarchical and flat component)
class Hybrid_Name:
	#phone_data = 'VA/Fairfax/GMU/CS/actionOn:1R153AN' #how the data appears raw
	def __init__(self, task: str='actionOn', device_name: str='1R153AN', data_hash: str='', hierarchical_component: str='VA/Fairfax/GMU/CS', flat_component: str='1R153AN'):
		self.task = task #can be either actionOn or sensing (hardcode to actionOn)
		self.device_name = device_name #data name hash (interest and data packet)
		self.data_hash = data_hash #data hash (data packet only)
		self.hierarchical_component = hierarchical_component
		self.flat_component = flat_component #limit is 4 bytes for data name, 8 bytes for data
		
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		print("Task: " + self.task)
		print("Device Name: " + self.device_name)
		print("Data Hash: " + str(self.data_hash))
		print("Hierarchical Component: " + self.hierarchical_component)
		print("Flat Component: " + self.flat_component)

#-------------------------------------------------------------------------------
# Packet
# Interest or Data packet that stores the hybrid name
# interest if data name has no data_hash, data if it does
# total_packets: tells PIT how many packets to expect
class Packet:
	def __init__(self, name: Hybrid_Name=None, time: float=0.0, total_packets: int=-1, counter: int=-1, alpha: float=0.0, delta: float=0.0, velocity: float=0.0, total_size: int=0, payload: str='', lambda_: float=0.0, destination: int=-1, precache: bool=False, number: int=0):
		self.name = name #Hybrid_Name object
		
		# interest packet
		self.time = time #time we sent the packet
		self.alpha = alpha #linger time
		self.delta = delta #delta
		self.velocity = velocity #v
		self.lambda_ = lambda_ # transmission rate of everything so far.
		
		# data packet only
		self.total_packets = total_packets #signifies how many sub packets make up the total data
		self.counter = counter #used to order the packets for reconstruction (for multiple data packets)
		self.total_size = total_size #k, total size of all expecting data packets
		self.payload = payload
		self.destination = destination #-1 if NDN, else destination for precaching
		self.precache = precache #True if packet was generated due to precaching
		self.number = number #bunches packets together for grouping
		
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		if self.name != None:
			print("Hierarchical Name Info Start")
			self.name.print_info()
			print("Hierarchical Name Info End")
		else:
			print("No Hierarchical Name!")
		print("Time packet sent: " + str(self.time))
		print("Total Packets : " + str(self.total_packets))
		print("Counter: " + str(self.counter))
		print("Alpha/Linger Time: " + str(self.alpha))
		print("Delta: " + str(self.delta))
		print("Velocity: " + str(self.velocity))
		print("Total Size: " + str(self.total_size))
		print("Payload: " + str(self.payload))
		print("Lambda: " + str(self.lambda_))
		print("Destination: " + str(self.destination))
		print("Precache: " + str(self.precache))
		print("Number (for grouping): " + str(self.number))

#-------------------------------------------------------------------------------
# Pit entry
# contains fields relevant to PIT entry and some metrics
# total: keeps track of how many returning data packets we've seen
class PIT_Entry:
	def __init__(self, data_name: Hybrid_Name=None, total: int=0, incoming_interface: int=-1):
		self.data_name = data_name #Hybrid_Name object
		self.total = total #total number of instances of a packet we have seen
		self.incoming_interface = incoming_interface #int - number of node we just came from
			
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		if self.data_name != None:
			print("Hierarchical Name Info Start")
			self.data_name.print_info()
			print("Hierarchical Name Info End")
		else:
			print("No Hierarchical Name!")
		print("Total Counter: " + str(self.total))
		print("Incoming Interface: " + str(self.incoming_interface))
	
#-------------------------------------------------------------------------------
# Cache entry
# Assumptions: infinite TTL, infinite cache size, no eviction policy
# Assumptions: Only precaching, not caching
# Assumptions: 1 cache entry is all the packets 
# Assumptions: Each cache entry has unique name (no dupes)
# Contains fields relevant to cache
class Cache_Entry:
	def __init__(self, data_name: Hybrid_Name=None, packet: list=[]):
		self.data_name = data_name #Hybrid_Name object
		self.packets = packet #array of packets of data chunks for this data
		
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		if self.data_name != None:
			print("Hierarchical Name Info Start")
			self.data_name.print_info()
			print("Hierarchical Name Info End")
		else:
			print("No Hierarchical Name!")
		for x in range(len(self.packets)):
			self.packets[x].print_info()
			print("")
			
#-------------------------------------------------------------------------------
# Node
# Represenetative of nodes (routers) in a topology
# Contains FIB, PIT, Cache, and values necessary to have it interact with other nodes
# IP; Port: allow other nodes to connect to this node for communication
# number: an ID that allows us to shut down the node (close threads and sockets) upon completion
# data_name: the data that this node is able to satisfy
class Node:	
	def __init__(self, IP: str='127.0.0.1', port: int=9999, number: int=-1, data_name: Hybrid_Name=None, PIT_lock: Lock=None, cache_lock: Lock=None, FIB: list=[], weights: list=[], PIT: list=[], cache: list=[], transmission_range: float=-1.0):
		self.IP = IP #IP for node
		self.port = port #port for node
		self.number = number #node identifier
		self.data_name = data_name #Hybrid_Name object
		self.PIT_lock = PIT_lock #lock for updating PIT
		self.cache_lock = cache_lock #lock for updating cache
		self.FIB = FIB
		self.weights = weights # for dijkstras calc; transmission rate 
		self.PIT = PIT
		self.cache = cache	
		self.transmission_range = transmission_range
		
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		print("IP: " + self.IP)
		print("Port: " + str(self.port))
		print("Number: " + str(self.number))
		if self.data_name != None:
			print("Hierarchical Name Info Start")
			self.data_name.print_info()
			print("Hierarchical Name Info End")
		else:
			print("No Hierarchical Name!")
		print("FIB: " + str(self.FIB))
		print("Weights: " + str(self.weights))
		print("PIT: ")
		for x in range(len(self.PIT)):
			self.PIT[x].print_info()
			print("")
		print("Cache: ")
		for x in range(len(self.cache)):
			self.cache[x].print_info()
			print("")
		print("Transmission Range: " + str(self.transmission_range))
		
#-------------------------------------------------------------------------------
# Topology 
# Reads in a file (formatted like Data_node_can_satisfy \t FIB entry for node connection or 0 if no connection to node
# The topology is N x N where N is the number of nodes
# Initiates and stores each node in topology in self.nodes
class Topology:
	def __init__(self, file: str='', weightdist: list=["uniform","0, 1"], trans_range_dist: list=["uniform","0, 8"]):
		self.file = file
		self.weightdist = weightdist
		self.trans_range_dist = trans_range_dist
		self.nodes = []
		self.weights = [] #complete weights
		self.NDN_FIB = [] #complete FIB
		self.read_in_file()
	
	#loads and initializes the topology
	def read_in_file(self):	
		wdist_str = self.weightdist[0]
		wdist_param = list(map(float, self.weightdist[1].split(", ")))
		
		tr_dist_str = self.trans_range_dist[0]
		tr_dist_param = list(map(float, self.trans_range_dist[1].split(", ")))
	
		#Reads in the topology
		try:
			f = open(self.file, 'r')
		except:
			print("Error! File does not exist!")
			exit(1)
		counter = 0
		while True:
			data = f.readline()
			if not data:
				break
				
			#Weights and FIB
			line = data.split('\t')
			FIB = line[1:]
			temp_FIB = deepcopy(FIB)
			temp_weights = []
			for x in range(len(temp_FIB)):
				temp_FIB[x] = temp_FIB[x].rstrip()
				if temp_FIB[x] == "0":
					temp_weights.append(-1)
				else:
					temp_weights.append(distribution_helper(wdist_str, wdist_param, False))
				if (x == counter):
					temp_weights[x] = 0
				if x < counter:
					try:
						temp_weights[x] = self.weights[x][counter]
					except:
						print("Error! Number of rows exceeds number of columns")
						f.close()
						exit(1)
				
			self.weights.append(temp_weights)
			self.NDN_FIB.append(temp_FIB)
			
			# Accepts formatting of hybrid name
			name = line[0]
			temp = name.split(":")
			hierarchical_component = temp[0]
			flat_component = temp[1]
			temp = flat_component.split("|")
			device_name = temp[0]
			data_hash = temp[1]
			# initializes hybrid name
			h_name = Hybrid_Name("", device_name, data_hash, hierarchical_component, flat_component)
			
			# initializes node
			temp_node = Node(ip, port + counter, counter, h_name, Lock(), Lock(), temp_FIB, temp_weights, [], [], distribution_helper(tr_dist_str, tr_dist_param, False))
			
			# keeps track of what port to connect to next 
			counter = counter + 1
			self.nodes.append(temp_node)
			
		f.close()
		
		#Assertions : make sure the weights and FIB have matching topologies
		if len(self.nodes) != len(self.weights) and len(self.nodes) != len(self.NDN_FIB):
			print("Error! Differing amount of rows for nodes and weights")
			exit(1)
		for x in range(len(self.weights)):
			if len(self.nodes) != len(self.weights[x]) and len(self.nodes) != len(self.NDN_FIB[x]):
				print("Error! Differing amount of columns for nodes and weights")
				exit(1)	
			for y in range(len(self.weights[x])):
				if x == y and self.weights[x][y] != 0:
					print("Error! Non-zero value detected for sending to yourself")
					exit(1)
				if ((self.weights[x][y] == -1 and self.NDN_FIB[x][y] != "0") or (self.weights[x][y] != -1 and self.NDN_FIB[x][y] == "0")) and x != y:
					print("Error! FIB entry provided in topology doesn't have matching weight")
					exit(1)
					
	#-------------------------------------------
	# Prints Hybrid name in a formatted way
	def print_info(self):
		print("File: " + self.file)
		print("Weight Dist: ", self.weightdist)
		print("Transmission Range Dist: ", self.trans_range_dist)
		print("Nodes: ")
		for x in range(len(self.nodes)):
			self.nodes[x].print_info()
			print("")
		print("Weights: ", self.weights)
		print("FIB: ", self.NDN_FIB)
		
#-------------------------------------------
# FUNCTIONS

#-------------------------------------------------------------------------------
#Prints object info thread safe
def print_info_helper(value):
	print_lock.acquire()
	value.print_info()
	print_lock.release()
	
#-------------------------------------------------------------------------------
#Distribution helper
def distribution_helper(distribution: str, values: list, cdf: bool) -> float:
	#Parameter checking
	for x in values:
		if x < 0:
			print("Error! One or more values is negative")
			exit(1)
	if distribution == "uniform" or distribution == "gaussian" or distribution == "normal":
		if len(values) != 2:
			print("Error! Values must be a list of len 2 for uniform or gaussian distribution")
			exit(1)
	if distribution == "zipf":
		if len(values) != 1:
			print("Error! Values must be a list of len 1 for zipf")
			exit(1)	

	if distribution == "uniform":
		if values[1] < values[0]:
			print("Error! Maximum value larger than minimum value")
			exit(1)
		number = uniform.rvs(values[0], values[1]-values[0]) # expected values are lower bounds and range (upper bounds + lower bounds)
		if cdf == False:
			return number
		else:
			if values[1] == values[0]:
				return 1.0
			else:
				return uniform.cdf(number, values[0], values[1]-values[0])

	elif distribution == "gaussian" or distribution == "normal":
		number = values[0]
		if values[1] != 0:
			number = norm.rvs(values[0], values[1]) # expected values are mean and std
		if cdf == False:
			return number
		else:
			if values[1] != 0:
				return norm.cdf(number, values[0], values[1])
			else:
				return 1.0
			
	elif distribution == "zipf":
		if values[0] <= 1:
			print("Error! a must be greater than 1")
			exit(1)
		number = zipf.rvs(values[0]) # expected value is distribution parameter
		if cdf == False:
			return number
		else:
			return zipf.cdf(number, values[0])
			
	else:
		print("Error! Unrecognized distribution")
		exit(1)	

#-------------------------------------------------------------------------------
# generate packets
# returns a list of packets and their total size
def generate_packets(packet: Packet, pktgen_num: int, string: str) -> (list, int):
	new_packets = []
	total_size = 0
	
	# if using iperf to generate data_name, run iperf subprocess
	# CHANGED: simply fetch data rather than generate
	if string != "":
		# chop up iperf results into pkSize and append
		pkSize = 256 #1024 doesn't work because of unpickling error
		total_size = len(string)
		for i in range(0, len(string), pkSize):
			temp_packet = deepcopy(packet)
			if temp_packet.name != None:
				temp_packet.name.data_hash = str(hash(string)) ##TODO - is this a hash of the payload or the entire string?
			if(i+pkSize >= len(string)):
				temp_packet.payload = string[i:len(string)]
			else:
				temp_packet.payload = string[i:i+pkSize]
			new_packets.append(temp_packet)
			
	# if testing dummy data, new packets are just str of number
	else:
		for x in range(pktgen_num):
			temp_packet = deepcopy(packet)
			if temp_packet.name != None:
				temp_packet.name.data_hash = str(hash(str(x)))
			temp_packet.payload = str(x)
			total_size = total_size + len(str(x))
			new_packets.append(temp_packet)
	
	# set all packets' total_packets for PIT entry
	# set all packets' counter for sorting at arrival
	for x in range(len(new_packets)):
		new_packets[x].total_packets = len(new_packets)
		new_packets[x].counter = x
		new_packets[x].total_size = total_size
	return new_packets, total_size
	
#-------------------------------------------------------------------------------
# Next Gateway
# determines where we are going next
# returns destination gateway ID
def next_gateway(current_node: Node, velocity: float, phone_node_connect_order: list) -> int:
	global phone_node_connect_order_counter
	ret_value = 0
	phone_node_connect_order_counter_lock.acquire()
	phone_node_connect_order_counter += 1
	phone_node_connect_order_counter_lock.release()
	try:
		ret_value = phone_node_connect_order[phone_node_connect_order_counter]
	except:
		ret_value = -1
	return ret_value	
	
#-------------------------------------------------------------------------------
# Calculates the linger time 
def calc_linger(transmission_range: float, velocity: float, linger_dist: list) -> float:
	pdist = linger_dist[0]
	pdist_params = []
	try:
		pdist_params = list(map(float, linger_dist[1].split(", ")))
	except:
		print("Error! Value(s) in: " + linger_dist[1] + " must be numbers")
		exit(1)
	return distribution_helper(pdist, pdist_params, False)
	
#-------------------------------------------------------------------------------
# argparse helper
# ex: "3:uniform:0, 8" generates 3 values using a uniform distribution with 0 and 8
def split_dist_string(dist_string: str) -> list:
	retval = []
	temp = dist_string.split(":")
	if len(temp) != 3:
		print("Error! Problem formatting string: " + dist_string)
		exit(1)
	
	number_to_gen = 0
	try:
		number_to_gen = int(temp[0])
	except:
		print("Error! First value in string: " + dist_string + " must be an int")
		exit(1)
		
	pdist = temp[1]
	pdist_params = []
	try:
		pdist_params = list(map(float, temp[2].split(", ")))
	except:
		print("Error! Value(s) in: " + temp[2] + " must be numbers")
		exit(1)
		
	for i in range(number_to_gen):
		retval.append(distribution_helper(pdist, pdist_params, False))	
	return retval
	
#-------------------------------------------------------------------------------
# dijkstras
# Finds shortest path from x to y
# only based on the 'weights' field of topology
# returns the shortest path, its weight, and the next hop.
def dijkstras(x: int, y: int, topology: Topology) -> (list, float, int):
	ret_value = 0
	if x == y: #if we are already at the end
		return [x, x], 0, x
	routes = []
	viable_routes = []
	
	# Find all nieghbors from x ; initializing routes to y
	for a in range(len(topology.weights[x])):
		if topology.weights[x][a] != -1 and topology.weights[x][a] != 0:
			routes.append([x, a])	
			if a == y:
				viable_routes.append([x, a])	
	
	# From x's neighbors, add next hop until no more routes.
	# keep track of viable_routes
	counter = 0
	while counter < len(routes):
		node = routes[counter][-1]
		curr_route = routes[counter]
		for a in range(len(topology.weights[node])):
			if topology.weights[node][a] != -1 and topology.weights[node][a]!= 0 and a not in curr_route:
				routes.append(curr_route + [a])
				if a == y:
					viable_routes.append(curr_route + [a])
		counter = counter + 1
		
	smallest_val = -1
	ret_route = []
	
	# find the shortest viable_route from x to y
	for a in range(len(viable_routes)):
		link_weight = 0
		for b in range(len(viable_routes[a])):
			try:
				link_weight = link_weight + 1/topology.weights[viable_routes[a][b]][viable_routes[a][b+1]] #1/n because faster rate means lower number
			except:
				break
		if smallest_val == -1 or link_weight < smallest_val:
			smallest_val = link_weight
			ret_route = viable_routes[a]
	
	return ret_route, smallest_val, ret_route[1]
	
#-------------------------------------------------------------------------------
# does the precaching		
def precache_helper(location, node, packet, new_packets, precache_dist, failure_range, phone_node_connect_order):
	global num_precache
	ret_Fail = True

	#find the number of hops from current to new dest
	new_destination = next_gateway(node, packet.velocity, phone_node_connect_order) 
	if new_destination == -1:
		return [], [], True
	num_hops = len(dijkstras(node.number, new_destination, global_topology)[0]) 
	
	#calculate the odds of failure
	failure_range_values = list(map(float, failure_range.split(", "))) #range of values (ie. [40-60])
	failure_chance = pow(failure_range_values[1], num_hops)
	
	precache_dist_values = list(map(float, precache_dist[1].split(", ")))
	precache_roll = distribution_helper(precache_dist[0], precache_dist_values, True)
	
	if precache_roll < failure_chance:
		print("Expected link failure! Sending via Infrastructure!")
		ret_Fail = False
		
	packets_to_append = []
	nodes_to_append = []
	if logging:
		if location == "cache":
			print("Precaching from cache!")
		else:
			print("Precaching from producer to node", new_destination, "!")	
	num_precache_lock.acquire()
	num_precache = num_precache + 1
	num_precache_lock.release()
	temp_next = -1
	if ret_Fail == True:
		temp_next = dijkstras(node.number, new_destination, global_topology)[2] #find the next hop
	else:
		temp_next = new_destination
	for x in range(len(new_packets)): #adding new packets and destination
		temp_packet = deepcopy(new_packets[x])
		temp_packet.destination = new_destination
		temp_packet.precache = True
		packets_to_append.append(temp_packet)
		nodes_to_append.append(temp_next)	
	return packets_to_append, nodes_to_append, ret_Fail	
	
#-------------------------------------------------------------------------------	
# Send packet
# Given source and dest port, connect, send packet, and disconnect  
def send_packet(ip, src_port, dest_port, packet, failure=True, failure_range="0, 0", failure_dist=["uniform", "0, 0.5"]):

	#Link failure
	if failure == True:
		failure_dist_values = list(map(float, failure_dist[1].split(", "))) #information about ditribution
		failure_range_values = list(map(float, failure_range.split(", "))) #range of values (ie. [40-60], uniform distribution
		failure_roll = distribution_helper(failure_dist[0], failure_dist_values, True) #single value based on distribution
		range_roll = distribution_helper("uniform", failure_range_values, False) #single value based on range
		if failure_roll < range_roll and (packet.name.hierarchical_component != 'close' and packet.name.hierarchical_component != 'test'):
			print("Link failure!")
			return
			
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client.bind((ip, src_port)) # connect
	while True: # keep trying to connect until it works
		try:
			client.connect((ip, dest_port))
			break
		except:
			continue
	
	data_to_send = pickle.dumps(packet) 
	client.send(data_to_send) # send data as pickle
	client.close() # disconnect
	
#-------------------------------------------------------------------------------
# close threads
# sends 'close' message to all nodes until all nodes and threads are closed
def close_threads(thread_list, failure_range, failure_dist):
	send_packet(ip, port-1, port+num_nodes, Packet(Hybrid_Name("", "", "", 'close', ""), time.time(), 0, 0, -1, -1, -1, -1, "", -1, -1, False, -1), False, failure_range, failure_dist)
	for x in range(len(thread_list)):
			thread_list[x].join()
	print("All nodes offline")

#-------------------------------------------------------------------------------
# Socket code
# Given a node, open server sockets to listen for connections
# When packet is received, close socket and Thread to process the packet
# When 'close' is receieved, shutdown the socket and child threads
def socket_code(node, pktgen_num, precache_dist, client, failure_range, failure_dist, phone_node_connect_order, num_nodes):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows us to reuse socket for next run
		s.bind((node.IP, node.port))
		
		if logging:
			print("Node " + str(node.number) + " up on port: " + str(node.port))
			
		s.listen()
		while True:
			conn, addr = s.accept()
			data = conn.recv(1024) # waits for data
			packet = pickle.loads(data) # uses pickle format for sending/receiving
			conn.close()
			
			if (packet.name.hierarchical_component != 'close' and packet.name.hierarchical_component != 'test') and logging:
				print("Node " + str(node.number) + " received data from Node " + str(addr[1]-port))
				
			# thread to process the packet (Cache, PIT, FIB stuff)
			t1 = Thread(target=service_connection, args=[packet, node, addr[1]-port, pktgen_num, precache_dist, client, failure_range, failure_dist, phone_node_connect_order, num_nodes])
			t1.start()
			
			# Closes child threads if we're done
			if packet.name.hierarchical_component == 'close':
				t1.join()
				break
		s.shutdown(socket.SHUT_RDWR)
		s.close()
			
#-------------------------------------------------------------------------------
# Service connection
# When a packet has been receivd at a node, we process it
def service_connection(packet, node, previous_node, pktgen_num, precache_dist, client, failure_range, failure_dist, phone_node_connect_order, num_nodes):
	global node_init, final_data, logging, num_cache_hit, num_precache
	ret_Fail = True
	
	# -----
	# If the packet is 'test' or 'close', don't do any NDN processes
	if packet.name.hierarchical_component == 'test' or packet.name.hierarchical_component == 'close':
		if packet.name.hierarchical_component == 'close' and logging:
			print("Shutting down node " + str(node.number))
			
		# If there are still nodes to be tested or closed, send it to the next node in line (indicated by port) 
		if num_nodes != node.number + 1:
			send_packet(ip, port+node.number, port+node.number+num_nodes+1, packet, False, failure_range, failure_dist)
		# if no more nodes need to be tested or closed, flip node_init flag 
		else:
			node_init_lock.acquire()
			if packet.name.hierarchical_component == 'test':
				node_init = 1
			elif packet.name.hierarchical_component == 'close':
				node_init = 0
			node_init_lock.release()	
	
	# -----
	# If the packet is not 'test' or 'close', begin NDN process
	else:
		cache_hit = -1
		next_node = [] # next node to send to, is list for sending multiple packets
		new_packets = []
		# -----
		# If we are an interest packet, check for a cache hit
		# Assumptions: 1 cache entry is all the packets, can check by seeing if the length of the entry is the value of total_size for the first entry
		if packet.payload == "": 
			node.cache_lock.acquire()
			local_cache = node.cache
			node.cache_lock.release()
			for x in range(len(local_cache)):
				# flat match = cache hit
				if local_cache[x].data_name.device_name == packet.name.device_name: 
					#if the cache entry has all of the data
					if logging:
						print("Cache entry match!")
					if len(local_cache[x].packets) == local_cache[x].packets[0].total_packets: 
						cache_hit = x		
						break
					elif logging:
						print("Cache entry is missing data")
		# -----
		# If we are an interest packet AND .. a cache hit occured OR we are at the producer	
		if packet.payload == "" and (cache_hit != -1 or packet.name.hierarchical_component == node.data_name.hierarchical_component): 
			if cache_hit != -1:
				if logging:
					print("Cache hit!")
				num_cache_hit_lock.acquire()	
				num_cache_hit = num_cache_hit + 1
				num_cache_hit_lock.release()
				node.cache_lock.acquire()
				local_cache = node.cache[cache_hit]
				final_data_lock.acquire()
				for x in range(len(local_cache.packets)): # appending cached data packets
					temp_packet = deepcopy(local_cache.packets[x])
					temp_packet.number = len(final_data)-1
					new_packets.append(temp_packet)
					next_node.append(previous_node) #always send back (clear PITs)
				final_data_lock.release()
				node.cache_lock.release()
				
				#Precache
				if not ((local_cache.packets[0].total_size/packet.lambda_) + (time.time()-packet.time) < packet.alpha):
					packets_to_append, nodes_to_append, ret_Fail = precache_helper("cache", node, packet, new_packets, precache_dist, failure_range, phone_node_connect_order)
					new_packets = new_packets + packets_to_append
					next_node = next_node + nodes_to_append
			
			else: # Not a cache hit, append node's data as payload in packet and add data_hash to data_name
				if logging:
					print("Reached Producer")
				new_packets, total_size = generate_packets(packet, pktgen_num, client) # generates data packets to be sent
				for x in range(len(new_packets)):
					next_node.append(previous_node) #always send back 

				#Precache
				if not ((total_size/packet.lambda_) + (time.time()-packet.time) < packet.alpha):
					packets_to_append, nodes_to_append, ret_Fail  = precache_helper("producer", node, packet, new_packets, precache_dist, failure_range, phone_node_connect_order)
					new_packets = new_packets + packets_to_append
					next_node = next_node + nodes_to_append

		# -----
		# If we are a data packet
		elif packet.payload != "":
			if packet.destination == -1: # NDN routing AKA reverse path
				node.PIT_lock.acquire()	
				pit_index = []
				#Check all PIT entries to see where to go to
				for x in range(len(node.PIT)):
					# match PIT entry
					if node.PIT[x].data_name.hierarchical_component == packet.name.hierarchical_component and node.PIT[x].data_name.device_name == packet.name.device_name:
						# append PIT entry's incoming interface as next node to send to
						next_node.append(node.PIT[x].incoming_interface)
						temp_packet = deepcopy(packet)
						new_packets.append(temp_packet) # add packet as packets to send
						node.PIT[x].total = node.PIT[x].total + 1 # increment the number of data packets we've seen for this PIT entry
						# if number of data packets we've seen matches the number of packets we expect
						if node.PIT[x].total == packet.total_packets: 
							pit_index.append(x) # keep track of PIT entry index to be removed
				# Remove all PIT entries we are going to send to
				# (There can be multiple because of interest collapsing) 
				for x in range(len(pit_index)):
					del node.PIT[(pit_index[-x-1])]
				node.PIT_lock.release()	
			else: # Precache forwarding
				temp_next = dijkstras(node.number, packet.destination, global_topology)[2] #get next hop
				if temp_next == packet.destination and node.number == temp_next:
					next_node.append(-1)
				else:
					next_node.append(temp_next)
				new_packets.append(packet)
			
			# -----
			#TODO - If we wanted to do normal caching (not precaching), do it here
		
		# -----
		# We are an interest packet that needs to go to the next node		
		else:
			collapse = False
			node.PIT_lock.acquire()	
						
			# Check PIT for interest collapsing
			for x in range(len(node.PIT)):
				# PIT entry match
				if node.PIT[x].data_name.hierarchical_component == packet.name.hierarchical_component and node.PIT[x].data_name.device_name == packet.name.device_name:
					print("Interest Collapsed!")
					collapse = True
					node.PIT.append(PIT_Entry(packet.name, deepcopy(node.PIT[x].total), previous_node)) #record in PIT
					node.PIT_lock.release()
					break 
			
			# If no collapsing, record in PIT
			if collapse == False:
				node.PIT.append(PIT_Entry(packet.name, 0, previous_node)) #record in PIT
				node.PIT_lock.release()
				# Using longest prefix matching, figure out where to go next
				counter = []
				packet_name = packet.name.hierarchical_component
				for x in range(len(node.FIB)):
					value = 0
					for y in range(len(node.FIB[x])):
						if node.FIB[x][y] == packet_name[y]:
							value = value + 1
						else:
							break
					counter.append(value) # append match length for xth FIB entry
				next_node.append(counter.index(max(counter))) # append the index of the longest match
				packet.lambda_ = packet.lambda_ + node.weights[counter.index(max(counter))]
				new_packets.append(packet)
		
		# -----
		#Send packet
		for x in range(len(next_node)):
			# If back to Access Point (aka -1)
			# update nth interest's final_data (sorted in main)
			if next_node[x] == -1:
				if packet.destination == -1: #if we are not precaching, return data
					final_data_lock.acquire()					
					final_data[new_packets[x].number].append(new_packets[x])
					packet_drop_lock.acquire()
					packet_drop[new_packets[x].number].append(time.time())
					packet_drop_lock.release()
					final_data_lock.release()
					
				else: #if precaching, cache the data
					node.cache_lock.acquire()
					local_cache = node.cache
					node.cache_lock.release()
					existing_entry = False
					# find pre-exisitng cache entry of same data, if exists
					
					if len(local_cache) > 0:
						for x in range(len(node.cache)):
							# flat match = cache hit
							if local_cache[x].data_name.device_name == new_packets[0].name.device_name: 
								existing_entry = True
								no_chunk = True
								for i in range(len(new_packets)):
									for j in range(len(local_cache[x].packets)):
										# replace old packets if we have it,
										if new_packets[i].counter == local_cache[x].packets[j].counter:
											no_chunk = False
											local_cache[x].packets[j] = new_packets[i]
									# add new packets if its missing
									if no_chunk:
										local_cache[x].packets.append(new_packets[i])
								break
					
					if not existing_entry:
						# if cache entry doesn't exist, create it
						new_cache = Cache_Entry(new_packets[0].name, new_packets)
						node.cache_lock.acquire()
						node.cache.append(new_cache)
						node.cache_lock.release()
					
			# Not done, send packets to next nodes.
			else:
				if logging:
					print("Node " + str(node.number) + " is sending data to Node " + str(next_node[x]))
				send_packet(ip, port+node.number, port+next_node[x]+num_nodes, new_packets[x], ret_Fail, failure_range, failure_dist)

#-------------------------------------------------------------------------------
# argparse
def readargs():
	global logging

	p = argparse.ArgumentParser(description = "Mobile Consumer NDN simulator")
		
	p.add_argument("-o", "--outfile", type = str, default = 'metric_outfile.csv',
		help = "Output file for simulation metrics. Appended to if exists already, creates if not.")
	 
	p.add_argument("-tp", "--topfile", type = str, default = 'topology.txt',
		help = "The file to read in the topology of the NDN system.")
		
	p.add_argument("-w", "--weights", type = str, default = 'uniform:0, 1',
		help = "distribution:distrubution values\n\
		The lambda_ values (aka transmission rates) for each link in the topology \n\
		chosen from the given probability distribution.\n\
		The default, \"uniform:0, 1\" means that each link has a transmission rate \n\
		chosen by the uniform probability distrobution between 0-1")
		
	p.add_argument("-r", "--range", type = str, default = "uniform:0, 2",
		help = "\"distribution:distrubution values\"\n\
		The probability distribution of each node's transmission range.\n\
		Eg, the default: \"uniform:0, 2\" means that each node's transmission range is\n\
		determined by the uniform probability distribution between 0 and 2.")
					
	p.add_argument("-fd", "--failure_dist", type = str, default = "uniform:1, 1",
		help = "\"distribution:distrubution values\"\n\
		The probability distribution for the probability that a packet will fail when sent to the next node.\n\
		Eg: \"uniform:0, 0.5\" means that every time a packet is being sent to another node,\n\
		the possibility of it being sent is determined by the uniform probability distribution between 0 and 0.5.")		
		
	p.add_argument("-fr", "--failure_range", type = str, default = "0, 0.01",
		help = "\"lower bounds, upper bounds\"\n\
		The percentage (from x to y) for the probability that a packet will fail when sent to the next node.\n\
		Eg, \"0.1, 0.5\" means that every time a packet is being sent to another node,\n\
		the possibility of it failing to be sent is between 10% and 50%.")
		
	p.add_argument("-pnco", "--phone_node_connect_order", type = str, default = "3:uniform:0, 8",
		help = "\"amount_to_gen:distribution:distrubution values\"\n\
		The probability distribution for the pattern in which the mobile consumer\n\
		will disconnect and re-connect to nodes in the topology.\n \
		Eg, the default: \"3:uniform:0, 8\" means that the phone will select the next node \
		to travel to by using the uniform probability distirbution between 0-8. It selects 3 times")
		
	p.add_argument("-v", "--velocity", type = str, default = "uniform:0, 2",
		help = "\"distribution:distrubution values\"\n\
		The probability distribution of MC's velocity at each gateway connection.\n\
		Eg, the default: \"uniform:0, 2\" means that at each node the mobile consumer is connecting to,\
		they are travelling at a speed chosen by the uniform probability distribution between 0 and 2.")
		
	p.add_argument("-pgn", "--pktgen_num", type = int, default = 5,
		help = "When generating dummy data, determines how many data packets to generate.\n\
		Default is 5 packets.")
		
	p.add_argument("-pd", "--precache_dist", type = str, default = "uniform:0, 0.01",
		help = "\"distribution:distrubution values\"\n\
		The probability distribution for determining whether a packet will be precached \n\
		through the topology or through the infrastructure.\n\
		Eg, \"uniform:0, 0.5\" means that if the probability of link failure on the link path\n\
		from the current location to the destination node (based on the link failure distribution)\n\
		is greater than a value between 0.0 and 0.5 (chosen by the uniform distribution), then the packet\n\
		will be delivered through the infrastructure instead of the topology.")
		
	p.add_argument("-l", "--linger", type = str, default = "uniform:0, 0.5",
		help = "\"distribution:distrubution values\"\n\
		The probability distribution for MC's linger time at each gateway connection.\n\
		Eg, the default: \"uniform:0, 0.5\" means that at each node the mobile consumer is connecting to,\n\
		they are in range of that node for x seconds as determined by the uniform probability distribution between 0 and 0.5.")		
		
	p.add_argument("-d", "--delta", type = str, default = "3:uniform:0, 0.5",
		help = "\"number_to_gen:distribution:distrubution values\"\n\
		The probability distribution of deadline in seconds before the data expires.\n\
		Eg, the default: \"3:uniform:0, 0.5\" means that the data packet must be received by the MC before \
		the amount of seconds selected by the uniform probability distribution, between 0-0.5, \
		before the MC moves and the interest is re-sent. This happens again 2 more times.")
				
	p.add_argument("-to", "--timeout", type = float, default = 5,
		help = "Deadline to resend for packets if you dont receive in timeout amount of seconds\n \
		timeout scenario: data packet is dropped before delta/linger has expired,\n \
		we want to resend so we might be able to get the data before delta/linger expires.\n\
		Default is 5 seconds.\
		")
		
	p.add_argument("-log", "--logging", type = str, default = False,
		help = "Toggle to determine whether all logging information will be printed. Default is False.")
		
	p.add_argument("-pt", "--phone_test", type = str, default = False,
		help = "Toggle to determine whether the simulation will connect to the Android Phone \
		to receive the initial interest packet and send final data. Default is False.")
		
	p.add_argument("-ipt", "--iperf_test", type = str, default = False,
		help = "Toggle to determine whether the simulation will generate dummy data or generate \
		data via iperf3. Default is False.")

	args = p.parse_args()
	
	if not (os.path.isfile(args.topfile)):
		print("Specified topfile", args.topfile ,"does not exist")
		exit()
	
	# values generated later
	weightdist = args.weights.split(":")
	linger_dist = args.linger.split(":")
	trans_range_dist = args.range.split(":")
	
	# link failure distribution and probability threshold
	failure_dist = args.failure_dist.split(":")
	failure_range = args.failure_range
	precache_dist = args.precache_dist.split(":")
	
	# generate phone node connect order 
	phone_node_connect_order = split_dist_string (args.phone_node_connect_order)
	f = open(args.topfile, 'r')
	data = f.read().split("\n")
	nodemax = len(data)-2
	f.close()
	phone_node_connect_order = [min(int(x), nodemax) for x in phone_node_connect_order]
	
	# generate velocity values
	velocity = split_dist_string (str(len(phone_node_connect_order))+":"+args.velocity)
			
	# generate deltas 
	delta = split_dist_string (args.delta)
	
	phone_test = True
	iperf_test = True
	if (args.phone_test in ["True", "true", "t", "T", "1", "on"]):
		phone_test = True
	else:
		phone_test = False	
	if (args.iperf_test in ["True", "true", "t", "T", "1", "on"]):
		iperf_test = True
	else:
		iperf_test = False
	if (args.logging in ["True", "true", "t", "T", "1", "on"]):
		logging = True
	else:
		logging = False		
		
	print("---")
	print("CLI: python3 NDNsim.py "+ \
	"-o \""+args.outfile+ \
	# for the topology
	"\" -tp \"" +args.topfile+ \
	"\" -w \"" +args.weights+ \
	"\" -r \"" +args.range+ \
	"\" -fd \""+args.failure_dist+ \
	"\" -fr \""+args.failure_range+	\
	# mobile consumer / caching info
	"\" -pnco \"" +args.phone_node_connect_order+\
	"\" -v \"" +args.velocity+ \
	"\" -pgn \"" +str(args.pktgen_num)+ \
	"\" -pd \""+args.precache_dist+ \
	# timeouts/deadlines
	"\" -l \"" +args.linger+ \
	"\" -d \"" +args.delta+ \
	"\" -to \"" +str(args.timeout)+  \
	#toggles
	"\" -log \"" +str(args.logging)+ \
	"\" -pt \"" +str(args.phone_test)+ \
	"\" -ipt \"" +str(args.iperf_test)+ "\"\n")
	
	if logging:
		print("-- DISTRIBUTIONS --")
		print("weightdist:", weightdist)
		print("trans_range_dist:", trans_range_dist)
		print("phone_node_connect_order:", phone_node_connect_order)
		print("velocity:", velocity)
		print("linger_dist:", linger_dist)
		print("delta:", delta)
		#note: failure distribution, failure range, and precache dist are rerolled at the moment.
	return args, args.topfile, weightdist, args.outfile, args.pktgen_num, args.timeout, velocity, delta, linger_dist, trans_range_dist, precache_dist, failure_range, failure_dist, phone_test, iperf_test, phone_node_connect_order

#-------------------------------------------------------------------------------
# MAIN
if __name__ == "__main__":

	args, topfile, weightdist, metrics_outfile, pktgen_num, timeout, velocity, delta, linger_dist, trans_range_dist, precache_dist, failure_range, failure_dist, phone_test, iperf_test, phone_node_connect_order = readargs()
	
	client = ""
	
	# starts iperf3 server if needed
	if iperf_test:
		server = subprocess.Popen(['iperf3', '-s'])
		client = subprocess.run(['iperf3', '-c', 'localhost'], stdout=subprocess.PIPE)
		client = client.stdout.decode("utf-8")
		# closes iperf3 server 
		server.terminate()
		server.wait()
		
	# -----
	# Read in topology & start threads for each node
	# each thread has a node listening, then when packet is received, node threads to service it
	topology = Topology(topfile, weightdist, trans_range_dist)
	global_topology = topology
	num_nodes = len(topology.nodes)
	thread_list = []
	for x in range(len(topology.nodes)):
		# port + num_nodes: differentiate between current and sending node
		topology.nodes[x].port = topology.nodes[x].port + num_nodes 
		t1 = Thread(target=socket_code, args=[topology.nodes[x], pktgen_num, precache_dist, client, failure_range, failure_dist, phone_node_connect_order, num_nodes])
		t1.start()
		thread_list.append(t1)
	
	# -----
	# Tests nodes 
	send_packet(ip, port-1, port+num_nodes, Packet(Hybrid_Name("", "", "", 'test', ""), time.time(), 0, 0, -1, -1, -1, -1, "", -1, -1, False, -1), False, failure_range, failure_dist)
	
	# waits until all nodes are online
	while node_init != 1:
		pass

	print("\n-- SIMULATION START--")
	print("All nodes online")
	# -----
	# Connect to server on phone
	if phone_test:
		try:
			phone_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			phone_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			phone_client.settimeout(120) # arbitrary timeout
			phone_client.connect((phone_ip, phone_port))

			# receive interest from phone
			phone_data = phone_client.recv(1024).decode('utf-8')
		except Exception as e:
			print("Failed to connect to server")
			print(e)
			close_threads(thread_list, failure_range, failure_dist)
			exit()
			
	# If not connecting to phone, use this as interest
	else:
		phone_data = 'VA/Fairfax/GMU/CS/actionOn:1R153AN'
		
	# -----
	# Parse data string and save as hybrid name object
	temp = phone_data.split(":")
	temp2 = temp[0].split("/")
	hierarchical_component = "/".join(temp2[0:len(temp2)-1])
	task = temp2[-1]
	flat_component = temp[1]
	device_name = flat_component
	data_hash = ""
	h_name = Hybrid_Name(task, device_name, data_hash, hierarchical_component, flat_component)

	# -----
	# NDN Gauntlet
	timeout_time = []
	timestamp = [] 
	linger = []

	counter_x = 0
	counter_delta = 0
	timeout_counter = 0 
	alphaout_counter = 0
	delta_timeout_counter = 0
	internal_timeout_counter = 0
	temp_alpha = 0 # linger time after timeout
	temp_linger_flag = False # determines when to use temp_alpha
	rec_data = False
	original_delta = deepcopy(delta)
	
	# Sends interest packets until data is received or timeout occurs.
	while True:
		phone_node = 0
		try:
			phone_node = phone_node_connect_order[counter_x]
		except: # connect to the last access point repeatedly
			phone_node = phone_node_connect_order[-1]
		
		# increment the number of interest packets out there
		total_packet_counter_lock.acquire()
		temp_packet_counter = total_packet_counter
		total_packet_counter = total_packet_counter + 1
		total_packet_counter_lock.release()
		
		# append counter for packets dropped for this interest
		packet_drop_lock.acquire()
		packet_drop.append([])
		packet_drop_lock.release()
		
		# append expecting final data
		final_data_lock.acquire() 
		final_data.append([])
		final_data_lock.release()
		
		# Sets a timer for each interest
		start_time = time.time()

		#Timeout (only do if not at the end of the list)
		timeout_check = False
		temp_final_data = []
		if temp_linger_flag == False: # calculate linger time
			alpha = calc_linger(topology.nodes[phone_node].transmission_range, velocity[counter_x], linger_dist)
			linger.append(alpha)
		else: # use updated linger time (resend occurred)
			alpha = temp_alpha
			temp_linger_flag = False
		
		curr_time = time.time()
		end_time = curr_time + delta[counter_delta]
		end_time_1 = curr_time + timeout 
		end_time_2 = curr_time + alpha 
		
		# Sends interest packet from dummy node (-1) to access point (phone node)
		send_packet(ip, port-1, port+phone_node+num_nodes, Packet(h_name, curr_time, 0, 0, alpha, delta[counter_delta], velocity[counter_x], -1, "", 0.0001, -1, False, len(final_data)-1), True, failure_range, failure_dist)	
		
		# loop until we reach delta, linger, or timeout (end time)
		while ((curr_time <= end_time) and (curr_time <= end_time_1) and (curr_time <= end_time_2)):
			final_data_lock.acquire()
			temp_final_data = final_data
			final_data_lock.release()
			curr_time = time.time()
			
			# checking for the final data in the latest entry (the most recent interest)
			if len(temp_final_data[-1]) == 0:
				continue
			# If we have all expected data packets, no timeout, break
			if len(temp_final_data[-1]) == temp_final_data[-1][0].total_packets:
				timeout_check = True 
				timestamp.append(curr_time-start_time)
				break
			
		# -----
		# Timeouts: if any chokehold is met, we move to the next hardcoded value 
		# unless it's an internal timeout, where instead of moving on, we resend
		# break when last element of listed delta/linger is reached. 
		
		if curr_time >= end_time:
			print("Delta time exceeded!")
			timestamp.append("Delta Timeout: " + str(delta[counter_delta]))
			counter_delta = counter_delta + 1 #if the timeout was from delta, DONT go to next gateway, just move to next delta
			timeout_counter = timeout_counter + 1
			delta_timeout_counter = delta_timeout_counter + 1
			timeout_time.append(end_time)
			if counter_delta >= len(delta):
				print("Last delta exceeded! Interest has failed!")
				break
				
		elif curr_time >= end_time_2:
			print("Linger time exceeded!")
			timestamp.append("Linger Time Timeout: " + str(alpha))
			counter_x = counter_x + 1
			timeout_counter = timeout_counter + 1
			alphaout_counter = alphaout_counter + 1
			timeout_time.append(end_time_2)
			if counter_x >= len(velocity):
				print("Last linger time exceeded! Interest has failed!")
				break
			else:
				print("MC is moving to node", phone_node_connect_order[counter_x])
				
		elif curr_time >= end_time_1: # when to update the linger/delta
			counter_x = counter_x + 0 # don't progress; resend instead
			delta[counter_delta] = delta[counter_delta] - timeout #update delta and linger wrt how much time has passed already
			temp_alpha = alpha - timeout
			temp_linger_flag = True
			timeout_counter = timeout_counter + 1
			internal_timeout_counter = internal_timeout_counter + 1
			timeout_time.append(end_time_1)
			timestamp.append("Internal Timeout: " + str(timeout))
			print("Internal timeout detected! Resending packet!", end=" ")
				
		# if we received data within timeout, break	
		if timeout_check:
			print("All packets received!")
			rec_data = True
			break

	# -----
	# Sort the data
	precache_check = True
	if rec_data == True:
		sorted_final_data = []
		final_data_lock.acquire()
		temp_final_copy = (deepcopy(final_data))[-1]
		test_test = (deepcopy(final_data))
		final_data_lock.release()
		sort_counter = 0
		
		while len(temp_final_copy) != 0:
			for y in range(len(temp_final_copy)):
				if temp_final_copy[y].counter == sort_counter:
					sorted_final_data.append(temp_final_copy[y])
					sort_counter = sort_counter + 1
					del temp_final_copy[y]
					break
		
		# print final data
		print("Data hash:", sorted_final_data[0].name.data_hash)
		print("Final Data: \n", end = "") 
		for x in range(len(sorted_final_data)):
			print(sorted_final_data[x].payload, end='') 
			# -----
			# Send the data packet to the phone
			if phone_test:
				phone_client.send((sorted_final_data[x].payload).encode('utf-8'))
		print("")
		
		
		for x in range(len(sorted_final_data)):
			if sorted_final_data[x].precache == False:
				precache_check = False
				break
	else:
		precache_check = False
	
	# close phone socket
	if phone_test: 
		phone_client.close()	
	
	# -----
	# Assert all PITs are empty
	# while waiting for everything to be done 
	pit_time = time.time()
	while True:
		empty = True
		for x in range(len(topology.nodes)):
			if len(topology.nodes[x].PIT) != 0:
				if pit_time+5 < time.time(): #only print the warning every 5sec, so you know you arent hanging
					pit_time = time.time()
					print("Warning: PIT for node " + str(x) + " is not empty!")
					if (logging):
						for y in range(len(topology.nodes[x].PIT)):
							print_info_helper(topology.nodes[x].PIT[y])
							print("")
						print("\n\n")
				empty = False
		if empty == True:
			break
	
	print("Taking nodes offline!")
	close_threads(thread_list, failure_range, failure_dist)
	
	# -----
	#Metrics
	print("\n--- METRICS ---")
	total_delay = 0
	
	# prints delay of each interest packet
	for x in range(len(timestamp)):
		print("Interest " + str(x) + " had end-to-end delay of: " + str(timestamp[x]))
		if isinstance(timestamp[x], str):
			total_delay = total_delay + float(timestamp[x][timestamp[x].index(":")+2 :])
		else:
			total_delay = total_delay + timestamp[x]
	print("Total End-to-End Delay: " + str(total_delay))
	print("")
	
	# prints number of timeouts for each interest packet
	print("Number of timeouts that happened: " + str(timeout_counter))
	print("")
	dropped_counter = 0
	total_data_counter = 0
	for x in range(len(final_data)):
		total_data_counter = total_data_counter + len(final_data[x])
	counter = 0
	for x in range(len(timeout_time)):
		local_counter = 0
		for y in range(len(packet_drop[x])):
			if packet_drop[x][y] > timeout_time[x]:
				local_counter = local_counter + 1
		dropped_counter = dropped_counter + local_counter
		print("Interest " + str(x) + " had " + str(local_counter) + "/" + str(len(packet_drop[x])) + " packets drop")
		counter = counter + 1
	if len(timeout_time) != len(final_data):
		print("Interest " + str(counter) + " had 0/" + str(len(final_data[counter])) + " packets drop")
	if(total_data_counter>0):
		print("Percentage of dropped packets: " + str(dropped_counter/total_data_counter*100) + "%")
	else:
		total_data_counter = 1
		print("Percentage of dropped packets: " + str(dropped_counter/total_data_counter*100) + "%")
	print("--- END ---\n")
	
	f = ""
	if os.path.isfile(metrics_outfile): #if the file exists already, append
		f = open(metrics_outfile, 'a')
	else: #if the file doesnt exist, create a new one and add the header
		f = open(metrics_outfile, 'w')
		f.write("Topfile, \
Weightdist, \
Range_dist, \
Failure_dist, \
Failure_range, \
Phone_node_connect_order_dist, \
Phone_node_connect_order, \
Velocity_dist,\
Velocity, \
Pktgen_num, \
Precache_dist, \
Linger_dist, \
Linger, \
Delta_dist, \
Delta, \
Timeout, \
Phone_test, iperf_test, \
End-To-End Delay, Total Number of Timeouts, Number of Linger Time Timeouts, Number of Delta Timeouts, Number of Internal Timeouts, Percent of dropped packets, Success?, Cache Hit?, Number of Cache Hits, Number of Times Precached\n")
	
	
	f.write("\""+args.topfile+\
	 "\", \"" +args.weights+\
	 "\", \"" +str(args.range)+\
	 "\", \"" +str(args.failure_dist)+\
	 "\", \"" +str(args.failure_range)+\
	 "\", \"" +args.phone_node_connect_order+\
	 "\", \"" +str(phone_node_connect_order)+\
	 "\", \"" +args.velocity+\
	 "\", \"" +str(velocity)+\
	 "\", \"" +str(args.pktgen_num)+\
	 "\", \"" +str(args.linger)+\
	 "\", \"" +str(linger)+\
	 "\", \"" +args.delta+ "\", \"" +str(delta)+\
	 "\", \"" +str(args.timeout)+\
	 "\", \"" +str(args.phone_test)+ \
	 "\", \"" +str(args.iperf_test)+ \
	 "\", "+ str(total_delay) + ", " + \
	 str(timeout_counter) + ", " + \
	 str(alphaout_counter) + ", " + \
	 str(delta_timeout_counter) + ", " + \
	 str(internal_timeout_counter) + ", " + \
	 str(dropped_counter/total_data_counter*100) + ", " + \
	 str(rec_data) + ", " + \
	 str(precache_check) + ", " + \
	 str(num_cache_hit) + ", " + \
	 str(num_precache) + "\n") 
	
	f.close()
	os._exit(0)
	
			
	
	
	
	
