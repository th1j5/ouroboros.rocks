---
title: "Raptor"
author: "Dimitri Staessens"
date: 2019-10-06
draft: false
description: >
    Proof-of-concept FPGA demonstrator for Ouroboros.
---

Raptor is a proof-of-concept FPGA demonstrator for running Ouroboros
directly over Ethernet PHY (OSI L1). For this, it uses the [NetFPGA
10G](http://netfpga.org/site/#/systems/3netfpga-10g/details/) platform,
which has Broadcom AEL2005 PHY 10G Ethernet devices. Raptor is
point-to-point and does not use addresses. It is available for Linux
only and support is minimal. If you are interested in trying it out,
please contact us via the ouroboros mailing list or the IRC channel.

You can clone the [raptor repository](/cgit/raptor/):

```bash
$ git clone https://ouroboros.rocks/git/raptor
$ git clone git://ouroboros.rocks/raptor
```

There are two directories. The *linux* directory contains the kernel
module, the *netfpga10g* directory contains the files necessary to build
the FPGA design.

To build and install the kernel module:

```bash
$ make
$ sudo make install
```

You can now load/unload the raptor kernel module:

```bash
$ sudo modprobe raptor
$ sudo rmmod raptor
```

To uninstall the module:

```bash
$ sudo make uninstall
```

You will need to get some cores (such as PCIe and XAUI) from Xilinx in
order to build this project using the provided tcl script. Detailed
instructions on how to build the NetFPGA project under construction.

Raptor is integrated in Ouroboros and the raptor IPCP will be built if
the kernel module is installed in the default location.

Raptor was developed as part of the master thesis (in Dutch)
"Implementatie van de Recursive Internet Architecture op een FPGA
platform" by Alexander D'hoore. The kernel module is licensed under
the [GNU Public License (GPL) version
2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html). The NetFPGA
design is available under the [GNU Lesser Public License (LGPL) version
2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).
