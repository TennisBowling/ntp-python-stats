#!/usr/bin/python3

import subprocess
import asyncpg
import socket
import struct
from threading import Thread
import asyncio

# Running this script as root is dangerous, someone with write access to this file can do bad things!!!
# This is advised:
# sudo groupadd pcap
# sudo usermod -a -G pcap $USER
# sudo chgrp pcap /usr/sbin/tcpdump
# sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
# sudo ln -s /usr/sbin/tcpdump /usr/bin/tcpdump

async def getdata():
  #connect to database, remember credentials and hostname and database
  db = await asyncpg.connect('postgresql://postgres@192.168.86.37/ntp')
  #start the tcpdump process (-n no reverse lookup)
  p = subprocess.Popen(('sudo', 'tcpdump', 'dst', 'port', '123', '-n', '-l'), stdout=subprocess.PIPE)

  while True:
    for row in iter(p.stdout.readline, b''):
      data = str(row.rstrip())
      #split output into list
      splitted = data.split()

      #sometimes something weird happens, therefor test the output
      try:
        type = splitted[6][:-1]
      except IndexError:
       pass

      #get the values we want
      sourceipsplit = splitted[2].split('.',4)
      sourceip = ".".join(sourceipsplit[0:-1])
      destinationip = splitted[4][:-1]
      protocolversion = splitted[5][:-1]

      #we are only interested in the client traffic
      if type == 'Client':
        ip = sourceip

        #parse this into integers for MySQL
        #construct SQL and replace (delete if exist and insert new)
        sql = """REPLACE INTO clients(time, ip) VALUES (now(), $1)"""
        sqlip = struct.unpack("!I", socket.inet_aton(ip))[0]
        db.execute(sql, sqlip)


def run_getdata():
    asyncio.run(getdata())

#multi-thread these functions
if __name__ == '__main__':
  Thread(target = run_getdata).start()
