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
communications. It consists of a C **library** that allows you to
write ouroboros-native programs and a bunch of **daemons** that allow
you to easily create your own (overlay) networks using ordinary PC
hardware (Linux, FreeBSD or MacOS X).

The **Ouroboros library** implements the **application API** (the
Ouroboros alternative to POSIX sockets) and the **management API**
(the Ouroboros alternative to things like netlink sockets). All
**end-to-end transport functions** are implemented in the application
library, such as **reliability** (packet ordering, retransmission logic
etc) and transport **encryption**.

The Ouroboros daemons can be thought of as **software routers** that
 can be connected to each other. Each one has an address,
 and they forward packets among each other. The daemons also implement
 a Distributed Hash Table, so the network has its own internal
 name-to-address resolution.