# 2024Thesis_MCNDN

## Contents
 - Project Description
 - Installation
 	- Python Installation
 	- iperf3 Installation
 	- Android SDK Installation
   - Android Application Configuration
 - Running
 	- Command Line Inputs
  - Configuring NDNsim For Android Device
 	- Configuring bash script

## Project Description

This project is a simulation for NDN with a mobile consumer. This simulation is made for Iris Chen's 2024 Master's Thesis, "Mobile Consumer Architecture For Named Data Networking" at George Mason Unversity under Doctor Robert Simon.

This simulation acts as a generalizable model for consumer mobility in NDN utilizing a mobility function to do proactive caching. 

This simulation is created and tested in Linux and Android SDK only.

## Installation

### Python Installation

Install python via the python website. https://www.python.org/downloads/
```
sudo apt-get update
sudo apt-get install python3.10.12
```

### Android SDK Installation

Installation instructions: https://stackoverflow.com/questions/34556884/how-to-install-android-sdk-on-ubuntu
Install latest version: 
```sudo apt install android-sdk```

The version used for this simulation is Studio Koala Feature Drop | 2024.1.2 which is available android SDK website https://developer.android.com/studio/archive

### Iperf3 Installation

Iperf3 is utilized for data generation and it is not necessarily required if simulator is not run with iperf3 toggled on. 

Install iperf3 via the iperf3 website. https://iperf.fr/iperf-download.php
```
sudo apt-get install iperf3
```


#### Android Application Configuration

After installation, select start a new project. This can be done under the file tab on the upper right, or it should be immediately recommended once it is installed.

Next, select a "Phone and Tablet" template that supports Java. This simulation uses "Empty Views Activity" template. Select the template, and then select "Java" in the language dropdown menu. Rename the project to "phone". 

Next, replace the contents of `app/res/layout/activity_main.xml` , `app/java/com.example/phone/MainActivity.java` , and `app/manifests/AndroidManifest.xml` in the Android SDK project files with the corresponding three files in this repo: `activity_main.xml`, `MainActivity.java`, `AndroidManifest.xml`. 

This implementation was adapted and modified from this template server socket code from Jennifer Nicholas https://www.tutorialspoint.com/sending-and-receiving-data-with-sockets-in-android

It should be noted that the Android Application will not be able to be utilized without a physical Android Device, as the scope of the network on the Android Device Emulator does not reach outside the emulator, and therefore will not be able to connect to the Python code. 

To run the application on your Android device, debugging mode must be enabled. Follow these instructions to enable USB debugging on your device: https://developer.android.com/studio/debug/dev-options


## Running

### Command Line Inputs

The program NDNsim.py contains 16 arguments for the NDN simulator.

