trap "exit" INT TERM
trap "kill 0" EXIT

while :
do
    date_time=$(date +"%d-%m-%y-%s")
    filename="pcap-${date_time}"
    tcpdump -i docker0 -G 10 -W 1 -n -tttt -w pcap-file/${filename}.pcap
    mv pcap-file/${filename}.pcap pcap-to-send/${filename}.pcap
done
