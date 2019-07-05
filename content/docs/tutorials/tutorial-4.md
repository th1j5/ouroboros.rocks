---
title: "Tutorial 4: Connecting two machines over Ethernet"
draft: false
---

In this tutorial we will connect two machines over an Ethernet network
using the eth-llc or eth-dix IPCPs. The eth-llc use of the IEEE 802.2
Link Layer Control (LLC) service type 1 frame header. The eth-dix IPCP
uses DIX (DEC, Intel, Xerox) Ethernet, also known as Ethernet II. Both
provide a connectionless packet service with unacknowledged delivery.

Make sure that you have an Ouroboros IRM daemon running on both
machines:

```
$ sudo irmd --stdout
```

The eth-llc and eth-dix IPCPs attach to an ethernet interface, which is
specified by its device name. The device name can be found in a number
of ways, we'll use the "ip" command here:

```
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
group default qlen 1
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
...
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast
state UP group default qlen 1000
link/ether fa:16:3e:42:00:38 brd ff:ff:ff:ff:ff:ff
...
3: ens6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast
state UP group default qlen 1000
link/ether fa:16:3e:00:76:c2 brd ff:ff:ff:ff:ff:ff
...
```

The output of this command differs between operating systems and
distributions. The interface we need to use in our setup is "ens3" on
both machines, but for you it may be something like "eth0" or
"enp0s7f1" if you are on a wired LAN, or something like "wlan0" or
"wlp2s0" if you are on a Wi-Fi network. For Wi-Fi networks, we
recommend using the eth-dix.

Usually the interface you will use is the one that has an IP address for
your LAN set. Note that you do not need to have an IP address for this
tutorial, but do make sure the interface is UP.

Now that we know the interfaces to connect to the network with, let's
start the eth-llc/eth-dix IPCPs. The eth-llc/eth-dix layers don't have
an enrollment phase, all eth-llc IPCPs that are connected to the same
Ethernet, will be part of the layer. For eth-dix IPCPs the layers can be
separated by ethertype. The eth-llc and eth-dix IPCPs can only be
bootstrapped, so care must be taken by to provide the same hash
algorithm to all eth-llc and eth-dix IPCPs that should be in the same
network. We use the default (256-bit SHA3) for the hash and 0xa000 for
the Ethertype for the DIX IPCP. For our setup, it's the exact same
command on both machines. You will likely need to set a different
interface name on each machine. The irm tool allows abbreviated commands
(it is modelled after the "ip" command), which we show here (both
commands do the same):

```
node0: $ irm ipcp bootstrap type eth-llc name llc layer eth dev ens3
node1: $ irm i b t eth-llc n llc l eth if ens3
```

Both IRM daemons should acknowledge the creation of the IPCP:

```
==26504== irmd(II): Ouroboros IPC Resource Manager daemon started...
==26504== irmd(II): Created IPCP 27317.
==27317== ipcpd/eth-llc(II): Using raw socket device.
==27317== ipcpd/eth-llc(DB): Bootstrapped IPCP over Ethernet with LLC
with pid 27317.
==26504== irmd(II): Bootstrapped IPCP 27317 in layer eth.
```

If it failed, you may have mistyped the interface name, or your system
may not have a valid raw packet API. We are using GNU/Linux machines, so
the IPCP announces that it is using a [raw
socket](http://man7.org/linux/man-pages/man2/socket.2.html) device. On
OS X, the default is a [Berkeley Packet Filter
(BPF)](http://www.manpages.info/macosx/bpf.4.html) device, and on
FreeBSD, the default is a
[netmap](http://info.iet.unipi.it/~luigi/netmap/) device. See the
[compilation options](/compopt) for more information on choosing the
raw packet API.

The Ethernet layer is ready to use. We will now create a normal layer
on top of it, just like we did over the local layer in the second
tutorial. We are showing some different ways of entering these
commands on the two machines:

```
node0:
$ irm ipcp bootstrap type normal name normal_0 layer normal_layer
$ irm bind ipcp normal_0 name normal_0
$ irm b i normal_0 n normal_layer
$ irm register name normal_layer layer eth
$ irm r n normal_0 l eth
node1:
$ irm ipcp enroll name normal_1 layer normal_layer autobind
$ irm r n normal_layer l eth
$ irm r n normal_1 l eth
```

The IPCPs should acknowledge the enrollment in their logs:

```
node0:
==27452== enrollment(DB): Enrolling a new neighbor.
==27452== enrollment(DB): Sending enrollment info (47 bytes).
==27452== enrollment(DB): Neighbor enrollment successful.
node1:
==27720== enrollment(DB): Getting boot information.
==27720== enrollment(DB): Received enrollment info (47 bytes).
```

You can now continue to set up a management flow and data transfer
flow for the normal layer, like in tutorial 2. This concludes the
fourth tutorial.
