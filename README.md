# ntp-python-stats
This Python program will monitor all NTP UDP traffic on port 123, it's very convenient for public NTP pool servers.
It generates statistics into a MySQL (in-memory) database, from there the statistics are queried and sent to Graphite exporter
to store the metrics into Prometheus.

Requirements:
* A working Prometheus server
* Working Graphite Exporter
* Working Node Exporter
* Working Grafana 
* Working MySQL (with a user and a working ntp database)
* Python 3+ (and PyMySQL)
* TCPdump (and the rights to run it, sudo for example)


Files
* ntp-dashboard.json (grafana dashboard) remember to change source and server name in queries
* ntp.sql (SQL dump of database structure)

The end-result in grafana will look like this:
![alt tag](https://github.com/HyperDevil/ntp-python-stats/blob/master/ntp.PNG?raw=true)
