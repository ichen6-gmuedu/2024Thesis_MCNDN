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
   - Configuring BASH script for Bulk Executions
   - Configuring Topology File
 - Expected Results
   - Simple Tests
   - Android
   - Output File
 - Modification and Testing
   - Code Overview
   - Unit Tests

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
sudo apt-get install python3-scipy
sudo pip3 install numpy
```

If there is an error, you may need to create a virtual environment in order to install numpy. Please replace `USERNAME` with your machine's name.
```
sudo apt install python3.12-venv
python3 -m venv /home/USERNAME/venv
source /home/USERNAME/venv/bin/activate
/home/USERNAME/venv/bin/pip3 install numpy
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

1. download tar file for android studio
2. extract file contents
3. in `home/USERNAME/android-studio/bin/` execute:
   ```
   ./studio.sh
   ```
4. Follow default installation process.

The version used for this simulation is Studio Koala Feature Drop | 2024.1.2 which is available on the Android SDK website https://developer.android.com/studio/archive


#### Android Application Configuration

To run Android SDK by either clicking on the application or navigating to the `android-studio/bin/` and executing `./studio.sh`

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

As an additional note, if you are using a virtual machine to install Android Studio, the Android device emulator will not work as it does not allow a virtual machine within a virtual machine. 

To run the application on your Android device, **USB debugging** must be enabled. Typically, this can be done by going into `Settings > System > Developer Options > USB Debugging` on your Android device. For specific Android version instructions: https://developer.android.com/studio/debug/dev-options#Enable-debugging


## Running

### Command Line Inputs

The program NDNsim.py contains 16 arguments for the NDN simulator.

| cmd line option    | Default	| Format | Description |
| --------- | --------- | --------- |  --------- | 
| -ihn, --interest_hybrid_name | 'VA/Fairfax/GMU/CS/actionOn:1R153AN' | Hybrid Name | The hybrid name of the requested data. Default is 'VA/Fairfax/GMU/CS/actionOn:1R153AN' and is able to be satisfied on the third node of the default topology. |
| -ip, --ip	| 'localhost' | IP address | IP for the topology (computer simulated nodes). |
| -port, --port	| '8080' | port number | Starting port number for the topology (computer simulated nodes). |
| -pip, --phone_ip	| '192.168.1.207' | IP address | IP for the mobile consumer. |
| -pport, --phone_port	| '9095' | port number | Starting port number for the mobile consumer. |
| -seed, --seed	| '' | int seed | Seed for randomization for a controlled run. Will not effect thread behavior. Must be an int. |
| -o, --outfile	| 'metric_outfile.csv'	| filename | Output file for simulation metrics. Appended to if exists already, creates if not. |
| -tp, --topfile	| 'topology.txt'	| filename | The file to read in the topology of the NDN system. |
| -w, --weights	| 'uniform:0, 0.5'	| distribution:distrubution values | The lambda_ values (aka transmission rates) for each link in the topology chosen from the given probability distribution. Eg: "uniform:0, 1" means that each link has a transmission rate chosen by the uniform probability distrobution between 0-1 |
| -r, --range	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of each node's transmission range.Eg, the default: "uniform:0, 2" means that each node's transmission range is determined by the uniform probability distribution between 0 and 2. |
| -ld, --link_dist	| 'uniform:1, 1'	| distribution:distrubution values | The probability distribution that determines whether a not a packet will be dropped when sent to the next node. Eg, "uniform:0, 0.5" means that every time a packet is being sent to another node, the number that determines whether or not it will be successfully delivered by the uniform probability distribution between 0 and 0.5. |
| -st, --success_thresh	| '0, 0'	| lower bounds, upper bounds | The percentage (from x to y) for the threshold that the resulting CDF from the link_dist value will need to surpass in order for successful packet delivery.	Eg, "0.1, 0.5" means that every time a packet is being sent to another node, the threshold that link_dist's CDF needs to surpass for successful packet delivery is between 10% and 50%."|
| -pnco, --phone_node_connect_order	| '3:uniform:0, 8' | amount to generate: distribution: distrubution values | The probability distribution for the pattern in which the mobile consumer	will disconnect and re-connect to nodes in the topology.	Eg, the default: \"3:uniform:0, 8\" means that the phone will select the next node	to travel to by using the uniform probability distirbution between 0-8. It selects 3 times. |
| -v, --velocity	| 'uniform:0, 2'	| distribution:distrubution values | The probability distribution of MC's velocity at each gateway connection. Eg, the default: "uniform:0, 2" means that at each node the mobile consumer is connecting to, they are travelling at a speed chosen by the uniform probability distribution between 0 and 2. |
| -pgn, --pktgen_num	| 5	| number of packets to generate | When generating dummy data, determines how many data packets to generate. |
| -tt, --top_thresh	| 'uniform:0, 0.01'	| distribution:distrubution values | The threshold that determines whether a packet will be precached through the topology or through the infrastructure. Eg, "uniform:0, 0.5" means that if the probability of link failure on the link path from the current location to the destination node (based on the link failure distribution) is less than a value between 0.0 and 0.5 (chosen by the uniform distribution), then the packet	will be delivered through the topology instead of the infrastructure. |
| -l, --linger	| 'uniform:1, 5'	| distribution:distrubution values | The probability distribution for MC's linger time at each gateway connection. Eg: "uniform:0, 0.5" means that at each node the mobile consumer is connecting to, they are in range of that node for x seconds as determined by the uniform probability distribution between 0 and 0.5. |
| -d, --delta	| '3:uniform:1, 5' | amount to generate: distribution: distrubution values | The probability distribution of deadline in seconds before the data expires. Eg: "3:uniform:0, 0.5" means that the data packet must be received by the MC before the amount of seconds selected by the uniform probability distribution, between 0-0.5, before the MC moves and the interest is re-sent. This happens again 2 more times. |
| -to, --timeout	| 5	| value | Deadline to resend for packets if you dont receive in timeout amount of seconds. timeout scenario: data packet is dropped before delta/linger has expired, we want to resend so we might be able to get the data before delta/linger expires. |
| -log, --logging	| 1	| int | Int to determine whether all logging information will be printed. 0 means that no logging or resulting metrics are displayed, only errors. 1 means that resulting metrics are displayed. 2 means that additionally some logging information is displayed (timeouts, link failure, MC movement, and expected link failure). 3 means that additionally verbose logging is displayed (cache hit, link success probabilities, node communication, etc). |
| -pt, --phone_test	| False	| True or False | Toggle to determine whether the simulation will connect to the Android Phone to receive the initial interest packet and send final data. |
| -ipt, --iperf_test	| False	| True or False | Toggle to determine whether the simulation will generate dummy data or generate data via iperf3. |

