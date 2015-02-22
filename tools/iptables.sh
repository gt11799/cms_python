#!/bin/bash

iptables -P INPUT ACCEPT

iptables -F
iptables -X

iptables  -A INPUT -i lo -p all -j ACCEPT 
iptables -A OUTPUT -o lo -p all -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT


iptables -A INPUT -p icmp  -j ACCEPT

iptables -A INPUT -s 10.171.242.34   -j  ACCEPT
iptables -A INPUT -s 10.168.20.1 -j  ACCEPT
iptables -A INPUT -s 10.132.41.180 -j  ACCEPT
iptables -A INPUT -s 10.168.178.192 -j  ACCEPT
iptables -A INPUT -s 10.168.185.228 -j  ACCEPT
iptables -A INPUT -s 10.168.181.196 -j  ACCEPT






