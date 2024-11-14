#!/usr/bin/env python3

#-------------------------------------------
# IMPORTS
from threading import Lock, Thread
import socket, pickle, time
from copy import deepcopy
import subprocess
import argparse
import os
#-------------------------------------------
# GLOBALS

#Sockets
ip = 'localhost'
port = 8080
phone_ip =  '192.168.1.207' #'localhost' #'192.168.1.1'
phone_port = 9095

# Variables
topfile = 'topology.txt'
weightfile = 'weights.txt'

timeout = 5 #resend for packets if you dont receive in this amount of seconds
# timeout scenario: data packet is dropped before delta/linger has expired, 
# we want to resend so we might be able to get the data before delta/linger expires

pktgen_num = 5
phone_node_connect_order_counter = 0 # index for mobile consumer location
phone_node_connect_order = [4, 7, 4] # connecting gateway after move
velocity = [100, 100, 100] # velocity at each gw connection
delta = [.1, .1, 100] # data deadline in seconds until we move

global_topology = [] #for dijkstras
num_nodes = -1 #number of nodes in the topology
time_left = 0 #remaining time
distance_left = 0 #remaining distance

client = "" # later assigned as subprocess

# Toggles
phone_test = False
iperf_test = False 
logging = True

#Locks
node_init = 0 #0 if nodes are not setup, 1 if nodes are setup
node_init_lock = Lock() #lock for updateing the node init
phone_node = -1 #the number of the node that the phone is currently connected to
phone_node_lock = Lock() #lock for updating the phone node
final_data = [] #so we can pull the data from a thread
final_data_lock = Lock() #lock for updating the data
print_lock = Lock() #lock for updating the data

# Metrics
total_packet_counter = 0 #number of total interests out
total_packet_counter_lock = Lock() #lock to track the total number of return packets
packet_drop = [] #number of packets dropped
packet_drop_lock = Lock() #lock for number of packets dropped

#-------------------------------------------
# CLASS OBJECTS
#-------------------------------------------------------------------------------
# Hybrid name
# contains some redundant fields (hierarchical and flat component)
# for the sake of simpler fetching...
# TODO: functions for fetching fields to get rid of redundant fields
class Hybrid_Name:
	def __init__(self, task, device_name, data_hash, hierarchical_component, flat_component):
		self.task = task #can be either actionOn or sensing (hardcode to actionOn)
		self.device_name = device_name #data name hash (interest and data packet)
		self.data_hash = data_hash #data hash (data packet only)
		self.hierarchical_component = hierarchical_component
		self.flat_component = flat_component #limit is 4 bytes for data name, 8 bytes for data
	#-------------------------------------------
	# Prints Hybrid name in a formatted way.
	def print_info(self):
		print_lock.acquire()
		print("Task: " + self.task)
		print("Device Name: " + self.device_name)
		print("data_hash: " + self.data_hash)
		print("Hierarchical Component: " + self.hierarchical_component)
		print("Flat Component: " + self.flat_component)
		print_lock.release()

#-------------------------------------------------------------------------------
# Pit entry
# contains fields relevant to PIT entry and some metrics
# total: keeps track of how many returning data packets we've seen
class PIT_Entry:
	def __init__(self, incoming_interface, data_name, total):
		self.incoming_interface = incoming_interface #int - number of node we just came from
		self.data_name = data_name #Hybrid_Name object
		self.total = total #total number of instances of a packet we have seen
	#-------------------------------------------
	# Prints pit entry info fomatted
	def print_info(self):
		print_lock.acquire()
		print("Incoming Interface: " + str(self.incoming_interface))
		print("Hierarchical Name Info Start")
		print_lock.release()
		self.data_name.print_info()
		print_lock.acquire()
		print("Hierarchical Name Info End")
		print("Total Counter: " + str(self.total))
		print_lock.release()
	
