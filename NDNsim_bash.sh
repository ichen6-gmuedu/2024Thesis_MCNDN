#!/bin/bash

IP=("localhost")
PORT=("8080")
PHONE_IP=("192.168.1.207")
PHONE_PORT=("9095")
METRICFILE=("metric_outfile.csv")
LOGGING="0"
rm $METRICFILE

echo "--------------------TESTING BASELINE--------------------"
METRICFILE=("baseline_metrics.csv")
rm $METRICFILE
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
LINKDIST=("uniform:1, 1")
SUCCESS_THRESH=("0, 0")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
TOP_THRESH=("uniform:0, 0")
LINGER=("uniform:10, 10")
DELTA=("3:uniform:10, 10")
TIMEOUT=("5")
PHONE_TEST=("False")
IPERF_TEST=("False")

for i in $(seq 0 10);
do
echo "...Testing Baseline"
python3 NDNsim.py  -seed $i -o "$METRICFILE" -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT"  -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -ld "$LINKDIST" -st "$SUCCESS_THRESH" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -tt "$TOP_THRESH" -l "$LINGER" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
echo "..."
done


echo "--------------------TESTING DELTA TIMEOUT--------------------"
METRICFILE=("delta_metrics.csv")
rm $METRICFILE
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
LINKDIST=("uniform:1, 1")
SUCCESS_THRESH=("0, 0")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
TOP_THRESH=("uniform:0, 0")
LINGER=("uniform:10, 10")
DELTA=("1:uniform:0, 2" "1:uniform:0, 1.5" "1:uniform:0, 1" "1:uniform:0, 0.5" "1:uniform:0, 0.25" "1:uniform:0, 0.15" "1:uniform:0, 0.1")
TIMEOUT=("5")
PHONE_TEST=("False")
IPERF_TEST=("False")

for j in $(seq 0 "$(("${#DELTA[@]}"-1))");
do
echo "...Testing DELTA: ${DELTA[$j]}"
	for i in $(seq 0 10);
	do
	python3 NDNsim.py -seed $i -o "$METRICFILE" -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -ld "$LINKDIST" -st "$SUCCESS_THRESH" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -tt "$TOP_THRESH" -l "$LINGER" -d "${DELTA[$j]}" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
	echo "..."
	done
done

echo "--------------------TESTING LINK FAILURE--------------------"
METRICFILE=("linkFailure_metrics.csv")
rm $METRICFILE
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
LINKDIST=("uniform:0, 1")
SUCCESS_THRESH=("1, 1" "0.95, 0.95" "0.8, 0.8" "0.75, 0.75" "0.5, 0.5" "0.25, 0.25" "0.1, 0.1" "0.05, 0.05")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
TOP_THRESH=("uniform:0, 0")
LINGER=("uniform:10, 10")
DELTA=("3:uniform:10, 10")
TIMEOUT=("5")
PHONE_TEST=("False")
IPERF_TEST=("False")

for j in $(seq 0 "$(("${#SUCCESS_THRESH[@]}"-1))");
do
echo "...Testing SUCCESS THRESHOLD: ${SUCCESS_THRESH[$j]}"
	for i in $(seq 0 10);
	do
	python3 NDNsim.py -seed $i -o "$METRICFILE" -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -ld "$LINKDIST" -st "${SUCCESS_THRESH[$j]}" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -tt "$TOP_THRESH" -l "$LINGER" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
	echo "..."
	done
done


echo "--------------------TESTING LINGER TIMEOUT--------------------"
METRICFILE=("linger_metrics.csv")
rm $METRICFILE
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
LINKDIST=("uniform:1, 1")
SUCCESS_THRESH=("0, 0")
PHONE_NODE_CONNECT_ORDER=("10:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
TOP_THRESH=("uniform:0, 0")
LINGER=("uniform:0, 2" "uniform:0, 1.5" "uniform:0, 1" "uniform:0, 0.5" "uniform:0, 0.25" "uniform:0, 0.2" "uniform:0, 0.15" "uniform:0, 0.1" "uniform:0, 0.05")
DELTA=("3:uniform:10, 10")
TIMEOUT=("5")
PHONE_TEST=("False")
IPERF_TEST=("False")

for j in $(seq 0 "$(("${#LINGER[@]}"-1))");
do
echo "...Testing LINGER: ${LINGER[$j]}"
	for i in $(seq 0 10);
	do
	python3 NDNsim.py -seed $i -o "$METRICFILE" -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -ld "$LINKDIST" -st "$SUCCESS_THRESH" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -tt "$TOP_THRESH" -l "${LINGER[$j]}" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
	echo "..."
	done
done


echo "--------------------TESTING LINGER TIMEOUT + LINK FAILURE--------------------"
METRICFILE=("linkFailure_Linger_InfrastructureThresh_metrics.csv")
rm $METRICFILE
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
LINKDIST=("uniform:0, 1")
SUCCESS_THRESH=("0.1, 0.1" "0.25, 0.25" "0.5, 0.5" "0.75, 0.75")
PHONE_NODE_CONNECT_ORDER=("10:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
TOP_THRESH=("uniform:0.9, 0.9" "uniform:0.75, 0.75" "uniform:0.5, 0.5" "uniform:0.25, 0.25")
LINGER=("uniform:0, 1" "uniform:0, 0.5" "uniform:0, 0.25" "uniform:0, 0.15")
DELTA=("3:uniform:10, 10")
TIMEOUT=("5")
PHONE_TEST=("False")
IPERF_TEST=("False")
METRICFILE=("linkFailure_Linger_InfrastructureThresh_metrics.csv")

for l in $(seq 0 "$(("${#SUCCESS_THRESH[@]}"-1))");
do
	for k in $(seq 0 "$(("${#LINGER[@]}"-1))");
	do
		for j in $(seq 0 "$(("${#TOP_THRESH[@]}"-1))");
		do
		echo "...Testing SUCCESS_THRESH | LINGER | TOP_THRESH: ${SUCCESS_THRESH[$l]} | ${LINGER[$k]} | ${TOP_THRESH[$j]}"
			for i in $(seq 0 10);
			do
			python3 NDNsim.py -seed $i -o "$METRICFILE" -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -ld "$LINKDIST" -st "${SUCCESS_THRESH[$l]}" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -tt "${TOP_THRESH[$j]}" -l "${LINGER[$k]}" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
			echo "..."
			done
		done
	done
done

































































