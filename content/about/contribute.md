---
title: Contact
date:  2019-06-22
draft: false
---

General discussion and support
------------------------------

For general discussion of Ouroboros,
[subscribe](https://www.freelists.org/list/ouroboros) to our mailing
list: [ouroboros@freelists.org](mailto:ouroboros@freelists.org).

For day-to-day discussions, join our IRC chat:
[\#ouroboros](irc://irc.freenode.net/ouroboros).

Contact us on twitter: @ODecentralize

Contributing code
-----------------

Contributions should be sent as patches to the mailing list, using your
real name and real e-mail address.

The git repository contains three branches:

-   master: Contains the most stable version of Ouroboros.
-   testing: Contains tested code but may still contain bugs.
-   be: Contains untested but compiling code.

New development is done against the 'be' branch of the git repository.
The testing and master branches take only bugfixes.

Bug reporting
-------------

Please report all bugs [here](/bugzilla). When reporting a bug, please
do the following:

1.  Provide a description of the bug. How did you get it and which
    version of Ouroboros were you using? Which Operating System are you
    on?
2.  Provide as much technical information as possible (system logs,
    debug traces, \...).
3.  If possible, provide a minimal code example to reproduce the bug.
4.  If you can provide a bugfix, provide it against the HEAD of the most
    stable branch where the bug is present and send the patch to the
    mailing list.

Todo list
---------

We are currently looking for

-   Testing and bugfixing.
-   Integration testing for the build system beyond the "make check"
    unit tests.
-   People that are interested in setting up some nodes to establish a
    global testing layer.
-   Non-blocking flow allocation: Allow specifying a {0, 0} timespec to
    return immediately and use fevent() to know when the flow is ready
    (or allocation failed).
-   Asynchronous IPC over the UNIX sockets. For each command to the
    IRMd, we create a UNIX socket, send the request and wait for the
    response. This could be changed so that there is only a single UNIX
    socket that is used for all messaging. This would simplify parallel
    querying of the IPCPs and speed up flow allocation. The far-future
    option is to ditch UNIX sockets and bootstrap Ouroboros local IPC
    over itself.
-   ECDH-AES encryption using libssl and/or libgcrypt. The goal is to
    support both libraries so that we have a fallback should major bugs
    be discovered in one of them.
-   Customized packet serialization to remove the dependency on Google
    Protocol Buffers. We like GPB, but it's not perfect. Importing
    .proto files may give rise to multiple definitions and we found no
    way to solve that.
-   Caching for the DHT.
-   Cross-compilation to OpenWRT (musl).
-   Ported applications! If you want to add native Ouroboros support for
    your applications, just let us know and we will help you out!