#-------------------------------------------------------------------------------
# Assumptions: infinite TTL, infinite cache size, no eviction policy
# Assumptions: Only precaching, not caching
# Assumptions: 1 cache entry is all the packets 
# Assumptions: Each cache entry has unique name (no dupes)
# Contains fields relevant to cache
class Cache_Entry:
	def __init__(self, data_name, packet):
		self.data_name = data_name #Hybrid_Name object
		self.packets = [packet] #first data chunk for this cache entry
	def print_info(self):
		print("Hybrid Name Info Start")
		self.data_name.print_info()
		print("Hybrid Name Info End")
		for x in range(len(self.packets)):
			print(self.packets[x].print_info())
			print("")
#-------------------------------------------------------------------------------
# Node
# Represenetative of nodes (routers) in a topology
# Contains FIB, PIT, Cache, and values necessary to have it interact with other nodes
# IP; Port: allow other nodes to connect to this node for communication
# number: an ID that allows us to shut down the node (close threads and sockets) upon completion
# data_name: the data that this node is able to satisfy
class Node:	
	def __init__(self, IP, port, number, data_name, PIT_lock, cache_lock, FIB, weights, PIT, cache):
		self.IP = IP #IP for node
		self.port = port #port for node
		self.number = number #node identifier
		self.data_name = data_name #Hybrid_Name object
		self.PIT_lock = PIT_lock #lock for updating PIT
		self.cache_lock = cache_lock #lock for updating cache
		self.weights = weights # for dijkstras calc; transmission rate 
		self.FIB = FIB
		self.PIT = PIT
		self.cache = cache	
		self.transmission_range = 10 #hardcode the range to 10 units
	#-------------------------------------------
	# Prints Node info formatted
	def print_info(self):
		print_lock.acquire()
		print("IP:" + self.IP)
		print("Port: " + str(self.port))
		print("Number: " + str(self.number))
		print("Hierarchical Name Info Start")
		print_lock.release()
		self.data_name.print_info()
		print_lock.acquire()
		print("Hierarchical Name Info End")
		print("FIB: " + str(self.FIB))
		print("Weights: " + str(self.weights))
		print("PIT: ")
		print_lock.release()
		for x in range(len(self.PIT)):
			print(self.PIT[x].print_info())
			print("")
		print("Cache: ")
		for x in range(len(self.cache)):
			print(self.cache[x].print_info())
			print("")
		print("Transmission Range: " + str(self.transmission_range))
		
#-------------------------------------------------------------------------------
# Topology 
# Reads in a file (formatted like Data_node_can_satisfy \t FIB entry for node connection or 0 if no connection to node
# The topology is N x N where N is the number of nodes
# Initiates and stores each node in topology in self.nodes
class Topology:
	def __init__(self, file, file_2): #pass in a file, set up nodes
		self.nodes = []
		self.weights = []
		self.NDN_FIB = [] #for NDN forwarding
		counter = 0
		f = open(file, 'r')
		
		#Reads in the topology
		while True:
			data = f.readline()
			if not data:
				break
			line = data.split('\t')
			FIB = line[1:]
			temp_FIB = deepcopy(FIB)
			for x in range(len(temp_FIB)):
				if temp_FIB[x].rstrip() == "0":
					temp_FIB[x] = 0
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
			
			# Strips FIB and initializes node
			for x in range(len(FIB)):
				FIB[x] = FIB[x].rstrip()
			temp_node = Node(ip, port + counter, counter, h_name, Lock(), Lock(), FIB, [], [], [])
			
			# keeps track of what port to connect to next 
			counter = counter + 1
			self.nodes.append(temp_node)
		f.close()
		
		f = open(file_2, 'r')
		counter = 0
		#Reads in the weights
		while True:
			data = f.readline()
			if not data:
				break
			line = data.split('\t')
			line = line[1:]
			line = [int(x) for x in line]
			self.weights.append(line)
			self.nodes[counter].weights = line
			counter = counter + 1
		f.close()
		
		#assertions : make sure the weights and FIB have matching topologies
		if len(self.nodes) != len(self.weights) and len(self.nodes) != len(self.NDN_FIB):
			print("Error! Differing amount of rows for nodes and weights!")
			exit(1)
		for x in range(len(self.weights)):
			if len(self.nodes) != len(self.weights[x]) and len(self.nodes) != len(self.NDN_FIB[x]):
				print("Error! Differing amount of columns for nodes and weights!")
				exit(1)	
			for y in range(len(self.weights[x])):
				if x == y and self.weights[x][y] != 0:
					print("Error! Non-zero value detected for sending to yourself!")
					exit(1)
				if ((self.weights[x][y] == -1 and self.NDN_FIB[x][y] != 0) or (self.weights[x][y] != -1 and self.NDN_FIB[x][y] == 0)) and x != y:
					print("Error! FIB entry provided in topology doesn't have matching weight!")
					exit(1)

