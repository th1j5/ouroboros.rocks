---
title: "ioq3"
author: "Dimitri Staessens"
date: 2019-10-06
draft: false
description: >
    Added support for Ouroboros to the ioq3 game engine.
---


As a demo, we have added Ouroboros support to the
[ioq3](https://github.com/ioquake/ioq3) game engine. ioq3 is a fork of
ID software's [Quake III Arena GPL Source
Release](https://github.com/id-Software/Quake-III-Arena). The port is
available as a [patch](/patches/ouroboros-ioq3.patch). The servers
currently only work in dedicated mode (there is no way yet to start a
server from the client).

To get the demo, first get the latest ioq3 sources:

```bash
$ git clone https://github.com/ioquake/ioq3.git
$ cd ioq3
```

Copy the patch via the link above, or get it via wget:

```bash
$ wget https://ouroboros.rocks/patches/ouroboros-ioq3.patch
```

Apply the patch to the ioq3 code:

```bash
$ git apply ouroboros-ioq3.patch
```

With Ouroboros installed, build the ioq3 project in standalone mode:

```bash
$ STANDALONE=1 make
```

You may need to install some dependencies like SDL2, see the [ioq3
documentation](http://wiki.ioquake3.org/Building_ioquake3).

The ioq3 project only supplies the game engine. To play Quake III Arena,
you need the original game files and a valid key. Various open source
games make use of the engine. We wil detail the procedure for running
OpenArena in your ioq3 build directory.

Go to your build directory:

```bash
$ cd build/<release_dir>/
```

To run OpenArena, you only need to the game files. First download the
zip archive (openarena-0.8.8.zip) from the [OpenArena
website](http://www.openarena.ws) (or via wget) and then extract the
baseoa folder:

```bash
$ wget http://www.openarena.ws/request.php?4 -O openarena-0.8.8.zip
$ unzip -j openarena-0.8.8.zip 'openarena-0.8.8/baseoa/*' -d
./baseoa
```

Make sure you have a local Ouroboros layer running in your system (see
[this tutorial](/tutorial-1/)).

To test the game, start a server (replace <arch> with the correct
architecture extension for your machine, eg x86_64):

```bash
$ ./ioq3ded.<arch> +set com_basegame baseoa +map aggressor
```

Bind the pid of the server to a name and register it in the local layer:

```bash
$ irm bind proc <pid> name my.ioq3.server
$ irm name reg my.ioq3.server layer <your_local_layer>
```

To connect, start a client (in a different terminal):

```bash
$ ./ioquake3.<arch> +set com_basegame baseoa
```

When the client starts, go to the console by typing ~ (tilde) and enter
the following command

```bash
connect -O my.ioq3.server
```

The client should now connect to the ioq3 dedicated server over
Ouroboros. Register the name in non-local layers to connect from other
machines. Happy Fragging!
