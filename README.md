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
 - Expected Results

## Project Description

This project is a simulation for NDN with a mobile consumer. This simulation is made for Iris Chen's 2024 Master Thesis, "Mobile Consumer Architecture For Named Data Networking" at George Mason Unversity under Doctor Robert Simon.

This simulation acts as a generalizable model for consumer mobility in NDN, utilizing proactive caching AKA precaching based on a linger time and probabilistic precaching based on probability of link failure. This simulation is implemented at the application layer with a python program on PC and a java application on Android.

This simulation is created and tested in Linux 22.04.5 LTS and Android SDK 2024.1.2.

## Installation

### Python Installation

Install python via the python website. https://www.python.org/downloads/
```
sudo apt-get update
sudo apt-get install python3
```

Install pip and the following libraries if they are not already present:
```
sudo apt install python3-pip
sudo pip3 install pickle5
sudo apt-get install python3-scipy
sudo pip install numpy
```


### Iperf3 Installation

Iperf3 is utilized for data generation and it is not required if simulator is not run with iperf3 toggled on. 

Install iperf3 via the iperf3 website. https://iperf.fr/iperf-download.php
```
sudo apt-get install iperf3
```
### Android SDK Installation

Installation instructions: https://stackoverflow.com/questions/34556884/how-to-install-android-sdk-on-ubuntu

Official installation instructions: https://developer.android.com/studio/install

Install latest version: 
```
sudo apt install android-sdk
```

The version used for this simulation is Studio Koala Feature Drop | 2024.1.2 which is available on the Android SDK website https://developer.android.com/studio/archive


#### Android Application Configuration

After installation, run Android SDK by either clicking on the application or navigating to the `android-studio/bin/` and executing `./studio.sh`

Select start a new project. This can be done under the file tab on the upper right, or it should be immediately recommended once it is installed.

![config1](/readme_images/AndroidAppConfig_1.png "new project")

Next, select a "Phone and Tablet" template that supports Java. This simulation uses "Empty Views Activity" template. 

![config2](/readme_images/AndroidAppConfig_2.png "Empty Views Activity")

Select the template, and then select "Java" in the language dropdown menu. Rename the project to "phone". Click the Finish Button.

![config3](/readme_images/AndroidAppConfig_3.png "project phone")

Next, replace the contents of `app/res/layout/activity_main.xml` , `app/java/com.example/phone/MainActivity.java` , and `app/manifests/AndroidManifest.xml` in the Android SDK project files with the corresponding three files in this repo: `activity_main.xml`, `MainActivity.java`, `AndroidManifest.xml`. 

![config4](/readme_images/AndroidAppConfig_4.png "Replace files")

This implementation was adapted and modified from this template server socket code from Jennifer Nicholas https://www.tutorialspoint.com/sending-and-receiving-data-with-sockets-in-android

It should be noted that the Android Application will not be able to be utilized without a **physical Android Device**, as the scope of the network on the Android Device Emulator does not reach outside the emulator, and therefore will not be able to connect to the Python program on PC. 

To run the application on your Android device, **USB debugging** must be enabled. Typically, this can be done by going into `Settings > System > Developer Options > USB Debugging` on your Android device. For specific Android version instructions: https://developer.android.com/studio/debug/dev-options#Enable-debugging


## Running

### Command Line Inputs

The program NDNsim.py contains 16 arguments for the NDN simulator.

