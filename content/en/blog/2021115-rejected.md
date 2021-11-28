---
date: 2021-11-15
title: "JACM paper rejected"
linkTitle: "JACM paper rejected"
description: "reflections"
author: Dimitri Staessens
---

This weekend we got word from the paper we submitted to JACM early
2019. Not too surprised that it was rejected. Actually, rather
surprised that we still hear of it after 3 years. So thanks to the
reviewer for his/her time.  The rejection was justified, and I got
something useful out of it, despite some of the reviewer's comments
being disgracefully wrong[^1].

I've written over 30 research papers in my first years at university,
most went from first conception to a paper in less than a month. I had
only 2 rejects. That's because they contained only work and very
little ideas. I was bored out of my skull. It took me months to write
the Ouroboros paper. Because I had no clear-cut conclusion yet to work
towards. And definitely no engineering results.

Publish or perish. To write publications, you need results. To
get results you need time. To get time you need funding. To get
funding you need publications. The vicious circle ensuring that
academics can't take on any long-term high-risk endeavour that doesn't fit the
ever shortening funding cycles.  What a waste of time.. Rob Pike
[saw it 20 years ago](http://doc.cat-v.org/bell_labs/utah2000/utah2000.html).

There's a joke that in most jobs, people hope to win to lottery so
they can quit. But in academia, they hope to win the lottery so they
can keep it.

Carl Sagan famously said that great claims require great evidence.
We've failed (and wasted tons of research time) trying to squeeze a
paper out of this work-in-progress. As I detailed in a
[previous blog post](blog/2021/03/20/how-does-ouroboros-relate-to-rina-the-recursive-internetwork-architecture/),
there is a lot of research and [implementation
work](https://tree.taiga.io/project/dstaesse-ouroboros/epics) (not
necessarily in that order) to be done before we can _comfortably_
write a paper on these ideas. We'll just have to ride it out.

Direction is more important than speed.

Cheers,

Dimitri

[^1]: The most ironic being that the reviewer (yes, we got only a
      single reviewer) accuses me of redefining graph theory and using
      pseudo-mathematics, without counter-examples or counter-proof or
      even a polite request for clarification. Even worse, the
      reviewer then claims that a _closed walk_ is the same as a
      _Hamiltonian path_. What the actual fuck. In a walk, vertices
      can be visited multiple times. All definitions in the paper are
      taken straight out of Dieter Jungnickels' excellent
      [Graphs, Networks and Algorithms](https://link.springer.com/book/10.1007/978-3-642-32278-5).
      I didn't fully trust engineering reviews and had an actual
      professor in discrete mathematics review the math before we
      submitted the paper. I'll just take it that it was justified to
      add the basic math definitions and build everything up from
      scratch. I still stand by the math in the paper.