#-------------------------------------------------------------------------------
# Packet
# Interest or Data packet that stores the hybrid name
# interest if data name has no data_hash, data if it does
# total_packets: tells PIT how many packets to expect
class Packet:
	def __init__(self, name, time, total_packets, counter, number, linger_time, delta, velocity, total_size, payload, alpha, destination):
		self.name = name #Hybrid_Name object
		
		# interest packet only
		self.linger_time = linger_time #lambda
		self.delta = delta #delta
		self.velocity = velocity #v
		self.alpha = alpha # transmission rate of everything so far.
		self.time = time #time we sent the packet
		self.number = number #the number of the packet ID
		
		
		# data packet only
		self.total_packets = total_packets #signifies how many sub packets make up the total data
		self.counter = counter #used to order the packets for reconstruction (for multiple data packets)
		self.total_size = total_size #k, total size of all expecting data packets
		self.payload = payload
		self.destination = destination #-1 if NDN, else destination for precaching
	#-------------------------------------------
	# Prints packet info formatted
	def print_info(self):
		print("Hierarchical Name Info Start")
		self.data_name.print_info()
		print("Hierarchical Name Info End")
		print("Total Packets : " + str(total_packets))
		print("Counter: " + str(self.counter))
		print("Number: " + str(self.number))
		print("Linger Time: " + str(self.linger_time))
		print("Delta: " + str(self.delta))
		print("Velocity: " + str(self.velocity))
		print("Payload: " + str(self.payload))
		print("Alpha: " + str(self.alpha))
		print("Mode: " + str(self.mode))