| cmd line option    | Default	| Format | Description |
| --------- | --------- | --------- |  --------- | 
| -ip, --ip	| 'localhost' | IP address | IP for the topology (computer simulated nodes). |
| -port, --port	| '8080' | port number | Starting port number for the topology (computer simulated nodes). |
| -pip, --phone_ip	| '192.168.1.207' | IP address | IP for the mobile consumer. |
| -pport, --phone_port	| '9095' | port number | Starting port number for the mobile consumer. |
| -seed, --seed	| '' | int seed | Seed for randomization for a controlled run. Will not effect thread behavior. Must be an int. |
| -o, --outfile	| 'metric_outfile.csv'	| filename | Output file for simulation metrics. Appended to if exists already, creates if not. |
| -tp, --topfile	| 'topology.txt'	| filename | The file to read in the topology of the NDN system. |
| -w, --weights	| 'uniform:0, 0.5'	| distribution:distrubution values | The lambda_ values (aka transmission rates) for each link in the topology chosen from the given probability distribution. Eg: "uniform:0, 1" means that each link has a transmission rate chosen by the uniform probability distrobution between 0-1 |
| -r, --range	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of each node's transmission range.Eg, the default: "uniform:0, 2" means that each node's transmission range is determined by the uniform probability distribution between 0 and 2. |
| -fd, --failure_dist	| 'uniform:1, 1'	| distribution:distrubution values | The probability distribution for the probability that a packet will fail when sent to the next node. Eg, "uniform:0, 0.5" means that every time a packet is being sent to another node,	the possibility of it being sent is determined by the uniform probability distribution between 0 and 0.5. |
| -fr, --failure_range	| '0, 0'	| lower bounds, upper bounds | The percentage (from x to y) for the probability that a packet will fail when sent to the next node.	Eg, "0.1, 0.5" means that every time a packet is being sent to another node,the possibility of it failing to be sent is between 10% and 50%."|
| -pnco, --phone_node_connect_order	| '3:uniform:0, 8' | amount to generate: distribution: distrubution values | The probability distribution for the pattern in which the mobile consumer	will disconnect and re-connect to nodes in the topology.	Eg, the default: \"3:uniform:0, 8\" means that the phone will select the next node	to travel to by using the uniform probability distirbution between 0-8. It selects 3 times. |
| -v, --velocity	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of MC's velocity at each gateway connection. Eg, the default: "uniform:0, 2" means that at each node the mobile consumer is connecting to, they are travelling at a speed chosen by the uniform probability distribution between 0 and 2. |
| -pgn, --pktgen_num	| 5	| number of packets to generate | When generating dummy data, determines how many data packets to generate. |
| -pd, --precache_dist	| 'uniform:0, 0.01'	| distribution:distrubution values | The probability distribution for determining whether a packet will be precached through the topology or through the infrastructure. Eg, "uniform:0, 0.5" means that if the probability of link failure on the link path	from the current location to the destination node (based on the link failure distribution) is greater than a value between 0.0 and 0.5 (chosen by the uniform distribution), then the packet	will be delivered through the infrastructure instead of the topology. |
| -l, --linger	| 'uniform:1, 5'	| distribution:distrubution values | The probability distribution for MC's linger time at each gateway connection. Eg: "uniform:0, 0.5" means that at each node the mobile consumer is connecting to, they are in range of that node for x seconds as determined by the uniform probability distribution between 0 and 0.5. |
| -d, --delta	| '3:uniform:1, 5' | amount to generate: distribution: distrubution values | The probability distribution of deadline in seconds before the data expires. Eg: "3:uniform:0, 0.5" means that the data packet must be received by the MC before the amount of seconds selected by the uniform probability distribution, between 0-0.5, before the MC moves and the interest is re-sent. This happens again 2 more times. |
| -to, --timeout	| 5	| value | Deadline to resend for packets if you dont receive in timeout amount of seconds. timeout scenario: data packet is dropped before delta/linger has expired, we want to resend so we might be able to get the data before delta/linger expires. |
| -log, --logging	| False	| True or False | Toggle to determine whether all logging information will be printed. |
| -pt, --phone_test	| False	| True or False | Toggle to determine whether the simulation will connect to the Android Phone to receive the initial interest packet and send final data. |
| -ipt, --iperf_test	| False	| True or False | Toggle to determine whether the simulation will generate dummy data or generate data via iperf3. |

To run with default values, you can simply use:

```
python3 NDNsim.py
```

To run with all command line inputs: 

```
python3 NDNsim.py -ip "localhost" -port "8080" -pip "192.168.1.207" -pport "9095" -seed "" -o "metric_outfile.csv" -tp "topology.txt" -w "uniform:0, 0.01" -r "uniform:0, 2" -fd "uniform:1, 1" -fr "0, 0" -pnco "3:uniform:0, 8" -v "uniform:0, 2" -pgn "5" -pd "uniform:0, 0" -l "uniform:5, 5" -d "3:uniform:1, 5" -to "5" -log "False" -pt "False" -ipt "False"
```

### Configuring NDNsim For Android Device

To run with the Android Device, first run the Android application using the **debugging button** or **run button** on Android SDK. 

The physical Android device should open the application automatically. On the application, the screen should display an IP, port, and "Not Connected" at the top and a button that says "SEND INTEREST" at the bottom. 

```
IMAGE HERE
```

The Phone's IP may be different depending on your network connection, so please have the Phone IP `-pip` and Phone Port `-pport` CLI reflect the IP displayed on your Android Device. It should be noted that simply 'localhost' will not work. Additionally, make sure the phone_test `-pt` toggle is on.

```
python3 NDNsim.py -pip 'DISPLAYED_IP' --port 'DISPLAYED_PORT' -pt True
```

Now, unless you are waiting for iperf3 to generate data, the text on the Android App should read "Connected". Now that it is connected, tap the "SEND INTEREST" button to begin the NDN simulator.

