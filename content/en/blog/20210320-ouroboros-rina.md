---
date: 2021-03-20
title: "How does Ouroboros relate to RINA, the Recursive InterNetwork Architecture?"
linkTitle: "Is Ouroboros RINA?"
description: "A brief history of Ouroboros"
author: Dimitri Staessens
---

```
There are two kinds of researchers: those that have implemented
something and those that have not. The latter will tell you that there
are 142 ways of doing things and that there isn't consensus on which
is best.The former will simply tell you that 141 of them don't work.
  -- David Cheriton
```

When I talk to someone that's interested in Ouroboros, a question that
frequently pops up is how the project relates to the
[Recursive InterNet(work) Architecture](https://en.wikipedia.org/wiki/Recursive_Internetwork_Architecture),
or **RINA**. I usually steer away from going into the technical
aspects of how the architectures differ, mostly because not many
people know the details of how RINA works. But the origin of Ouroboros
definitely lies with our research and our experiences implementing
RINA, so it's a good question. I'll address it as best as I can,
without going overboard on a technical level. I will assume the reader
is at least somewhat familiar with RINA. Also keep in mind that both
projects are ongoing and should not be considered as "done"; things
may change in the future. These are my -- inevitably subjective and
undoubtedly somewhat inaccurate -- recollections of how it went down,
why Ouroboros exists, and how it's different from RINA.

And a quick note here: Ouroboros _the network prototype_ has no
relation to Ouroboros _the Proof-of-Stake protocol_ in the Cardano
blockchain. That some of the Cardano guys are also interested in RINA
doesn't help to ease any confusion.

### IBBT meets RINA

I first came into contact with RINA somewhere in 2012, while working
as a senior researcher in the field of telecommunication networks at
what was then known as IBBT (I'll save you the abbreviation). IBBT
would soon be known as iMinds, and is now integrated into
[IMEC](https://www.imec-int.com).  A new research project was going to
start and our research group was looking for someone to be responsible
for the IBBT contributions. That project, called
[IRATI](https://cordis.europa.eu/project/id/317814) was a relatively
short (2 years duration) project in the "Future Internet Research and
Experimentation" (FIRE) area of the _7th framework programme_ of the
European Commission. I won't go into the details and strategies of
research funding; the important thing to know is that the objectives
of FIRE are "hands-on", aimed at building and deploying Internet
technologies. Given that I had some experience deploying experiments
(at that time OpenFlow prototypes) on our lab testbeds, I listened to
the project pitch, an online presentation with Q&A given by the
project lead, Eduard Grasa from [i2cat]((https://i2cat.net/)), who
explained the concepts behind RINA, and got quite excited about how
elegant this all looked. So I took on the project and read John Day's
[Patterns in Network Architecture](https://www.oreilly.com/library/view/patterns-in-network/9780132252423/),
which we later usually referred to as _PNA_.  It was also the time
when I was finishing my PhD thesis, so my PostDoc track was going to
be for a substantial part on computer network architecture and RINA.
Unifying
[Inter-Process Communication](https://en.wikipedia.org/wiki/Inter-process_communication)
(IPC) and networking. How exciting was that!

IRATI -- Investigating RINA as an Alternative to TCP/IP -- was
something different from the usual research projects, involving not
only some substantially new and unfamiliar ideas, but it also relied
very heavily on software development. Project work was performed as
part of PhD tracks, so who would do the work? There was a PhD student
under my guidance working mostly on OpenFlow, Sachin -- one of the
kindest people I have ever met, and now a professor at TU Dublin --
and there was also a master thesis student, Sander Vrijders, that was
interested in pursuing a PhD in our research group. After a couple of
internal sessions where we explained possible research tracks aligned
to ongoing and upcoming projects in our group, Sander decided to take
on the challenge of IRATI and start a PhD track on RINA.

### IRATI

**IRATI** kicked off in January 2013 at i2cat in Barcelona. It was
followed by a RINA workshop, bringing the project in touch with the
RINA community, which had its epicenter at Boston University
(BU). It's where I first met John Day, who gave a 2-day in-depth
tutorial of RINA. Eduard also presented an outline of the IRATI
objectives. The project promised an implementation of RINA in Linux
_and_ FreeBSD/JunOS, with detailed comparisons of RINA against TCP/IP
in various scenarios, and also demonstrate interoperability with other
RINA prototypes: the
[TINOS prototype](https://github.com/PouzinSociety/tinos) and the
[TRIA](http://trianetworksystems.com/) prototype. IRATI would also
prepare the European FIRE testbeds for RINA experiments using the
prototype. In 2 years, on 870k Euros in research funding. A common
inside joke at project kick-off meetings in our field was to put a
wager on the number slides that the presentation deck at the final
project review meeting would differ from the slide decks presented at
the initial kick-off meeting. IRATI was _not_ going to be one of those
projects!

With the RINA community gathered at the workshop, there were initial
ideas for a follow-up research proposal to IRATI. Of course, almost
every potential participant present was on board.

Three partners were responsible for the implementation: i2cat, who had
experience on RINA; [Nextworks](https://www.nextworks.it) a
private-sector company with substantial experience on implementing
networking solutions, and iMinds/imec, bringing in our testbed
experience. Interoute (now part of [GTT](https://gtt.net)) validated
the test scenarios that we would use for evalutions. Boston University
had an advisory role in the project.

The first work was determining the software design of the
implementation. IRATI was going to build an in-kernel implementation
of RINA. A lot of the heavy lifting on the design was already done
during the project proposal preparation phase, and the components to
be implemented were
[well-defined](https://core.ac.uk/download/pdf/190646748.pdf).
Broadly speaking, there were 3 things to implement: the IPCPs that
make up the RINA layers (Distributed IPC Facilities, DIFs), the
component that is responsible for creating and starting these IPCPs
(the IPC manager, which had a user space and a kernel space part), and
the core library to communicate between these components, called
_librina_. The prototype would be built in 3 phases over the course of
2 years.

i2cat was going to get started on most of the management parts (IPC
Manager, based on their existing Java implementation; librina,
including the Common Distributed Application Protocol (CDAP) and the
DIF management functions in the normal IPCP) and the Data Transfer
Protocol (DTP). iMinds was going to be responsible for the kernel
modules that will allow the prototype to run on top of
Ethernet. Nextworks was taking a crucial software-architectural role
on kernel development and software integration. For most of these
parts we had access to a rough draft of what they were supposed to do,
John Day's RINA reference model, which we usually referred to as _the
specs_.

i2cat had a vested interest in RINA and was putting in a lot of
development effort with 3 people working on the project: Eduard,
Leonardo Bergesio and Miquel Tarz&aacute;n. Nextworks assigned
Francesco Salvestrini, an experienced kernel developer to the
project. From iMinds, the development effort would come from
Sander. My personal involvement in the project software development
was limited, as I still had other ongoing projects (at least until the
end of 2014) and my main role would be in the experimentation work,
which was only planned start after the initial development phase.

The project established efficient lines of communications, mostly
using Skype and the mailing lists and the implementation work got
underway swiftly. I have been fortunate to be a part of a couple of
projects where collaboration between partners was truly excellent, but
the level of teamwork in IRATI was unprecedented. There was a genuine
sense of excitement in everybody involved in the project.

So, Sander's first task was to implement the
[_shim DIF over Ethernet_](https://ieeexplore.ieee.org/document/6798429).
This is a Linux loadable kernel module (LKM) that wraps the Ethernet
802.1Q VLAN with a thin software layer to present itself using the
RINA API. The VLAN ID would be used as the layer name. No
functionality would be added to the existing Ethernet protocol so with
only the src and dst address fields left, this _shim DIF_ was
restricted to having only a single application registered at a time,
and to a single RINA "flow" between the endpoints. We could deploy
about 4000 of these _shim DIFs_ in parallel to support larger RINA
networks. The name resolution for endpoint applications was planned to
be using the Address Resolution Protocol (ARP), which was readily
available in the Linux kernel.

Or so we thought. The ARP implementation in the kernel assumed IPv4 as
the only L3 protocol (IPv6 doesn't use ARP), so it could not handle
the resolution of RINA _application names_ to MAC addresses, which we
needed for the shim DIF. So after some deliberation, we decided to
implement an RFC 826 compliant version of ARP to support the shim DIF.

In the meantime, we also submitted a small 3-partner project proposal
the GEANT framework, tailored to researching RINA in an NREN (National
Research and Education Networks) environment. The project was lead by
us, partnering with i2cat, and teaming up with
[TSSG](https://tssg.org/).  [IRINA](https://i2cat.net/projects/irina/)
would kick off in October 2013, meaning we'd have 2 parallel projects
on RINA.

The project had made quite some progress in its first 6 months, there
were initial implementations for most of the components, and in terms
of core prototype functionality, IRATI was quickly overtaking the
existing RINA prototypes. However, the pace of development in the
kernel was slower than anticipated and some of the implementation
objectives were readjusted (and FreeBSD/JunOS was dropped in favor of
a _shim DIF for Hypervisors_). With the eye on testbed deployments,
Sander started work on the design of a second _shim DIF_, one that
would allow us to run the IRATI prototype over TCP/UDP.

In the meantime, the follow-up project that was coined during the
first RINA workshop took shape and was submitted. Lead by our IRINA
partner TSSG, it was envisioned to be a a relatively large project,
about 3.3 million Euros in EC contributions, running for 30 months and
bringing together 13 partners with the objective to build the IRATI
prototype into what was essentially a carrier network demonstrator for
RINA, adding _policies_ for mobility, security and reliability.
[**PRISTINE**](https://cordis.europa.eu/project/id/619305) got
funded. This was an enormous boon to the RINA community, but also a
bit of a shock for us as IRATI developers, as the software was already
a bit behind schedule with a third project on the horizon. The
furthest we could push forward the start of PRISTINE was January 2014.

As the IRATI project was framed within
[FIRE](https://dl.acm.org/doi/10.1145/1273445.1273460), there was a
strong implied commitment to get experimental results with the project
prototype. By the last quarter of 2013, the experimentation work got
started, and the prototype was getting its first deployment trials on
the FIRE testbeds. This move to real hardware brought more problems to
light. The network switches in the OFELIA testbed wasn't agreeing very
well with our RFC-compliant ARP implementation, dropping everything
that hadn't IPv4 as the network addresses. One of the testbeds also
relied on VLANs to seperate experiments, which didn't fare well with
our idea to (ab)use them within an experiment for the _shim
DIF_. While Sander did the development of the _shim DIFs_ using the
actual testbed hardware, other components had been developed
predominantly in a virtual machine environment and had not been
subjected to the massive parallellism that was available on dual-Xeon
hardware. The stability of the implementation had to be substantially
improved to get stable and reliable measurements. These initial trials
in deploying IRATI also showed that configuring the prototype was very
time consuming. The components used json configuration files which
were to be created for each experiment deployment, causing substantial
overhead.

The clock was ticking and while the IRATI development team was working
tirelessly to stabilize the stack, I worked on some (kernel) patches
and fixes for the testbeds so we could use VLANs (on a different
Ethertype) in our experiment. We would get deployment and stability
testing done and (internally) release _prototype 1_ before the end of
the year.

### PRISTINE

January 2014. The PRISTINE kick-off was organized together with a
workshop, where John Day presented RINA, similar to the IRATI kick-off
one year earlier, except this time it was in Dublin and the project
was substantially bigger, especially in headcount. It brought together
experts in various fields of networking with the intent of them
applying that experience into developing polcies for RINA. But many of
the participants to the PRISTINE project were very new to RINA, still
getting to grips with some of the concepts (and John didn't shy away
from making that abundantly clear).

The first couple of months of PRISTINE was mostly about getting the
participants up-to-speed with the RINA architecture and defining the
use-case, which centered on a 5G scenario with highly mobile end-users
and intelligent edge nodes. It was very elaborate, and the associated
deliverables were absolute dreadnoughts.

During this PRISTINE ramp-up phase, development of the IRATI prototype
was going on at a fierce pace. The second project brought in some
extra developers to work on the IRATI core Bernat Gaston (i2cat),
Vincenzo Maffione (Nextworks), and Douwe de Bock (a master student at
iMinds). i2cat focusing on management and flow control and was also
porting the Java user-space parts to C++, Vincenzo was focusing on the
_shim Hypervisor_, which would allow communications between processes
running over a VM host and guest, and we were building the shim layer
to run RINA over TCP and UDP.

By this time, frustrations were starting to creep in. Despite all the
effort in development, the prototype was not in a good shape.  The
development effort was also highly skewed, with i2cat putting in the
bulk of the work. The research dynamic was also changing. At the start
of IRATI, there was a lot of ongoing architectural discussions about
what each component should do, to improve the _specs_, but due to the
ever increasing time pressure, the teams were working more and more in
isolation. Getting it _done_ became a lot more important than getting
it _right_.

All this development had led to very little dissemination output,
which didn't go unnoticed at project reviews. The upshot of the large
time-overlap between the two projects was that, in combination with
the IRATI design paper that got published early-on in the project, we
could afford to lose out a bit on dissemination in IRATI and try to
catch up in PRISTINE. But apart from the relatively low output in
research papers, this project had no real contributions to
standardization bodies.

In any case, the project had no choice but to push on with
development, and, despite all difficulties, somewhere mid 2014 IRATI
had most basic functionalities in place to bring the software in a
limited way into PRISTINE so it could start development of the
_PRISTINE software developement kit (SDK)_ (which was developed by
people also in IRATI).

Mostly to please the reviewers, we tried to get some standardization
going, presenting RINA at an ISO SC6 JTC1 meeting in London and also
at IETF91. Miquel and myself would continue to follow up on
standardization in SC6 WG7 on "Future Network" as part of PRISTINE,
gathering feedback on the _specs_ and getting them on the track
towards ISO RINA standards. I still have many fond memories of my
experiences discussing RINA within WG7.

The IRATI project was officially ending soon, and the development was
now focusing on the last functions of the Data Transfer Control
Protocol (DTCP) component of EFCP, such as retransmission logic
(delta-t). Other development was now shifted completely out of IRATI
towards the PRISTINE SDK.

In the meantime, we also needed some experimental
results. Experimentation with the prototype was a painful and very
time-consuming undertaking. We finally squeezed a publication at
Globecom 2014 out of some test results and could combine that with a
RINA tutorial session.

January 2015, another new year, another RINA workshop. This time in
Ghent, as part of a Flemish research project called RINAiSense --
which should be pronounced like the French _renaissance_ -- that would
investigate RINA in sensor networks (which now falls under the nomer
"Internet of Things" (IoT). After the yearly _John Day presents RINA_
sessions, this was also the time to properly introduce the IRATI
prototype to everyone with a hands-on VM tutorial session, and to
introduce [RINAsim](https://rinasim.omnetpp.org/), an OMNET++ RINA
simulator developed within PRISTINE.

After the workshop, it was time to wrap up IRATI. For an external
observer it may lack impact and show little output in publications,
and it definitely didn't deliver a convincing case for _RINA as an
alternative for TCP/IP_. But despite that, I think the project really
achieved a lot, in terms of bringing for the first time some tools
that can be used to explore RINA, and for the people that worked on
it, an incredible experience and deeps insights into computer networks
in general. This would not have been possible without the enthousiasm
and hard work put in by all those involved, but especially Eduard and
the i2cat team.

As IRINA was wrapping up, a paper on the how the _shim DIF over
Hypervisors_ could be used to [reduce complexity of VM
networking](https://ieeexplore.ieee.org/document/7452280) was
submitted for IEEE COMMAG.

We're approaching the spring of 2015, and IRATI was now officially
over, but there was no time to rest as the clock was ticking on
PRISTINE. The project was now already halfway its anticipated 30-month
runtime, and its first review, somewhere end of 2014, wasn't met with
all cheers, so we had to step up. This was also the period where some
of my other (non-RINA) projects were running out. Up to then, my
personal involvement on RINA had been on (software) design our
components, reviewing the _specs_, and the practical hands-on was in
using the software: deploying it on the testbeds and validating its
functionality.  But now I could finally free up time to help Sander on
the development of the IRATI prototype.

Our main objective for PRISTINE was on _resilient routing_: making
sure the _DIF_ survives underlying link failures. This has been a
long-time research topic in our group, so we pretty much quickly know
_how_ to do it at a conceptual level. But there were three
requirements: first and foremost, it needed _scale_: we needed to be
able to run something that could be called a network, not just 3 or 4
nodes and not just a _couple_ of flows in the network. Second, it
needed _stability_: to measure the recovery time, we needed to send
packets at small but -- more importantly -- steady intervals and
thirdly, we needed measurement _tools_.

As part of IRINA, we developed a basic traffic-generator, which would
be extended for PRISTINE and tailored to suit our needs. Stability was
improving gradually over time. Our real problem was _scale_, to which
the biggest hurdle was the configuration of the IRATI stack. It was a
complete nightmare. Almost anything and everything had to be
preconfigured in _json_. I remember that by that time, Vincenzo had
developed a tool called the _demonstator_ based on tiny buildroot VMs
to create setups for local testing, but this wasn't going to help us
deploy it on the Fed4FIRE testbeds. So Sander developed one of the
first orchestrators for RINA, called the _configurator_ for deploying
IRATI on [emulab](https://www.emulab.net/portal/frontpage.php).

Somewhere around that time, the _one-flow-only-limitation_ of the
_shim DIF over VLAN_ was showing and a _shim DIF over Ethernet Link
Layer Control (LLC)_ was drafted and developed. By mapping endpoints
to LLC Service Access Points (SAPs), this _shim DIF_ could support
parallel flows (data flows and management flows) between the client
IPCPs in the layer above.

With the PRISTINE SDK released as part of "openIRATI" somewhere after
the January workshop a good month prior, there was another influx of
code into the prototype for all the new features
(a.k.a. _policies_). Francesco, who had been managing a lot of the
software integration, was also leaving the RINA projects. This is the
point where I really noticed that Sander and Vincenzo were quickly
losing faith in the future of the IRATI codebase, and the first ideas
of branching off -- or even starting over -- began to emerge.

The next Horizon-2020-proposal deadline was also approaching, so our
struggles at that point also inspired us to propose developing a more
elaborate RINA orchestrator and make deployment and experimentation
with (open)IRATI a much more enjoyable experience. That project,
[ARCFIRE](https://ict-arcfire.eu/) would start in 2016.

Now, we were still focusing on the basics: getting link state routing
running, adding some simple _loop-free alternates_ policy to it, based
on the operation of [IP FRR](https://tools.ietf.org/html/rfc5286) and
running a bunch of flows over that network to measure packet loss when
we break a link. Sander was focusing on the policy design and
implementation, I was going to have a look at the IRATI code for
scaling up the flow counts, which needed non-blocking I/O. I won't go
into the details, but after that short hands-on stint in the IRATI
codebase, I was onboard with Sander to starting looking to options for
a RINA implementation beyond IRATI.

It was now summer 2015, PRISTINE would end in 12 months and the
project was committed to openIRATI, so at least for PRISTINE, we again
had no choice but to plow on. A couple of frustrating months lied
ahead of us, trying to get experimental results out of a prototype
that was nowhere near ready for it, and with a code base that was also
becoming so big and complex that it was impossible to fix for anyone
but the original developers. This is unfortunately the seemingly
inescapable fate of any software project whose development cycle is
heavily stressed by external deadlines, especially deadlines set
within the rigid timeline of a publicly funded research project.

By the end of summer, we were still a long way off the mark in terms
of what we hoped to achieve. The traffic generator tool and
configurator were ready, and the implementation of LFA was as good as
done, so we could deploy the machines for the use case scenarios,
which were about 20 nodes in size, on the testbeds. But the deployment
that actually worked was still limited to a 3-node PoC in a triangle
that showed the traffic getting routed over the two remaining link if
a link got severed.

In the meantime, Vincenzo had started work on his own RINA
implementation, [rlite](https://github.com/vmaffione/rlite), and
Sander and myself started discussing options on a more and more
regular basis on what to do. Should we branch off IRATI and try to
clean it up? Keep only IRATI kernel space and rewrite user space? Hop
on the _rlite_ train? Or just start over entirely? Should we go
user-space entirely or keep parts in-kernel?

In the last semester of 2015, Sander was heading for a 3-month
research stint in Boston to work on routing in RINA with John and the
BU team. By that time, we had ruled out branching off of openIRATI.
Our estimate was that cleaning up the code base would be more work
than starting over. We'd have IRATI as an upstream dependency, and
trying to merge contributions upstream would lead to endless
discussions and further hamper progress for both projects. IRATI was
out.  Continuing on rlite was still a feasible option. Vincenzo was
making progress fast, and we knew he was extremely talented. But we
were also afraid of running into disagreements of how to proceed. In
the meantime, Sander's original research plans in Boston got subverted
by a 'major review' decision on the _shim Hypervisor_ article, putting
priority on getting that accepted and published. When I visited Sander
in Boston at the end of October, we were again assessing the
situation, and agreed that the best decision was to start our own
prototype, to avoid having _too many cooks in the kitchen_.
Development was not part of some funded project, so we were free to
evaluate and scrutinize all design decisions, and we could get
feedback on the RINA mailing lists on our findings. When all
considerations settled, our own RINA implementation was going to be
targeting POSIX and be user space only.

We were confident we could get it done, so we took the gamble. ARCFIRE
was going to start soon, but the first part of the project would be
tool development. Our experimentation contributions to PRISTINE were
planned to wrap up by April -- the project was planned to end in June,
but a 4-month extension pushed it to the end of October. But starting
May, we'd have some time to work on Ouroboros relatively
undisturbed. In the very worst case, if our project went down the
drain, we could still use IRATI or rlite to meet any objectives for
ARCFIRE. We named our new RINA-implementation-to-be _Ouroboros_, the
mythical snake that eats its own tail represented recursion, and also
-- with a touch of imagination -- resembles the operation of a _ring
buffer_.

### ARCFIRE

Another year, another RINA project kick-off, this time it was again in
Barcelona, but this time without a co-located workshop. ARCFIRE (like
IRATI before it) was within the FIRE framework, and the objective was
to get some experiments running with a reasonable number of nodes (on
the order of 100) to demonstrate stability and scale of the prototypes
and also to bring tooling to the RINA community. The project was
coordinated by Sven van der Meer (Ericsson), who had done significant
work on the PRISTINE use cases, and would focus on the impact of RINA
on network management. The industry-inspired use cases were brought by
Diego L&oacute;pez (Telef&oacute;nica), _acteur incontournable_ in the
Network Functions Virtualization (NFV) world. The project was of
course topped off with i2cat, Nextworks, and ourselves, as we were
somewhere in the process of integration into IMEC. The order at hand
for us was to develop an fleshed-out testbed deployment framework for
RINA, which we named [Rumba](https://gitlab.com/arcfire/rumba). (A
rhumba is a bunch of rattlesnakes, and Ouroboros is a snake, and it
was written in Python -- rhumba already existed, and rumba was an
accepted alternate spelling).

In early 2016, the RINA landscape was very different from when we
embarked on IRATI in 2013. There were 2 open source prototypes, IRATI
was the de-facto standard used in EC projects, but Vincenzo's rlite
was also becoming available at the time and would be used in
ARCFIRE. And soon, the development of a third prototype -- _ouroboros_
-- would start. External perception of RINA in the scientific
community had also been shifting, and not in a positive direction. At
the start of the project, we had the position paper with project plans
and outlines, and the papers on the _shims_ showed some ways on how
RINA could be deployed. But other articles trying to demonstrate the
benefits of RINA were -- despite all the efforts and good will of all
people involved -- lacking in quality, mostly due to the limitations
of the software. All these subpar publications did more harm than
good, as the quality of the publications rubbed off on the perceived
merits of the RINA architecture as a whole. We were always feeling
this pressure to publish _something_, _anything_ -- and reviewers were
always looking for a value proposition -- _Why is this better than my
preferred solution?_, _Compare this in depth to my preferred solution_
-- that we simply couldn't support with data at this point in
time. And not for lack of want or a lack of trying. But at least,
ARCFIRE had at 2 years to look forward to, a focused scope and by now,
the team had a lot of experience in the bag. But for the future of
RINA, we knew the pressure was on -- this was a _now or never_ type of
situation.

### Ouroboros

We laid the first stone on Ouroboros on Friday February 12th, 2016. At
that point in time Ouroboros was still planned as a RINA
implementation, so we started from the beginning: an empty git
repository under our cursor, renewed enthousiasm in our minds, fresh
_specs_ -- still warm from the printer and smelling of toner -- in our
hands, and Sanders initial software design and APIs in colored marker
on the whiteboard. Days were long -- we still had work to do on
PRISTINE, mind you -- and evenings were short. I could now imagine the
frustration of the i2cat people, who a couple of years prior were
probably also spending their evenings and nights enthousiastically
coding on IRATI while, for us, IRATI was still a (very interesting)
job rather than a passion. We would feel no such frustrations as we
knew from the onset that the development of Ouroboros was going to be
a two-man job.

While we were spending half our days gathering and compiling results
from our _LFA_ experiments for PRISTINE, which -- fortunately or
unfortunately depending on the way I look at it -- did not result in a
publication, and half our days on the rumba framework, our early
mornings and early evenings were filled with discussions on the RINA
API used in Ouroboros. It was initially based on IRATI. Flow
allocation used source and destination _naming information_ -- 4
objects that the RINA _specs_ (correctly, might I add) say should be
named: Application Process Name, Application Process Instance Id,
Application Entity Name and Application Entity Instance Id. This
_naming information_ as in IRATI, was built into a single structure --
a 4-tuple -- and we were quickly running into a mess, because, while
these names need to be identified, they are not resolved at the same
time, nor in the same place. Putting them in a single struct and
passing that around with NULL values all the time was really ugly. The
naming API in Ouroboros changed quickly over time, initially saving
some state in an _init_ call (the naming information of the current
application, for instance) and later on removing the source naming
information from the flow allocation protocol alltogether, because it
could so easily be filled with fake garbage that one shouldn't rely on
it for anything. The four-tuple was then broken up to pass two 2-tuple
name and instance-id, using one for the Process, the other for the
Entity. But we considered these changes to be just a footnote in the
RINA service definition, -- taste, one could take it or leave it, no
big deal. Little did we know that these small changes were just the
start -- the first notes of a gentle, breezy prelude that was slowly
building towards a fierce, stormy cadenza that would signify the
severance of Ouroboros from RINA almost exactly one year later.

Another such change was with the _register_ function. To be able to
reach a RINA application, you need to register it in the _DIF_. When
we were implementing this, it just struck us that this code was being
repeated over and over again in applications. And just think about it,
_how does an application know which DIFs there are in the system?_.
And if new DIFs are created while the application is running, how do I
feed that information? That's all functionality that would have to be
included in _every_ RINA application. IRATI has this as whole set of
library calls. But we did something rather different. We moved the
registering of applications _outside_ of the applications
themselves. It's _application management_, not _IPC_. Think about how
much simpler this small change makes life for an application
developer, and a network administrator. Think about how it would be if
-- in the IP world -- you could create a socket on port 80 or port 443
_from the shell_, and set options on that socket _from the shell_, and
then tell your kernel that incoming connections on that socket should
be sent to this Apache or that Nginx program _from the shell_, and all
that the Apache or Nginx developers would need to do is call accept()
and read/write/select/epoll etc calls, instead of having to handle
sockets and all their options. That's what the bind() and register()
calls in Ouroboros do for Ouroboros applications: you bind some
program to that name _from the command line_, you register the name in
the layer (equivalent of creating the socket) _from the command line_
, and all the (server) program has to do is call _flow\_accept()_ and
it will receive incoming flows.  It is this change in the RINA API
that inspired us to name our very first public presentation about
Ouroboros, at FOSDEM 2018,
[IPC in 1-2-3](https://archive.fosdem.org/2018/schedule/event/ipc/).

When we tried to propose them to the RINA community, these changes
were not exactly met with cheers. The interactions with that community
was alse beginning to change. RINA was the _specs_. Why are we now
again asking questions about basic things that we implemented in IRATI
years ago? IRATI shows its works. Want to change the _specs_: talk to
John.

We had also implemented our first _shim DIF_, which would allow to run
the Ouroboros prototype over UDP/IPv4. We started with a UDP shim
because there is a POSIX sockets API for UDP. Recall that we were
targeting POSIX, including FreeBSD and MacOS X to make the Ouroboros
prototype more accessible. But programming interfaces into Ethernet,
such as _raw sockets_, were not standard between operating systems, so
we would implement an Ethernet _shim DIF_ later. Now, the Ouroboros
_shim DIF_ stopped being a _shim_ pretty fast. When we were developing
the _shim DIFs_ for IRATI, there was one very important rule: we were
not allowed to add functionality to the protocol we were wrapping with
the RINA API, we could only _map_ functions that were existing in the
(Etherent/UDP) protocol. This -- was the underlying reasoning -- would
show that the protocol/layers in the current internet were
_incomplete_ layers. But that also meant that the functions that were
not present -- the flow allocator in particular -- would need to be
circumvented through manual configuration at the endpoints. We weren't
going to have any of that -- the Ouroboros IPCP daemons all implement
a flow allocator. You may also be wondering why none of the prototypes
have a _shim DIF_ directly over IP. It's perfectly possible! But the
reason is simple: it would use a non-standardized value for the
_protocol_ field in the IP header, and most IP routers simply drop
such packets.

Somewhere around April, we were starting the implementation of a
_normal_ IPCP in Ouroboros, and another RINA component was quickly
becoming a nuisance to me: the _Common Distributed Application
Protocol_ or _CDAP_. While I had no problem with the objectives of
CDAP, I was -- to put it mildly -- not a big fan of the
object-oriented paradigm that was underneath it. Its methods,
_read/write, create/destroy, start/stop_ make sense to many, but just
like the HTTP methods PUT/GET/DELETE/POST/... there is nothing
_fundamental_ about it. It might as well have just one method,
_[execute](http://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html)_.
It's taste, and it definitely wasn't _my_ taste. I found that it only
proved my long-holding observation that for every engineer there were
at least three overengineers. I made a bold prediction to Sander: one
day, we would kick CDAP out of the Ouroboros prototype.

Summer was approaching again. Most of the contributions to PRISTINE
were in, so the ARCFIRE partners could start to focus on that
project. There was a risk: ARCFIRE depended on the Fed4FIRE testbeds,
and Fed4FIRE was ending and its future was not certain. The projected
target API for _rumba_ was
[jFed](https://jfed.ilabt.imec.be/).
To mitigate the risk, we made an inventory of other potential
testbeds, and to accomodate for the wait for the results of the
funding calls, we proposed (and got) an extention to ARCFIRE with 6
months to a 30-month project duration. In the end, Fed4FIRE+ was
funded, ARCFIRE had some breathing space -- after all, we had to fire
on all cylinders to get the best possible results and make a case for
RINA -- and Sander and myself had some extra time to get Ouroboros up
and running.

Sander quickly developed an Ethernet LLC _shim DIF_ based on the UDP
one, and after that, we both moved our focus on the key components in
the _normal IPCP_, implementing the full flow allocator and building
the data transfer protocol (DTP), and the routing and forwarding
functionality. CDAP was getting more and more annoying, but apart from
that, this part of the RINA _specs_ were fairly mature following the
implementation work in IRATI, and the implementation progress was
steady and rather uneventful. For now.

Work on the PRISTINE project was wrapped up, and the final
deliverables were submitted at the end of October. PRISTINE was a
tough project for us, with very little outcomes. Together with Miquel,
I did make some progress with RINA standardization in ISO
JTC1/SC6. But Sander and myself could show few research results, no
published papers where we were the main authors. PRISTINE as a whole
also fell short a bit in its main objectives, the RINA community
hadn't substantially grown, and its research results were still --
from an external vantage point -- mediocre. For us, it was a story of
trying to do too much, too soon. Everyone tried their best, and I
think we achieved what was achieveable given the time and resources we
had. The project definitely had some nice outcomes. Standardization at
least got somewhere, with a project in ISO and also some traction
within the Next Generation Protocols (NGP) group at
[ETSI](www.etsi.org). RINAsim was a nice educational tool, especially
for visualizing the operation of RINA.

Our lack of publication output was also noticed by our direct
superiors at the University, who got more and more anxious. The
relationship deteriorated steadily, we were constantly nagged about
publications, _minimum viable papers_, and the _value proposition_ of
RINA: _killer features_, _killer apps_. For us, the simplicity and
elegance of the design was all we needed as a motivation to
continue. There were some suggestions to build a simulator instead of
a full prototype. My feeling was that a simulator would be
unconvincing to show any _benefits of RINA_ -- I can't express in
words how much I hated that phrase. To prove anything, simulators need
to be validated against the real thing. And there are certain pitfalls
that can only be found in an implementation. This is the reason why I
chose that particular quote at the top of this blog post. Both parties
started to sound like broken records to eachother, every meeting was
devolving into a pointless competition in
who-knows-the-most-workarounds. As the saying goes, arguing with an
engineer is like wrestling a pig in the mud. There wasn't anything
constructive or useful to those interactions, so we stopped giving a
shit -- pardon my French. The Ouroboros prototype was coming along, we
were confident that we knew what we were doing. All we needed was time
to get it done. We'll write a paper on Ouroboros when we had one worth
writing.

By January 2017, we had a minimal working _normal_ IPCP. Sander was
looking into routing, working on a component we called the _graph
adjacency manager_ (GAM). As its name suggest, the GAM would be
responsible for managing links in the network, what would be referred
to as the _network topology_, and would get policies that instruct it
how to maintain the graph based on certain parameters. This component,
however, was short-lived and replaced by an API to connect IPCPs so
the actual layer management logic could be a standalone program
outside of the IPCPs instead of a module inside the IPCPs, which is
far more flexible.

### Ouroboros diverges from RINA

In the meantime, I was implementing and revising _CACEP_, the Common
Application Connection Establishment Phase that was accompanying CDAP
in RINA. Discussions on CACEP between Sander and myself were
interesting and sometimes heated -- whiteboard markers have
experienced flight and sudden deceleration. CDAP was supposed to
support different encoding schemes -- the OSI _presentation layer_. We
were only going to implement Google Protocol Buffers, which was also
used in IRATI, but the support for others should be there. The flow
allocator and the RIB were built on top of our CDAP
implementation. And something was becoming more and more obvious. What
we were implementing -- agreeing on protocol versions, encoding etc --
was something rather universal to all protocols.  Now, you may
remember that the flow allocator is passing something -- the
information needed to connect to a specific Application Entity or
Application Entity Instace -- that was actually only needed after the
flow allocation procedure was basically established.  But after a
while, it was clear to me that this information should be _there_ in
that CACEP part, and was rather universal for all application
connections, not just CDAP. After I presented this to Sander _despair_
over IRC, he actually recognized how this -- to me seemingly small --
change impacted the entire architecture. Now, I will never forget the
exchange, and I actually saved that conversation as a text file. The
date was February 24th, 2017.

```
...
<despair> nice, so then dev.h is even simpler
<despair> ae name is indeed not on the layer boundary
<dstaesse> wait why is dev.h simpler?
<despair> since ae name will be removed there
<dstaesse> no
<dstaesse> would you?
<despair> yes
<despair> nobody likes balls on the line
<despair> it's balls out
...
```

Now, RINA experts will (or should) gasp for air when reading this. It
refers to something that traces back to John's ISO JTC1/SC6 days
working on Open Systems Interconnect (OSI), when there was a heavy
discussion ongoing about the "Application Entity": _where was it
located_? If it was in the _application_, it would be outside of SC6,
which was dealing with networks, if it was in the network, it would be
dealt with _only_ in SC6. It was a turf battle battle between two ISO
groups, and because Application Entities were usually drawn as a set
of circles, and the boundary between the network application as a
line, that battle was internally nicknamed -- boys will be boys -- the
_balls-in, balls-out_ question. If you ever attended one of John's
presentations, he would take a short pause and then continue: "this
was the only time that a major insight came from a turf war": _the
balls were on the line_. The Application Entity needed to be known in
both the application and the network. Alas! Our implementation was
clearly showing that this was not the case. The balls were _above_ the
line, the _network_ (or more precise: the flow allocator) doesn't need
to know _anything_ about application entities! Then and there, Sander
had found a mistake in RINA.

Ouroboros now had a crisp and clear boundary between the flow in a
_DIF_, and any connections using that flow in the layer above. Flow
allocation creates a flow between _Application Instances_ and after
that, a connection phase would create a _connection_ between
_Application Entity Instances_. So roughtly speaking -- without the
OSI terminology -- first the network connects the running programs,
and after that, the programs decide which protocol to use (which can
be implicit). What was in the _specs_ , what the RINA API was actually
doing, was piggybacking these exchanges! Now, we have no issues with
that from an operational perspective: _en effet_, the Ouroboros flow
allocator has a _piggyback API_. But the contents of the piggybacked
information in Ouroboros is _opaque_. And all this has another, even
bigger, implication. One that I would only figure out via another line
of reasoning some time later.

With ARCFIRE rolling along and the implementation of the _rumba_
framework in full swing, Sander was working on the link-state routing
policy for Ouroboros, and I started implementing a _Distributed Hash
Table (DHT)_ that would serve as the directory -- think of the
equivalent of [DNS-SRV](https://en.wikipedia.org/wiki/SRV_record) for
a RINA DIF -- a key-value store mapping _application names_ to
_addresses_ in the layer. The link-state routing component was
something that was really closely related to the Resource Information
Base -- the RIB. That RIB was closely coupled with CDAP. Remember that
prediction that I made about a year prior, somewhere in April 2016? On
September 9th 2017, two weeks before the ARCFIRE RINA hackathon, CDAP
was removed from Ouroboros. I still consider it the most satisfying
[git commit](https://ouroboros.rocks/cgit/ouroboros/commit/?id=45c6615484ffe347654c34decb72ff1ef9bde0f3&h=master)
of my life, removing 3700 lines of utter uselessness -- CDAP got 3 out
of 4 characters right. From that day, Ouroboros could definitely not
be considered a RINA implementation anymore.

It was time to get started on the last big component: DTCP -- the
_Data Transfer Control Protocol_. When implementing this, a couple of
things were again quickly becoming clear. First, the implementation
was proving to be completely independent of DTP. The RINA _specs_, you
may recall, propose a state vector between DTP and DTCP. This solves
the _fragmentation problem_ in TCP: If an IP fragment gets lost, TCP
would resend all fragments. Hence TCP needs to know about the
fragmentation in IP and only retransmit the bytes in that fragment.
But the code was again speaking otherwise. It was basically telling
us: TCP was independent of IP. But fragmentation should be in TCP, and
IP should specify its maximum packet size. Anything else would result
in an intolerable mess.  So that's how we split the _Flow and
Retransmission Control Protocol_ (FRCP) and the _Data Transfer
Protocol_ (DTP) in Ouroboros. Another mistake in RINA.

With FRCP split from DTP in roughly along the same line as TCP was
originally split from IP, we had a new question: where to put FRCP?
RINA has DTCP/DTP in the layer as EFCP. And this resulted in something
that I found rather ugly: a normal layer would "bootstrap" its traffic
(e.g. flow allocator) over its own EFCP implementation to deal with
underlying layers that do not have EFCP (such as the _shim
DIFs_). Well, fair enough I guess. But there is another thing. One
that bugged me even more. RINA has an assumption on the _system_, one
that has to be true. The EFCP implementation -- which is the guarantee
that packets are delivered, and that they are delivered in-order -- is
in the IPCP. But the application process that makes use of the IPCP is
a _different process_. So, in effect, the transfer of data, the IPC,
between the Application Process and the IPCP has to be reliable and
preserve data order _by itself_. RINA has no control over this
part. RINA is not controlling _ALL_ IPC; there is IPC _outside of
RINA_. Another way of seeing it, is like this: If a set of processes
(IPCPs) are needed to provide reliable state synchronization between
two applictions A and B, who is providing reliable state
synchronization between A and the first IPCP? If it's again an IPCP,
that's _infinite_ recursion! Now -- granted -- this is a rather
_academic_ issue, because most (all?) computer hardware does provide
this kind of preserving IPC. However, to me, even theoretical issues
were issues. I wanted Ouroboros to be able to guarantee _ALL_ IPC,
even between its own components, and not make _any_ assumptions! Then,
and only then, it would be universal. Then, and only then, the
_unification of networking and IPC_ would be complete.

The third change in the architecture was the big one. And in
hindsight, we should already have seen that coming with our
realization that the application entity was _above the line_: we moved
FRCP into the application. It would be implemented in the library, not
in the IPCP, as a set of function calls, just like HTTP
libraries. Sander was initially skeptic, because to his taste, if a
single-threaded application uses the library, it should remain
single-threaded. How could it send acknowledgements, restransmit
packets etc? I agreed, but said I was confident that it would work by
running the functionality as part of the IPC calls,
read/write/fevent. And that's how it's implemented now.  All this
meant that Ouroboros layers were not DIFs, and we stopped using that
terminology.

By now, the prototype was running stable enough for us to go _open
source_. We got approval from IMEC to release it to the public under
the GPLv2 / LGPL license, and in early 2018, almost exactly 2 years
after we started the project, we presented the first public version of
Ouroboros at FOSDEM 2018 in Brussels.

But we were still running against the clock. ARCFIRE was soon to end,
and Ouroboros had undergone quite some unanticipated changes that
meant the implementation was facing the reality of [Hofstadter's
Law](https://en.wikipedia.org/wiki/Hofstadter%27s_law).

We were again under pressure to get some publications out; in order to
meet ARCFIRE objectives, and Sander had to meet some publication quota
to finish his PhD. The design of Rumba was interesting enough for a
[paper](https://www.geni.net/), the implementation allowed us to
deploy 3 Recursive Network prototypes (IRATI, rlite and Ouroboros) on
testeds using different APIs: jFed for Fed4Fire and
[GENI](https://www.geni.net/), Emulab for iMinds virtual wall testbed,
QEMU using virtual machines, docker using -- well -- docker
containers, and a local option only for Ouroboros. But we needed more
publications, so for ARCFIRE Sander had implemented Loop-Free
Alternates routing in Ouroboros and was getting some larger-scale
results with them. And I reluctantly started working on a paper on
Ouroboros -- I still felt the time wasn't right, and we first needed
to have a full FRCP implementation and full congestion avoidance to
make a worthwile analysis. By then I long had a feeling that my days
at the university were numbered, it was time to move on, and I was
either leaving after submitting a publication on Ouroboros, or without
a publication on Ouroboros.

We finished the experiments for ARCFIRE, but as with PRISTINE, the
results were not accepted for publication. During the writing of the
paper, a final realization came. We had implemented our link-state
routing a while ago, and it was doing something interesting, akin to
all link-state routing protocols: a link-state packet that came in on
some flow, was sent out on all other flows. It was -- in effect
--doing broadcast. But... OSPF is doing the same. Wait a minute. OSPF
uses a multicast IP address. But of course! Multicast wasn't what it
seemed to be. Multicast was broadcast on a layer, creating a multicast
group was enrollment in that layer. A multicast IP address is a
broadcast layer name! Let that one sink in. Based on the link-state
routing code in the _normal IPCP_, I implemented the broadcast IPCP in
a single night. The _normal IPCP_ was renamed _unicast IPCP_. It had
all fallen into place, the Ouroboros architecture was shaped.

But we had no value proposition to pitch, no value-added feature, no
killer app, no unique selling point. Elegance? I received my notice on
Christmas Eve 2018. Life as a researcher would be over. But what a
ride those last 3 years had been. I'd do the same all over again.

The [paper](https://arxiv.org/abs/2001.09707) was submitted in January
2019. We haven't received any word from it since.

With the GPL license on Ouroboros, Sander and myself decided to
continue to update the prototype and build a bit of a website for
it. So, if you made it all the way to the end of this blog post: thank
you for your interest in the project, that's why we did what we did,
and continue to do what we do.

Stay curious,

Dimitri