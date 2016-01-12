#!/usr/bin/python26
# This extremely simple Python 2.6 script blocks suspected http attackers when the load on the server has reached 30. For something more complex use CloudFlare.
# Anatoliy Dimitrov 2016 All Rights Reserved

import subprocess
import socket
import smtplib
import os

if os.getloadavg()[0] > 30:

    ips =  subprocess.Popen("tail -10000 /var/log/httpd/access_log |cut -d ' ' -f1 | grep -v ::1 | sort | uniq -c", shell=True, stdout=subprocess.PIPE).stdout.read()
    ips = ips.strip()

    ips_list = ips.splitlines()

    for line in ips_list:
        line = line.strip()
        count, sep, ip = line.partition(' ')
        if int(count) > 1000:
            try:
                name, alias, addresslist = socket.gethostbyaddr(ip)
                if 'google' not in name:
                    subprocess.call(["/sbin/iptables", "-I", "INPUT", "-s", ip, "-p", "tcp", "--destination-port", "80", "-j", "DROP"])
            except:
                subprocess.call(["/sbin/iptables", "-I", "INPUT", "-s", ip, "-p", "tcp", "--destination-port", "80", "-j", "DROP"])
