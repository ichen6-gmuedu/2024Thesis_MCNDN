# 2024Thesis_MCNDN

## Contents
 - Project Description
 - Installation
 	- Python Installation
 	- Android SDK Installation
 	- iperf3 Installation
 - Running
 	- Configuring bash script

## Project Description

This project is a simulation for NDN with a mobile consumer. This simulation is made for Iris Chen's 2024 Master's Thesis, "Mobile Consumer Architecture For Named Data Networking" at George Mason Unversity under Doctor Robert Simon.

This simulation acts as a generalizable model for consumer mobility in NDN utilizing a mobility function to do proactive caching. 

This simulation is created and tested in Linux only.

## Installation

### Python Installation

Install python via the python website. https://www.python.org/downloads/

### Android SDK Installation

Install Android SDK via the android SDK website. The version tested for this simulation is Studio Koala Feature Drop | 2024.1.2 .  
https://developer.android.com/studio/archive

First, select start a new project. This can be done under the file tab on the upper right, or it should be immediately recommended once it is installed.

Next, select a "Phone and Tablet" template that supports Java. This simulation uses "Empty Views Activity" template. Select the template, and then select "Java" in the language dropdown menu. Rename the project to "phone". 

Next, replace the contents of app/res/layout/activity_main.xml , app/java/com.example/phone/MainActivity.java , and app/manifests/AndroidManifest.xml with the corresponding three files in this repo: activity_main.xml, MainActivity.java, AndroidManifest.xml. 

This implementation was adapted and modified from this template server socket code from Jennifer Nicholas https://www.tutorialspoint.com/sending-and-receiving-data-with-sockets-in-android

It should be noted that the Android Application will not be able to be utilized without a physical Android Device, as the scope of the network on the Android Device Emulator does not reach outside the emulator, and therefore will not be able to connect to the Python code. 

To run the application on your Android device, debugging mode must be enabled. Follow these instructions to enable USB debugging on your device: https://developer.android.com/studio/debug/dev-options

### Iperf3 Installation

Install iperf3 via the iperf3 website. https://iperf.fr/iperf-download.php

## Running

The program NDNsim.py contains 10 parameters for the NDN simulator.

| cmd line option    | Default	| Description |
| -------- | ------- |  ------- | 
| -tp,--topfile	| 'topology.txt'	| The file to read in the topology of the NDN system. Should be the same shape as weightfile |
| -wp, --weightfile	| 'weights.txt'	| The file to read in the weights of the NDN topology. Should be the same shape as topfile |
| -pgn, --pktgen_num	| 5	| When generating dummy data, determines how many data packets to generate. |
| -to, --timeout"	| 5	| Deadline to resend for packets if you dont receive in timeout amount of seconds. timeout scenario: data packet is dropped before delta/linger has expired, we want to resend so we might be able to get the data before delta/linger expires. |
| -pnco, --phone_node_connect_order	| 4, 7, 4	| The Pattern in which the mobile consumer will disconnect and re-connect to nodes in the topology. Eg, the default: 4, 7, 4 means the MC will connect to node 4, then disconnect from node 4 and connect to node 7, then disconnect from node 7 and connect to node 4. It will stay there until the simulation ends. Must be the same length as velocity. |
| -v, --velocity	| 100, 100, 100	| The MC's velocity at each gateway connection. Eg, the default: .1, .1, .1 means that at each node the mobile consumer is connecting to, they are travelling at a speed of 0.1 . Must be the same length as phone_node_connect_order |
| -d, --delta	| .1, .1, 100	| The deadline in seconds before the data expires and we are no longer interested. Eg, the default: .1, .1, 100 means that the data packet must be received by the MC before .1 seconds before the MC moves and the interest is re-sent, this happens again at the re-connection, and finally sits for 100 seconds until the data is received. |
| -pt, --phone_test	| False	| Toggle to determine whether the simulation will connect to the Android Phone to receive the initial interest packet and send final data. |
| -ipt, --iperf_test	| False	| Toggle to determine whether the simulation will generate dummy data or generate data via iperf3. |
| -l, --logging	| False	| Toggle to determine whether all logging information will be printed. |

To run, you can simply use `python3 NDNsim.py` or use the cli.

### Configuring bash script

The file NDNsim_bash.sh allows you to execute batch runs of NDNsim.py with your specified parameters. The lines 2 through 11 allow you to specify the parameters for each run you are interested in executing. 

For example, if you want to execute 5 runs of NDNsim.py with the same topology file and the varying timeouts as 5, 4, 3, 2, and 1, then you would change line 5 of NDNsim_bash.sh to be: 
`TIMEOUT=("5" "4" "3" "2" "1")`

You will additionally need to modify the other parameters to match the same number of runs that you plan on making. So for example, you would also need to modify line 2 to be: 
`TOPFILE=("topology.txt" "topology.txt" "topology.txt" "topology.txt" "topology.txt")`

To use the bash script, simply run `bash NDNsim_bash.sh` after modifying the file to your specifications.
