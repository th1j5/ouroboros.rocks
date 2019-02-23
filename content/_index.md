---
title: "A decentralized packet network"
---

The current TCP/IP network stack has a long development history,
leading to inefficiencies that allow hackers to infiltrate networks
with childish ease. In order to get to a trustworthy and secure
communications infrastructure, the structure of the Internet needs to
be drastically revised. The current protocols have so much deprecated,
unused and unnecessary bits and fields, that trying to guard against
every possible exploit is inefficient and virtually impossible.

Ouroboros is a new decentralized packet transport network for POSIX
operating systems that aims to accepts Edward Snowdens
[challenge](https://www.theatlantic.com/politics/archive/2014/05/edward-snowdens-other-motive-for-leaking/370068/):
to build a network infrastructure that will "*enforce a principle
whereby the only way the powerful may enjoy privacy is when it is the
same kind shared by the ordinary: one enforced by the laws of nature,
rather than the policies of man*."

Ouroboros is a peer-to-peer recursive architecture that follows a UNIX
design philosphy, with minimal packet headers. The aim is to provide a
secure and private network experience. Ouroboros provides its own name
resolution, reliability mechanisms, routing algorithms, and congestion
control. It can be overlayed on top of UDP and Ethernet, and IP
applications can be tunneled over Ouroboros.

Ouroboros is [free
software](https://www.fsf.org/about/what-is-free-software), written in
C for and its application library provides a simple, unified API for
synchronous and asynchronous Inter-Process Communication (IPC) and
networking.

The best place to start exploring Ouroboros is this introduction
presented at [FOSDEM
2018](https://www.fosdem.org/2018/schedule/event/ipc/).

This new website is currently under construction and undergoing
frequent updates. The documentation is still sparse, please don't
hesitate to [contact us](/contribute) with any questions you might
have.
