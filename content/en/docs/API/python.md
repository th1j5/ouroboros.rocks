---
title: "Python API for applications"
author: "Dimitri Staessens"
description: Python
date:  2020-05-17
weight: 20
draft: false
description: >
     Python API
---

The python API allows you to write Ouroboros-native programs in Python
(>=3.4) is available as a separate repository. You need Ouroboros
installed before installing PyOuroboros. To download and install
PyOuroboros(virtual environment recommended):

```sh
$ git clone https://ouroboros.rocks/git/pyouroboros
# Or github mirror:
# git clone https://github.com/dstaesse/pyouroboros
$ cd pyouroboros
./setup.py install
```

## Basic Usage

import the Ouroboros dev library:

```Python
from ouroboros.dev import *
```

On the server side, Accepting a flow:

```Python
f = flow_accept()
```

returns a new allocated flow object.

Client side: Allocating a flow to a certain _name_:

```Python
f = flow_alloc("name")
```
returns a new allocated Flow object.

Broadcast:

```Python
f = flow_join("name")
```

returns a new allocated Flow object to a broadcast layer.

When a flow is not needed anymore, it can be deallocated:

```Python
f.dealloc()
```

To avoid having to call dealloc(), you can also use the with
statement:

```Python
with flow_alloc("dst") as f:
    f.writeline("line")
    print(f.readline())
```

After the flow is deallocated, it is not readable or writeable
anymore.

```Python
f.alloc("name")
```

will allocate a new flow for an existing Flow object.

To read / write from a flow:

```Python
f.read(count)             # read up to _count_ bytes and return bytes
f.readline(count)         # read up to _count_ characters as a string
f.write(buf, count)       # write up to _count_ bytes from buffer
f.writeline(str, count)   # write up to _count_ characters from string
```

## Quality of Service (QoS)

You can specify a QoSSpec for flow allocation.
```Python
    """
    delay:        In ms, default 1000s
    bandwidth:    In bits / s, default 0
    availability: Class of 9s, default 0
    loss:         Packet loss in ppm, default MILLION
    ber:          Bit error rate, errors per billion bits. default BILLION
    in_order:     In-order delivery, enables FRCT, default 0
    max_gap:      Maximum interruption in ms, default MILLION
    cypher_s:     Requested encryption strength in bits
    """
```

For instance,

```Python
qos = QoSSpec(loss=0, cypher_s=256)
f = flow_alloc("name", qos)
```

will create a new flow with FRCP retransmission enabled and encrypted
using a 256-bit ECDHE-AES-SHA3 cypher. The number of encryption
options will further expand as the prototype matures.

## Manipulating flows

A number of methods are currently available for how to interact with
Flow. This will further expand as the prototype matures.

```Python
f.set_snd_timeout(0.5) # set timeout for blocking write
f.set_rcv_timeout(1.0) # set timeout for blocking read
f.get_snd_timeout()    # get timeout for blocking write
f.get_rcv_timeout()    # get timeout for blocking read
f.get_qos()            # get the QoSSpec for this flow
f.get_rx_queue_len()   # get the number of packets in the rx buffer
f.get_tx_queue_len()   # get the number of packets in the tx buffer
f.set_flags(flags)     # set a number of flags for this flow
f.get_flags()          # get the flags for this flow
```

The following flags are specified as an enum FlowProperties:

```Python
class FlowProperties(IntFlag):
    ReadOnly
    WriteOnly
    ReadWrite
    Down
    NonBlockingRead
    NonBlockingWrite
    NonBlocking
    NoPartialRead
    NoPartialWrite
```

See the Ouroboros fccntl documentation for more details.

```shell
man fccntl
```

## Event API

Multiple flows can be monitored for activity in parallel using a
FlowSet and FEventQueue objects.

FlowSets allow grouping a bunch of Flow objects together to listen for
activity. It can be constructed with an optional list of Flows, or
flows can be added or removed using the following methods:

```Python
set = FlowSet() # create a flow set,
set.add(f)      # add a Flow 'f' to this set
set.remove(f)   # remove a Flow 'f' from this set
set.zero()      # remove all Flows in this set
```

An FEventQueue stores pending events on flows.

The event types are defined as follows:
```Python
class FEventType(IntFlag):
    FlowPkt
    FlowDown
    FlowUp
    FlowAlloc
    FlowDealloc
```

and can be obtained by calling the next method:

```Python
    f, t = fq.next() # Return active flow 'f' and type of event 't'
```

An FEventQueue is populated from a FlowSet.

```Python
fq = FEventQueue()            # Create an eventqueue
set = FlowSet([f1, f2, f3])   # Create a new set with a couple of Flow objects
set.wait(fq, timeo=1.0)       # Wait for 1 second or until event
while f, t = fq.next():
    if t == FEventType.FlowPkt:
        msg = f.readline()
    ...
set.destroy()
```

A flow_set must be destroyed when it goes out of scope.
To avoid having to call destroy, Python's with statement can be used:

```Python
fq = FEventQueue()
with FlowSet([f]) as fs:
    fs.wait(fq)
f2, t = fq.next()
if t == FEventType.FlowPkt:
    line = f2.readline()
```

## Examples

Some example code is in the repository's
[examples](https://ouroboros.rocks/cgit/pyouroboros/tree/examples/) folder.

The following example is a clone of the oecho program in Python. The
client opens a flow to oecho and sends a brief message. The server
will echo this message back to the client.

```Python
from ouroboros.dev import *
import argparse


def client():
    with flow_alloc("oecho") as f:
        f.writeline("Hello, PyOuroboros!")
        print(f.readline())


def server():
    print("Starting the server.")
    while True:
        with flow_accept() as f:
            print("New flow.")
            line = f.readline()
            print("Message from client is " + line)
            f.writeline(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple echo client/server')
    parser.add_argument('-l', '--listen', help='run as a server', action='store_true')
    args = parser.parse_args()
    server() if args.listen is True else client()
```

Running it is just the same as the binary program, register the name
"oecho", bind the server to "oecho" (you can even bind both the C and
Python programs at the same time), and allocating a flow should reach
the server. For a local layer

```bash
$ irm i b t local n local l local
$ irm n r oecho l local
$ irm b prog ./oechy.py n oecho
$ ./oecho.py -l &
# or:
# python oecho.py -l
$ ./oechy.py
```

## License
pyOuorboros is LGPLv2.1. The examples are 3-clause BSD.