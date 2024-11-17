#!/bin/bash

# python3 NDNsim.py -tp "${TOPFILE[$i]}" -wp "${WEIGHTFILE[$i]}" -pgn "${PLTGEN_NUM[$i]}" -to "${TIMEOUT[$i]}" -pnco "${PHONE_NODE_CONNECT_ORDER[$i]}" -v "${LINGER[$i]}" -d "${DELTA[$i]}" -pt "${PHONE_TEST[$i]}" -ipt "${IPERF_TEST[$i]}" -l "$LOGGING"

METRICFILE=("metric_outfile.csv")
rm $METRICFILE

:'
echo "--------------------TESTING DELTA ONLY--------------------"
# Testing delta only
TOPFILE=("topology.txt")
WEIGHTFILE=("weights.txt")
PLTGEN_NUM=("5")
TIMEOUT=("5")
PHONE_NODE_CONNECT_ORDER=("4")
LINGER=("100")
DELTA=("0.15" "0.2" "0.3" "0.5")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"


for i in $(seq 0 "$(("${#DELTA[@]}"-1))");
do
echo "...Testing Delta: ${DELTA[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -wp "$WEIGHTFILE" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$LINGER" -d "${DELTA[$i]}" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -l "$LOGGING" -o "$METRICFILE"
echo "..."
done
# testing velocity/LINGER only
'

echo ""
echo "--------------------TESTING 1 HOP LINGER (NO WAIT)--------------------"
TOPFILE=("topology.txt")
WEIGHTFILE=("weights.txt")
PLTGEN_NUM=("5")
TIMEOUT=("5")
PHONE_NODE_CONNECT_ORDER=("4, 7")
LINGER=("0.1, 0.1" "0.15, 0.15" "0.2, 0.2" "0.3, 0.3" "0.5, 0.5" "1,1")
DELTA=("900")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"

for i in $(seq 0 "$(("${#LINGER[@]}"-1))");
do
echo "...Testing LINGER: ${LINGER[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -wp "$WEIGHTFILE" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "${LINGER[$i]}" -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -l "$LOGGING" -o "$METRICFILE"
echo "..."
done
# testing velocity/LINGER only

echo ""
echo "--------------------TESTING 1 HOP LINGER--------------------"
TOPFILE=("topology.txt")
WEIGHTFILE=("weights.txt")
PLTGEN_NUM=("5")
TIMEOUT=("5")
PHONE_NODE_CONNECT_ORDER=("4, 7")
LINGER=("0.1, 50" "0.15, 50" "0.2, 50" "0.3, 50" "0.5, 5" "1,50")
DELTA=("900")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"

for i in $(seq 0 "$(("${#LINGER[@]}"-1))");
do
echo "...Testing LINGER: ${LINGER[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -wp "$WEIGHTFILE" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "${LINGER[$i]}" -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -l "$LOGGING" -o "$METRICFILE"
echo "..."
done

# testing velocity/LINGER only

echo ""
echo "--------------------TESTING 2 HOP LINGER--------------------"
TOPFILE=("topology.txt")
WEIGHTFILE=("weights.txt")
PLTGEN_NUM=("5")
TIMEOUT=("5")
PHONE_NODE_CONNECT_ORDER=("4, 7, 3")
LINGER=("0.1, 0.1, 50" "0.15, 0.15, 50" "0.2, 0.2, 50" "0.3, 0.3, 50" "0.5, 0.5, 50" "1, 1, 50")
DELTA=("900")
PHONE_TEST=("False")
IPERF_TEST=("False")
LOGGING="False"

for i in $(seq 0 "$(("${#LINGER[@]}"-1))");
do
echo "...Testing LINGER: ${LINGER[$i]}"
python3 NDNsim.py -tp "$TOPFILE" -wp "$WEIGHTFILE" -pgn "$PLTGEN_NUM" -to "$TIMEOUT" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "${LINGER[$i]}" -d "$DELTA" -pt "$PHONE_TEST" -ipt "$IPERF_TEST" -l "$LOGGING" -o "$METRICFILE"
echo "..."
done
