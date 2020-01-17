---
title: "Check installation"
date:  2019-12-30
weight: 40
description: >
  Check if ouroboros works.
draft: false
---

To check if everything is installed correctly, you can now jump into
the [Tutorials](../../tutorials/) section, or you can try to ping this
webhost over ouroboros using the name _ouroboros.rocks.oping_

Our webserver is of course on an IP network, and ouroboros does not
control IP, but it can run over UDP.

To be able to contact our server over ouroboros, you will need to do
some IP configuration: to tell the ouroboros UDP system that the
process "ouroboros.rocks.oping" is running on our webserver by adding
the line

```
51.38.114.133      1bf2cb4fb361f67a59907ef7d2dc5290
```

to your /etc/hosts file (it's the IP address of our server and the MD5
hash of _ouroboros.rocks.oping_).

You will also need to forward UDP port 3435 on your NAT firewall if
you are behind a NAT. Else this will not work.

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

Now you should be able to ping our server!

```bash
$ oping -n ouroboros.rocks.oping
```
