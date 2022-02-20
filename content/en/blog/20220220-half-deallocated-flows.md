---
date: 2022-02-20
title: "Half-deallocated flows"
linkTitle: "Flows vs connections/sockets (2)"
author: Dimitri Staessens
---

A few weeks back I wrote a post about Ouroboros flows vs TCP
connections, and how "half-closed connections" should be handled in
the Ouroboros architecture. This was very basic functionality that was
sorely missing. You can refresh your memory on that
[post](/blog/2021/12/29/behaviour-of-ouroboros-flows-vs-udp-sockets-and-tcp-connections/sockets/)
if needed.

Today I wrapped up an initial implementation without whistles and
bells (fixed timeout at 120s), and I'll share a bit with you how it
works.

The modified oecho application looks as follows (decluttered). On the
server side, we have:

```C
       while (true) {
                fd = flow_accept(NULL, NULL);

                printf("New flow.\n");

                count = flow_read(fd, &buf, BUF_SIZE);

                printf("Message from client is %.*s.\n", (int) count, buf);

                flow_write(fd, buf, count);

                flow_dealloc(fd);
        }

        return 0;
```
And on the client side, we have:

```C
        char *  message = "Client says hi!";
        qosspec_t qs = qos_raw;

        fd = flow_alloc("oecho", &qs, NULL);

        flow_write(fd, message, strlen(message) + 1);

        count = flow_read(fd, buf, BUF_SIZE);

        printf("Server replied with %.*s\n", (int) count, buf);

        /* The server has deallocated the flow, this read should fail. */
        count = flow_read(fd, buf, BUF_SIZE);
        if (count < 0) {
                printf("Failed to read packet: %zd.\n", count);
                flow_dealloc(fd);
                return -1;
        }

        flow_dealloc(fd);

```

Previously, the second flow_read would hang forever, (unless a timeout
was set on the read operation using fccntl, which we didn't do).

Now the IPCP will detect the peer as gone, and mark the flow as DOWN
to the application.

```
[dstaesse@heteropoda website]$ oecho
Server replied with Client says hi!
Failed to read packet: -1005.
```

We can see this in a simple test case over the
loopback adapter:

```
feb 20 18:50:06 heteropoda irmd[70364]: irmd: Flow on flow_id 13 allocated.
feb 20 18:50:06 heteropoda irmd[70364]: irmd: Flow on flow_id 12 allocated.
feb 20 18:50:06 heteropoda irmd[70364]: irmd: Partial deallocation of flow_id 13 by process 70597.
feb 20 18:50:06 heteropoda irmd[70364]: irmd: Completed deallocation of flow_id 13 by process 70534.
feb 20 18:50:06 heteropoda irmd[70364]: irmd: New instance (70597) of oecho added.
feb 20 18:50:06 heteropoda irmd[70364]: irmd: This process accepts flows for:
feb 20 18:50:06 heteropoda irmd[70364]: irmd:         oecho
feb 20 18:52:13 heteropoda ipcpd-unicast[70405]: flow-allocator: Flow 66 down: Unresponsive peer.
feb 20 18:52:13 heteropoda irmd[70364]: irmd: Partial deallocation of flow_id 12 by process 70598.
feb 20 18:52:13 heteropoda irmd[70364]: irmd: Completed deallocation of flow_id 12 by process 70405.
feb 20 18:52:13 heteropoda irmd[70364]: irmd: Dead process removed: 70598.
```

In the first 2 lines, the flow between the oecho client and server is
allocated, creating a flow endpoint 13 at the server side, and flow
endpoint id 12 at the client side. Then the server calls flow_dealloc
and the flow is deallocated (lines 3 and 4). The server re-enters its
accept loop, and it's ready for new incoming flow requests (lines
5-7). About 2 minutes later, the flow liveness mechanism in the flow
allocator at the client side detects that the remote is gone, and
flags the flow as DOWN (line 8).  After that, the client's read call
terminates and the client calls dealloc, after which the flow is
deallocated (lines 9-10) and the client exits (last line).

Note that works independent of the QoS of the flow. I'll add a
configurable timeout soon, and it will work at any scale, from seconds
to years. I thought seconds should be small enough, but if anyone
makes a good case for timing out flows at sub-second timescales, I'll
happily enable it.

Stay curious,

Dimitri