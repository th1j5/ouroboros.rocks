---
title: "Welcome to Ouroboros"
linkTitle: "Introduction"
author: "Dimitri Staessens"
date: 2019-12-30
weight: 5
description: >
   Introduction.
---

```
Simplicity is a great virtue but it requires hard work to achieve it and
education to appreciate it.
And to make matters worse: complexity sells better.
        -- Edsger Dijkstra
```

This is the portal for the ouroboros networking prototype. Ouroboros
aims to make packet networks simpler, and as a result, more reliable,
secure and private. How? By introducing strong, well-defined
abstractions and hiding internal complexity. A bit like modern
programming languages abstract away details such as pointers.

The main driver behind the ouroboros prototype is a good ol' personal
itch. I've started my academic research career on optical networking,
and moved up the stack towards software defined networks, learning the
fine details of Ethernet, IP, TCP and what not. But when I came into
contact with John Day and his Recursive InterNetwork Architecture
(RINA), it really struck home how unnecessarily complicated today's
networks are. The core abstractions that RINA moved towards simplify
things a lot. I was fortunate to have a PhD student that understood
the implications of these abstractions, and together we just went on
and digged deeper into the question of how we could make everything as
simple as possible. When something didn't fall into place or felt
awkward, we trace back to why it didn't fit, instead of plough forward
and make it fit. Ouroboros is the current state of affairs in this
quest.

We often get the question "How is this better than IP"? To which the
only sensible answer that we can give right now is that ouroboros is
way more elegant. It has far fewer abstractions and every concept is
well-defined. It's funny (or maybe not) how many times when we start
explaining Ouroboros to someone, people immediately interrupt and
start explaining how they can do this or that with IP. We know,
they're right, but it's also completely besides our point.

If you don't care about elegance, this prototype is not (yet) for
you. If you're fine with the quality of engineering in the Internet,
this prototype is not (yet) for you. But, if you're open to the idea
that the TCP/IP network stack is a huge gummed-up mess that's in need
for some serious redesign, do read on. If you are interested in
computer networks in general, if you are eager to learn something new
and exciting without the need to deploy it tomorrow to solve whatever
problem you have right now, and if you are willing to put in the time
and effort to understand how all of this works, by all means: ask
away!

We're very open to constructive suggestions on how to further improve
the prototype and the documentation, in particular this website. We
know it's hard to understand in places. No matter how simple we made
the architecture, it's still a lot to explain, and writing efficient
documentation is a tough trade. So don't hesitate to contact us with
any questions you may have. Above all, stay curious!

```
... for the challenge of simplification is so fascinating that, if
we do our job properly, we shall have the greatest fun in the world.
        -- Edsger Dijkstra
```