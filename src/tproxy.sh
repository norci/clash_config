#!/bin/bash -ux
start() {
    iptables -t nat -N clash
    iptables -t nat -F clash
    iptables -t nat -A clash -d 0.0.0.0/8      -j RETURN
    iptables -t nat -A clash -d 10.0.0.0/8     -j RETURN
    iptables -t nat -A clash -d 127.0.0.0/8    -j RETURN
    iptables -t nat -A clash -d 169.254.0.0/16 -j RETURN
    iptables -t nat -A clash -d 172.16.0.0/12  -j RETURN
    iptables -t nat -A clash -d 192.168.0.0/16 -j RETURN
    iptables -t nat -A clash -d 224.0.0.0/4    -j RETURN
    iptables -t nat -A clash -d 240.0.0.0/4    -j RETURN
    iptables -t nat -A clash -p tcp            -j REDIRECT --to-port 7892
    iptables -t nat -A PREROUTING -p tcp            -j clash
    ### fake ip
    iptables -t nat -A OUTPUT     -p tcp -d 198.18.0.0/16 -j REDIRECT --to-port 7892
    ### DNS
    iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 1053
    ip6tables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 1053
    ### local machine. set DNS to 127.0.0.1 first.
    iptables -t nat -A OUTPUT -o lo -p udp -d 127.0.0.1 --dport 53 -j REDIRECT --to-port 1053
    ### ipv6
    ip6tables -t nat -A OUTPUT -p udp -d fe80::1 --dport 53 -j REDIRECT --to-port 1053
}
stop() {
    iptables -t nat -D PREROUTING -p tcp              -j clash
    iptables -t nat -D OUTPUT     -p tcp -d 198.18.0.0/16 -j REDIRECT --to-port 7892
    iptables -t nat -F clash
    iptables -t nat -X clash
    iptables -t nat -D PREROUTING -p udp --dport 53 -j REDIRECT --to-port 1053
    iptables -t nat -D OUTPUT -o lo -p udp -d 127.0.0.1 --dport 53 -j REDIRECT --to-port 1053
    ip6tables -t nat -D PREROUTING -p udp --dport 53 -j REDIRECT --to-port 1053
    ip6tables -t nat -D OUTPUT -p udp -d fe80::1 --dport 53 -j REDIRECT --to-port 1053
}
status() {
    iptables -t nat -vnL
    ip6tables -t nat -vnL
}
case $1 in
    start)
	start
	;;
    stop)
	stop
	;;
    status)
	status
	;;
    restart)
	stop
	status
	start
	;;
    *)
	echo "$0 start | stop | status"
	;;
esac