To run with default values, you can simply use:

```
python3 NDNsim.py
```

To run with all command line inputs: 

```
python3 NDNsim.py -ign "VA/Fairfax/GMU/CS/actionOn:1R153AN" -ip "localhost" -port "8080" -pip "192.168.1.207" -pport "9095" -seed "" -o "metric_outfile.csv" -tp "topology.txt" -w "uniform:0, 0.01" -r "uniform:0, 2" -fd "uniform:1, 1" -fr "0, 0" -pnco "3:uniform:0, 8" -v "uniform:0, 2" -pgn "5" -pd "uniform:0, 0" -l "uniform:5, 5" -d "3:uniform:1, 5" -to "5" -log "False" -pt "False" -ipt "False"
```

### Configuring NDNsim For Android Device

To run with the Android Device, first run the Android application using the **debugging button** or **run button** on Android SDK. 

The physical Android device should open the application automatically. On the application, the screen should display an IP, port, and "Not Connected" at the top and a textbox, a button that says "SEND CUSTOM INTEREST", a button that says "SEND DEFAULT INTEREST", and a button that says "CLEAR SCREEN" at the bottom. 

![phone_notconnected](/readme_images/phone_notconnected.png "phone_notconnected")

The Phone's IP may be different depending on your network connection, so please have the Phone IP `-pip` and Phone Port `-pport` CLI reflect the IP displayed on your Android Device. It should be noted that simply 'localhost' will not work. Additionally, make sure the phone_test `-pt` toggle is on.

```
python3 NDNsim.py -pip 'DISPLAYED_IP' --port 'DISPLAYED_PORT' -pt True
```

Unless you are waiting for iperf3 to generate data, the text on the Android App should now read "Connected". Now that it is connected, tap the "SEND DEFAULT INTEREST" button to begin the NDN simulator.

![phone_connected](/readme_images/phone_connected.png "phone_connected")

