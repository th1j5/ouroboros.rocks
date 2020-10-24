---
date: 2020-10-24
title: "Why is this better than IP?"
linkTitle: "Why is this better than IP?"
description: "The problem with the Internet isn't that it's
wrong, it's that it's almost right. -- John Day"
author: Dimitri Staessens
---

With the COVID-19 pandemic raging on at its current peak all over the
world, it has been a weird couple of months for most of us. In the
last few weeks I did a first implementation of the missing part of the
FRCP protocol (retransmission and flow control, fragmentation is still
needed), and I hope to get congestion control done by the end of the
year, which is very needed because with the retransmission the
prototype experiences congestion collapse on a bottleneck caused by
the bandwidth of the shared memory allocator we implemented. Then I
can finally get rid of the many annoying bugs, stabilize the
prototype, and then implement a better allocator. But this is not the
main thing I wanted to adress.

I've also been pondering the question I always get from network
engineers. It's the one that annoys me the most, because it seems that
first this question needs to be answered for the questioner to even
consider taking any attempt or spending any effort in trying to
understand the body of work presented. This question is, of course,
*Why is this better than IP?*

Now,there are two things we did when building Ouroboros. The most
visible is the prototype implementation, but behind it is a network
model. This network model is not some arbitrary engineering excercise,
we tried to find the minimum *required and sufficient conditions* for
networking, mathematically. In this sense -- under the precondition
that the model is correct[^2] -- every working network has to fulfill
the model, like it or not. It's not a choice one can take or
leave. I'll try to find more time (and to be perfectly honest: the
motivation) in the next couple of weeks to get this aspect across with
more clarity and precision than with which it is currently presented
in the [paper](https://arxiv.org/pdf/2001.09707.pdf).

Now, I would argue that the current Internet with all its technologies
(TCP/IP, VPNs, MPLS, QUIC, ...) is closer to the model we derived than
it is to the 7-layer-model. NASA's
[DTNs](https://www.nasa.gov/content/dtn) don't violate the
model[^1]. RINA is of course very close to the model, as it also
predicts the recursive nature of networks. The prototype is an
implementation of the model (and thus in some way, close to a minimal
network).

While the model predicts recursive layering, it doesn't forbid
engineers to use different APIs for each layer, mix and combine layers
into logical constructs, expose layer internals, rewrite packet
headers, and do whatever they please. It may have economical benefits
for an engineer to put a solution in whatever logical part of the
network, hack in an API to expose what the solution needs and then
sell it. But this engineering comes at the cost of adding complexity
without functionality.

I'll use an analogy from programming: a simple C for loop uses an
index variable, typically named "i". It is generally seen as bad
practice to modify this index variable inside the loop, something like
this.

```C
for (int i = 1; i <= 10; ++i) {
        if(i == 2)
                i = 4;
        /* Do some work */
}
```

But is such code "worse" than another solution to skip 2 and 3, such
as this?

```C
for (int i = 1; i <= 10; ++i) {
         if(i == 2 || i == 3)
                 continue;
         /* Do some work */
}
```

The reason it is considered bad practice, is based on years of
programming experience: thousands of programmers noticing that such
constructs often lead to bugs and lower maintainability. I would argue
that the Internet is full of this kind of bad practices -- it doesn't
take a huge stretch of the imagination to take the example above as an
analogy for Network Address Translation. Only instead of being seen as
bad practices, they are taught as indispensible networking technologies.

And that's why I think Ouroboros is a "good" network model. If the
minimal necessary and sufficient conditions for networking are
understood as a consistent model for networks, we can better assess
where engineering decisions have been made that add complexity without
objectively adding functionality to the whole. Unfortunately, there
aren't many scientists that design networking solutions from the
ground up, so there isn't much experience to go around.

So then, is Ouroboros better than IP? From an engineering perspective,
maybe not, or not by much. But I'm fine with that, it's not my objective.

Keep safe social distancing, take care and stay curious.

Dimitri

P.S. Of course, I was curious about what the GCC
[compiler](https://godbolt.org) does with the source code examples
above. It does seems like the "better" solution also optimizing a bit
better:

<iframe width="80%" height="800px" src="https://godbolt.org/e#g:!((g:!((g:!((h:codeEditor,i:(fontScale:14,j:1,lang:___c,selection:(endColumn:2,endLineNumber:18,positionColumn:2,positionLineNumber:18,selectionStartColumn:2,selectionStartLineNumber:18,startColumn:2,startLineNumber:18),source:'//+Type+your+code+here,+or+load+an+example.%0A%23include+%3Cstdio.h%3E%0A%0Avoid+func()+%7B%0A++++for+(int+i+%3D+1%3B+i+%3C%3D+10%3B+%2B%2Bi)+%7B%0A++++++++if(i+%3D%3D+2)%0A+++++++++++i+%3D+4%3B%0A++++++++printf(%22%25d%5Cn.%22,+i)%3B%0A++++%7D%0A%7D%0A%0Avoid+func2()+%7B%0A++++for+(int+i+%3D+1%3B+i+%3C%3D+10%3B+%2B%2Bi)+%7B%0A++++++++if(i+%3D%3D+2+%7C%7C+i+%3D%3D+3)%0A++++++++++++continue%3B%0A++++++++printf(%22%25d%5Cn.%22,+i)%3B%0A++++%7D%0A%7D'),l:'5',n:'0',o:'C+source+%231',t:'0')),k:50,l:'4',n:'0',o:'',s:0,t:'0'),(g:!((h:compiler,i:(compiler:cg102,filters:(b:'0',binary:'1',commentOnly:'0',demangle:'0',directives:'0',execute:'1',intel:'0',libraryCode:'1',trim:'1'),fontScale:14,j:1,lang:___c,libs:!(),options:'-O4',selection:(endColumn:25,endLineNumber:11,positionColumn:25,positionLineNumber:11,selectionStartColumn:25,selectionStartLineNumber:11,startColumn:25,startLineNumber:11),source:1),l:'5',n:'0',o:'x86-64+gcc+10.2+(Editor+%231,+Compiler+%231)+C',t:'0')),k:50,l:'4',n:'0',o:'',s:0,t:'0')),l:'2',n:'0',o:'',t:'0')),version:4"></iframe>


[^1]: I came across this when thinking about the limits for the timers for retransmission. A DTN is basically two layers, one without retransmission on top of one with retransmission at very long timeouts.
[^2]: Of all the comments from peer review, not a single one has addressed any technical issues -- let alone correctness -- of the model. Most are that I fail to justify why the reviewer should bother to read the article or make an effort to try to understand it as it doesn't fit current engineering workflows and thus has little chance of short-term deployment. Sorry, but I don't care.