# ntp-python-stats
This Python program will monitor all NTP UDP traffic on port 123, it's very convenient for public NTP pool servers.
It generates staticstics into a MySQL (in-memory) database, from there the statistics are queried and sent to Graphite exporter
to store the metrics into Prometheus.
