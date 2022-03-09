trap "exit" INT TERM
trap "kill 0" EXIT

while :
do
    date_time=$(date +"%d-%m-%y-%s")
    filename="pcap-${date_time}"
    tcpdump -i cbr0 -G 120 -W 1 -n -vv -tttt -w pcap-file/${filename}.pcap
    mv pcap-file/${filename}.pcap pcap-to-send/${filename}.pcap
done
