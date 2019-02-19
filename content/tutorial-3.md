---
title: "Tutorial 3: IPCP statistics"
draft: false
---

For this tutorial, you should have a local layer, a normal layer and a
ping server registered in the normal layer. You will need to have the
FUSE libraries installed and Ouroboros compiled with FUSE support. We
will show you how to get some statistics from the network layer which is
exported by the IPCPs at /tmp/ouroboros (this mountpoint can be set at
compile time):

```
$ tree /tmp/ouroboros
/tmp/ouroboros/
|-- ipcpd-normal.13569
|   |-- dt
|   |   |-- 0
|   |   |-- 1
|   |   `-- 65
|   `-- lsdb
|       |-- 416743497.465922905
|       |-- 465922905.416743497
|       |-- dt.465922905
|       `-- mgmt.465922905
`-- ipcpd-normal.4363
    |-- dt
    |   |-- 0
    |   |-- 1
    |   `-- 65
    `-- lsdb
        |-- 416743497.465922905
        |-- 465922905.416743497
        |-- dt.416743497
        `-- mgmt.416743497

6 directories, 14 files
```

There are two filesystems, one for each normal IPCP. Currently, it shows
information for two components: data transfer and the link-state
database. The data transfer component lists flows on known flow
descriptors. The flow allocator component will usually be on fd 0 and
the directory (DHT). There is a single (N-1) data transfer flow on fd 65
that the IPCPs can use to send data (these fd's will usually not be the
same). The routing component sees that data transfer flow as two
unidirectional links. It has a management flow and data transfer flow to
its neighbor. Let's have a look at the data transfer flow in the
network:

```
$ cat /tmp/ouroboros/ipcpd-normal.13569/dt/65
Flow established at:       2018-03-07 18:47:43
Endpoint address:                    465922905
Queued packets (rx):                         0
Queued packets (tx):                         0

Qos cube   0:
 sent (packets):                             4
 sent (bytes):                             268
 rcvd (packets):                             3
 rcvd (bytes):                             298
 local sent (packets):                       4
 local sent (bytes):                       268
 local rcvd (packets):                       3
 local rcvd (bytes):                       298
 dropped ttl (packets):                      0
 dropped ttl (bytes):                        0
 failed writes (packets):                    0
 failed writes (bytes):                      0
 failed nhop (packets):                      0
 failed nhop (bytes):                        0

<no traffic on other qos cubes>
```

The above output shows the statistics for the data transfer component of
the IPCP that enrolled into the layer. It shows the time the flow was
established, the endpoint address and the number of packets that are in
the incoming and outgoing queues. Then it lists packet statistics per
QoS cube. It sent 4 packets, and received 3 packets. All the packets
came from local sources (internal components of the IPCP) and were
delivered to local destinations. Let's have a look where they went.

```
$ cat /tmp/ouroboros/ipcpd-normal.13569/dt/1
Flow established at:       2018-03-07 18:47:43
Endpoint address:               flow-allocator
Queued packets (rx):                         0
Queued packets (tx):                         0

<no packets on this flow>
```

There is no traffic on fd 0, which is the flow allocator component. This
will only be used when higher layer applications will use this normal
layer. Let's have a look at fd 1.

```
$ cat /tmp/ouroboros/ipcpd-normal.13569/dt/1
Flow established at:       2018-03-07 18:47:43
Endpoint address:                          dht
Queued packets (rx):                         0
Queued packets (tx):                         0

Qos cube   0:
 sent (packets):                             3
 sent (bytes):                             298
 rcvd (packets):                             0
 rcvd (bytes):                               0
 local sent (packets):                       0
 local sent (bytes):                         0
 local rcvd (packets):                       6
 local rcvd (bytes):                       312
 dropped ttl (packets):                      0
 dropped ttl (bytes):                        0
 failed writes (packets):                    0
 failed writes (bytes):                      0
 failed nhop (packets):                      2
 failed nhop (bytes):                       44

<no traffic on other qos cubes>
```

The traffic for the directory (DHT) is on fd1. Take note that this is
from the perspective of the data transfer component. The data transfer
component sent 3 packets to the DHT, these are the 3 packets it received
from the data transfer flow. The data transfer component received 6
packets from the DHT. It only sent 4 on fd 65. 2 packets failed because
of nhop. This is because the forwarding table was being updated from the
routing table. Let's send some traffic to the oping server.

```
$ oping -n oping_server -i 0
Pinging oping_server with 64 bytes of data:

64 bytes from oping_server: seq=0 time=0.547 ms
...
64 bytes from oping_server: seq=999 time=0.184 ms

--- oping_server ping statistics ---
1000 SDUs transmitted, 1000 received, 0% packet loss, time: 106.538 ms
rtt min/avg/max/mdev = 0.151/0.299/2.269/0.230 ms
```

This sent 1000 packets to the server. Let's have a look at the flow
allocator:

```
$ cat /tmp/ouroboros/ipcpd-normal.13569/dt/0
Flow established at:       2018-03-07 18:47:43
Endpoint address:               flow-allocator
Queued packets (rx):                         0
Queued packets (tx):                         0

Qos cube   0:
 sent (packets):                             1
 sent (bytes):                              59
 rcvd (packets):                             0
 rcvd (bytes):                               0
 local sent (packets):                       0
 local sent (bytes):                         0
 local rcvd (packets):                       1
 local rcvd (bytes):                        51
 dropped ttl (packets):                      0
 dropped ttl (bytes):                        0
 failed writes (packets):                    0
 failed writes (bytes):                      0
 failed nhop (packets):                      0
 failed nhop (bytes):                        0

<no traffic on other qos cubes>
```

The flow allocator has sent and received a message: a request and a
response for the flow allocation between the oping client and server.
The data transfer flow will also have additional traffic:

```
$ cat /tmp/ouroboros/ipcpd-normal.13569/dt/65
Flow established at:       2018-03-07 18:47:43
Endpoint address:                    465922905
Queued packets (rx):                         0
Queued packets (tx):                         0

Qos cube   0:
 sent (packets):                          1013
 sent (bytes):                           85171
 rcvd (packets):                          1014
 rcvd (bytes):                           85373
 local sent (packets):                      13
 local sent (bytes):                      1171
 local rcvd (packets):                      14
 local rcvd (bytes):                      1373
 dropped ttl (packets):                      0
 dropped ttl (bytes):                        0
 failed writes (packets):                    0
 failed writes (bytes):                      0
 failed nhop (packets):                      0
 failed nhop (bytes):                        0
```

This shows the traffic from the oping application. The additional
traffic (the oping sent 1000, the flow allocator 1 and the DHT
previously sent 3) is additional DHT traffic (the DHT periodically
updates). Also note that the traffic reported on the link includes the
FRCT and data transfer headers which in the default configuration is 20
bytes per packet.

This concludes tutorial 3.
