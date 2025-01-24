#-------------------------------------------
# IMPORTS

import unittest, sys, logging, io
import numpy as np
from threading import Lock
sys.path.insert(1, '../')
import NDNsim

#-------------------------------------------
# CLASS OBJECT TESTS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
class TestHybridName(unittest.TestCase): #Hybrid Name

	print("Starting Hybrid Name Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests object is correctly made (1)
	#-------------------------------------
	def test_Hybrid_Creation_1(self):
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
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (5)
	#-------------------------------------
	def test_Packet_Creation_2(self):
		#Object 1
		packet_1 = NDNsim.Packet()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', 1.0, 1, True, 1)	
	
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
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (6)
	#-------------------------------------
	def test_Packet_Modification_1(self):
		#Object 1
		packet_1 = NDNsim.Packet()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111')
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', 1.0, 1, True, 1)	
		
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
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
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
		expected_2 = 'Time packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: 1.0\nDestination: 1\nPrecache: True\nNumber (for grouping): 1'
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
		expected = 'No Hierarchical Name!'
		self.assertEqual(output, expected)
		
	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (11)
	#-------------------------------------
	def test_Cache_Entry_Creation_2(self):
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
		expected = 'No Hierarchical Name!'
		self.assertEqual(output, expected)

	#-------------------------------------
	#Tests changing fields only effects 1 object (12)
	#-------------------------------------
	def test_Cache_Entry_Modification_1(self):
		#Object 1
		Cache_Entry_1 = NDNsim.Cache_Entry()
	
		#Object 2
		#phone_data = 'VA/Fairfax/GMU/ECE/sensing/111111' #how the data appears raw
		h_name_2 = NDNsim.Hybrid_Name('sensing', '111111', '', 'VA/Fairfax/GMU/ECE', '111111') #data fields for object
		packet_2 = NDNsim.Packet(h_name_2, 1.0, 1, 1, 1.0, 1.0, 1.0, 1, 'hello', 1.0, 1, True, 1)	
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
		expected_1 = 'Hierarchical Name Info Start\nTask: newTask\nDevice Name: 1R153AN\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN\nHierarchical Name Info End\n'
		expected_2 = 'No Hierarchical Name!\nTime packet sent: 0.0\nTotal Packets : -1\nCounter: -1\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 0\nPayload: \nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
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
		expected_1 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\n'
		expected_2 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\nTime packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: 1.0\nDestination: 1\nPrecache: True\nNumber (for grouping): 1\n\n'
		expected_3 = 'Hierarchical Name Info Start\nTask: sensing\nDevice Name: 111111\nData Hash: \nHierarchical Component: VA/Fairfax/GMU/ECE\nFlat Component: 111111\nHierarchical Name Info End\nTime packet sent: 1.0\nTotal Packets : 1\nCounter: 1\nAlpha/Linger Time: 1.0\nDelta: 1.0\nVelocity: 1.0\nTotal Size: 1\nPayload: hello\nLambda: 1.0\nDestination: 1\nPrecache: True\nNumber (for grouping): 1'
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
		expected_4 = 'PIT: \nNo Hierarchical Name!\nTotal Counter: 0\nIncoming Interface: -1\n\n'
		expected_5 = 'Cache: \nNo Hierarchical Name!\n\n'
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
		node_1 = "IP: localhost\nPort: 8080\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.417022004702574), -1]\nPIT: \nCache: \nTransmission Range: 5.762595947537265\n\n"
		node_2 = "IP: localhost\nPort: 8081\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)]\nPIT: \nCache: \nTransmission Range: 1.1740471265369044\n\n"
		node_3 = "IP: localhost\nPort: 8082\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.30233257263183977), 0]\nPIT: \nCache: \nTransmission Range: 1.4900816910213672\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.417022004702574), -1], [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)], [-1, np.float64(0.30233257263183977), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)

	#-------------------------------------	
	#Tests original object isnt overwritten on new object creation (17)
	#-------------------------------------
	def test_Topology_Creation_2(self):
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
		node_1 = "IP: localhost\nPort: 8080\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.417022004702574), -1]\nPIT: \nCache: \nTransmission Range: 5.762595947537265\n\n"
		node_2 = "IP: localhost\nPort: 8081\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)]\nPIT: \nCache: \nTransmission Range: 1.1740471265369044\n\n"
		node_3 = "IP: localhost\nPort: 8082\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.30233257263183977), 0]\nPIT: \nCache: \nTransmission Range: 1.4900816910213672\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.417022004702574), -1], [np.float64(0.417022004702574), 0, np.float64(0.30233257263183977)], [-1, np.float64(0.30233257263183977), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)
		
	#-------------------------------------
	#Tests changing fields only effects 1 object (18)
	#-------------------------------------
	def test_Topology_Modification_1(self):
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
		node_1 = "IP: localhost\nPort: 8080\nNumber: 0\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/Safeway\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [0, np.float64(0.34556072704304774), -1]\nPIT: \nCache: \nTransmission Range: 3.1741397938453595\n\n"
		node_2 = "IP: localhost\nPort: 8081\nNumber: 1\nHierarchical Name Info Start\nTask: \nDevice Name: xxx\nData Hash: yyy\nHierarchical Component: VA/Fairfax/GMU/EEC\nFlat Component: xxx|yyy\nHierarchical Name Info End\nFIB: ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS']\nWeights: [np.float64(0.34556072704304774), 0, np.float64(0.4191945144032948)]\nPIT: \nCache: \nTransmission Range: 5.481756003174076\n\n"
		node_3 = "IP: localhost\nPort: 8082\nNumber: 2\nHierarchical Name Info Start\nTask: \nDevice Name: 1R153AN\nData Hash: Irisean\nHierarchical Component: VA/Fairfax/GMU/CS\nFlat Component: 1R153AN|Irisean\nHierarchical Name Info End\nFIB: ['0', 'VA/Fairfax/GMU/EEC', '0']\nWeights: [-1, np.float64(0.4191945144032948), 0]\nPIT: \nCache: \nTransmission Range: 7.024939491127563\n\n"
		expected_5 = "Weights:  [[0, np.float64(0.34556072704304774), -1], [np.float64(0.34556072704304774), 0, np.float64(0.4191945144032948)], [-1, np.float64(0.4191945144032948), 0]]\n"
		expected_6 = "FIB:  [['0', 'VA/Fairfax/GMU/EEC', '0'], ['VA/Fairfax/Safeway', '0', 'VA/Fairfax/GMU/CS'], ['0', 'VA/Fairfax/GMU/EEC', '0']]"
		expected = expected_1 + expected_2 + expected_3 + expected_4 + node_1 + node_2 + node_3 + expected_5 + expected_6
		self.assertEqual(output, expected)
		
	#-------------------------------------
	#File exists checks (19)
	#-------------------------------------
	def test_Topology_File_Exists_1(self):
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
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], False)
		self.assertEqual(output, np.float64(0.834044009405148))
	
	#-------------------------------------
	#Uniform cdf check (24)
	#-------------------------------------	
	def test_uniform_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], True)
		self.assertEqual(output, np.float64(0.417022004702574))

	#-------------------------------------
	#Uniform random number check if same values (25)
	#-------------------------------------	
	def test_uniform_same_value_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Uniform cdf check if same values (26)
	#-------------------------------------	
	def test_uniform_same_value_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Assertion checks - uniform min > max (27)
	#-------------------------------------
	def test_uniform_assertion(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("uniform", [1, 0], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Maximum value larger than minimum value")		
		
	#-------------------------------------
	#Gaussian/normal random number check (28)
	#-------------------------------------	
	def test_gaussian_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 1], False)
		self.assertEqual(output, np.float64(1.6243453636632417))
		
	#-------------------------------------
	#Gaussian/normal cdf check (29)
	#-------------------------------------	
	def test_gaussian_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 1], True)
		self.assertEqual(output, np.float64(0.9478489396588523))
		
	#-------------------------------------
	#Gaussian/normal random number check if std = 0 (30)
	#-------------------------------------	
	def test_gaussian_random_number_std_0(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Gaussian/normal cdf check if std = 0 (31)
	#-------------------------------------	
	def test_gaussian_cdf_std_0(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Zipf random number check (32)
	#-------------------------------------	
	def test_zipf_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], False)
		self.assertEqual(output, 1)
		
	#-------------------------------------
	#Zipf cdf check (33)
	#-------------------------------------	
	def test_zipf_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], True)
		self.assertEqual(output, np.float64(0.6079271018540265))
		
	#-------------------------------------
	#Assertion checks - a > 1 (34)
	#-------------------------------------
	def test_zipf_assertion(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("zipf", [1], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! a must be greater than 1")		
				
	#-------------------------------------
	#Assertion checks - negative values (35)
	#-------------------------------------
	def test_negative_assertion(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("uniform", [-1, 0], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! One or more values is negative")	
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("uniform", [0, -1], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! One or more values is negative")		
		
	#-------------------------------------
	#Assertion checks - wrong number of values (36)
	#-------------------------------------		
	def test_incorrect_assertion(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("uniform", [0], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Values must be a list of len 2 for uniform or gaussian distribution")			
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("gaussian", [0, 0, 2], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Values must be a list of len 2 for uniform or gaussian distribution")	
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("normal", [], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Values must be a list of len 2 for uniform or gaussian distribution")		
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("zipf", [1, 0], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Values must be a list of len 1 for zipf")	
		
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.distribution_helper("zipf", [], True)	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Values must be a list of len 1 for zipf")						

	#-------------------------------------
	#Assertion checks - unknown distribution (37)
	#-------------------------------------	
	def test_unknown_assertion(self):		
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
	#Generate 0 packets (38)
	#-------------------------------------
	def test_generate_0_packet(self):
		packet = NDNsim.Packet()
		new_packets, total_size = NDNsim.generate_packets(packet, 0, "")
		self.assertEqual(len(new_packets), 0)	
		self.assertEqual(total_size, 0)
		
	#-------------------------------------
	#Generate 1 packet (39)
	#-------------------------------------
	def test_generate_1_packet(self):
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
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: 0\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 1\nPayload: 0\nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(packet_output[0], expected)
		self.assertEqual(total_size, 1)
		
	#-------------------------------------
	#Generate 1 packet with a name (40)
	#-------------------------------------
	def test_generate_1_name_packet(self):
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
		expected_2 = 'Time packet sent: 0.0\nTotal Packets : 1\nCounter: 0\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: 1\nPayload: 0\nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
		expected = expected_1 + expected_2
		self.assertEqual(packet_output[0], expected)
		self.assertEqual(total_size, 1)		
	
	#-------------------------------------
	#Generate 10 packets (41)
	#-------------------------------------	
	def test_generate_15_packets(self):
	
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
			expected_2 = 'Time packet sent: 0.0\nTotal Packets : ' + str(num_packets) + '\nCounter: ' + str(x) + '\nAlpha/Linger Time: 0.0\nDelta: 0.0\nVelocity: 0.0\nTotal Size: ' + str(size) + '\nPayload: ' + str(x) + '\nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)	
		
	#-------------------------------------
	#Generate packets according to iperf (42)
	#-------------------------------------
	def test_iperf3_generation(self):
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
			expected_4 = '\nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2 + expected_3 + expected_4
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)
		
	#-------------------------------------
	#Generate packets according to iperf with a name (43)
	#-------------------------------------
	def test_iperf3_name_generation(self):
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
			expected_4 = '\nLambda: 0.0\nDestination: -1\nPrecache: False\nNumber (for grouping): 0'
			expected = expected_1 + expected_2 + expected_3 + expected_4
			self.assertEqual(packet_output[x], expected)
		self.assertEqual(total_size, size)		
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestNextGateway(unittest.TestCase): #next_gateway

	print("Starting Next Gateway Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the next gateway for an empty list (44)
	#-------------------------------------
	def test_next_empty_list(self):
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 1)
		self.assertEqual(output, -1)

	#-------------------------------------
	#Tests the next gateway for a 2 sized list (45)
	#-------------------------------------	
	def test_next_2_item_list(self):
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1, 2])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 1)
		self.assertEqual(output, 2)
		
	#-------------------------------------
	#Tests the next gateway for the end of the list (46)
	#-------------------------------------		
	def test_next_end_of_list(self):
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		phone_node_connect_order_counter_lock = Lock()
		
		output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1])
		self.assertEqual(NDNsim.phone_node_connect_order_counter, 1)
		self.assertEqual(output, -1)
	
	#-------------------------------------
	#Tests the next gateway for a 5 sized list (47)
	#-------------------------------------		
	def test_next_complete_test(self):
		#Init globals
		NDNsim.phone_node_connect_order_counter = 0
		phone_node_connect_order_counter_lock = Lock()
		
		for x in range(5):
			output = NDNsim.next_gateway(NDNsim.Node(), 0.0, [1, 2, 3, 4, 5])
			self.assertEqual(NDNsim.phone_node_connect_order_counter, x+1)
			if x == 4:
				self.assertEqual(output, -1)
			else:
				self.assertEqual(output, x+2)

#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestCalcLinger(unittest.TestCase): #calc_linger

	print("Starting Calc Linger Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the function (most work is done by distribution helper) (48)
	#-------------------------------------
	def test_calc_linger_getValue(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.calc_linger(0.0, 0.0, ["uniform", "0, 2"])
		self.assertEqual(output, np.float64(0.834044009405148))
		
	#-------------------------------------
	#Assertion check - not numbers (49)
	#-------------------------------------
	def test_calc_linger_assertion(self):
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.calc_linger(0.0, 0.0, ["uniform", "a, 2"])	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: a, 2 must be numbers")
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.calc_linger(0.0, 0.0, ["uniform", "1, b"])	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: 1, b must be numbers")
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.calc_linger(0.0, 0.0, ["zipf", "a"])	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: a must be numbers")
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestSplitDistString(unittest.TestCase): #split_dist_string

	print("Starting Split Dist String Tests")	
	maxDiff = None
	#-------------------------------------
	#Tests the function (most work is done by distribution helper) (50)
	#-------------------------------------
	def test_split_dist_get_value(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.split_dist_string("3:uniform:0, 8")
		expected = [np.float64(3.336176037620592), np.float64(5.762595947537265), np.float64(0.0009149985387590931)]
		for x in range(len(output)):
			self.assertEqual(output[x], expected[x])
		
	#-------------------------------------
	#Tests the formatting to see if 3 values (51)
	#-------------------------------------
	def test_split_dist_assertion_1(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.split_dist_string("3:uniform")
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Problem formatting string: 3:uniform")	
		
	#-------------------------------------
	#Tests the formatting to see if first value is int (52)
	#-------------------------------------
	def test_split_dist_assertion_2(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.split_dist_string("a:uniform:0, 8")
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! First value in string: a:uniform:0, 8 must be an int")	

	#-------------------------------------
	#Tests the formatting to see if 3rd values are numbers (53)
	#-------------------------------------	
	def test_split_dist_assertion_3(self):
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.split_dist_string("1:uniform:a, 2")
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: a, 2 must be numbers")
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.split_dist_string("1:uniform:1, b")	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: 1, b must be numbers")
		
		#Redirect STD
		prev_stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out
		
		with self.assertRaises(SystemExit) as cm:
			output = NDNsim.split_dist_string("1:zipf:a")	
		
		self.assertEqual(cm.exception.code, 1)
		
		#Capture print
		output = out.getvalue().rstrip()
		
		#Redirect STD
		sys.stdout = prev_stdout
		self.assertEqual(output, "Error! Value(s) in: a must be numbers")		
#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestDijkstras(unittest.TestCase): #dijkstras

	print("Starting Dijkstras Tests")	
	maxDiff = None
	#-------------------------------------
	#Checks for a simple line topology
	#-------------------------------------
	def test_1_node_topology(self):
		topology = NDNsim.Topology('./topologies/small_topology.txt')
		topology.print_info()
		#only need to modifiy 'weights'
	
	def test_2_node_topology(self):
		pass
	def test_5_node_topology(self):
		pass
	def test_50_node_topology(self):
		pass
	def test_same_weights(self):
		pass
	def test_varying_weights(self):
		pass
	
#-------------------------------------------------------------------------------	
'''	
#-------------------------------------------------------------------------------
class TestSocketCode(unittest.TestCase): #socket_code

	print("Starting Socket Code Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_connection(self):
	
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestPrecacheHelper(unittest.TestCase): #precache_helper

	print("Starting Distribution Helper Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_SendViaInfrastructure(self):
	def test_SendViaTopology(self):
		
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------

class TestServiceConnection(unittest.TestCase): #service_connection

	print("Starting Distribution Helper Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_TestOrClose(self):
	# interest packet
	def test_MissingCacheData(self):
	def test_CacheEntryMatch(self):
	def test_CacheHit(self):
	def test_ReachedProducer(self):
	def test_FIB_Forwarding(self):
	def test_InterestCollapse(self):
	# data packet	
	def test_Precache_Forwarding(self):
	def test_PIT_Forwarding(self):
	def test_ClearPIT(self):
	def test_CreateNewCacheEntry(self):
	def test_AddToExistingCache(self):
	def test_SatisfyInterestCollapse(self):

	
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------

class TestReadargs(unittest.TestCase): #readargs

	print("Starting Readargs Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_CorrectArgs(self):

#-------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------
class TestSendPacket(unittest.TestCase): #send_packet TODO Mayebe

	print("Starting Send Packet Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_linkfailure(self):
	def test_send_one_packet(self):
	def test_send_5_packets(self):
	def test_send_50_packets(self):
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestCloseThreads(unittest.TestCase): #close_threads TODO Mayebe

	print("Starting Close Threads Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_close_one_thread(self):
	def test_close_5_threads(self):
	def test_close_50_threads(self):
	
#-------------------------------------------------------------------------------	


'''
	
if __name__ == '__main__':
	unittest.main()

