trap "exit" INT TERM
trap "kill 0" EXIT

python3 polling.py & bash tcpdump-script.sh