| cmd line option    | Default	| Format | Description |
| -------- | ------- |  ------- |  ------- | 
| -o,--outfile	| 'metric_outfile.csv'	| filename | Output file for simulation metrics. Appended to if exists already, creates if not. |
| -tp,--topfile	| 'topology.txt'	| filename | The file to read in the topology of the NDN system. |
| -w,--weights	| 'uniform:0, 1'	| distribution:distrubution values | The lambda_ values (aka transmission rates) for each link in the topology chosen from the given probability distribution. The default, "uniform:0, 1" means that each link has a transmission rate chosen by the uniform probability distrobution between 0-1 |
| -r,--range	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of each node's transmission range.Eg, the default: "uniform:0, 2" means that each node's transmission range is determined by the uniform probability distribution between 0 and 2. |
| -fd,--failure_dist	| 'uniform:1, 1'	| distribution:distrubution values | The probability distribution for the probability that a packet will fail when sent to the next node. Eg, "uniform:0, 0.5" means that every time a packet is being sent to another node,	the possibility of it being sent is determined by the uniform probability distribution between 0 and 0.5. |
| -fr,--failure_range	| '0, 0.1'	| lower bounds, upper bounds | The percentage (from x to y) for the probability that a packet will fail when sent to the next node.	Eg, "0.1, 0.5" means that every time a packet is being sent to another node,the possibility of it failing to be sent is between 10% and 50%."|
| -pnco, --phone_node_connect_order	| '3:uniform:0, 8' | amount to generate: distribution: distrubution values | The probability distribution for the pattern in which the mobile consumer	will disconnect and re-connect to nodes in the topology.	Eg, the default: \"3:uniform:0, 8\" means that the phone will select the next node	to travel to by using the uniform probability distirbution between 0-8. It selects 3 times. |
| -v, --velocity	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of MC's velocity at each gateway connection. Eg, the default: "uniform:0, 2" means that at each node the mobile consumer is connecting to, they are travelling at a speed chosen by the uniform probability distribution between 0 and 2. |
| -pgn, --pktgen_num	| 5	| number of packets to generate | When generating dummy data, determines how many data packets to generate. |
| -pd, --precache_dist	| 'uniform:0, 0.01'	| distribution:distrubution values | The probability distribution for determining whether a packet will be precached through the topology or through the infrastructure. Eg, "uniform:0, 0.5" means that if the probability of link failure on the link path	from the current location to the destination node (based on the link failure distribution) is greater than a value between 0.0 and 0.5 (chosen by the uniform distribution), then the packet	will be delivered through the infrastructure instead of the topology. |
| -l, --linger	| 'uniform:0, 0.5'	| distribution:distrubution values | The probability distribution for MC's linger time at each gateway connection. Eg, the default: "uniform:0, 0.5" means that at each node the mobile consumer is connecting to, they are in range of that node for x seconds as determined by the uniform probability distribution between 0 and 0.5. |
| -d, --delta	| '3:uniform:0, 0.5' | amount to generate: distribution: distrubution values | The probability distribution of deadline in seconds before the data expires. Eg, the default: "3:uniform:0, 0.5" means that the data packet must be received by the MC before the amount of seconds selected by the uniform probability distribution, between 0-0.5, before the MC moves and the interest is re-sent. This happens again 2 more times. |
| -to, --timeout	| 5	| value | Deadline to resend for packets if you dont receive in timeout amount of seconds. timeout scenario: data packet is dropped before delta/linger has expired, we want to resend so we might be able to get the data before delta/linger expires. |
| -log, --logging	| False	| True or False | Toggle to determine whether all logging information will be printed. |
| -pt, --phone_test	| False	| True or False | Toggle to determine whether the simulation will connect to the Android Phone to receive the initial interest packet and send final data. |
| -ipt, --iperf_test	| False	| True or False | Toggle to determine whether the simulation will generate dummy data or generate data via iperf3. |

To run with default values, you can simply use:
```python3 NDNsim.py```
To run with command line inputs: 
```
python3 NDNsim.py -o "metric_outfile.csv" -tp "topology.txt" -w "uniform:0, 1" -r "uniform:0, 2" -fd "uniform:1, 1" -fr "0, 0.01" -pnco "3:uniform:0, 8" -v "uniform:0, 2" -pgn "5" -pd "uniform:0, 0.01" -l "uniform:0, 0.5" -d "3:uniform:0, 0.5" -to "5" -log "False" -pt "False" -ipt "False"
```

### Configuring NDNsim For Android Device

To run with the Android Device, first run the Android application using the debugging button or run button on Android SDK. It should have an IP port, and "Not Connected" on the top of screen with a button that says "SEND INTEREST" at the bottom. 

The IP may be different depending on your network connection, so please modify `NDNsim.py` line 17 to reflect the IP displayed on your Android Device. It should be noted that simply 'localhost' will not work.

`phone_ip =  '192.168.1.207'`

Next, run the python code with the phone_test option on

`python3 NDNsim.py -pt True`

Now, unless you are waiting for iperf3 to generate data, the text on the Android App should read "Connected". Now that it is connected, tap the "SEND INTEREST" button to begin the NDN simulator.

Once the simulator is complete, you should see the requested data displayed on the phone screen. This may be dummy data (The numbers 1, 2, 3, 4, 5) or the generated iperf3 data.

### Configuring bash script

The file NDNsim_bash.sh allows you to execute batch runs of NDNsim.py with your specified parameters. The lines 2 through 11 allow you to specify the parameters for each run you are interested in executing. 

For example, if you want to execute 5 runs of NDNsim.py with the same topology file and the varying timeouts as 5, 4, 3, 2, and 1, then you would change line 5 of NDNsim_bash.sh to be: 
`TIMEOUT=("5" "4" "3" "2" "1")`

You will additionally need to modify all other parameters to match the same number of runs that you plan on making. So for example, you would also need to modify line 2 to be: 
`TOPFILE=("topology.txt" "topology.txt" "topology.txt" "topology.txt" "topology.txt")`

To use the bash script, simply run ```bash NDNsim_bash.sh``` after modifying the file to your specifications.

