#!/bin/bash
TOPFILE=("topology.txt" "topology.txt")
WEIGHTFILE=("weights.txt" "weights.txt")
PLTGEN_NUM=("5" "10")
TIMEOUT=("5" "5")
PHONE_NODE_CONNECT_ORDER=("4, 7, 4" "4, 7, 4")
VELOCITY=("100, 100, 100" ".1, .1, 100")
DELTA=(".1, .1, 100" "100, 100, 100")
PHONE_TEST=("False" "False")
IPERF_TEST=("False" "False")
LOGGING="False"


for i in $(seq 0 1);
do
python3 Client_NDN.py -tp "${TOPFILE[$i]}" -wp "${WEIGHTFILE[$i]}" -pgn "${PLTGEN_NUM[$i]}" -to "${TIMEOUT[$i]}" -pnco "${PHONE_NODE_CONNECT_ORDER[$i]}" -v "${VELOCITY[$i]}" -d "${DELTA[$i]}" -pt "${PHONE_TEST[$i]}" -ipt "${IPERF_TEST[$i]}" -l "$LOGGING"

done
