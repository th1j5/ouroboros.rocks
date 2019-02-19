---
title: "Extra"
draft: false
menu: "main"
menu:
  main:
    weight: 40
---

Raptor
------

Raptor is a proof-of-concept FPGA demonstrator for running Ouroboros
directly over Ethernet PHY (OSI L1). For this, it uses the [NetFPGA
10G](http://netfpga.org/site/#/systems/3netfpga-10g/details/) platform,
which has Broadcom AEL2005 PHY 10G Ethernet devices. Raptor is
point-to-point and does not use addresses. It is available for Linux
only and support is minimal. If you are interested in trying it out,
please contact us via the ouroboros mailing list or the IRC channel.

You can clone the [raptor repository](/cgit/raptor/):

```
$ git clone http://ouroboros.rocks/git/raptor
$ git clone https://ouroboros.rocks/git/raptor
$ git clone git://ouroboros.rocks/raptor
```

There are two directories. The *linux* directory contains the kernel
module, the *netfpga10g* directory contains the files necessary to build
the FPGA design.

To build and install the kernel module:

```
$ make
$ sudo make install
```

You can now load/unload the raptor kernel module:

```
$ sudo modprobe raptor
$ sudo rmmod raptor
```

To uninstall the module:

```
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

ioq3
----

As a demo, we have added Ouroboros support to the
[ioq3](https://github.com/ioquake/ioq3) game engine. ioq3 is a fork of
ID software's [Quake III Arena GPL Source
Release](https://github.com/id-Software/Quake-III-Arena). The port is
available as a [patch](/patches/ouroboros-ioq3.patch). The servers
currently only work in dedicated mode (there is no way yet to start a
server from the client).

To get the demo, first get the latest ioq3 sources:

```
$ git clone https://github.com/ioquake/ioq3.git
$ cd ioq3
```

Copy the patch via the link above, or get it via wget:

```
$ wget https://ouroboros.rocks/patches/ouroboros-ioq3.patch
```

Apply the patch to the ioq3 code:

```
$ git apply ouroboros-ioq3.patch
```

With Ouroboros installed, build the ioq3 project in standalone mode:

```
$ STANDALONE=1 make
```

You may need to install some dependencies like SDL2, see the [ioq3
documentation](http://wiki.ioquake3.org/Building_ioquake3).

The ioq3 project only supplies the game engine. To play Quake III Arena,
you need the original game files and a valid key. Various open source
games make use of the engine. We wil detail the procedure for running
OpenArena in your ioq3 build directory.

Go to your build directory:

```
$ cd build/<release_dir>/
```

To run OpenArena, you only need to the game files. First download the
zip archive (openarena-0.8.8.zip) from the [OpenArena
website](http://www.openarena.ws) (or via wget) and then extract the
baseoa folder:

```
$ wget http://www.openarena.ws/request.php?4 -O openarena-0.8.8.zip
$ unzip -j openarena-0.8.8.zip 'openarena-0.8.8/baseoa/*' -d
./baseoa
```

Make sure you have a local Ouroboros layer running in your system (see
[this](/tutorial-1/).

To test the game, start a server (replace <arch> with the correct
architecture extension for your machine, eg x86_64):

```
$ ./ioq3ded.<arch> +set com_basegame baseoa +map aggressor
```

Bind the pid of the server to a name and register it in the local layer:

```
$ irm bind proc <pid> name my.ioq3.server
$ irm reg name my.ioq3.server layer <your_local_layer>
```

To connect, start a client (in a different terminal):

```
$ ./ioquake3.<arch> +set com_basegame baseoa
```

When the client starts, go to the console by typing ~ (tilde) and enter
the following command

```
connect -O my.ioq3.server
```

The client should now connect to the ioq3 dedicated server over
Ouroboros. Register the name in non-local layers to connect from other
machines. Happy Fragging!

Rumba
-----

Rumba is an experimentation framework for deploying recursive network
experiments in various network testbeds. It is developed as part of the
[ARCFIRE](http://ict-arcfire.eu) project, and available on
[gitlab](https://gitlab.com/arcfire/rumba) .
