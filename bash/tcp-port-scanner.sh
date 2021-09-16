#!/bin/bash

exit_program() {
	local exit_code=$1
	local failed_message=$2

	if [ $exit_code -ne 0 ]; then
		echo -e $failed_message
		echo "[+] Exiting..."
		exit $exit_code
	fi
}

USAGE_OPTIONS="$0 -h <host> [-p <ports>]"
USAGE_EXAMPLES="$0 -h 10.10.10.10\n$0 -h 10.10.10.10 -p 21,80,443"
USAGE="Use: $USAGE_OPTIONS\n\n--- Examples ---\n\n$USAGE_EXAMPLES\n"

while getopts :h:p: arg; do
	case $arg in
		h) IP=$OPTARG ;;
		p) PORTS=$OPTARG ;;
		*) exit_program 1 "$USAGE"
	esac
done

if [ -z "$IP" ]; then
	exit_program 1 "$USAGE"
fi

if [ -z "$PORTS" ]; then
	PORTS=( $(seq 1 65535) )
	echo -e "[+] Ready to scan all 65535 ports on $IP"
else
	PORTS=( $(echo $PORTS | tr "," " " ) )
	echo -e "[+] Ready to scan (${PORTS[@]}) ports on $IP"
fi

echo -e "[+] Scanning..."

for port in ${PORTS[@]}; do
	timeout 1 bash -c "echo 2>/dev/null 1>/dev/tcp/$IP/$port" && echo "[+] tcp/$port open"
done

echo -e "[+] Completed"