#-------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
# Socket code
# Given a node, open server sockets to listen for connections
# When packet is received, close socket and Thread to process the packet
# When 'close' is receieved, shutdown the socket and child threads
def socket_code(node):
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
				print("", end="")
				
			# thread to process the packet (Cache, PIT, FIB stuff)
			t1 = Thread(target=service_connection, args=[packet, node, addr[1]-port])
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
def service_connection(packet, node, previous_node):
	global node_init
	global node_init_lock
	global final_data
	global final_data_lock
	global logging
	
	# -----
	# If the packet is 'test' or 'close', don't do any NDN processes
	if packet.name.hierarchical_component == 'test' or packet.name.hierarchical_component == 'close':
		if packet.name.hierarchical_component == 'test':
			print("", end="")
		elif packet.name.hierarchical_component == 'close' and logging:
			print("Shutting down node " + str(node.number))
			
		# If there are still nodes to be tested or closed, send it to the next node in line (indicated by port) 
		if num_nodes != node.number + 1:
			send_packet(ip, port+node.number, port+node.number+num_nodes+1, packet)
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
		precache = False
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
				if local_cache[x].data_name.flat_component == packet.name.flat_component: 
					#if the cache entry has all of the data
					if len(local_cache[x].packets) == local_cache[x].packets[0].total_packets: 
						cache_hit = x
						# if transmission rate is less than delta and linger time --> precache
						# TODO: Shouldn't alpha be a list instead of a sum?
						if not((local_cache[x].packets[0].total_size/packet.alpha) + (time.time()-packet.time) < packet.delta and 
								(local_cache[x].packets[0].total_size/packet.alpha) + (time.time()-packet.time) < packet.linger_time):
							precache = True
						break
		# -----
		# If we are an interest packet AND .. a cache hit occured OR we are at the producer	
		if packet.payload == "" and (cache_hit != -1 or packet.name.hierarchical_component == node.data_name.hierarchical_component): 
			if cache_hit != -1:
				if logging:
					print("Cache hit")
				node.cache_lock.acquire()
				local_cache = node.cache[cache_hit]
				node.cache_lock.release()
				for x in range(len(local_cache)): # appending cached data packets
					new_packets.append(local_cache.packets[x])
					next_node.append(previous_node) #always send back (clear PITs)
				if precache == True:
					if logging:
						print("Precaching")
					new_destination = next_gateway(node, packet.velocity) 
					temp_next = dijkstras(node.number, new_destination, global_topology)[2] #find the next hop
					for x in range(len(new_packets)): #adding new packets and destination
						temp_packet = deepcopy(new_packet[x])
						temp_packet.destination = new_destination
						new_packets.append(temp_packet)
						next_node.append(temp_next)
			
			else: # Not a cache hit, append node's data as payload in packet and add data_hash to data_name
				if logging:
					print("Reached Producer")
				new_packets, total_size = generate_packets(packet, node.data_name) # generates data packets to be sent
				for x in range(len(new_packets)):
					next_node.append(previous_node) #always send back 
				# if sending to original won't meet delta/linger requirement --> precache
				if not((total_size/packet.alpha) + (time.time()-packet.time) < packet.delta and (total_size/packet.alpha) + (time.time()-packet.time) < packet.linger_time):
					if logging:
						print("Precaching")
					new_destination = next_gateway(node, packet.velocity)
					temp_next = dijkstras(node.number, new_destination, global_topology)[2]
					for x in range(len(new_packets)): #adding new packets and destination
						temp_packet = deepcopy(new_packets[x])
						temp_packet.destination = new_destination
						new_packets.append(temp_packet)
						next_node.append(temp_next)
		
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
				if temp_next == packet.destination:
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
					node.PIT.append(PIT_Entry(previous_node, packet.name, deepcopy(node.PIT[x].total))) #record in PIT
					node.PIT_lock.release()
					break 
			
			# If no collapsing, record in PIT
			if collapse == False:
				node.PIT.append(PIT_Entry(previous_node, packet.name, 0)) #record in PIT
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
				packet.alpha = packet.alpha + node.weights[counter.index(max(counter))]
				new_packets.append(packet)
		
		# -----
		#Send packet
		for x in range(len(next_node)):
		
			# If back to Access Point (aka -1)
			# update nth interest's final_data (sorted in main)
			if next_node[x] == -1:
				if packet.destination == -1: #only care about non precache
					final_data_lock.acquire()					
					final_data[new_packets[x].number].append(new_packets[x])
					packet_drop_lock.acquire()
					packet_drop[new_packets[x].number].append(time.time())
					packet_drop_lock.release()
					final_data_lock.release()
			# Not done, send packets to next nodes.
			else:
				if logging:
					print("Node " + str(node.number) + " is sending data to Node " + str(next_node[x]))
				send_packet(ip, port+node.number, port+next_node[x]+num_nodes, new_packets[x])

#-------------------------------------------------------------------------------	
# Send packet
# Given source and dest port, connect, send packet, and disconnect  
def send_packet(ip, src_port, dest_port, packet):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client.bind((ip, src_port)) # connect
	success = False
	while True: # keep trying to connect until it works
		try:
			client.connect((ip, dest_port))
			success = True
			break
		except:
			continue
	data_to_send = pickle.dumps(packet) 
	client.send(data_to_send) # send data as pickle
	client.close() # disconnect
#-------------------------------------------------------------------------------
# close threads
# sends 'close' message to all nodes until all nodes and threads are closed
def close_threads(thread_list):
	send_packet(ip, port-1, port+num_nodes, Packet(Hybrid_Name("", "", "", 'close', ""), time.time(), 0, 0, -1, -1, -1, -1, -1, "", -1, -1))
	for x in range(len(thread_list)):
			thread_list[x].join()
	print("All nodes offline")

