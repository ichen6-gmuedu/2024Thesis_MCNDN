#-------------------------------------------
# IMPORTS

import unittest, sys, logging, io, socket, pickle
import numpy as np
from threading import Lock, Thread
sys.path.insert(1, '../')
import NDNsim

#-------------------------------------------
# FUNCTIONS

#Generic socket code to receive 1 packet
#NOT a unit test
def generic_server(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows us to reuse socket for next run
	s.bind((ip, port))
	s.listen()
	while True:
		conn, addr = s.accept()
		data = conn.recv(1024) # waits for data
		packet = pickle.loads(data) # uses pickle format for sending/receiving
		packet.print_info()
		conn.close()
		# Closes child threads if we're done
		if packet.name.hierarchical_component == 'close':
			break
	s.shutdown(socket.SHUT_RDWR)
	s.close()

#-------------------------------------------
# CLASS OBJECT TESTS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestHybridName(unittest.TestCase): #Hybrid Name
	print("WARNING! It is assumed for all objects and functions that the correct *type* of variable is passed in (ie. if a 'int' is expected, an 'int' is received, or if a list of packets it expected, a list of packets is received) and the correct values are passed in (ie. strings should be formatted correctly and numbers are logical).\n\n")
	print("Starting Hybrid Name Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (1)
	#-------------------------------------
	def test_Hybrid_Creation_1(self):
		NDNsim.logging = 3
		#Object 1
		#phone_data = 'VA/Fairfax/GMU/CS/actionOn:1R153AN' #how the data appears raw
		h_name_1 = NDNsim.Hybrid_Name()
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		h_name_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Task: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN'
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (2)
	#-------------------------------------
	def test_Hybrid_Creation_2(self):
		NDNsim.logging = 3
		#Object 1
		#phone_data = 'VA/Fairfax/GMU/CS/actionOn:1R153AN' #how the data appears raw
		h_name_1 = NDNsim.Hybrid_Name()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		h_name_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Task: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN'
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (3)
	#-------------------------------------
	def test_Hybrid_Modification_1(self):
		NDNsim.logging = 3
		#Object 1
		#phone_data = 'VA/Fairfax/GMU/CS/actionOn:1R153AN' #how the data appears raw
		h_name_1 = NDNsim.Hybrid_Name()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		
		h_name_1.task = 'newTask' #Modify value
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		h_name_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Task: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN'
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		h_name_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Task: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111'
		self.assertEqual(output, expected)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestPacket(unittest.TestCase): #Packet

	print("Starting Packet Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (4)
	#-------------------------------------
	def test_Packet_Creation_1(self):
		NDNsim.logging = 3
		#Object 1
		packet_1 = NDNsim.Packet()
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		packet_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'No Hierarchical Name!\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (5)
	#-------------------------------------
	def test_Packet_Creation_2(self):
		NDNsim.logging = 3
		#Object 1
		packet_1 = NDNsim.Packet()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', [1.0], 1, True, 1)	
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		packet_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'No Hierarchical Name!\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (6)
	#-------------------------------------
	def test_Packet_Modification_1(self):
		NDNsim.logging = 3
		#Object 1
		packet_1 = NDNsim.Packet()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', [1.0], 1, True, 1)	
		
		packet_1.name = NDNsim.Hybrid_Name()
		packet_1.name.task = 'newTask' #Modify value
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		packet_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Hierarchical Name Info Start\nTask: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		packet_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: [1.0]\nDestination: 1\nPrecache: True\nNumber (for grouping): 1'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestPIT_Entry(unittest.TestCase): #PIT_Entry

	print("Starting PIT Entry Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (7)
	#-------------------------------------
	def test_PIT_Entry_Creation_1(self):
		NDNsim.logging = 3
		#Object 1
		PIT_Entry_1 = NDNsim.PIT_Entry()
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		PIT_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'No Hierarchical Name!\nTotal Counter: 0\nIncoming Interface: -1'
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (8)
	#-------------------------------------
	def test_PIT_Entry_Creation_2(self):
		NDNsim.logging = 3
		#Object 1
		PIT_Entry_1 = NDNsim.PIT_Entry()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		PIT_Entry_2 = NDNsim.PIT_Entry(1, h_name_2, 1)
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		PIT_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'No Hierarchical Name!\nTotal Counter: 0\nIncoming Interface: -1'
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (9)
	#-------------------------------------
	def test_PIT_Entry_Modification_1(self):
		NDNsim.logging = 3
		#Object 1
		PIT_Entry_1 = NDNsim.PIT_Entry()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111') 
		PIT_Entry_2 = NDNsim.PIT_Entry(h_name_2, 0, -1)
		
		PIT_Entry_1.data_name = NDNsim.Hybrid_Name()
		PIT_Entry_1.data_name.task = 'newTask' #Modify value
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		PIT_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Hierarchical Name Info Start\nTask: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: -1'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		PIT_Entry_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: -1'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestCache_Entry(unittest.TestCase): #Cache Entry

	print("Starting Cache Entry Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (10)
	#-------------------------------------
	def test_Cache_Entry_Creation_1(self):
		NDNsim.logging = 3
		#Object 1
		Cache_Entry_1 = NDNsim.Cache_Entry()
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Cache_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Cache Entry Info Start\nNo Hierarchical Name!\nCache Entry Info End'
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (11)
	#-------------------------------------
	def test_Cache_Entry_Creation_2(self):
		NDNsim.logging = 3
		#Object 1
		Cache_Entry_1 = NDNsim.Cache_Entry()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		packet_2 = NDNsim.Packet()
		Cache_Entry_2 = NDNsim.Cache_Entry(h_name_2, [packet_2])
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Cache_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'Cache Entry Info Start\nNo Hierarchical Name!\nCache Entry Info End'
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (12)
	#-------------------------------------
	def test_Cache_Entry_Modification_1(self):
		NDNsim.logging = 3
		#Object 1
		Cache_Entry_1 = NDNsim.Cache_Entry()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111') #data fields for object
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', [1.0], 1, True, 1)	
		Cache_Entry_2 = NDNsim.Cache_Entry(h_name_2, [packet_2, packet_2])
		
		Cache_Entry_1.data_name = NDNsim.Hybrid_Name()
		Cache_Entry_1.packets = [NDNsim.Packet()]
		Cache_Entry_1.data_name.task = 'newTask' #Modify value
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Cache_Entry_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = '\nPacket 0\nNo Hierarchical Name!\nTime packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\nCache Entry Info End'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Cache_Entry_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\n'
		expected_2 = '\nPacket 0\nHierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\nTime packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: [1.0]\nDestination: 1\nPrecache: True\nNumber (for grouping): 1\n'
		expected_3 = '\nPacket 1\nHierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\nTime packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: [1.0]\nDestination: 1\nPrecache: True\nNumber (for grouping): 1\nCache Entry Info End'
		expected = expected_1 + expected_2 + expected_3
		self.assertEqual(output, expected)
		
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestNode(unittest.TestCase): #Node

	print("Starting Node Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (13)
	#-------------------------------------
	def test_Node_Creation_1(self):
		NDNsim.logging = 3
		#Object 1
		Node_1 = NDNsim.Node()
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Node_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'IP: 127.0.0.1\nPort: 9999\nNumber: -1\nNo Hierarchical Name!\nFIB: []\nWeights: []\nPIT: \nCache: \nTransmission Range: -1.0'
		self.assertEqual(output, expected)

	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (14)
	#-------------------------------------
	def test_Node_Creation_2(self):
		NDNsim.logging = 3
		#Object 1
		Node_1 = NDNsim.Node()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		Node_2 = NDNsim.Node(data_name=h_name_2)
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Node_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected = 'IP: 127.0.0.1\nPort: 9999\nNumber: -1\nNo Hierarchical Name!\nFIB: []\nWeights: []\nPIT: \nCache: \nTransmission Range: -1.0'
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (15)
	#-------------------------------------
	def test_Node_Modification_1(self):
		NDNsim.logging = 3
		#Object 1
		Node_1 = NDNsim.Node()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		Node_2 = NDNsim.Node(data_name=h_name_2)
		
		Node_1.data_name = NDNsim.Hybrid_Name()
		Node_1.data_name.task = 'newTask' #Modify value
		Node_1.cache = [NDNsim.Cache_Entry()]
		Node_1.PIT = [NDNsim.PIT_Entry()]
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Node_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'IP: 127.0.0.1\nPort: 9999\nNumber: -1\n'
		expected_2 = 'Hierarchical Name Info Start\nTask: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_3 = 'FIB: []\nWeights: []\n'
		expected_4 = 'PIT: \nPIT Entry 0:\nNo Hierarchical Name!\nTotal Counter: 0\nIncoming Interface: -1\n\n'
		expected_5 = 'Cache: \nCache Entry Info Start\nNo Hierarchical Name!\nCache Entry Info End\n'
		expected_6 = 'Transmission Range: -1.0'
		expected = expected_1 + expected_2 + expected_3 + expected_4 + expected_5 + expected_6
		self.assertEqual(output, expected)
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Node_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'IP: 127.0.0.1\nPort: 9999\nNumber: -1\n'
		expected_2 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\n'
		expected_3 = 'FIB: []\nWeights: []\n'
		expected_4 = 'PIT: \n'
		expected_5 = 'Cache: \n'
		expected_6 = 'Transmission Range: -1.0'
		expected = expected_1 + expected_2 + expected_3 + expected_4 + expected_5 + expected_6
		self.assertEqual(output, expected)	

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestTopology(unittest.TestCase): #Node

	print("Starting Topology Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (16)
	#-------------------------------------
	def test_Topology_Creation_1(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Object 1
		Topology_1 = NDNsim.Topology('./topologies/small_topology.txt')
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Topology_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		
		expected_1 = 'File: ./topologies/small_topology.txt\n'
		expected_2 = "Weight Dist:  ['uniform', '0, 1']\n"
		expected_3 = "Transmission Range Dist:  ['uniform', '0, 8']\n"
		expected_4 = 'Nodes: \n'
		node_1 = "IP: 127.0.0.1\nPort: 9999\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.417022004702574), -1]\nPIT: \nCache: \nTransmission Range: 5.762595947537265\n\n"
		node_2 = "IP: 127.0.0.1\nPort: 10000\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)]\nPIT: \nCache: \nTransmission Range: 1.1740471265369044\n\n"
		node_3 = "IP: 127.0.0.1\nPort: 10001\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.30233257263183977), 0]\nPIT: \nCache: \nTransmission Range: 1.4900816910213672\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.417022004702574), -1], [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)], [-1, np.float64(0.30233257263183977), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)

	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (17)
	#-------------------------------------
	def test_Topology_Creation_2(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Object 1
		Topology_1 = NDNsim.Topology('./topologies/small_topology.txt')
		
		#Object 2
		Topology_2 = NDNsim.Topology('./topologies/small_topology.txt')
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Topology_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		
		expected_1 = 'File: ./topologies/small_topology.txt\n'
		expected_2 = "Weight Dist:  ['uniform', '0, 1']\n"
		expected_3 = "Transmission Range Dist:  ['uniform', '0, 8']\n"
		expected_4 = 'Nodes: \n'
		node_1 = "IP: 127.0.0.1\nPort: 9999\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.417022004702574), -1]\nPIT: \nCache: \nTransmission Range: 5.762595947537265\n\n"
		node_2 = "IP: 127.0.0.1\nPort: 10000\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)]\nPIT: \nCache: \nTransmission Range: 1.1740471265369044\n\n"
		node_3 = "IP: 127.0.0.1\nPort: 10001\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.30233257263183977), 0]\nPIT: \nCache: \nTransmission Range: 1.4900816910213672\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.417022004702574), -1], [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)], [-1, np.float64(0.30233257263183977), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)
		
	#-------------------------------------
	#Tests changing fields only effects 1 object (18)
	#-------------------------------------
	def test_Topology_Modification_1(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Object 1
		Topology_1 = NDNsim.Topology('./topologies/small_topology.txt')
		
		#Object 2
		Topology_2 = NDNsim.Topology('./topologies/small_topology.txt')
		
		Topology_1.file = ""
		Topology_1.weightdist = ""
		Topology_1.trans_range_dist = ""
		Topology_1.nodes = [NDNsim.Node()]
		Topology_1.weights = [[1]]
		Topology_1.NDN_FIB = [["0"]]
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Topology_1.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'File: \n'
		expected_2 = "Weight Dist:  \n"
		expected_3 = "Transmission Range Dist:  \n"
		expected_4 = 'Nodes: \n'
		node_1 = "IP: 127.0.0.1\nPort: 9999\nNumber: -1\nNo Hierarchical Name!\nFIB: []\nWeights: []\nPIT: \nCache: \nTransmission Range: -1.0\n\n"
		expected_5 = "Weights:  [[1]]\n"
		expected_6 = "FIB:  [['0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + expected_5 + expected_6
		self.assertEqual(output, expected)
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		Topology_2.print_info()
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		
		expected_1 = 'File: ./topologies/small_topology.txt\n'
		expected_2 = "Weight Dist:  ['uniform', '0, 1']\n"
		expected_3 = "Transmission Range Dist:  ['uniform', '0, 8']\n"
		expected_4 = 'Nodes: \n'
		node_1 = "IP: 127.0.0.1\nPort: 9999\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.34556072704304774), -1]\nPIT: \nCache: \nTransmission Range: 3.1741397938453595\n\n"
		node_2 = "IP: 127.0.0.1\nPort: 10000\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.34556072704304774), 0, np.float64(0.4191945144032948)]\nPIT: \nCache: \nTransmission Range: 5.481756003174076\n\n"
		node_3 = "IP: 127.0.0.1\nPort: 10001\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.4191945144032948), 0]\nPIT: \nCache: \nTransmission Range: 7.024939491127563\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.34556072704304774), -1], [np.float64(0.34556072704304774), 0, np.float64(0.4191945144032948)], [-1, np.float64(0.4191945144032948), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)
		
	#-------------------------------------
	#File exists checks (19)
	#-------------------------------------
	def test_Topology_File_Exists_1(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Object 1
		with self.assertRaises(SystemExit) as cm:
			Topology_1 = NDNsim.Topology('')
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! File does not exist!")
		
	#-------------------------------------
	#Assertion checks - missing cell (20)
	#-------------------------------------
	def test_Topology_Assertion_1(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Object 1
		with self.assertRaises(SystemExit) as cm:
			Topology_1 = NDNsim.Topology('./topologies/malformed_topology_1.txt')
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Differing amount of columns for nodes and weights")
		
	#-------------------------------------
	#Assertion checks - missing row (21)
	#-------------------------------------
	def test_Topology_Assertion_2(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Object 1
		with self.assertRaises(SystemExit) as cm:
			Topology_1 = NDNsim.Topology('./topologies/malformed_topology_2.txt')
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Differing amount of columns for nodes and weights")
		
	#-------------------------------------
	#Assertion checks - missing column (22)
	#-------------------------------------
	def test_Topology_Assertion_3(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Object 1
		with self.assertRaises(SystemExit) as cm:
			Topology_1 = NDNsim.Topology('./topologies/malformed_topology_3.txt')
		
		#self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Number of rows exceeds number of columns")				
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestDistributionHelper(unittest.TestCase): #distribution_helper

	print("Starting Distribution Helper Tests")	
	maxDiff = None
	#-------------------------------------
	#Uniform random number check (23)
	#-------------------------------------
	def test_uniform_random_number(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], False)
		self.assertEqual(output, np.float64(0.834044009405148))
	
	#-------------------------------------
	#Uniform cdf check (24)
	#-------------------------------------	
	def test_uniform_cdf(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], True)
		self.assertEqual(output, np.float64(0.417022004702574))

	#-------------------------------------
	#Uniform random number check if same values (25)
	#-------------------------------------	
	def test_uniform_same_value_random_number(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Uniform cdf check if same values (26)
	#-------------------------------------	
	def test_uniform_same_value_cdf(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Gaussian/normal random number check (27)
	#-------------------------------------	
	def test_gaussian_random_number(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 1], False)
		self.assertEqual(output, np.float64(1.6243453636632417))
		
	#-------------------------------------
	#Gaussian/normal cdf check (28)
	#-------------------------------------	
	def test_gaussian_cdf(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 1], True)
		self.assertEqual(output, np.float64(0.9478489396588523))
		
	#-------------------------------------
	#Gaussian/normal random number check if std = 0 (29)
	#-------------------------------------	
	def test_gaussian_random_number_std_0(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Gaussian/normal cdf check if std = 0 (30)
	#-------------------------------------	
	def test_gaussian_cdf_std_0(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Zipf random number check (31)
	#-------------------------------------	
	def test_zipf_random_number(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], False)
		self.assertEqual(output, 1)
		
	#-------------------------------------
	#Zipf cdf check (32)
	#-------------------------------------	
	def test_zipf_cdf(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], True)
		self.assertEqual(output, np.float64(0.6079271018540265))
		
	#-------------------------------------
	#Assertion checks - unknown distribution (33)
	#-------------------------------------	
	def test_unknown_assertion(self):
		NDNsim.logging = 3		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("hello", [], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Unrecognized distribution")				
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestGeneratePackets(unittest.TestCase): #generate_packets

	print("Starting Generate Packets Tests")	
	maxDiff = None
	#-------------------------------------
	#Generate 0 packets (34)
	#-------------------------------------
	def test_generate_0_packet(self):
		NDNsim.logging = 3
		packet = NDNsim.Packet()
		new_packets, total_size = NDNsim.generate_packets(packet, 0, "")
		self.assertEqual(len(new_packets), 0)	
		self.assertEqual(total_size, 0)
		
	#-------------------------------------
	#Generate 1 packet (35)
	#-------------------------------------
	def test_generate_1_packet(self):
		NDNsim.logging = 3
		packet = NDNsim.Packet()
		new_packets, total_size = NDNsim.generate_packets(packet, 1, "")
		packet_output = []
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		for x in range(len(new_packets)):
			new_packets[x].print_info()
			output = out.getvalue().rstrip()
			packet_output.append(output)
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'No Hierarchical Name!\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: 0\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 1\nPayload: 0\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(packet_output[0], expected)
		self.assertEqual(total_size, 1)
		
	#-------------------------------------
	#Generate 1 packet with a name (36)
	#-------------------------------------
	def test_generate_1_name_packet(self):
		NDNsim.logging = 3
		packet = NDNsim.Packet()
		packet.name = NDNsim.Hybrid_Name()
		new_packets, total_size = NDNsim.generate_packets(packet, 1, "")
		packet_output = []
	
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Capture print
		for x in range(len(new_packets)):
			new_packets[x].print_info()
			output = out.getvalue().rstrip()
			packet_output.append(output)
		
		#Redirect STD
		sys.stdout = prev_stdout
		
		#Compare output
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: ' + str(hash(str(0))) + '\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: 0\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 1\nPayload: 0\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(packet_output[0], expected)
		self.assertEqual(total_size, 1)		
	
	#-------------------------------------
	#Generate 15 packets (37)
	#-------------------------------------	
	def test_generate_15_packets(self):
		NDNsim.logging = 3
		#Setting the number of packets and the total size
		num_packets = 2
		size = 0
		for x in range(num_packets):
			size = size + len(str(x))
			
		#Creating and generating packets
		packet = NDNsim.Packet()
		new_packets, total_size = NDNsim.generate_packets(packet, num_packets, "")
		packet_output = []
	
		#Capture print
		for x in range(len(new_packets)):
		
			#Redirect STD
			prev_stdout = sys.stdout
			out = io.StringIO()
			sys.stdout = out
			
			new_packets[x].print_info()
			output = out.getvalue().rstrip()
			packet_output.append(output)
		
			#Redirect STD
			sys.stdout = prev_stdout

			expected_1 = 'No Hierarchical Name!\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : ' + str(num_packets) + '\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: ' + str(size) + '\nPayload: ' + str(x) + '\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)	
		
	#-------------------------------------
	#Generate packets according to iperf (38)
	#-------------------------------------
	def test_iperf3_generation(self):
		NDNsim.logging = 3
		iperf_string = """Client: Connecting to host localhost, port 5201
[  5] local 127.0.0.1 port 57126 connected to 127.0.0.1 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.15 GBytes  61.4 Gbits/sec    0   1.69 MBytes       
[  5]   1.00-2.00   sec  7.28 GBytes  62.5 Gbits/sec    0   1.69 MBytes       
[  5]   2.00-3.00   sec  7.34 GBytes  63.0 Gbits/sec    0   1.69 MBytes       
[  5]   3.00-4.00   sec  7.12 GBytes  61.2 Gbits/sec    0   1.69 MBytes       
[  5]   4.00-5.00   sec  7.49 GBytes  64.3 Gbits/sec    0   1.69 MBytes       
[  5]   5.00-6.00   sec  7.35 GBytes  63.1 Gbits/sec    0   1.69 MBytes       
[  5]   6.00-7.00   sec  7.34 GBytes  63.0 Gbits/sec    0   3.93 MBytes       
[  5]   7.00-8.00   sec  7.34 GBytes  63.1 Gbits/sec    0   3.93 MBytes       
[  5]   8.00-9.00   sec  7.31 GBytes  62.8 Gbits/sec    0   3.93 MBytes       
[  5]   9.00-10.00  sec  7.30 GBytes  62.7 Gbits/sec    0   3.93 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  73.0 GBytes  62.7 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  73.0 GBytes  62.5 Gbits/sec                  receiver

iperf Done.
		"""
		
		#Dividing the payload into 256 byte chunks
		payload = []
		string = ''
		for x in range(len(iperf_string)):
			string = string + iperf_string[x]
			if len(string) == 256:
				payload.append(string)
				string = '' 
		if string != '':
			payload.append(string)
			
		#Setting the number of packets and the total size
		size = len(iperf_string)
			
		#Creating and generating packets
		packet = NDNsim.Packet()
		new_packets, total_size = NDNsim.generate_packets(packet, 0, iperf_string)
		packet_output = []

		#Capture print
		for x in range(len(new_packets)):
		
			#Redirect STD
			prev_stdout = sys.stdout
			out = io.StringIO()
			sys.stdout = out
			
			new_packets[x].print_info()
			output = out.getvalue().rstrip()
			packet_output.append(output)
		
			#Redirect STD
			sys.stdout = prev_stdout

			expected_1 = 'No Hierarchical Name!\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : ' + str(len(new_packets)) + '\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: ' + str(size) + '\nPayload: '
			expected_3 = payload[x]
			expected_4 = '\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2 + expected_3 + expected_4
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)
		
	#-------------------------------------
	#Generate packets according to iperf with a name (39)
	#-------------------------------------
	def test_iperf3_name_generation(self):
		NDNsim.logging = 3
		iperf_string = """Client: Connecting to host localhost, port 5201
[  5] local 127.0.0.1 port 57126 connected to 127.0.0.1 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  7.15 GBytes  61.4 Gbits/sec    0   1.69 MBytes       
[  5]   1.00-2.00   sec  7.28 GBytes  62.5 Gbits/sec    0   1.69 MBytes       
[  5]   2.00-3.00   sec  7.34 GBytes  63.0 Gbits/sec    0   1.69 MBytes       
[  5]   3.00-4.00   sec  7.12 GBytes  61.2 Gbits/sec    0   1.69 MBytes       
[  5]   4.00-5.00   sec  7.49 GBytes  64.3 Gbits/sec    0   1.69 MBytes       
[  5]   5.00-6.00   sec  7.35 GBytes  63.1 Gbits/sec    0   1.69 MBytes       
[  5]   6.00-7.00   sec  7.34 GBytes  63.0 Gbits/sec    0   3.93 MBytes       
[  5]   7.00-8.00   sec  7.34 GBytes  63.1 Gbits/sec    0   3.93 MBytes       
[  5]   8.00-9.00   sec  7.31 GBytes  62.8 Gbits/sec    0   3.93 MBytes       
[  5]   9.00-10.00  sec  7.30 GBytes  62.7 Gbits/sec    0   3.93 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  73.0 GBytes  62.7 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  73.0 GBytes  62.5 Gbits/sec                  receiver

iperf Done.
		"""
		
		#Dividing the payload into 256 byte chunks
		payload = []
		string = ''
		for x in range(len(iperf_string)):
			string = string + iperf_string[x]
			if len(string) == 256:
				payload.append(string)
				string = '' 
		if string != '':
			payload.append(string)
			
		#Setting the number of packets and the total size
		size = len(iperf_string)
			
		#Creating and generating packets
		packet = NDNsim.Packet()
		packet.name = NDNsim.Hybrid_Name()
		new_packets, total_size = NDNsim.generate_packets(packet, 0, iperf_string)
		packet_output = []

		#Capture print
		for x in range(len(new_packets)):
		
			#Redirect STD
			prev_stdout = sys.stdout
			out = io.StringIO()
			sys.stdout = out
			
			new_packets[x].print_info()
			output = out.getvalue().rstrip()
			packet_output.append(output)
		
			#Redirect STD
			sys.stdout = prev_stdout

			expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: ' + str(hash(payload[x])) + '\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : ' + str(len(new_packets)) + '\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: ' + str(size) + '\nPayload: '
			expected_3 = payload[x]
			expected_4 = '\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2 + expected_3 + expected_4
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)		
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestNextGateway(unittest.TestCase): #next_gateway

	print("Starting Next Gateway Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the next gateway for an empty list (40)
	#-------------------------------------
	def test_next_empty_list(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 0)
		self.assertEqual(output, -1)

	#-------------------------------------
	#Tests the next gateway for a 2 sized list (41)
	#-------------------------------------	
	def test_next_2_item_list(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1, 2])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 0)
		self.assertEqual(output, 2)
		
	#-------------------------------------
	#Tests the next gateway for the end of the list (42)
	#-------------------------------------		
	def test_next_end_of_list(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 0)
		self.assertEqual(output, -1)
	
	#-------------------------------------
	#Tests the next gateway for a 5 sized list (43)
	#-------------------------------------		
	def test_next_complete_test(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		
		for x in range(5):
			output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1, 2, 3, 4, 5])
			self.assertEqual(NDNsim.phone_node_connect_order_counter, x)
			if x == 4:
				self.assertEqual(output, -1)
			else:
				self.assertEqual(output, x+2)
			NDNsim.phone_node_connect_order_counter = NDNsim.phone_node_connect_order_counter + 1

#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestCalcLinger(unittest.TestCase): #calc_linger

	print("Starting Calc Linger Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the function (most work is done by distribution helper) (44)
	#-------------------------------------
	def test_calc_linger_getValue(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.calc_linger(0.0, 0.0, ["uniform", "0, 2"])
		self.assertEqual(output, np.float64(0.834044009405148))
		
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestSplitDistString(unittest.TestCase): #gen_N_random_values

	print("Starting Gen N Random Values Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the function (most work is done by distribution helper) (45)
	#-------------------------------------
	def test_gen_N_get_value(self):
		NDNsim.logging = 3
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.gen_N_random_values("3:uniform:0, 8")
		expected = [np.float64(3.336176037620592), np.float64(5.762595947537265), np.float64(0.0009149985387590931)]
		for x in range(len(output)):
			self.assertEqual(output[x], expected[x])
		
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestDijkstras(unittest.TestCase): #dijkstras

	print("Starting Dijkstras Tests")	
	maxDiff = None
	#-------------------------------------
	#Checks for a triangle topology with unequal weights (46)
	#-------------------------------------
	def test_dijkstras_triangle_longest_path(self):
		NDNsim.logging = 3
		#Right triangle, index 0 is top, index 1 is 90 corner, index 2 is other 
		weights = [[0, 1, .001], [1, 0, 1], [.001, 1, 0]]
		shortest_path, weight, next_hop = NDNsim.dijkstras(0, 2, weights)
		self.assertEqual(shortest_path, [0, 1, 2])
		self.assertEqual(weight, 2)
		self.assertEqual(next_hop, 1)

	#-------------------------------------
	#Checks for a triangle topology with equal weights (47)
	#-------------------------------------
	def test_dijkstras_triangle_same_weights(self):
		NDNsim.logging = 3
		#Right triangle, index 0 is top, index 1 is 90 corner, index 2 is other 
		weights = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
		shortest_path, weight, next_hop = NDNsim.dijkstras(0, 2, weights)
		self.assertEqual(shortest_path, [0, 2])
		self.assertEqual(weight, 1)
		self.assertEqual(next_hop, 2)

	#-------------------------------------
	#Checks for starting at the end (48)
	#-------------------------------------		
	def test_dijkstras_triangle_start_at_end(self):
		NDNsim.logging = 3
		#Right triangle, index 0 is top, index 1 is 90 corner, index 2 is other 
		weights = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
		shortest_path, weight, next_hop = NDNsim.dijkstras(0, 0, weights)
		self.assertEqual(shortest_path, [0, 0])
		self.assertEqual(weight, 0)
		self.assertEqual(next_hop, 0)

	#-------------------------------------
	#Checks for equal paths (49)
	#-------------------------------------		
	def test_dijkstras_equal_paths(self):
		NDNsim.logging = 3
		#4 point circle - 0 is south, 1 is west, 2 is north, 3 is east 
		weights = [[0, 1, -1, 1], [1, 0, 1, -1], [-1, 1, 0, 1], [1, -1, 1, 0]]
		shortest_path, weight, next_hop = NDNsim.dijkstras(0, 2, weights)
		self.assertEqual(shortest_path, [0, 1, 2])
		self.assertEqual(weight, 2)
		self.assertEqual(next_hop, 1)
		
	#-------------------------------------
	#Checks for full_topology, assuming all weights are equal (50)
	#-------------------------------------		
	def test_dijkstras_full_topology(self):
		NDNsim.logging = 3
		#Object 1
		Topology_1 = NDNsim.Topology('./topologies/full_topology.txt')
		weights = []
		for x in range(len(Topology_1.weights)):
			temp_weights = []
			for y in range(len(Topology_1.weights[x])):
				if Topology_1.weights[x][y] == 0 or Topology_1.weights[x][y] == -1:
					temp_weights.append(Topology_1.weights[x][y])
				else:
					temp_weights.append(1)
			weights.append(temp_weights)
		shortest_path, weight, next_hop = NDNsim.dijkstras(4, 2, weights)
		self.assertEqual(shortest_path, [4, 1, 2])
		self.assertEqual(weight, 2)
		self.assertEqual(next_hop, 1)
	
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestPrecacheHelper(unittest.TestCase): #precache_packet_helper

	print("Starting Precache Packet Helper Tests")	
	maxDiff = None
	#-------------------------------------
	#Checks if at last node in order (51)
	#-------------------------------------	
	def test_precache_no_next_node(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_pro_del = 0
		NDNsim.num_pro_del_lock = Lock()
		NDNsim.num_infrastructure = 0
		NDNsim.num_infrastructure_lock = Lock()
		NDNsim.phone_node_connect_order_counter = 2
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		NDNsim.global_topology = NDNsim.Topology('./topologies/full_topology.txt')
		
		#Init values for function
		node = NDNsim.global_topology.nodes[0] #node 0 in the topology
		packet = NDNsim.Packet()
		new_packets = []
		top_thresh = ["uniform","0, 1"]
		success_thresh = "50, 50"
		phone_node_connect_order = [0, 1, 2]
		for x in range(5):
			new_packets.append(NDNsim.Packet())
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		packets_to_append, nodes_to_append, ret_Fail = NDNsim.precache_packet_helper("cache", node, packet, new_packets, top_thresh, success_thresh, phone_node_connect_order)
		self.assertEqual(NDNsim.num_pro_del, 0)
		self.assertEqual(NDNsim.num_infrastructure, 0)
		self.assertEqual(packets_to_append, [])
		self.assertEqual(nodes_to_append, [])
		self.assertEqual(ret_Fail, True)

	#-------------------------------------
	#Checks if send thru infrastructure (52)
	#-------------------------------------		
	def test_precache_send_via_infrastructure(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_pro_del = 0
		NDNsim.num_pro_del_lock = Lock()
		NDNsim.num_infrastructure = 0
		NDNsim.num_infrastructure_lock = Lock()
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		NDNsim.global_topology = NDNsim.Topology('./topologies/full_topology.txt')
		
		#Init values for function
		node = NDNsim.global_topology.nodes[0] #node 0 in the topology
		packet = NDNsim.Packet()
		new_packets = []
		top_thresh = ["uniform","0, 1"]
		success_thresh = "1, 1"
		phone_node_connect_order = [0, 2]
		for x in range(5):
			new_packets.append(NDNsim.Packet())
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		packets_to_append, nodes_to_append, ret_Fail = NDNsim.precache_packet_helper("cache", node, packet, new_packets, top_thresh, success_thresh, phone_node_connect_order)
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout
		
		expected_1 = 'No Hierarchical Name!\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: 2\nPrecache: True\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, ("Expected link failure! Sending via Infrastructure!\nPrecaching from cache! Probability of successful delivery: 0.0"))
		self.assertEqual(NDNsim.num_pro_del, 1)
		self.assertEqual(NDNsim.num_infrastructure, 1)
		for x in range(len(packets_to_append)):
			#Redirect STD
			prev_stdout = sys.stdout
			out = io.StringIO()
			sys.stdout = out
			
			packets_to_append[x].print_info()
			output = out.getvalue().rstrip()
		
			#Redirect STD
			sys.stdout = prev_stdout		
		
			self.assertEqual(output, expected)
			self.assertEqual(nodes_to_append[x], 2)
		self.assertEqual(ret_Fail, False)
		
	#-------------------------------------
	#Checks if send thru topology (53)
	#-------------------------------------		
	def test_precache_send_via_topology(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_pro_del = 0
		NDNsim.num_pro_del_lock = Lock()		
		NDNsim.num_infrastructure = 0
		NDNsim.num_infrastructure_lock = Lock()
		NDNsim.phone_node_connect_order_counter = 0
		NDNsim.phone_node_connect_order_counter_lock = Lock()
		NDNsim.global_topology = NDNsim.Topology('./topologies/full_topology.txt')
		
		#Init values for function
		node = NDNsim.global_topology.nodes[0] #node 0 in the topology
		packet = NDNsim.Packet()
		new_packets = []
		top_thresh = ["uniform","0, 1"]
		success_thresh = "0, 0"
		phone_node_connect_order = [0, 2]
		for x in range(5):
			new_packets.append(NDNsim.Packet())
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		packets_to_append, nodes_to_append, ret_Fail = NDNsim.precache_packet_helper("producer", node, packet, new_packets, top_thresh, success_thresh, phone_node_connect_order)
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout
		
		expected_1 = 'No Hierarchical Name!\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: 2\nPrecache: True\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, ("Precaching from producer! Probability of successful delivery: 1.0"))
		self.assertEqual(NDNsim.num_pro_del, 1)
		self.assertEqual(NDNsim.num_infrastructure, 0)
		for x in range(len(packets_to_append)):
			#Redirect STD
			prev_stdout = sys.stdout
			out = io.StringIO()
			sys.stdout = out
			
			packets_to_append[x].print_info()
			output = out.getvalue().rstrip()
		
			#Redirect STD
			sys.stdout = prev_stdout		
		
			self.assertEqual(output, expected)
			self.assertEqual(nodes_to_append[x], 1)
		self.assertEqual(ret_Fail, True)
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestSendPacket(unittest.TestCase): #send_packet
	
	print("Starting Send Packet Tests")	
	maxDiff = None
	#-------------------------------------
	#Checks if a packet can be sent using function and received via generic server code (54)
	#-------------------------------------	
	def test_send_1_packet(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_failure = 0
		NDNsim.num_failure_lock = Lock()	
		
		#Socker config
		ip = 'localhost'
		src_port = 8080
		dest_port = 8081
		
		#Start the server
		t1 = Thread(target=generic_server, args=[ip, dest_port])
		t1.start()
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Send a packet
		packet = NDNsim.Packet()
		packet.name = NDNsim.Hybrid_Name(hierarchical_component = 'close')
		NDNsim.send_packet(ip, src_port, dest_port, packet, False, "0, 0", ["uniform", "0, 0.5"])
		t1.join()
		
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout		
	
		#Check value
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: close\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(NDNsim.num_failure, 0)

	#-------------------------------------
	#Checks if 5 packets can be sent using function and received via generic server code (55)
	#-------------------------------------		
	def test_send_5_packets(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_failure = 0
		NDNsim.num_failure_lock = Lock()	
		
		#Socker config
		ip = 'localhost'
		src_port = 8080
		dest_port = 8081
		
		#Start the server
		t1 = Thread(target=generic_server, args=[ip, dest_port])
		t1.start()
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Send a packet
		expected = ''
		for x in range(5):
			packet = NDNsim.Packet(payload = str(x))
			packet.name = NDNsim.Hybrid_Name()
			if x != 4:
				packet.name.hierarchical_component = 'VA/Fairfax/GMU/CS'
				expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			else:
				packet.name.hierarchical_component = 'close'
				expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: close\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: ' + str(x) + '\nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected + expected_1 + expected_2 + "\n"
			NDNsim.send_packet(ip, src_port, dest_port, packet, False, "0, 0", ["uniform", "0, 0.5"])
		t1.join()
		
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout		
	
		#Check value
		self.assertEqual(output, expected[0:-1])	
		self.assertEqual(NDNsim.num_failure, 0)
		
	#-------------------------------------
	#Checks if link failure is done (56)
	#-------------------------------------		
	def test_link_failure(self):
		#Init globals
		NDNsim.logging = 3
		NDNsim.num_failure = 0
		NDNsim.num_failure_lock = Lock()	
		
		#Socker config
		ip = 'localhost'
		src_port = 8080
		dest_port = 8081
		
		#Start the server
		t1 = Thread(target=generic_server, args=[ip, dest_port])
		t1.start()
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		#Send a packet that will fail
		packet = NDNsim.Packet()
		packet.name = NDNsim.Hybrid_Name()
		NDNsim.send_packet(ip, src_port, dest_port, packet, True, "1, 1", ["uniform", "0, 0.5"])		
		
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
			
		#Check value
		self.assertEqual(output, "Link failure!")	
		self.assertEqual(NDNsim.num_failure, 1)	
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
				
		#Send a packet that will close
		packet = NDNsim.Packet()
		packet.name = NDNsim.Hybrid_Name(hierarchical_component = 'close')
		NDNsim.send_packet(ip, src_port, dest_port, packet, False, "0, 0", ["uniform", "0, 0.5"])
		t1.join()
	
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestPrecache(unittest.TestCase): #precache

	print("Starting Precache Tests")	
	maxDiff = None
	#-------------------------------------
	#Test precache on empty cache (57)
	#-------------------------------------	
	def test_precache_empty_test(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_precache = 0
		NDNsim.num_precache_lock = Lock()

		#Create a node
		node_1 = NDNsim.Node()
		
		#Create 5 new packets to be cached
		new_packets = []
		expected = 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: hello\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		for x in range(5):
			new_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='hello'), counter=x))
			expected_1 = '\nPacket ' + str(x) + '\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: hello\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
			expected = expected + expected_1 + expected_2
		expected = expected + 'Cache Entry Info End\n'
		NDNsim.precache(node_1, new_packets)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.cache)):
			node_1.cache[x].print_info()
	
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
		
		#Check values
		self.assertEqual(output, expected[0:-1])
		self.assertEqual(NDNsim.num_precache, 1)

	#-------------------------------------
	#Test precache on a non-empty cache with no matching entry (58)
	#-------------------------------------	
	def test_precache_not_empty_no_match_test(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_precache = 0
		NDNsim.num_precache_lock = Lock()

		#Create a node
		node_1 = NDNsim.Node()
		
		#Fill the cache with 5 entry of 5 packets
		expected = ''
		for x in range(5):
			temp_packets = []
			expected = expected + 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			for y in range(5):
				expected_1 = '\nPacket ' + str(y) + '\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(y) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
				expected = expected + expected_1 + expected_2
				temp_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name=str(x)), counter=y))
			node_1.cache.append(NDNsim.Cache_Entry(NDNsim.Hybrid_Name(device_name=str(x)), temp_packets))
			expected = expected + 'Cache Entry Info End\n'
	
		#Create 5 new packets to be cached
		new_packets = []
		expected = expected + 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: hello\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		for x in range(5):
			new_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='hello'), counter=x))
			expected_1 = '\nPacket ' + str(x) + '\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: hello\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
			expected = expected + expected_1 + expected_2
		expected = expected + 'Cache Entry Info End\n'
		NDNsim.precache(node_1, new_packets)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.cache)):
			node_1.cache[x].print_info()
	
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
		
		#Check values
		self.assertEqual(output, expected[0:-1])
		self.assertEqual(NDNsim.num_precache, 1)

	#-------------------------------------
	#Test precache on a non-empty cache with matching entry with missing packets (59)
	#-------------------------------------	
	def test_precache_not_empty_test_match_missing(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_precache = 0
		NDNsim.num_precache_lock = Lock()

		#Create a node
		node_1 = NDNsim.Node()
		
		#Fill the cache with 5 entry of 5 packets
		expected = ''
		for x in range(5):
			temp_packets = []
			expected = expected + 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			for y in range(5):
				expected_1 = '\nPacket ' + str(y) + '\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(y) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
				expected = expected + expected_1 + expected_2
				temp_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name=str(x)), counter=y))
			node_1.cache.append(NDNsim.Cache_Entry(NDNsim.Hybrid_Name(device_name=str(x)), temp_packets))
			expected = expected + 'Cache Entry Info End\n'
	
		#Create 5 new packets to be cached
		new_packets = []
		for x in range(5):
			new_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='3'), counter=x))
		NDNsim.precache(node_1, new_packets)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.cache)):
			node_1.cache[x].print_info()
	
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
		
		#Check values
		self.assertEqual(output, expected[0:-1])
		self.assertEqual(NDNsim.num_precache, 1)

	#-------------------------------------
	#Test precache on a non-empty cache with matching entry with no missing packets (60)
	#-------------------------------------	
	def test_precache_not_empty_test_match_not_missing(self):
		NDNsim.logging = 3
		#Init globals
		NDNsim.num_precache = 0
		NDNsim.num_precache_lock = Lock()

		#Create a node
		node_1 = NDNsim.Node()
		
		#Fill the cache with 5 entry of 5 packets
		expected = ''
		for x in range(5):
			temp_packets = []
			expected = expected + 'Cache Entry Info Start\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			for y in range(5):
				expected_1 = '\nPacket ' + str(y) + '\nHierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = ''
				if x == 3:
					expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(y) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 999\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
				else:
					expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: ' + str(y) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0\n'
				expected = expected + expected_1 + expected_2
				temp_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name=str(x)), counter=y))
			node_1.cache.append(NDNsim.Cache_Entry(NDNsim.Hybrid_Name(device_name=str(x)), temp_packets))
			expected = expected + 'Cache Entry Info End\n'
	
		#Create 5 new packets to be cached
		new_packets = []
		for x in range(5):
			new_packets.append(NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='3'), counter=x, total_size=999))
		NDNsim.precache(node_1, new_packets)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.cache)):
			node_1.cache[x].print_info()
	
		#Grab print
		output = out.getvalue().rstrip()
	
		#Redirect STD
		sys.stdout = prev_stdout	
		
		#Check values
		self.assertEqual(output, expected[0:-1])
		self.assertEqual(NDNsim.num_precache, 1)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestInterestPacketNext(unittest.TestCase): #interest_packet_next

	print("Starting Interest Packet Next Tests")	
	maxDiff = None
	#-------------------------------------
	#Test empty PIT (61)
	#-------------------------------------
	def test_interest_empty_pit(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1R153AN', hierarchical_component='VA/Fairfax/GMU/CS'))
		node_1.FIB = ['VA', 'VA/Fairfax/', 'Hello/Fairfax/GMU/CS', 'NA'] #match with [1]
		node_1.weights = [1, 2, 3, 4] #match with [1]
		
		new_packets, next_node = NDNsim.interest_packet_next(node_1, packet, 0)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)	
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: [2]\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [1])	
		
	#-------------------------------------
	#Test interest collapsing, non empty PIT (62)
	#-------------------------------------
	def test_interest_interest_collapse(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'))
		node_1.FIB = ['VA', 'VA/Fairfax/', 'Hello/Fairfax/GMU/CS', 'NA'] #match with [1]
		node_1.weights = [1, 2, 3, 4] #match with [1]
		
		#Make 3 PIT entries
		expected = ''
		for x in range(3):
			node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name=str(x), hierarchical_component='VA/Fairfax/GMU/CS'), 0, 4)))
			expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n'
			expected = expected + expected_1 + expected_2
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
			
		new_packets, next_node = NDNsim.interest_packet_next(node_1, packet, 0)
		
		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Interest Collapsed!")
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: 0'
		expected = expected + expected_1 + expected_2
		
		self.assertEqual(output, expected)	
		self.assertEqual(new_packets, [])
		self.assertEqual(next_node, [])
			
	#-------------------------------------
	#Test no interest collapsing (63)
	#-------------------------------------
	def test_interest_no_interest_collapse(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='100', hierarchical_component='VA/Fairfax/GMU/CS'))
		node_1.FIB = ['VA', 'VA/Fairfax/', 'Hello/Fairfax/GMU/CS', 'NA'] #match with [1]
		node_1.weights = [1, 2, 3, 4] #match with [1]
		
		#Make 3 PIT entries
		expected = ''
		for x in range(3):
			node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name=str(x), hierarchical_component='VA/Fairfax/GMU/CS'), 0, 4)))
			expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n\n'
			expected = expected + expected_1 + expected_2
		
		new_packets, next_node = NDNsim.interest_packet_next(node_1, packet, 0)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()
			print("")

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: 0'
		expected = expected + expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: [2]\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [1])	
	
	#-------------------------------------
	#Test sending packet twice for 2 lambdas (64)
	#-------------------------------------
	def test_interest_multiple_lambda(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		node_2 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='100', hierarchical_component='VA/Fairfax/GMU/CS'))
		node_1.FIB = ['VA', 'VA/Fairfax/', 'Hello/Fairfax/GMU/CS', 'NA'] #match with [1]
		node_1.weights = [1, 2, 3, 4] #match with [1]
		node_2.FIB = ['VA', 'Hello/Fairfax/GMU/CS', 'VA/Fairfax/', 'NA'] #match with [2]
		node_2.weights = [1, 2, 3, 4] #match with [2]
		
		new_packets, next_node = NDNsim.interest_packet_next(node_1, packet, 0)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()
			print("")

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: [2]\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [1])		

		new_packets, next_node = NDNsim.interest_packet_next(node_2, new_packets[0], 1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_2.PIT[x].print_info()
			print("")

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Total Counter: 0\nIncoming Interface: 1'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 100\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: [2, 3]\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [2])						
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestDataPacketNext(unittest.TestCase): #data_packet_next

	print("Starting Data Packet Next Tests")	
	maxDiff = None
	#-------------------------------------
	#Test empty PIT, no precache forwarding (65)
	#-------------------------------------
	def test_data_empty_pit(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1R153AN', hierarchical_component='VA/Fairfax/GMU/CS'), total_packets=1)
		
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		self.assertEqual(new_packets, [])	
		self.assertEqual(next_node, [])	
		
	#-------------------------------------
	#Test non empty PIT, no precache forwarding, 1 matching entry (66)
	#-------------------------------------
	def test_data_1_match(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), total_packets=1)
		
		#Make 3 PIT entries
		expected = ''
		for x in range(3):
			node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name=str(x), hierarchical_component='VA/Fairfax/GMU/CS'), 0, 4)))
			if x != 1:
				expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n'
				expected = expected + expected_1 + expected_2
		
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, expected[0:-1])
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [4])	

	#-------------------------------------
	#Test non empty PIT, no precache forwarding, 2 matching entry (67)
	#-------------------------------------
	def test_data_2_match(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), total_packets=1)
		
		#Make 3 PIT entries
		expected = ''
		for x in range(3):
			node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name=str(x), hierarchical_component='VA/Fairfax/GMU/CS'), 0, 4)))
			if x != 1:
				expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n'
				expected = expected + expected_1 + expected_2
		node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), 0, 7)))
		
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, expected[0:-1])
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected + "\n" + expected)
		self.assertEqual(next_node, [4, 7])	
		
	#-------------------------------------
	#Test non empty PIT, no precache forwarding, 1 matching entry, total_packets (68)
	#-------------------------------------
	def test_data_1_match_total_size(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node()
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), total_packets=2)
		
		#Make 3 PIT entries
		expected = ''
		for x in range(3):
			node_1.PIT.append((NDNsim.PIT_Entry(NDNsim.Hybrid_Name(device_name=str(x), hierarchical_component='VA/Fairfax/GMU/CS'), 0, 4)))
			expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
			expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n'
			if x == 1:
				expected_2 = 'Total Counter: 1\nIncoming Interface: 4\n'
			expected = expected + expected_1 + expected_2
		
		#Send 1/2 packets
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()

		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, expected[0:-1])
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 2\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [4])
		
		#Send 2/2 packets
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	
		
		expected = ''
		for x in range(3):
			if x != 1:
				expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: ' + str(x) + '\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
				expected_2 = 'Total Counter: 0\nIncoming Interface: 4\n'
				expected = expected + expected_1 + expected_2
				
		for x in range(len(node_1.PIT)):
			node_1.PIT[x].print_info()
			
		#Grab print
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, expected[0:-1])
			
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 2\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [4])		
	
	#-------------------------------------
	#Test precache forwarding (69)
	#-------------------------------------
	def test_data_precache(self):
		NDNsim.logging = 3
		node_1 = NDNsim.Node(number=1)
		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), destination=7)
		NDNsim.global_topology = NDNsim.Topology('./topologies/full_topology.txt')
		
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: 7\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [2])

		packet = NDNsim.Packet(name=NDNsim.Hybrid_Name(device_name='1', hierarchical_component='VA/Fairfax/GMU/CS'), destination=1)
		
		new_packets, next_node = NDNsim.data_packet_next(node_1, packet)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out	

		#Grab print		
		for x in range(len(new_packets)):
			new_packets[x].print_info()
		output = out.getvalue().rstrip()

		#Redirect STD
		sys.stdout = prev_stdout	
		
		expected_1 = 'Hierarchical Name Info Start\nTask: actionOn\nDevice Name: 1\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: []\nDestination: 1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		self.assertEqual(next_node, [-1])
				
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
# UNTESTED
#class TestShutdownNodes(unittest.TestCase): #close_threads TODO Mayebe
#class TestSocketCode(unittest.TestCase): #socket_code
#class TestServiceConnection(unittest.TestCase): #service_connection
#class TestReadargs(unittest.TestCase): #readargs
#-------------------------------------------------------------------------------	
	
if __name__ == '__main__':
	unittest.main()

