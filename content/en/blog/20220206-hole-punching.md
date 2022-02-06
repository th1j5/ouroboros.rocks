---
date: 2022-02-06
title: "Decentralized UDP hole punching"
linkTitle: "Decentralized hole punching"
description: >
    Can we make O7s-over-UDP scale with many nodes behind firewalls?
author: Dimitri Staessens
---

Today, Max Inden from the libp2p project gave a very interesting
presentation at FOSDEM 2022 about decentralized hole punching, project
Flare.

The problem is this: if servers A and B are each behind a (possibly
symmetric) NAT firewall, they can't _directly_ communicate unless the
firewall opens some ports from the external source to the internal LAN
destination. Let's assume A's NAT has public address 1.1.1.1 and B's
NAT has public address 2.2.2.2. If A runs a service, lets say a web
server on its local LAN address 192.168.0.1 on port 443 -- it works
for both TCP and UDP, so I will not specify this further, B cannot
connect to this server directly. The firewall for A will need to
forward some port on the public address 1.1.1.1:X to the internal
address 192.168.0.1:443. If B is also behind a NAT firewall, that
firewall will need to forward a port on 2.2.2.2:Y towards 1.1.1.1:X.
In a symmetric NAT, the firewall rule is tied to the remote address,
so once established, another node will not be able to send traffic to
1.1.1.1:X, only B can from 2.2.2.2:Y. That's why centralized solutions
like [STUN](https://en.wikipedia.org/wiki/STUN) may fail on symmetric
NATs.

What Max describes is basically a timing attack on a NAT firewall. I
definitely recommend you
[watch it](https://fosdem.org/2022/schedule/event/peer_to_peer_hole_punching_without_centralized_infrastructure/)
when the talk becomes available. The specification can be found
[here](https://github.com/libp2p/specs/blob/master/relay/DCUtR.md)
Instead of using a central server, consider the following.

If A sends a packet to 2.2.2.2:Y, it will upen up a temporary hole it
its firewall (1.1.1.1:X <-> 2.2.2.2:Y) for the response to arrive
(providing the firewall doesn't block all outbound traffic on port Y
or some other rule that prevents it). If B sends a packet to
1.1.1.1:X, it will also create a temporary hole in its firewall
(2.2.2.2:Y <-> 1.1.1.1:X). So, if both do this roughly _at the same
time_, the packets can slip through, the firewall rules become
established and B can communicate with A! Pretty nifty!

Whether this is "decentralized" is a bit debatable, because there
needs to be some coordination between A and B to get the timing
right. And what I don't fully understand (yet), is how the ports X and
Y are known at the time of the hole punching. I *think* there is some
guesswork involved based on the ports that A and B used to contact the
node(s) that provided the synchronization information, as NAT
firewalls may use sequential allocation of these ports. I will try to
find out more (or read the code).

How would this benefit Ouroboros? Well, most likely exactly the same
as libp2p. Firewalls do not pose a connectivity issue, but they do
pose a scalability issue.

The ipcpd-udp allows running Ouroboros over UDP (over IPv4). What it
does is create a point-to-point UDP datagram stream with another
ipcpd-udp. We have redesigned the inner workings a couple of times --
mainly how the ipcpd-udp juggles around UDP ports. At first, we wanted
it to mimic how a real unicast IPCP works -- listening on a fixed port
for incoming requests, and then use randomly chosen ports on either
side for the actual Ouroboros data 'flow'. But that was quickly thrown
out because of -- you guessed it -- firewalls, in favor of using the
listening port also for the incoming 07s data flows. That way, all
that was needed was to open up a single port on a firewall. Opening up
the firewall port was also needed for creating connections. The
reasoning being that we wanted anyone that would connect TO the
network, also accept incoming connections FROM the network. This would
ensure that we could create any mesh between the Ouroboros nodes. But
after some further deliberation, we caved in and made the ipcpd-udp
behave like a normal UDP service, allowing incoming connection even if
the remote "client" ipcpd-udp was not publicly available.

{{<figure width="40%" src="/blog/20220206-hole-punching.png">}}

So this is the current situation shown above left. The red squares
represent nodes that are not publicly reachable, the green ones nodes
that are. By allowing the red nodes, the network will look less like a
mess, and more like a centralized 'star' network, putting extra load
on the "central" green server.  What this hole punching technique
would allow us to do, is to add a (distributed) auxiliary program on
top the Ouroboros layer that coordinates the hole punching for the UDP
connectivity so we can add some 'direct' links at the UDP level.
Definitely something I'll consider later on.

So, if you haven't already, have a look at Max's
[talk](https://fosdem.org/2022/schedule/event/peer_to_peer_hole_punching_without_centralized_infrastructure/).

Cheers,

Dimitri