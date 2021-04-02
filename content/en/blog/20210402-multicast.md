---
date: 2021-04-02
title: "How does Ouroboros do anycast and multicast?"
linkTitle: "Does Ouroboros do (any,multi)-cast?"
description: >
     Searching for the answer to the question: why do packet networks work?
author: Dimitri Staessens
---

```
Nothing is as practical as a good theory
  -- Kurt Lewin
```

How does Ouroboros handle routing and how is it different from the
Internet? How does it do multicast? That's a good subject for a blog
post! I assume the reader to be a bit knowledgeable about the Internet
Protocol (IP) suite. I limit this discussion to IPv4, but generally
speaking it's also applicable to IPv6. Hope you enjoy the read.

Network communications is commonly split up into four classes based on
the delivery model of the message. If it is a single source sending to
a single receiver, it is called _unicast_. This is the way most of the
traffic on the Internet works: a packet is forwarded to a specific
destination IP address. This process is then called _unicast routing_.
If a sender is transmitting a message to _all_ nodes in a network,
it's called _broadcast_. To do this efficiently, the network will run
a bunch of protocols to construct some form of _spanning tree_ between
the nodes in the network a process referred to as _broadcast
routing_. If the destination is a specific set of receivers, it's
called _multicast_. Broadcast routing is augmented with a protocol to
create groups of nodes, the so-called multicast group, to again create
some form of a spanning tree between the group members, called
_multicast routing_. The last class is _anycast_, when the destination
of the communication is _any_ single member of a group, usually the
closest.

Usually these concepts are explained in an Internet/IP setting where
the destinations are (groups of) IP addresses, but the concepts can
also be generalized towards the naming system: resolving a (domain)
name to a set of addresses, for instance, which can then be used in a
multicast implementation called _multidestination
routing_. Multidestination routing (i.e. specifying a bunch of
destination addresses in a packet) doesn't scale well.

Can we contemplate other classes? Randomcast (sending to a random
destination)?  Or stupidcast (sending to all destinations that don't
need to receive the message)? All kidding aside, the 4 classes above
are likely to be all the _sensible_ delivery models.

### Conundrum, part I

During the development of Ouroboros, it became clearer and clearer to
us that the distinction based on the delivery model is not a
_fundamental_ one. If I have to make a -- definitely imperfect --
analogy, it's a bit like classifying animals by the number of eyes
they have. Where two eyes is unicast, more is multicast and composite
eyes broadcast. Now, it will tell you _something useful_ about the
animals if they are in the 2, multi or composite-eye class, but it's
not how biologists classify animals. Some animal orders -- spiders --
have members with 2, 4, 6 and 8 eyes. There are deeper, more
meaningful distinctions that can be made on more fundamental grounds,
such as whether the species has a backbone or not, that traces back
their evolution. What are those fundamental differences for networks?

Take a minute to contemplate the following little conundrum. Take a
network that is linear, e.g.

```
source - node - node - node - node - destination
```

and imagine observing a packet traveling over every _link_ on this
linear network, from source to destination. Was that communication
anycast, unicast, multicast or broadcast? Now this may seem like a
silly question, but it should become clearer why it's relevant, and --
in fact -- fundamental. I will come back to this at the end of this
post.

But first, let's have a look at how it's done, shall we?

### Unicast

This is the basics. IP routers will forward packets based on the
destination IP address (not in any special range) in their header to
the host (in effect: an interface) that has been assigned that IP
address. The forwarding is based on a forwarding table that is
constructed using some routing protocol (OSPF/IS-IS/BGP/...).  I'll
assume you know how this works, and if not, there are plenty of online
resources on these protocols.