#-------------------------------------------------------------------------------
# generate packets
# returns a list of data_names
def generate_packets(packet, data_name):
	#global iperf3_time
	global pktgen_num
	global client
	new_packets = []
	total_size = 0
	
	# if using iperf to generate data_name, run iperf subprocess
	# CHANGED: simply fetch data rather than generate
	if iperf_test:
		# chop up iperf results into pkSize and append
		pkSize = 600 #1024 doesn't work because of unpickling error
		total_size = len(client.stdout)
		for i in range(0,len(client.stdout), pkSize):
			temp_packet = deepcopy(packet)
			temp_packet.name.data_hash = hash(client.stdout)
			if(i+pkSize >= len(client.stdout)):
				temp_packet.payload = client.stdout[i:len(client.stdout)]
			else:
				temp_packet.payload = client.stdout[i:i+pkSize]
			temp_packet.total_size = len(client.stdout)
			new_packets.append(temp_packet)
	
	# if testing dummy data, new packets are just str of number
	else:
		'''
		total_packet_counter_lock.acquire()
		temp_packet_counter = total_packet_counter
		total_packet_counter_lock.release()
		'''
		total_size = pktgen_num
		for x in range(pktgen_num):
			temp_packet = deepcopy(packet)
			temp_packet.name.data_hash = hash(pktgen_num)
			temp_packet.payload = str(x)
			temp_packet.total_size = pktgen_num
			new_packets.append(temp_packet)
	
	# set all packets' total_packets for PIT entry
	# set all packets' counter for sorting at arrival
	for x in range(len(new_packets)):
		new_packets[x].total_packets = len(new_packets)
		new_packets[x].counter = x
	return new_packets, total_size
#-------------------------------------------------------------------------------
# Next Gateway
# determines where we are going next
# returns destination gateway ID
# TODO: currently hardcoded
def next_gateway(current_node, velocity):
	ret_value = 0
	try:
		ret_value = phone_node_connect_order[phone_node_connect_order_counter]
		phone_node_connect_order_counter += 1
		return ret_value
	except:
		return phone_node_connect_order[-1]
	return ret_value	
#-------------------------------------------------------------------------------
# Calculates the linger time 
# TODO: currently hardcoded
def calc_linger(transmission_range, velocity):
	return velocity	
#-------------------------------------------
# dijkstras
# Finds shortest path from x to y
# returns the shortest path, its weight, and the next hop.
def dijkstras(x, y, topology):
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
				link_weight = link_weight + 1/topology.weights[viable_routes[a][b]][viable_routes[a][b+1]]
			except:
				break
		if smallest_val == -1 or link_weight < smallest_val:
			smallest_val = link_weight
			ret_route = viable_routes[a]
	
	return ret_route, smallest_val, ret_route[1]
	
	
