#!/bin/bash

# python3 NDNsim.py -tp "${TOPFILE[$i]}" -wp "${WEIGHTDIST[$i]}" -pgn "${PLTGEN_NUM[$i]}" -to "${TIMEOUT[$i]}" -pnco "${PHONE_NODE_CONNECT_ORDER[$i]}" -v "${VELOCITY[$i]}" -d "${DELTA[$i]}" -pt "${PHONE_TEST[$i]}" -ipt "${IPERF_TEST[$i]}" -l "$LOGGING"

METRICFILE=("metric_outfile.csv")
rm $METRICFILE


echo "--------------------TESTING DEFAULT 5 times--------------------"
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
PLTGEN_NUM=("5")
TIMEOUT=("5")
LINGER=("uniform:0, 0.5")
RANGE=("uniform:0, 2")
VELOCITY=("uniform:0, 2")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
DELTA=("3:uniform:0, 0.5")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"


#for i in $(seq 0 "$(("${#DELTA[@]}"-1))");
for i in $(seq 0 5);
do

echo "...Testing Default"
python3 NDNsim.py -tp "$TOPFILE" -w "$WEIGHTDIST" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -l "$LINGER" -r "$RANGE" -v "$VELOCITY" -pnco "$PHONE_NODE_CONNECT_ORDER"  -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -log "$LOGGING" -o "$METRICFILE"
echo "..."
done

echo "--------------------TESTING UNIFORM WEIGHT 1-5--------------------"
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1" "uniform:0, 2" "uniform:0, 3" "uniform:0, 4" "uniform:0, 5")
PLTGEN_NUM=("5")
TIMEOUT=("5")
LINGER=("uniform:0, 0.5")
RANGE=("uniform:0, 2")
VELOCITY=("uniform:0, 2")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
DELTA=("3:uniform:0, 2")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"


for i in $(seq 0 "$(("${#WEIGHTDIST[@]}"-1))");
do
echo "...Testing WEIGHTDIST: ${WEIGHTDIST[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -w "${WEIGHTDIST[$i]}" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -l "$LINGER" -r "$RANGE" -v "$VELOCITY" -pnco "$PHONE_NODE_CONNECT_ORDER"  -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -log "$LOGGING" -o "$METRICFILE"
echo "..."
done

echo "--------------------TESTING UNIFORM LINGER 0.01-1--------------------"
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
PLTGEN_NUM=("5")
TIMEOUT=("5")
LINGER=("uniform:0, 0.01" "uniform:0, 0.05" "uniform:0, 0.1" "uniform:0, 0.5" "uniform:0, 1")
RANGE=("uniform:0, 2")
VELOCITY=("uniform:0, 2")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
DELTA=("3:uniform:0, 999")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"


for i in $(seq 0 "$(("${#VELOCITY[@]}"-1))");
do
echo "...Testing LINGER: ${LINGER[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -w "$WEIGHTDIST" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -l "${LINGER[$i]}" -r "$RANGE" -v "$VELOCITY"  -pnco "$PHONE_NODE_CONNECT_ORDER" -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -log "$LOGGING" -o "$METRICFILE"
echo "..."
done



echo "--------------------TESTING UNIFORM DELTA 0.01-1--------------------"
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
PLTGEN_NUM=("5")
TIMEOUT=("5")
LINGER=("uniform:0, 999")
RANGE=("uniform:0, 2")
VELOCITY=("uniform:0, 2")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
DELTA=("3:uniform:0, 0.01" "3:uniform:0, 0.05" "3:uniform:0, 0.1" "3:uniform:0, 0.5" "3:uniform:0, 1")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"


for i in $(seq 0 "$(("${#DELTA[@]}"-1))");
do
echo "...Testing DELTA: ${DELTA[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -w "$WEIGHTDIST" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -d "${DELTA[$i]}" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -log "$LOGGING" -o "$METRICFILE"
echo "..."
done
