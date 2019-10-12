---
title: "Writing your first Ouroboros C program"
author: "Dimitri Staessens"
date:  2019-08-31
draft: false
description: >
    A simple Hello World! example.
---

Here we guide you to write your first ouroboros program. It will use
the basic Ouroboros IPC Application Programming Interface. It will has
a client and a server that send a small "Hello World!" message from
the client to the server.

We will explain how to connect two applications. The server application
uses the flow_accept() call to accept incoming connections and the
client uses the flow_alloc() call to connect to the server. The
flow_accept and flow_alloc call have the following definitions:

```C
int flow_accept(qosspec_t * qs, const struct timespec * timeo);
int flow_alloc(const char * dst, qosspec_t * qs, const struct timespec * timeo);
```

On the server side, the flow_accept() call is a blocking call that will
wait for an incoming flow from a client. On the client side, the
flow_alloc() call is a blocking call that allocates a flow to *dst*.
Both calls return an non-negative integer number describing a "flow
descriptor", which is very similar to a file descriptor. On error, they
will return a negative error code. (See the [man
page](/man/man3/flow_alloc.html) for all details). If the *timeo*
parameter supplied is NULL, the calls will block indefinitely, otherwise
flow_alloc() will return -ETIMEDOUT when the time interval provided by
*timeo* expires. We are working on implementing non-blocking versions if
the provided *timeo* is 0.

After the flow is allocated, the flow_read() and flow_write() calls
are used to read from the flow descriptor. They operate just like the
read() and write() POSIX calls. The default behaviour is that these
calls will block. To release the resource, the flow can be deallocated
using flow_dealloc.

```C
ssize_t flow_write(int fd, const void * buf, size_t count);
ssize_t flow_read(int fd, void * buf, size_t count); int
flow_dealloc(int fd);
```

So a very simple application would just need a couple of lines of code
for both the server and the client:

```C
/* server side */
char msg[BUF_LEN];
int fd = flow_accept(NULL, NULL);
flow_read(fd, msg, BUF_LEN);
flow_dealloc(fd);

/* client side */
char * msg = "Hello World!";
int fd = flow_alloc("server", NULL, NULL);
flow_write(fd, msg, strlen(msg));
flow_dealloc(fd);
```

The full code for an example is the
[oecho](/cgit/ouroboros/tree/src/tools/oecho/oecho.c)
application in the tools directory.

To compile your C program from the command line, you have to link
-louroboros-dev. For instance, in the Ouroboros repository, you can do

```bash
cd src/tools/oecho
gcc -louroboros-dev oecho.c -o oecho
```