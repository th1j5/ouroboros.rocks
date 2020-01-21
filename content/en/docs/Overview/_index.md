---
title: "Overview"
linkTitle: "Overview"
date: 2019-10-21
weight: 10
description: >
   A bird's eye view of Ouroboros.
---

{{% pageinfo %}}
Under construction.
{{% /pageinfo %}}

Ouroboros is a (prototype) **distributed system** for packet network
communications. It consists of a C **library** that allows you
to write ouroboros-native programs and the subsystem that consists of
a bunch of **daemons** that allow you to easily create your own
(overlay) networks using ordinary PC hardware (Linux, FreeBSD or MacOS
X).

The **Ouroboros library** implements the **application API** (the
Ouroboros alternative to POSIX sockets) and the **management API**
(the Ouroboros alternative to things like netlink sockets).

{{<figure width="60%" src="/docs/overview/intro.jpg">}}

From an application perspective, all that's needed is to link your
application with Ouroboros and you can use the Ouroboros networking
primitives.

All **end-to-end transport functions** are implemented in the
application library, such as **reliability** (packet ordering,
retransmission logic etc) and transport **encryption**.

The Ouroboros daemons can be thought of as **software routers** that
 can be connected to each other. Each one has an address,
 and they forward packets among each other. The daemons also implement
 a Distributed Hash Table, so the network has its own internal
 name-to-address resolution.

The best place to start understanding a bit what this does and how it
differs from other packet networks is to have a quick look at the
[flow allocation](/docs/concepts/fa/) and [data
path](/docs/concepts/datapath/) sections.