#-------------------------------------------
# argparse
#-------------------------------------------------------------------------------
def readargs():
	global topfile, weightfile, pktgen_num, timeout, phone_node_connect_order
	global velocity, delta, phone_test, iperf_test, logging

	p = argparse.ArgumentParser(description = "Mobile Consumer NDN simulator")
	 
	p.add_argument("-tp", "--topfile", type = str, default = 'topology.txt',
		help = "The file to read in the topology of the NDN system. Should be the same shape as weightfile")
	p.add_argument("-wp", "--weightfile", type = str, default = 'weights.txt',
		help = "The file to read in the weights of the NDN topology. Should be the same shape as topfile")
		
	p.add_argument("-pgn", "--pktgen_num", type = int, default = 5,
		help = "When generating dummy data, determines how many data packets to generate.\n\
		Default is 5 packets.")
		
	p.add_argument("-to", "--timeout", type = float, default = 5,
		help = "Deadline to resend for packets if you dont receive in timeout amount of seconds\n \
		timeout scenario: data packet is dropped before delta/linger has expired,\n \
		we want to resend so we might be able to get the data before delta/linger expires.\n\
		Default is 5 seconds.\
		")
		
	p.add_argument("-pnco", "--phone_node_connect_order", type = str, default = "4, 7, 4",
		help = "The Pattern in which the mobile consumer will disconnect and re-connect to nodes in the topology.\n \
		Eg, the default: 4, 7, 4 means the MC will connect to node 4, then disconnect from node 4 and connect to node 7, then disconnect from node 7 and connect to node 4. It will stay there until the simulation ends. Must be the same length as velocity")
		
	p.add_argument("-v", "--velocity", type = str, default = "100, 100, 100",
		help = "The MC's velocity at each gateway connection.\n\
		Eg, the default: .1, .1, .1 means that at each node the mobile consumer is connecting to,\
		they are travelling at a speed of 0.1 . Must be the same length as phone_node_connect_order")
		
	p.add_argument("-d", "--delta", type = str, default = ".1, .1, 100",
		help = "The deadline in seconds before the data expires and we are no longer interested.\n\
		Eg, the default: .1, .1, 100 means that the data packet must be received by the MC before \
		.1 seconds before the MC moves and the interest is re-sent, this happens again at the re-\
		connection, and finally sits for 100 seconds until the data is received.")
		
	p.add_argument("-pt", "--phone_test", type = str, default = False,
		help = "Toggle to determine whether the simulation will connect to the Android Phone \
		to receive the initial interest packet and send final data. Default is False.")
	p.add_argument("-ipt", "--iperf_test", type = str, default = False,
		help = "Toggle to determine whether the simulation will generate dummy data or generate \
		data via iperf3. Default is False.")
	p.add_argument("-l", "--logging", type = str, default = False,
		help = "Toggle to determine whether all logging information will be printed. Default is False.")
		
	args = p.parse_args()
	
	if not (os.path.isfile(args.topfile)):
		print("Specified topfile", args.topfile ,"does not exist")
		exit()
	if not (os.path.isfile(args.weightfile)):
		print("Specified topfile", args.weightfile ,"does not exist")
		exit()
	if len(args.phone_node_connect_order.split(', ')) != len(args.velocity.split(', ')):
		print("Length of phone_node_connect_order",args.phone_node_connect_order,"is different from length of velocity",args.velocity,"")
		exit()
	
	topfile = args.topfile
	weightfile = args.weightfile
	pktgen_num = args.pktgen_num
	timeout = args.timeout
	phone_node_connect_order = list(map(int, args.phone_node_connect_order.split(', ')))
	velocity = list(map(float, args.velocity.split(', ')))
	delta = list(map(float, args.delta.split(', ')))
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
#-------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__ == "__main__":

	readargs()
	
	# starts iperf3 server if needed
	if iperf_test:
		server = subprocess.Popen(['iperf3', '-s'])
		client = subprocess.run(['iperf3', '-c', 'localhost'], stdout=subprocess.PIPE)
		# closes iperf3 server 
		server.terminate()
		server.wait()
	
	# -----
	# Read in topology & start threads for each node
	# each thread has a node listening, then when packet is received, node threads to service it
	topology = Topology(topfile, weightfile)
	global_topology = topology
	num_nodes = len(topology.nodes)
	thread_list = []
	for x in range(len(topology.nodes)):
		# port + num_nodes: differentiate between current and sending node
		topology.nodes[x].port = topology.nodes[x].port + num_nodes 
		t1 = Thread(target=socket_code, args=[topology.nodes[x]])
		t1.start()
		thread_list.append(t1)
	
	# -----
	# Tests nodes 
	send_packet(ip, port-1, port+num_nodes, Packet(Hybrid_Name("", "", "", 'test', ""), time.time(), 0, 0, -1, -1, -1, -1, -1, "", -1, -1))
	
	# waits until all nodes are online
	while node_init != 1:
		pass

	print("All nodes online")
	
	# -----
	# Connect to server on phone
	if phone_test:
		try:
			

			phone_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			phone_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			phone_client.settimeout(120) # arbitrary timeout
			phone_client.connect((phone_ip, phone_port))

			'''
			phone_client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			#phone_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			#phone_client.settimeout(60) # arbitrary timeout
			#phone_client.connect(('fe80::876:ce23:ba1e:c458', port, 0, 0))
			phone_client.connect(('::1', port, 0, 0))
			'''
			# receive interest from phone
			phone_data = phone_client.recv(1024).decode('utf-8')
		except Exception as e:
			print("Failed to connect to server")
			print(e)
			close_threads(thread_list)
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

	#global phone_node_connect_order
	counter_x = 0
	timeout_counter = 0 
	temp_linger_time = 0 # linger time after timeout
	temp_linger_flag = False # determines when to use temp_linger_time
	rec_data = False
	
	# Sends interest packets until data is received or timeout occurs.
	while True:
		phone_node_lock.acquire()
		try:
			phone_node = phone_node_connect_order[counter_x]
		except: # connect to the last access point repeatedly
			phone_node = phone_node_connect_order[-1]
		phone_node_lock.release()
		
		# increment the number of interest packets out there
		total_packet_counter_lock.acquire()
		temp_packet_counter = total_packet_counter
		total_packet_counter = total_packet_counter + 1
		total_packet_counter_lock.release()
		
		# append expecting final data
		final_data_lock.acquire() 
		final_data.append([])
		final_data_lock.release()
		
		# append counter for packets dropped for this interest
		packet_drop_lock.acquire()
		packet_drop.append([])
		packet_drop_lock.release()
		
		# Sets a timer for each interest
		start_time = time.time()

		#Timeout (only do if not at the end of the list)
		timeout_check = False
		temp_final_data = []
		if temp_linger_flag == False: # calculate linger time
			linger_time = calc_linger(topology.nodes[phone_node].transmission_range, velocity[counter_x])
		else: # use updated linger time (resend occurred)
			linger_time = temp_linger_time
			temp_linger_flag = False
		curr_time = time.time()
		end_time = curr_time + delta[counter_x]
		end_time_1 = curr_time + timeout 
		end_time_2 = curr_time + linger_time 
		
		# Sends interest packet from dummy node (-1) to access point (phone node)
		send_packet(ip, port-1, port+phone_node+num_nodes, Packet(h_name, curr_time, 0, 0, temp_packet_counter, linger_time, delta[counter_x], velocity[counter_x], -1, "", 0, -1))	
		
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
			timestamp.append("Delta Timeout: " + str(delta[counter_x]))
			counter_x = counter_x + 1 #if the timeout was from delta, go to next
			timeout_counter = timeout_counter + 1
			timeout_time.append(end_time)
			if counter_x >= len(delta):
				print("Last delta exceeded! No packets received!")
				break
				
		elif curr_time >= end_time_2:
			print("Linger time exceeded!")
			timestamp.append("Linger Time Timeout: " + str(linger_time))
			counter_x = counter_x + 1
			timeout_counter = timeout_counter + 1
			timeout_time.append(end_time_2)
			if counter_x >= len(delta):
				print("Last linger time exceeded! No packets received!")
				break
				
		elif curr_time >= end_time_1: # when to update the linger/delta
			counter_x = counter_x + 0 # don't progress; resend instead
			delta[counter_x] = delta[counter_x] - timeout #update delta and linger wrt how much time has passed already
			temp_linger_time = linger_time - timeout
			temp_linger_flag = True
			timeout_counter = timeout_counter + 1
			timeout_time.append(end_time_1)
			timestamp.append("Internal Timeout: " + str(timeout))
			print("Internal timeout detected! Resending packet!")
				
		# if we received data within timeout, break	
		if timeout_check:
			print("All packets received!")
			rec_data = True
			break

	# -----
	# Sort the data
	if rec_data == True:
		sorted_final_data = []
		final_data_lock.acquire()
		temp_final_copy = (deepcopy(final_data))[-1]
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
				# iperf data is bytestream
				if iperf_test:
					phone_client.send((sorted_final_data[x].payload))
				else:
					phone_client.send((sorted_final_data[x].payload).encode('utf-8'))
				time.sleep(3)
		print("")
	# close phone socket
	if phone_test: 
		phone_client.close()	
	
	# -----
	# Assert all PITs are empty
	# while waiting for everything to be done 
	while True:
		empty = True
		for x in range(len(topology.nodes)):
			if len(topology.nodes[x].PIT) != 0:
				print("Warning: PIT for node " + str(x) + " is not empty!")
				for y in range(len(topology.nodes[x].PIT)):
					topology.nodes[x].PIT[y].print_info()
					print("")
				print("\n\n")
				empty = False
		if empty == True:
			break
	
	print("Taking nodes offline!")
	close_threads(thread_list)
	
	# -----
	#Metrics
	print("")
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
	print("Percentage of dropped packets: " + str(dropped_counter/total_data_counter*100) + "%")
	print("")
	exit()
	
			
	
	
	
	
