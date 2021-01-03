---
title: "Check installation"
date:  2021-01-03
weight: 40
description: >
  Check if ouroboros works.
draft: false
---

To check if everything is installed correctly, you can now jump into
the [Tutorials](../../tutorials/) section, or you can try to ping this
webhost over ouroboros using the name _ouroboros.rocks.oping_

Our webserver is of course on an IP network, and ouroboros does not
control IP, but it can run over UDP/IP.

To be able to contact our server over ouroboros, you will need to do
some small DNS configuration: to tell the ouroboros UDP system that
the process "ouroboros.rocks.oping" is running on our webserver by
add the line

```
51.38.114.133      1bf2cb4fb361f67a59907ef7d2dc5290
```

to your ```/etc/hosts``` file[^1][^2].

Here are the steps to ping our server over ouroboros:

Run the IRMd:

```bash
$ sudo irmd &
```
Then you will need find your (private) IP address and start an ouroboros UDP
daemon (ipcpd-udp) on that interface:
```bash
$ irm ipcp bootstrap type udp name udp layer udp ip <your local ip address>
```

Now you can ping our server:

```bash
$ oping -n ouroboros.rocks.oping
```

The output from the IRM daemon should look something like this (in DEBUG mode):
```
[dstaesse@heteropoda build]$ sudo irmd --stdout
==01749== irmd(II): Ouroboros IPC Resource Manager daemon started...
==01749== irmd(II): Created IPCP 1781.
==01781== ipcpd/udp(DB): Bootstrapped IPCP over UDP with pid 1781.
==01781== ipcpd/udp(DB): Bound to IP address 192.168.66.233.
==01781== ipcpd/udp(DB): Using port 3435.
==01781== ipcpd/udp(DB): DNS server address is not set.
==01781== ipcpd/ipcp(DB): Locked thread 140321690191424 to CPU 7/8.
==01749== irmd(II): Bootstrapped IPCP 1781 in layer udp.
==01781== ipcpd/ipcp(DB): Locked thread 140321681798720 to CPU 6/8.
==01781== ipcpd/ipcp(DB): Locked thread 140321673406016 to CPU 1/8.
==01781== ipcpd/udp(DB): Allocating flow to 1bf2cb4f.
==01781== ipcpd/udp(DB): Destination UDP ipcp resolved at 51.38.114.133.
==01781== ipcpd/udp(DB): Flow to 51.38.114.133 pending on fd 64.
==01749== irmd(II): Flow on flow_id 0 allocated.
==01781== ipcpd/udp(DB): Flow allocation completed on eids (64, 64).
==01749== irmd(DB): Partial deallocation of flow_id 0 by process 1800.
==01749== irmd(II): Completed deallocation of flow_id 0 by process 1781.
==01781== ipcpd/udp(DB): Flow with fd 64 deallocated.
==01749== irmd(DB): Dead process removed: 1800.
```

If connecting to _ouroboros.rocks.oping_ failed, you are probably
behind a NAT firewall that is actively blocking outbound UDP port
3435.

[^1]: This is the IP address of our server and the MD5 hash of the
      string _ouroboros.rocks.oping_. To check if this is configured
      correctly, you should be able to ping the server with ```ping
      1bf2cb4fb361f67a59907ef7d2dc5290``` from the command line.

[^2]: The ipcpd-udp allows setting up a (private) DDNS server and
      using the Ouroboros ```irm name``` API to populate it, instead
      of requiring each node to manually edit the ```/etc/hosts```
      file. While we technically could also set up such a DNS on our
      server for demo purposes, it is just too likely that it would be
      abused. The Internet is a nasty place.