Once the simulator is complete, which should only take a few seconds, you should see the requested data displayed on the phone screen. This should be dummy data (The numbers 0, 1, 2, 3, 4) or the generated iperf3 data if the toggle was turned on `-ipt True`.

![phone_defaultinterest](/readme_images/phone_defaultinterest.png "phone_defaultinterest")


To send interest packets with a custom hybrid name, type your custom hybrid name into the text box and tap "SEND CUSTOM INTEREST" when you are done. If the requested data name is formatted incorrectly, and there is a path to the requested data in the topology via the FIBs, then you should see a message that tells you so. 

The hierarchical name for an interest packet is formatted with `/` separating the name sectinos and `:` separating the flat component. The following graphic is taken from "Hierarchical and Flat-Based Hybrid Naming Scheme in Content-Centric Networks of Things" by Arshad and Shahzaad et al., 2018. For the interest packet, only the interest message format is needed as input. 

![hybrid_name](/readme_images/hybrid_example.png "hybrid_name")

If the requested data name is formatted correctly and present in the topology with a node being able to satisfy the request, then you should be able to see the output with default the CLI. 

![phone_custominterest](/readme_images/phone_custominterest.png "phone_custominterest")

### Configuring BASH script for Bulk Executions

The file NDNsim_bash.sh allows you to execute batch runs of NDNsim.py with your specified parameters. This requires knowledge of Bash and the command line inputs. 

The current version of the script simply includes a template for running 5 executions with one set of inputs, and another template for running 5 executions with changing values for the `TIMEOUT` while keeping all the other inputs the same. 

To modify the bash script to run executions with your specific varying input, follow this guide. We will use the `TIMEOUT` input as the example.
1. Find the existing value for your input (`TIMEOUT`). The line should look like `TIMEOUT=("1")`
2. Replace the single value in the parenthesis with multiple values in quotes separated by a space. The line should now look like `TIMEOUT=("1" "2" "3")`
3. Replace the existing value in the for loop so that it loops the same number of times as values you have put in. That line should look like `for i in $(seq 0 "$(("${#TIMEOUT[@]}"-1))");`
4. Replace the Portion of the command that runs NDNsim.py with your variable so that it takes the i'th element of your variable. That section should now look like `-to "${TIMEOUT[$i]}"`
5. Make sure the previous version of the variable is now replaced with a single value, and is not indexed in the command line input for NDNsim.py
6. For readability, change the echo to reflect what you are testing in this batch. The line should look like echo `"...Testing TIMEOUT: ${TIMEOUT[$i]}"`

After modifying the file to your specifications, execute the bash script with:

```
bash NDNsim_bash.sh
```

### Configuring Topology File

The example topology is a simple eight node topology as pictured in the accompanying thesis paper. 

![topology_graphic](/readme_images/Topology_graphic.png "topology_graphic")

From this example, the corresponding default topology file utilized in the simulation.

![default_topology](/readme_images/default_topology.png "default_topology")

The format of the topology has N rows and N+1 columns, where N is the number of nodes in the topology. The first elemt of each row is the data that this node would be able to satisfy, in essence, a hybrid name. The hybrid name consists of the Hierarchical Component that is used for the forwarding table and the flat component which consists of a hash of the device name and the data that this node would be able to satisfy. 

In this example topology, the third node with "VA/Fairfax/GMU/CS:12153AN|Irisean" as the name of the data it is able to satisfy is the only one that acts as the producer in example tests.

The rest of the row consists of that node's Forwarding Information Base (FIB), where the element is 0 if there is no connection between the two nodes, and a FIB entry for that node's hierarchical component if there is a connection. Refer to the hybrid name guide for data packets, except there is no need to include the task ("ActionOn") for the topology. 

To create your own topology file, follow the this guide:
1. There are N rows and N+1 columns for N nodes in the topology
2. The first element of a row is the name and data hash that the node would be able to satisfy.
3. The hierarchical name is formatted with `/` separating the name sectinos, `:` separating the flat component, and `|` separating the device name hash and the data hash. 
4. Each element in a row is separated by a tab character.
5. The Hierarchical component of the data a neighboring node is able to satisfy is the FIB entry for that node
6. If there is no neighboring node for the corresponding element, then it is a 0.

