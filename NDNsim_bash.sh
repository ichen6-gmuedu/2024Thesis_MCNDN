#!/bin/bash

IP=("localhost")
PORT=("8080")
PHONE_IP=("192.168.1.207")
PHONE_PORT=("9095")
METRICFILE=("metric_outfile.csv")
rm $METRICFILE

echo "--------------------TESTING DEFAULT 5 times--------------------"
SEED=("")
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
FAILDIST=("uniform:1, 1")
FAILRANGE=("0, 0")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
PRECACHEDIST=("uniform:0, 0")
LINGER=("uniform:1, 5")
DELTA=("3:uniform:1, 5")
TIMEOUT=("5")
LOGGING="False"
PHONE_TEST=("False")
IPERF_TEST=("False")

for i in $(seq 0 5);
do
echo "...Testing Default"
python3 NDNsim.py -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -seed "$SEED" -o "$METRICFILE" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -fd "$FAILDIST" -fr "$FAILRANGE" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -pd "$PRECACHEDIST" -l "$LINGER" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
echo "..."
done


echo "--------------------TESTING INTERNAL TIMEOUT--------------------"
SEED=("")
INT_HYBRID_NAME=("VA/Fairfax/GMU/CS/actionOn:1R153AN")
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1")
RANGE=("uniform:0, 2")
FAILDIST=("uniform:1, 1")
FAILRANGE=("0, 0.01")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
PRECACHEDIST=("uniform:0, 0.01")
LINGER=("uniform:0, 0.5")
DELTA=("3:uniform:0, 0.5")
TIMEOUT=("5" "4" "3" "2" "1")
LOGGING="False"
PHONE_TEST=("False")
IPERF_TEST=("False")

for i in $(seq 0 "$(("${#TIMEOUT[@]}"-1))");
do
echo "...Testing TIMEOUT: ${TIMEOUT[$i]}"
python3 NDNsim.py -ihn "$INT_HYBRID_NAME" -ip "$IP" -port "$PORT" -pip "$PHONE_IP" -pport "$PHONE_PORT" -seed "$SEED" -o "$METRICFILE" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -fd "$FAILDIST" -fr "$FAILRANGE" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -pd "$PRECACHEDIST" -l "$LINGER" -d "$DELTA" -to "${TIMEOUT[$i]}" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
echo "..."
done

