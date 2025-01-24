#!/bin/bash

# python3 NDNsim.py -o "metric_outfile.csv" -tp "topology.txt" -w "uniform:0, 1" -r "uniform:0, 2" -fd "uniform:0, 0.5" -fr "0, 0.5" -pnco "3:uniform:0, 8" -v "uniform:0, 2" -pgn "5" -pd "uniform:0, 0.5" -l "uniform:0, 0.5" -d "3:uniform:0, 0.5" -to "5" -log "False" -pt "False" -ipt "False"
# python3 NDNsim.py -o "${METRICFILE[$i]}" -tp "${TOPFILE[$i]}" -w "${WEIGHTDIST[$i]}" -r "${RANGE[$i]}" -fd "${FAILDIST[$i]}" -fr "${FAILRANGE[$i]}" -pnco "${PHONE_NODE_CONNECT_ORDER[$i]}" -v "${VELOCITY[$i]}" -pgn "{$PLTGEN_NUM[$i]}" -pd "${PRECACHEDIST[$i]}" -l "${LINGER[$i]}" -d "${DELTA[$i]}" -to "${TIMEOUT[$i]}" -log "${LOGGING[$i]}" -pt "${PHONE_TEST[$i]}" -ipt "${IPERF_TEST[$i]}"

METRICFILE=("metric_outfile.csv")
rm $METRICFILE

echo "--------------------TESTING DEFAULT 5 times--------------------"
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
TIMEOUT=("5")
LOGGING="False"
PHONE_TEST=("False")
IPERF_TEST=("False")

#for i in $(seq 0 "$(("${#DELTA[@]}"-1))");
for i in $(seq 0 5);
do
echo "...Testing Default"
python3 NDNsim.py -o "$METRICFILE" -tp "$TOPFILE" -w "$WEIGHTDIST" -r "$RANGE" -fd "$FAILDIST" -fr "$FAILRANGE" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -pd "$PRECACHEDIST" -l "$LINGER" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
echo "..."
done


echo "--------------------TESTING UNIFORM WEIGHT 1-5--------------------"
TOPFILE=("topology.txt")
WEIGHTDIST=("uniform:0, 1" "uniform:0, 2" "uniform:0, 3" "uniform:0, 4" "uniform:0, 5")
RANGE=("uniform:0, 2")
FAILDIST=("uniform:1, 1")
FAILRANGE=("0, 0.01")
PHONE_NODE_CONNECT_ORDER=("3:uniform:0, 8")
VELOCITY=("uniform:0, 2")
PLTGEN_NUM=("5")
PRECACHEDIST=("uniform:0, 0.01")
LINGER=("uniform:0, 0.5")
DELTA=("3:uniform:0, 0.5")
TIMEOUT=("5")
LOGGING="False"
PHONE_TEST=("False")
IPERF_TEST=("False")

for i in $(seq 0 "$(("${#WEIGHTDIST[@]}"-1))");
do
echo "...Testing WEIGHTDIST: ${WEIGHTDIST[$i]}"
python3 NDNsim.py -o "$METRICFILE" -tp "$TOPFILE" -w "${WEIGHTDIST[$i]}" -r "$RANGE" -fd "$FAILDIST" -fr "$FAILRANGE" -pnco "$PHONE_NODE_CONNECT_ORDER" -v "$VELOCITY" -pgn "$PLTGEN_NUM" -pd "$PRECACHEDIST" -l "$LINGER" -d "$DELTA" -to "$TIMEOUT" -log "$LOGGING" -pt "$PHONE_TEST" -ipt "$IPERF_TEST"
echo "..."
done