A note about the default topology: the third node is the only node that is guaranteed to have a path towards it, as the hierarchical components of the other nodes were created in service of it. If an interest packet's requested data name has a hierarchical component of "VA/Fairfax" it would not always be able to find a path towards the node that satisfies that data. This simulator currently supports nodes that satisfy only one data name and FIB entries that have only one data name for each neighboring node. 

## Expected Results

### Simple Tests

The image below is the expected output from the following command. For the default inputs, the linger and delta timeouts are determined by a uniform distribution between 1 and 5 seconds and additionally the link failure is determined by a uniform distribution between 1 and 1. 

There should be no opportunities for the interest or data packets to be dropped or miss the deadlines, so the expected output has 0.0% dropped packets.

```
python3 NDNsim.py -seed 1
```
![NDNsim with seed=1](/readme_images/test_seed1.png "seed1 test")

The end-to-end delay of your experiments may differ, as this simulator is threaded and the seed is only able to control the resulting values of the probability distributions. To see some of these values, run the following command to see the logging information. 

```
python3 NDNsim.py -seed 1 -log true
```
![NDNsim with seed=1 and log=true](/readme_images/test_seed1log.png "seed1log test")

Your distribution values for phone_node_connect_order, velocity, and delta should match the ones in the image above. However as mentioned before, this simulation is threaded, so the order of packets ("data") being sent from one node to the next may be in a different order.

For this next test, we will set the failure range ot be from 1 to 1, meaning that the failure distribution will need to surpass 1 in order to successfully deliver data from one node to the next. Next, we set failure distribution to be decided by a uniform distribution from 0 to 0.5, so that it will always fail. 

```
python3 NDNsim.py -seed 1 -fd "uniform:0, 0.5" -fr "1, 1"
```
![NDNsim with link failure](/readme_images/test_linkfailure.png "linkfailure test")

The expected result is the interest failing to be sent to the first node in the topology, and all the timeouts having expired. This run should take a few seconds, as we are waiting for the timeouts to occur. In this run, the delta timeout occured three times, and it should be the same for you. 

For the next test, we are going to force precaching to occur. To do this, we shall set the linger timeout to be determined by a uniform distribution between 0 and 0.1, and for the phone node connect order to have 10 re-connections, each node chosen by the uniform distribution between 0 and 8 (since there are 8 nodes total in the default topology).
```
python3 NDNsim.py -seed 1 -l "uniform:0, 0.1" -pnco "10:uniform:0, 8"
```
![NDNsim with precache](/readme_images/test_seedprecache.png "precache test")

The expected result should have the text "Linger time exceeded!" occur in the simulation about three times and see the mobile consumer (MC) move to nodes 5, 0, and 2. There have been three proactive deliveries, and 12 precaches. 

This means that we have reached a node that can satisfy the interest packet but cannot deliver to the MC at its original location and have decided to precache (proactively deliver) three times. Since we are generating 5 packets of data, there are more than 3 instances of precaching. "Number of Precaches" increases every time data is actually cached at the node.

There were no deliveries through the infrastructure, as the default inputs for link failure probabilities are set to always deliver.

Unfortunately, for this experiment the successful delivery of data was not due to a cache hit. This means that the mobile consumer had not received the data due to precaching, and instead recieved the data from the original producer. 

### iperf3 

For the iperf3 test, we shall introduce iperf3 as the data instead of the generated dummy data. 
```
python3 NDNsim.py -seed 1 -ipt true
```
![NDNsim with iperf3](/readme_images/test_iperf3.png "iperf3 test")

The resulting iperf3 data may be different, but instead of listing the final data as "01234", it should now display the output of the client side of iperf3. This test should take an extra few seconds, as iperf3 takes time to execute before the simulation begins. 

Here you can see that since the iperf3 data was so large, the simulator decides to proactively deliver and precache the data at the mobile consumer's next expected location. The reason for this is because the transmission rates of the links in the topology are not accurate to real life, and since the iperf3 data is so large (comparatively), the simulation expects to take a long time to deliver the data. 

However, even though the data was proactively cached, the data was also sent back using the reverse path in order to clear the PIT entries, and our mobile consumer had received the data at its original location before any linger timeouts occured. 

### Android 

To test with the physical Android device, `-pt` must be true, and the `-pport` and `-pip` must reflect the IP address and port displayed on the physical Android device. 

