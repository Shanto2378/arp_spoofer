# This is a hobby/learning project developed in Python

# Usecase
Using this code, you can spoof a target to get all the packets through you and the router. It's called arp spoofing. This way, you can read all the packets, such as "Username, Password, Images," sent through the target machine. This means you are the Man in the middle of the target machine and the router. The target machine will think you are the router and the router will think you are the target. **Please see the example code for better understanding** 
+ Better use with packet_sniffer for full potential.
```bash
  git clone https://github.com/Shanto2378/packet_sniffer.git
```

# Port Forward In Linux
```bash
  echo 1 > /proc/sys/net/ipv4/ip_forward
```
Use 0 instead of 1 to turn of Port Forwarding.

# Example Code
```bash
  sudo python3 arp_spoofer.py -t "Target IP" -g "Gateway IP"
```
# Thank you.
