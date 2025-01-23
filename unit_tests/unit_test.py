#-------------------------------------------
# IMPORTS

import unittest, sys, logging, io
import numpy as np
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#Tests object is correctly made
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
	#Tests original object isnt overwritten on new object creation
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
	#Tests changing fields only effects 1 object
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
	#File exists checks
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
	#Assertion checks - missing cell
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
	#Assertion checks - missing row
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
	#Assertion checks - missing column
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
class TestDistributionHelper(unittest.TestCase): #Distribution Helper

	print("Starting Distribution Helper Tests")	
	maxDiff = None
	#-------------------------------------
	#Uniform random number check
	#-------------------------------------
	def test_uniform_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], False)
		self.assertEqual(output, np.float64(0.834044009405148))
	
	#-------------------------------------
	#Uniform cdf check
	#-------------------------------------	
	def test_uniform_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 2], True)
		self.assertEqual(output, np.float64(0.417022004702574))

	#-------------------------------------
	#Uniform random number check if same values
	#-------------------------------------	
	def test_uniform_same_value_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Uniform cdf check if same values
	#-------------------------------------	
	def test_uniform_same_value_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("uniform", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Assertion checks - uniform min > max
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
	#Gaussian/normal random number check
	#-------------------------------------	
	def test_gaussian_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 1], False)
		self.assertEqual(output, np.float64(1.6243453636632417))
		
	#-------------------------------------
	#Gaussian/normal cdf check
	#-------------------------------------	
	def test_gaussian_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 1], True)
		self.assertEqual(output, np.float64(0.9478489396588523))
		
	#-------------------------------------
	#Gaussian/normal random number check if std = 0
	#-------------------------------------	
	def test_gaussian_random_number_std_0(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("gaussian", [0, 0], False)
		self.assertEqual(output, 0)
		
	#-------------------------------------
	#Gaussian/normal cdf check if std = 0
	#-------------------------------------	
	def test_gaussian_cdf_std_0(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("normal", [0, 0], True)
		self.assertEqual(output, 1)		
		
	#-------------------------------------
	#Zipf random number check
	#-------------------------------------	
	def test_zipf_random_number(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], False)
		self.assertEqual(output, 1)
		
	#-------------------------------------
	#Zipf cdf check
	#-------------------------------------	
	def test_zipf_cdf(self):
		#Setting seeds for distribution
		np.random.seed(seed=1)
		
		output = NDNsim.distribution_helper("zipf", [2], True)
		self.assertEqual(output, np.float64(0.6079271018540265))
		
	#-------------------------------------
	#Assertion checks - a > 1
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
	#Assertion checks - negative values
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
	#Assertion checks - wrong number of values
	#-------------------------------------		
	def test_negative_assertion(self):
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
	#Assertion checks - unknown distribution
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
'''
#-------------------------------------------------------------------------------
class TestGeneratePackets(unittest.TestCase): #generate_packets

	print("Starting Generate Packets Tests")	
	maxDiff = None
	#-------------------------------------
	#Generate 1 packet
	#-------------------------------------
	def test_generate_1_packet(self):
	
	#-------------------------------------
	#Generate 10 packets
	#-------------------------------------	
	def test_generate_10_packets(self):
	
	#-------------------------------------
	#Generate packets according to iperf
	#-------------------------------------
	def test_iperf3_generation(self):
	
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestNextGateway(unittest.TestCase): #next_gateway

	print("Starting Next Gateway Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_empty_list(self):
	def test_1_item_list(self):
	def test_5_item_list(self):
	def test_end_of_list(self):
	
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestCalcLinger(unittest.TestCase): #calc_linger

	print("Starting Calc Linger Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_getValue(self):
	
#-------------------------------------------------------------------------------	
	
#-------------------------------------------------------------------------------
class TestDijkstras(unittest.TestCase): #dijkstras

	print("Starting Dijkstras Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_1_node_topology(self):
	def test_2_node_topology(self):
	def test_5_node_topology(self):
	def test_50_node_topology(self):
	def test_same_weights(self):
	def test_varying_weights(self):
	
#-------------------------------------------------------------------------------	
	
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

#-------------------------------------------------------------------------------

class TestSplitDistString(unittest.TestCase): #split_dist_string

	print("Starting Distribution Helper Tests")	
	maxDiff = None
	#-------------------------------------
	
	def test_CorrectFormat(self):
'''
	
if __name__ == '__main__':
	unittest.main()

