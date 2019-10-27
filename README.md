# Setup

1. Setup noobs on RPI
1. Run `sudo raspi-config` to setup localization options (should be using en_US.utf8)
1. Run `sudo aptitude` and install `mitmproxy`, `dnsmasq`, `hostapd`
1. Edit `/etc/network/interfaces` and add the following:
   ```
   ## ADDED by orangerd: keeping wlan0 static in its own IP subnet
   allow-hotplug wlan0
   iface wlan0 inet static
     address 192.168.10.1
     netmask 255.255.255.0

   ## ADDED by orangerd: restore iptables for NAT
   up iptables-restore < /etc/iptables.ipv4.nat
   ```
1. Edit `/etc/hostapd/hostapd.conf` and add the following:
   ```
   ssid=<SSID>
   interface=wlan0
   hw_mode=g
   channel=2
   beacon_int=100
   max_num_sta=5
   macaddr_acl=0
   auth_algs=1
   wpa=2
   wpa_passphrase=<PASSPHRASE>
   wpa_key_mgmt=WPA-PSK
   wpa_pairwise=TKIP
   rsn_pairwise=CCMP
   ```
1. Edit `/etc/default/hostapd` and set the following:
   ```
   DAEMON_CONF="/etc/hostapd/hostapd.conf"
   ```
1. Run the following to unmask hostapd:
   ```
   sudo systemctl unmask hostapd
   sudo systemctl enable hostapd
   sudo systemctl start hostapd
   ```
1. Edit `/etc/dnsmasq.conf` and add the following at the end:
   ```
   ## ADDED by orangerd: setup DHCP on wlan0
   no-dhcp-interface=eth0
   interface=wlan0
   dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,12h
   dhcp-option=3,192.168.10.1
   dhcp-option=option:router,192.168.10.1
   ```
1. Edit `/etc/sysctl.conf` and set the following:
   ```
   net.ipv4.ip_forward=1
   ```
1. Run the following:
   ```
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  
   sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  
   sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT  
   ```
1. Run `sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"`

# Snooping

1. In order to snoop for traffic, setup port forwarding to mitmproxy using iptables:
   ```
   iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
   iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080
   ```
1. Start up `mitmdump` to snoop on some requests: `mitmdump -w outfile -T --host`
