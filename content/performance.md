---
title: "Performance tests"
draft: false
---

Below you will find some measurements on the performance of Ouroboros.

### Local IPC performance test

This test uses the *oping* tool to measure round trip time. This tools
generates traffic from a single thread. The server has a single thread
that handles ping requests and sends responses.

```
$ oping -n oping -i 0 -s <sdu size>
```

The figure below shows the round-trip-time (rtt) in milliseconds (ms)
for IPC over a local layer for different packet sizes, measured on an
Intel Core i7 4500U (2 cores @ 2.4GHz). For small payloads (up to 1500
bytes), the rtt is quite stable at around 30 µs. This will mostly depend
on CPU frequency and to a lesser extent the OS scheduler.

![Ouroboros local rtt](/images/avgrttlocal.png)

This test uses the *ocbr* tool to measure goodput between a sender and
receiver. The sender generates traffic from a single thread. The
receiver handles traffic from a single thread. The performance will
heavily depend on your system's memory layout (cache sizes etc). This
test was run on a Dell XPS13 9333 (2013 model).

```
$ ocbr -n ocbr -f -s <sdu size>
```

![Ouroboros local pps](/images/throughputlocalpps.png)

The goodput (Mb/s) is shown below:

![ouroboros local mbits](/images/goodputlocalmbits.png)

### Ethernet + Normal test

This connects 2 machines over a Gb LAN using the eth-dix and a normal
layer. The oping server is registered in the dix as oping.dix and in the
normal as oping.normal. The machines (dual-socket Intel Xeon E5520) are
connected over a non-blocking switch.

Latency test:

ICMP ping:

```
--- 192.168.1.2 ping statistics ---
1000 packets transmitted, 1000 received, 0% packet loss, time 65ms
rtt min/avg/max/mdev = 0.046/0.049/0.083/0.002 ms, ipg/ewma 0.065/0.049 ms
```

oping over eth-dix:

```
--- oping.dix ping statistics ---
1000 SDUs transmitted, 1000 received, 0% packet loss, time: 66.142 ms
rtt min/avg/max/mdev = 0.098/0.112/0.290/0.010 ms
```

oping over eth-normal:

```
--- oping.normal ping statistics ---
1000 SDUs transmitted, 1000 received, 0% packet loss, time: 71.532 ms
rtt min/avg/max/mdev = 0.143/0.180/0.373/0.020 ms
```