On unicast in Ouroboros, I will be pretty brief: it operates in a
similar way as unicast IP: packets are forwarded to a destination
address, and the layer uses some algorithm to build a forwarding table
(or more general, a _forwarding function_). In the current
implementation, unicast is based on IS-IS link-state routing with
support for ECMP (equal-cost multipath). The core difference with IP
is that there are _no_ special case addresses: an address is _always_
uniquely assigned to a single network node. To scale the layer, there
can be different _levels_ of (link-state) routing in a layer. It's
very interesting in its own right, but I'll focus on the _modus
operandi_ in this post, which is: packets get forwarded based on an
address. I'll take a more in-depth look into Ouroboros addressing in
(maybe the next) post (or you can find it in the
[paper](https://arxiv.org/abs/2001.09707).

### Anycast

IP anycast is a funny thing. It's pretty simple: it's just unicast,
but multiple nodes (interfaces) in the network have the same address,
and the shortest path algorithm used in the routing protocol will
forward the packet to the nearest node (interface) with that
address. The network is otherwise completely oblivious; there is no
such thing as an _anycast address_, it's a concept in the mind of
network engineers.

Now, if your reaction is _that can't possibly work_, you're absolutely
right! Equal length paths can lead to _route flapping_, where some
packets would be delivered _over here_ and other packets _over
there_. That's why IP anycast is not something that _anyone_ can do. I
can't run this server somewhere in Germany and a clone of it in
Denver, and yet another clone in Singapore, and give them the same IP
address. IP anycast is therefore highly restricted to some select
cases, most notably DNS, NTP and some big Content Delivery Networks
(CDNs). There is a certain level of trust needed between BGP peers,
and BGP routers are monitored to remove routes that exhibit
flapping. In addition, NTP and DNS use protocols that are UDP-based
with a simple request-response mechanism, so sending subsequent
packets to a different server isn't a big problem. CDN providers go to
great _traffic engineering_ lengths to configure their peering
relations in such a way that the anycast routes are stable. IP anycast
"works" because there are a lot of assumptions and it's engineered --
mostly through human interactions -- into a safe zone of
operations[^1]. In the case of DNS in particular, IP anycast is an
essential part of the Internet. Being close to a root DNS server
impacts response times! The alternative would be to specify a bunch of
alternate servers to try. But it's easier to remember
[9.9.9.9](https://www.quad9.net/) than a whole list of random IP
addresses where you have to figure out where they are! IP anycast also
offers some protection against network failures in case the closest
server becomes unreachable, but this benefit is relatively small as
the convergence times of the routing protocols (OSPF/BGP) are on the
order of minutes (and should be). That's why most hosts usually have 2
DNS servers configured, because relying on anycast could mean a couple
of minutes without DNS.

Now, about anycast in Ouroboros, I can again be brief: I won't allow
multiple nodes with the same address in a layer in the prototype, as
this doesn't _scale_. Anycast is supported by name resolution. A
service can be registered at different locations (addresses) and
resolving such a name will return a (subset of) address(es) from the
locations. If a flow allocation fails to the closest address, it can
be repeated to the next one. Name resolution is an inherent function
of a _unicast layer_, and currently implemented as a Distributed Hash
Table (DHT). When joining a network (we call this operation
_enrolment_, Kademlia calls it _join_), a list of known DHT node
addresses is passed. The DHT stores its &lt;name, address&gt; entries
in multiple locations (in the prototype this number is 8) and the
randomness of the DHT hash assignment in combination with caching
ensures the _proximity_ of the most popular lookups with reasonable
probability.

### Broadcast

IP broadcast is also a funny thing, as it's not really IP that's doing
the broadcasting. It's a coating of varnish on top of _layer 2_
broadcast. So let's first look at Ethernet broadcast.

Ethernet broadcast does what you would expect from a broadcasting
solution. Note that switched Ethernets are confined to a loop-free
topology by grace of the (Rapid) Spanning-Tree Protocol. A message to
the reserved MAC address FF:FF:FF:FF:FF:FF will be _broadcasted_ by
every intermediate Layer 2 node to all nodes (interfaces) that are
connected on that Ethernet segment.  If VLANs are defined, the
broadcast is confined to all nodes (interfaces) on that
VLAN. Quite nice, no objections _your honor_!

The semantics of IP broadcast are related to the scope of the
underlying _layer 2_ network. An IP broadcast address is the last "IP
address" in a _subnet_. So, for instance, in the 192.168.0.0/24
subnet, the IP broadcast address is 192.168.0.255. When sending a
datagram to that IP broadcast destination, the Ethernet layer will be
sending it to FF:FF:FF:FF:FF:FF, and every node _on that Ethernet_
which has an IP address in the 192.168.0.0/24 network will receive it.
You'd be forgiven to think that an IP broadcast to 255.255.255.255
should be spread to every host on the Internet, but for obvious
reasons that's not the case. The semantic of 0.0.0.0/0 is to mean your
own local IP subnet on that specific interface. The DHCP protocol, for
instance, makes use of this. A last thing to mention is that, in
theory, you could send IP broadcast messages to a _different_ subnet,
but few routers allows this, because it invites some very obvious
[smurf attacks](https://en.wikipedia.org/wiki/Smurf_attack).
Excuse me for finding it more than mildly amusing that standards
originally
[_required_](https://tools.ietf.org/html/rfc2644)
routers to forward directed broadcast packets!

So, in practice,IP broadcast is a _passthrough_ interface towards
layer 2 (Ethernet, Wi-Fi, ...) broadcast.

In Ouroboros -- like in Ethernet -- broadcast is a rather simple
affair. It is facilitated by the _broadcast layer_, for which each
node implements a _broadcast function_: what comes in on one flow,
goes out on all others. The implementation is a stateless layer that
-- also like Ethernet -- requires the graph to be a tree. But it has
no addresses -- in fact, it doesn't even have a _header_ at all!
Access control is part of _enrolment_, where participants in the
broadcast layer get read and/or write access to the broadcast layer
based on credentials. Every message on a broadcast layer is actually
broadcast. This is the only way -- at least that I know of -- to make
a broadcast layer _scaleable_ to billions of receivers![^2]

So here is the first clue to the answer to the little conundrum at the
beginning of this post. The Ouroboros model makes a distinction
between _unicast layers_ and _broadcast layers_, based on the _nature
of the algorithm_ applied to the message. If it's based on a
_destination address_ in the message, we call the algorithm
_FORWARDING_, and if it's sending on all interfaces except the
incoming one, we call the algorithm _FLOODING_.

An application like 'ping', where one broadcasts a message to a bunch
of remotes, and each one responds back requires _both_ a broadcast
layer and a unicast layer of (at least) the same size, with the 'ping'
application using both[^3]. Tools like _ping_ and _traceroute_ and
_nmap_ are administrative tools which reveal network information. They
should only be available to _administrators_.

It's not prohibited to implement an IPCP that does both broadcast (to
the complete layer) and unicast. In fact, the unicast IPCP in the
prototype in some sense does it, as we only figured out broadcast
layers _after_ we implemented the link-state protocol, which is
effectively broadcasting link-state messages within the unicast
layer. All it would take is to implement the _flow\_join()_ API in the
unicast IPCP and send those packets like we send Link-State
Messages. But I won't do it, for a number of reasons: the first is
that it is rare to have broadcast layers and unicast layers to be
exactly the same size. Usually broadcast layers will be much
smaller. The second is that, in the current implementation, the
link-state messages are stateful: they have the source address and a
sequence number to be able to deal with loops in the meshed
topology. This doesn't scale to the _full_ unicast layer. To create a
scaleable _do-both-unicast-and-broadcast_ layer, it would require to
create a "virtual tree-topology-network" within the unicast layer,
which is adjacency management. This would require an adjacency
management module (running something like a hypothetical RSTP that is
able to scale to billions of nodes) as part of the unicast
IPCP. Adjacency management is functionality that was removed -- we
called it the _graph adjaceny manager_ and the logic put _outside_ of
the IPCP and replaced with a _connect_ API so it could be scripted as
part of network management.  And the third, and most important, is
that we like the prototype to reflect the _model_, as it is more
educational. Unicast layers and broadcast layers _are_ different
layers. Always have been, and always will be. Combining them in an
implementation only obfuscates this fact. To make a long (and probably
confusing) story short, combining unicast and broadcast in a single
IPCP _can_ be done, but at present I don't see any real benefit in
doing it, and I'm pretty sure it will be hard to avoid
[_making a mess_](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD13xx/EWD1304.html)
out of it.

This transitions us nicely into multicast. Because combining unicast
and multicast in the same layer is exactly what IP tries to do.

### Multicast

Before looking at IP, let's first have a look at how one would do
multicast in Ethernet, because it's simpler.

The simplest way to achieve multicast within Ethernet 802.1Q is using
a VLAN: Configure VLANs on the end hosts and switch, and then just
broadcast packets on that VLAN. The Ethernet II (MAC) frame will look
like this:

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
| FF:FF:FF:FF:FF:FF | SRC | 0x8100 | TCI | Ethertype | ..
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

The 0x8100 _en lieu_ of the Ethertype specifies that it's a VLAN, the
Tag Control Information (TCI) has 12 bits that specify a VLAN ID, so
one can have 4096 parallel VLANs. There are two fields needed to
achieve the multicast nature of the communications: The destination
set to the broadcast address, and a VLAN ID that will only be assigned
to members of the group.

Now, it won't come as a surprise to you, but IP multicast _is_ a funny
thing. The gist of it is that there are protocols that do group
management and protocols that assist in building a (spanning) tree.
There is a range of IP addresses, 224.0.0.0 -- 239.255.255.255 (or in
binary: starting with the 1110), called _class D_, which are only
allowed as destination addresses. This _class D_ is further subdivided
in different ranges for different functionalities, such as
source-specific multicast. An IPv4 multicast packet can be
distinguished by a single field: a destination address in the _class
D_ range.

If we compare this with Ethernet above, the _class D_ IP address is
behaving more like the VLAN ID than the destination MAC _address_. The
reason IP doesn't need an extra destination address is that the
_broadcast_ functionality is _implied_ by the _class D_ address range,
whereas a VLAN also supports unicast via MAC learning.

Ethernet actually also has a special address range for multicast,
01:00:5E:00:00:00 to 01:00:5E:7F:FF:FF, that copies the last 23 bits
of the IP multicast address when that host joins the multicast
tree. The reasoning behind it is this: if there are multiple endpoints
for an IP multicast tree on the _same_ Ethernet segment, instead of
the IP router sending individual unicast messages to each of them,
that last "hop" can use a single Ethernet broadcast message.

Next Ouroboros. From the discussion of the Ouroboros broadcast layer,
you probably already figured out how Ouroboros does multicast. The
same as broadcast! There is literally _zero_ difference. The only
difference between multicast and broadcast is in the eye of the
beholder when comparing a unicast layer and a broadcast layer.

There is something else to remember about (Ouroboros) broadcast
layers: the broadcast function is _stateless_, and _all_ broadcast
IPCPs are _identical_ in function. The reason I mention this, is in
relation the problem that I just mentioned above. What if I have a
broadcast layer, for which a number of endpoints are also connected
over a _lower_ broadcast layer? Can we, like IP/Ethernet, leverage
this? And the answer is: no, there is no sharing of information
between layers, and broadcast layers have no state. But we don't
really need to!  If there is a device with a broadcast IPCP in a lower
broadcast layer, just add a broadcast IPCP to the higher level
broadcast layer! It's not a matter of functionality, since the
functionality for the higher level broadcast layer is _exactly_ the
same as the lower one.

While I am not eager to mix broadcast and unicast in a single IPCP
program, I have few objections for creating a single program that
behaves like multiple IPCPs of the same type. Especially for the
stateless broadcast IPCP it would be rather trivial to make a single
program that implements parallel broadcast IPCPs. And allowing
something like _sublayers_ (like VLANs, with a single tag) is also
something that can be considered for optimization purposes.

### Conundrum, part II

Now, let's look back at our little riddle, with a packet observed to
move from source to destination over a linear network.

```
source - node - node - node - node - destination
```

Now, if we pedantically apply the definition of one-to-one
communication given in most textbooks, it is unicast, since it has
only a single source and a single destination. But to know what's
going on at the routing level, can not be known. But I hope you gave
it some thought about what information you'd need to be _able to
tell_.

Let's start with Ethernet. The Ethernet standard says that all MAC
addresses are unique, so it's not anycast, and there is no _real_
difference between multicast and broadcast. So, if the address is not
the broadcast address or in some special range, it's _unicast_, else
it's multi/broadcast. But really? What if the nodes were hubs instead
of switches?

What about IP? Bit harder. If it was anycast, it wouldn't have reached
the destination if there was another node with the same address in
this particular setup. But in a general IP network, it's not really
possible to tell the difference between unicast and anycast without
looking at all reachable node addresses. To know if it was broadcast
or multicast, it would suffice to know the destination address in the
packet.

For Ouroboros, all you'd need to know what was going on is the type of
layer. To detect anycast, one would need to query the directory to
check if it returns a single or multiple destination addresses (since
we don't allow _anycast routing_), and, like Ethernet in a way, it
makes the distinction between multicast and broadcast rather moot.

### The Ouroboros model

In a nutshell, what does the Ouroboros model say?

First, all communications is composed of either unicast or broadcast,
and these two types of communications are fundamentally different and
give rise to distinct types of layers. In a _unicast_ layer, nodes
implement _FORWARDING_, which moves packets based on a destination
address. In a _broadcast_ layer, nodes implement _FLOODING_, which
sends incoming packets out on all links except for the incoming link.

If we leave out the physical layer (wiring, spectrum tuning etc),
constructing a layer goes through 2 phases: adding a node to a network
layer (enrolment) and adding links (by which I mean allowed
adjacencies) between that node and other members of the layer
(adjacency management). After this the node becomes active in the
network. During enrolment, nodes can be authenticated and permissions
are acquired such as read/write access. Both types of layers go
through this phase. A unicast layer, may, in addition, periodically
disseminate information that enables _FORWARDING_. We call this
dissemination function _ROUTING_, but if you know a better word that
avoids confusion, we'll take it. _ROUTING_ is distinct from adjacency
management, in the sense that adjacency management is administrative,
and tells the networks which links it is allowed to use, which links
_exist_. _ROUTING- will make use of these links and make decisions
when they are unavailable, for instance due to failures.

Let's apply the Ouroboros model to Ethernet. Ethernet implements both
types of layers. Enrolment and topology management are taken care of
by the _spanning tree protocol_. It might be tempting to think that
STP does _only_ topology management, but that's not really the
case. Just add a new _root bridge_ to an Ethernet network: at some
point, that network will go down completely. The default operation of
Ethernet is as a _broadcast layer_: the default function applied to a
packet is _FLOODING_. To allow unicast, Ethernet implements _ROUTING_
via _MAC learning_. MAC learning is thus a highly specific routing
protocol, that piggybacks its dissemination information on user
frames, and calculates the forwarding tables based on the knowledge
that the underlying topology is a _tree_. This brings a caveat: it
only detects sending interfaces. If there are receivers on an Ethernet
that never send a frame (but for which the senders know the MAC
address), that traffic will always be broadcast. And in any case, the
_first_ packet will always be broadcast.

Next, VLAN. In Ouroboros speak, a VLAN is an implementation detail
(important, of course) to logically combine parallel Ethernets. VLANs
are independent layers, and indeed, must be enrolled (VLAN IDs set on
bridge interfaces) and will keep their own states of (R)STP and MAC
learning. Without VLAN, Ethernet is thus a single broadcast layer and
a single multicast layer. With VLAN, Ethernet is potentially 4096
broadcast layers and 4096 unicast layers.

If we apply the Ouroboros model to IP, we again see that IP tries to
implement both unicast and broadcast. A lot is configured
manually. Enrolment and adjacency management are basically assigning
IP addresses and, in addition, adding BGP routes and rules. IP has two
levels of _ROUTING_, one is inside an autonomous system using
link-state protocols such as OSPF, and on top there is BGP, which is
disseminating routes as path vectors. Multicast in IP is building a
broadcast layer, which is identified using a "multicast address",
which is really the name of that broadcast layer. Enrolment into this
virtual broadcast layer is handled via protocols such as IGMP, with
adjacencies managed in many possible ways that involve calculating
spanning trees based on internal topology information from OSPF or
other means. The tree is then grafted into the routing table by
labeling outgoing interfaces with the name of the broadcast
layer. Yes, _that_ is what adding a multicast destination address to
an IP forwarding table is _really_ doing! It's just hidden in plain
sight!

Now, my claim is that the Ouroboros model can be applied to _any_
packet network technology. To conclude this post, let's take a real
tricky one: Multi-Protocol Label Switching (MPLS).

MPLS looks very different from Ethernet and IP. It doesn't have
addresses at all, but uses _labels_, and it can swap and stack labels.

Now, surely, MPLS doesn't fit the unicast layer, which says that every
node gets an address, and forwards based on the destination address.
Here's the solution to MPLS: it is a set of broadcast layers! The
labels are a distributed way of identifying the layer _by its links_,
instead of a single identifier for the whole layer, like a VLAN or a
multicast IP address. RSVP / LDP (and their traffic engineering -TE
cousins) are protocols that do enrolment and adjacency management.

I hope this gave you a bit of an insight into the Ouroboros view of
the world. Course materials on computer networks consist of a
compendium of technologies and _how_ they work. The Ouroboros model is
an attempt to figure out _why_ they work.

Stay curious.

Dimitri


[^1]: I'm sure someone has or will propose some AI to solve it.

[^2]: Individual links on a broadcast layer can be protected with
      retransmission and using multi-path routing in the underlying
      unicast layer.

[^3]: Now that I'm writing this, I put it on my todo list to
      implement this into the oping application.
