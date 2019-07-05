---
title: "Philosophy"
date: 2019-02-28T09:52:26+01:00
publishDate: 2019-02-28T09:52:26+01:00
author: "Dimitri Staessens"
images: []
draft: false
tags: []
---

<center>![](https://effectivesoftwaredesign.files.wordpress.com/2015/10/quote-if-10-years-from-now-when-you-are-doing-something-quick-and-dirty-you-suddenly-visualize-that-i-edsger-dijkstra-50997.jpg)</center>

During his entire scientific career, Edsger Dijkstra broke a lance for
the creed -- which he attributes to Tony Hoare -- that [*simplicity is
prerequisite for
reliability*](http://www.cs.utexas.edu/users/EWD/transcriptions/EWD06xx/EWD619.html). He
spent a lot of time and effort convincing his contemporaries in the
computing science community that *elegance is not a dispensable
luxury, but a matter of life and death*. Dijkstra was painfully aware
that [*simplicity is very hard to
achieve*](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD896.html)
and grossly underrated, even to the point that the academic and
economic reward systems work against any attempt do so: "*complexity
sells better*". With some computer engineers living by the motto *move
fast and break things*, Dijkstra would most definitely [not have been
happy](http://www.cs.utexas.edu/users/EWD/transcriptions/EWD12xx/EWD1213.html)
with much of the current state of affairs of computing science. While
he always will be considered one of the greatest computer scientists
that ever lived, his passionate message to diligently strive for
elegance seems to be all but erased from the collective consciousness
of engineers and computer scientists. Are we further away today from
computing's central challenge than we were [almost 20 years ago]
(https://www.cs.utexas.edu/users/EWD/transcriptions/EWD13xx/EWD1304.html)?

<center> {{<figure
class="fl"
src="https://imgs.xkcd.com/comics/move_fast_and_break_things.png"
width="200">}}
</center>

The current TCP/IP network stack has a long development history, and
its technical debt is leading to inefficiencies that allow hackers to
infiltrate networks with childish ease. In order to get to a
trustworthy and secure communications infrastructure, the structure of
the Internet needs to be drastically revised. The current protocols
have so much deprecated, unused and unnecessary bits and fields, that
trying to guard against every possible exploit is inefficient and
virtually impossible.

Ouroboros is a new decentralized packet transport network for POSIX
operating systems that aims to accepts Edward Snowdens
[challenge](https://www.theatlantic.com/politics/archive/2014/05/edward-snowdens-other-motive-for-leaking/370068/):
to build a network infrastructure that will "*enforce a principle
whereby the only way the powerful may enjoy privacy is when it is the
same kind shared by the ordinary: one enforced by the laws of nature,
rather than the policies of man*."