Running the previous tests with these additional command line inputs should result in the same output for NDNsim.py, but should additionally have these two outputs for the Android Application when sending the default interest. In the following examples, there is the default behavior with generated data, the behavior if the NDNsim.py fails to deliver the final data, and default behavior with iperf3 data.

```
python3 NDNsim.py -seed 1 -pt true
```
![phone_defaultinterest](/readme_images/phone_defaultinterest.png "phone_defaultinterest")

```
python3 NDNsim.py -seed 1 -fd "uniform:0, 0.5" -fr "1, 1" -pt true
```
![phone_failed](/readme_images/phone_failed.png "phone_failed")

```
python3 NDNsim.py -seed 1 -ipt true -pt true
```
![phone_iperf3](/readme_images/phone_iperf3.png "phone_iperf3")

### Output file 

The output file is `metric_outfile.csv` by default and records the inputs of the execution, the numbers generated by the probability distribution, and the resulting metrics of the simulation. The following table includes almost all the command line inputs as well as the recorded metrics. 

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
| dropped_packets | int | Number of Dropped Packets of the test. Can occur due to link failure or packets received after a deadline. |
| rec_data | True or False | Whether or not all of the data was successfully received by the Mobile Consumer. |
| precache_check | True or False | Whether or not the successful recieving of data was due to a cache hit from precaching. |
| num_pro_del | int | Number of Proactive Deliveries, where it was expected for a linger time timeout to occur at the original node, and precaching had begun. |
| num_infrastructure | int | Number of Infrastructure Deliveries, where it was expected that there would be link failure on the path to precaching, so data was instead delivered through the infrastructure. |
| num_precache | int | Number of times data was proactively cached at the node the mobile consumer was expected to reconnect after a linger time timeout. |
| num_cache_hit | int | Number of Cache Hits in the test. |

## Modification and Testing

Feel welcome to download and modify this simulation to fit your needs.

### Code Overview

#### Classes

##### Hybrid_Name

Stores the information of the hybrid name, including attributes for the task, device name, data hash, hierarchical component, and flat component. Additionally has a print_info() function to display this information.

##### Packet

Stores the packet information. For the interest packet, the relevant attributes are name, time the packet was sent, linger time, delta time, velocity, and lambda. The name is the hybrid name of the interested data, the linger time is the time the mobile consumer is expected to stay connected at the original node the interest was sent, the delta time is a deadline for the data we are interested in, the velocity is the velocity of the mobile consumer, and the lambda is a list of transmission rates from each of the links the packet has travelled so far.

For the data packet, the relevant attributes are the name, total packets, counter, total size, payload, destination, precache, and number. the total packets is the number of total packets for the complete information the requested (since each packet may only contain a segment of the complete data), the counter is used for data reconstruction, the total size is the number of bytes for the data packets of the complete information, the payload is the requested data, the destination is used for precaching (when we are not following PIT for reverse path), precache is a flag to determine whether we are precaching, and number is for grouping the data packets.

Additionally has a print_info() function to display this information.

##### PIT_Entry

Stores the information for a PIT entry, including attributes for the name, total number of instances of a packet we have seen, and incoming interface. It additionally has a print_info() function to display this information.

##### Cache_Entry

Stores the information for a cache entry, including attributes for name, and data packets. The data packet attribute is an array of packet objects. It additionally has a print_info() function to display this information.

##### Node

Stores the information for a Node, including attributes for the node's IP and port (since all nodes are both a server and a client), number, name of the data this node is able to satisfy, PIT, FIB, transmission rates for neighbors, cache, transmission range, and relevant locks. It additionally has a print_info() function to display this information.

##### Topology

Stores information on the NDN topology, including attributes for the topology file, the probability distribution that determines the transmission rates of all links in the topology, the probability distribution that determines the transmission range of each node in the topology and the IP and port. It has a read_in_file() function for reading the topology file, creating all the Node objects, assigning each node a transmission range, assigning each link in the topology a transmission rate, and creating FIB entries for each node. It additionally has a print_info() function to display this information.

### Unit Tests

Unit tests are included for the various functions in NDNsim.py in the `unit_tests` folder. If the program is modified, please refer to the unit tests.

It is recommended to run the unit tests after downloading the repo to make sure that everything works as expected. To run the unit tests, use the following command. 
```
./unit_tests/run_tests.sh
```

Note: depending on your version of numpy and python, some unit tests may fail due to typcasting of numpy array elements (ie: np.float(0.0) VS 0.0)