Once the simulator is complete, you should see the requested data displayed on the phone screen. This should be dummy data (The numbers 1, 2, 3, 4, 5) or the generated iperf3 data if the toggle was turned on `-ipt True`.

```
IMAGE HERE
```

### Configuring BASH script for Bulk Executions

The file NDNsim_bash.sh allows you to execute batch runs of NDNsim.py with your specified parameters. This requires knowledge of Bash and the command line inputs. 

For example, if you want to execute 5 runs of NDNsim.py with the same topology file and the varying timeouts as 5, 4, 3, 2, and 1, then you would change line 5 of NDNsim_bash.sh to be: 
`TIMEOUT=("5" "4" "3" "2" "1")`

After modifying the file to your specifications, execute the bash script with:

```
bash NDNsim_bash.sh
```

## Expected Results

### Android 

### Output file 

The output file is `metric_outfile.csv` by default and records the inputs of the execution, the numbers generated by the probability distribution, and the resulting metrics of the simulation. The following table 

| Label | Format | Description |
| --------- | --------- |  --------- | 
| IP | IP address | IP for the topology (computer simulated nodes). |
| Port | int | Starting port number for the topology (computer simulated nodes) |
| Phone_IP | IP address | IP for the Android Phone Mobile Consumer. |
| Phone_Port | int | Starting port number for the Android Phone Mobile Consumer. |
| Seed | int | Seed for randomization for a controlled run. |
| Topfile | filename | The file to read in the topology of the NDN system. |
| Weight_dist | distribution inputs | Probability distirbution and inputs that determines the weights (transmission rates) of each link in the topology. |
| Range_dist | distribution inputs  | Probability distirbution and inputs that determines the transmission arnge of each node in the topology. |
| Failure_dist | distribution inputs | Probability distirbution and inputs that determines whether a link will faill to transmit data. |
| Failure_range | distribution inputs | Probability distirbution and inputs that determines the threshold that failure_dist must surpass in order to successfully transmit data. |
| Phone_node_connect_order_dist | distribution inputs | Probability distirbution and inputs that determines the connect order of the mobile consumer. |
| Phone_node_connect_order | list of ints | The resulting list of nodes (represented by ints) that the mobile consumer will connect to. |
| Velocity_dist | distribution inputs | Probability distirbution and inputs that determines the velocity of the mobile consumer at each connection to a node in the topology. |
| Velocity | list of floats | The resulting velocities of the mobile consumer at each connection to the topology. |
| Pktgen_num | int | The number of packets to generate if iperf3 test is not activated. Filled with incrementing ints. |
| Precache_dist | distribution inputs | Probability distirbution and inputs that determines the threshold that the calculation for probability of successful delivery must surpass in order to proactively deliver through the topology instead of through the infrastructure. |
| Linger_dist | distribution inputs  | Probability distirbution and inputs that determines the linger time of the mobile consumer at each connection to a node in the topology. |
| Linger | list of floats | The resulting list of linger times of the mobile consumer at each connection in seconds. |
| Delta_dist | distribution inputs | Probability distirbution and inputs that determines the delta timeout of the interest packet. |
| Delta | list of floats | The resulting list of delta times of the interest packets in seconds. |
| Timeout | int | The internal timeout for the mobile consumer to resend a packet in seconds. |
| Phone_test | True or False | Whether test was run with the Android Device sending the initial interst packet and recieving the final data. |
| iperf_test | True or False | Whether test was run with iperf3 output in the data packets. |
| total_delay | float in seconds | End-To-End Delay of the test. |
| timeout_counter | int | Total Number of Timeouts of the test. |
| linger_timeout_counter | int | Number of Linger Time (aka alpha) Timeouts of the test. |
| delta_timeout_counter | int | Number of Delta Timeouts of the test. |
| internal_timeout_counter | int | Number of Internal Timeouts  of the test. |
| num_failure | int | Number of Link Failures of the test. |
| dropped_packets_percent | percent | Percent of Dropped Packets of the test. Can occur due to link failure or timeouts. |
| rec_data | True or False | Whether or not all of the data was successfully received by the Mobile Consumer. |
| precache_check | True or False | Whether or not the successful recieving of data was due to a cache hit from precaching. |
| num_pro_del | int | Number of Proactive Deliveries, where it was expected for a linger time timeout to occur at the original node, and precaching had begun. |
| num_infrastructure | int | Number of Infrastructure Deliveries, where it was expected that there would be link failure on the path to precaching, so data was instead delivered through the infrastructure. |
| num_precache | int | Number of times data was proactively cached at the node the mobile consumer was expected to reconnect after a linger time timeout. |
| num_cache_hit | int | Number of Cache Hits in the test. |


## Modification and Testing

### Code Overview

### Unit Tests
