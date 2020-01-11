---
title: "The problem with the current layered model of the Internet"
author: "Dimitri Staessens"

date:  2019-07-06
weight: 1
description: >
   The current networking paradigm
---

{{<figure width="40%" src="/docs/concepts/aschenbrenner.png">}}

Every computer science class that deals with networks explains the
[7-layer OSI model](https://www.bmc.com/blogs/osi-model-7-layers/).
Open Systems Interconnect (OSI) defines 7 layers, each providing an
abstraction for a certain *function* that a network application may
need.

From top to bottom, the layers provide (roughly) the following
functions:

The __application layer__ implements the details of the application
protocol (such as HTTP), which specifies the operations and data that
the application understands (requesting a web page).

The __presentation layer__ provides independence of data representation,
and may also perform encryption.

The __session layer__ sets up and manages sessions (think of a session
as a conversation or dialogue) between the applications.

The __transport layer__ handles individual chunks of data (think of them
as words in the conversation), and can ensure that there is end-to-end
reliability (no words or phrases get lost).

The __network layer__ forwards the packets across the network, it
provides such things as addressing and congestion control.

The __datalink layer__ encodes data into bits and moves them between
hosts. It handles errors in the physical layer. It has two sub-layers:
Media access control layer (MAC), which says when hosts can transmit
on the medium, and logical link control (LLC) that deals with error
handling and control of transmission rates.

Finally, the __physical layer__ is responsible for translating the
bits into a signal (e.g. laser pulses in a fibre) that is carried
between endpoints.

This functional layering provides a logical order for the steps that
data passes through between applications. Indeed, existing (packet)
networks go through these steps in roughly this order (however, some
may be skipped).

However, when looking at current networking solutions in more depth,
things are not as simple as these 7 layers seem to indicate. Consider
a realistic scenario for a software developer working
remotely. Usually it goes something like this: he connects over the
Internet to the company __Virtual Private Network__ (VPN) and then
establishes an SSH __tunnel__ over the development server to a virtual
machine and then establishes another SSH connection into that virtual
machine.

We are all familiar enough with this kind of technologies to take them
for granted. But what is really happnening here? Let's assume that the
Internet layers between the home of the developer and his office
aren't too complicated. The home network is IP over Wi-Fi, the office
network IP over Ethernet, and the telecom operater has a simple IP
over xDSL copper network (because in reality operator networks are
nothing like L3 over L2 over L1).  Now, the VPN, such as openVPN,
creates a new network on top of IP, for instance a layer 2 network
over TAP interfaces supported by a TLS connection to the VPN server.

Technologies such as VPNs, tunnels and some others (VLANs,
Multi-Protocol Label switching) seriously jumble around the layers in
this layered model. Now, by my book these counter-examples prove that
the 7-layered model is, to put it bluntly, wrong. That doesn't mean
it's useless, but from a purely scientific view, there has to be a
better model, one that actually fits implementations.

Ouroboros is our answer towards a more complete model for computer networks.