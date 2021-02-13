---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 20
description: >
  How to get up and running with the Ouroboros prototype.
---

### Get Ouroboros

**Packages:**

For ArchLinux users, the easiest way to try Ouroboros is via the [Arch
User Repository](https://aur.archlinux.org/packages/ouroboros-git/),
which will also install all dependencies.

**Source:**

You can clone the [repository](/cgit/ouroboros) over https or
git:

```bash
$ git clone https://ouroboros.rocks/git/ouroboros
$ git clone git://ouroboros.rocks/ouroboros
```

Or download a [snapshot](/cgit/ouroboros/) tarball and extract it.

### System requirements

Ouroboros builds on most POSIX compliant systems. Below you will find
instructions for GNU/Linux, FreeBSD and OS X. On Windows 10, you can
build Ouroboros using the [Linux Subsystem for
Windows](https://docs.microsoft.com/en-us/windows/wsl/install-win10) .

You need [*git*](https://git-scm.com/) to clone the
repository. To build Ouroboros, you need [*cmake*](https://cmake.org/),
[*google protocol buffers*](https://github.com/protobuf-c/protobuf-c)
installed in addition to a C compiler ([*gcc*](https://gcc.gnu.org/) or
[*clang*](https://clang.llvm.org/)) and
[*make*](https://www.gnu.org/software/make/).

Optionally, you can also install
[*libgcrypt*](https://gnupg.org/software/libgcrypt/index.html),
[*libssl*](https://www.openssl.org/),
[*fuse*](https://github.com/libfuse), and *dnsutils*.

On GNU/Linux you will need either libgcrypt (≥ 1.7.0) or libssl if your
[*glibc*](https://www.gnu.org/software/libc/) is older than version
2.25.

On OS X, you will need [homebrew](https://brew.sh/).
[Disable System Integrity Protection](https://developer.apple.com/library/content/documentation/Security/Conceptual/System_Integrity_Protection_Guide/ConfiguringSystemIntegrityProtection/ConfiguringSystemIntegrityProtection.html)
during the
[installation](#install)
and/or
[removal](#remove)
of Ouroboros.

### Install the dependencies

**Debian/Ubuntu Linux:**

```bash
$ apt-get install git protobuf-c-compiler cmake
$ apt-get install libgcrypt20-dev libssl-dev libfuse-dev dnsutils cmake-curses-gui
```

If during the build process cmake complains that the Protobuf C
compiler is required but not found, and you installed the
protobuf-c-compiler package, you will also need this:

```bash
$ apt-get install libprotobuf-c-dev
```

**Arch Linux:**

```bash
$ pacman -S git protobuf-c cmake
$ pacman -S libgcrypt openssl fuse dnsutils
```

**FreeBSD 11:**

```bash
$ pkg install git protobuf-c cmake
$ pkg install libgcrypt openssl fusefs-libs bind-tools
```

**Mac OS X Sierra / High Sierra:**

```bash
$ brew install git protobuf-c cmake
$ brew install libgcrypt openssl
```

### Install Ouroboros

We recommend creating a build directory:

```bash
$ mkdir build && cd build
```

Run cmake providing the path to where you cloned the Ouroboros
repository. Assuming you created the build directory inside the
repository directory, do:

```bash
$ cmake ..
```

Build and install Ouroboros:

```bash
$ sudo make install
```

### Advanced options

Ouroboros can be configured by providing parameters to the cmake
command:

```bash
$ cmake -D<option>=<value> ..
```

Alternatively, after running cmake and before installation, run
[ccmake](https://cmake.org/cmake/help/latest/manual/ccmake.1.html) to
configure Ouroboros:

```bash
$ ccmake .
```

A list of all options can be found [here](/docs/reference/compopt).

### Remove Ouroboros

To uninstall Ouroboros, simply execute the following command from your
build directory:

```bash
$ sudo make uninstall
```

To check if everything is installed correctly, you can now jump into
the [Tutorials](../../tutorials/) section, or you can try to ping this
webhost over ouroboros using the name _ouroboros.rocks.oping_

Our webserver is of course on an IP network, and ouroboros does not
control IP, but it can run over UDP/IP.

To be able to contact our server over ouroboros, you will need to do
some small DNS configuration: to tell the ouroboros UDP system that
the process "ouroboros.rocks.oping" is running on our webserver by
add the line

```
51.38.114.133      1bf2cb4fb361f67a59907ef7d2dc5290
```

to your ```/etc/hosts``` file[^1][^2].

Here are the steps to ping our server over ouroboros:

Run the IRMd:

```bash
$ sudo irmd &
```
Then you will need find your (private) IP address and start an ouroboros UDP
daemon (ipcpd-udp) on that interface:
```bash
$ irm ipcp bootstrap type udp name udp layer udp ip <your local ip address>
```

Now you can ping our server:

```bash
$ oping -n ouroboros.rocks.oping
```

The output from the IRM daemon should look something like this (in DEBUG mode):
```
[dstaesse@heteropoda build]$ sudo irmd --stdout
==01749== irmd(II): Ouroboros IPC Resource Manager daemon started...
==01749== irmd(II): Created IPCP 1781.
==01781== ipcpd/udp(DB): Bootstrapped IPCP over UDP with pid 1781.
==01781== ipcpd/udp(DB): Bound to IP address 192.168.66.233.
==01781== ipcpd/udp(DB): Using port 3435.
==01781== ipcpd/udp(DB): DNS server address is not set.
==01781== ipcpd/ipcp(DB): Locked thread 140321690191424 to CPU 7/8.
==01749== irmd(II): Bootstrapped IPCP 1781 in layer udp.
==01781== ipcpd/ipcp(DB): Locked thread 140321681798720 to CPU 6/8.
==01781== ipcpd/ipcp(DB): Locked thread 140321673406016 to CPU 1/8.
==01781== ipcpd/udp(DB): Allocating flow to 1bf2cb4f.
==01781== ipcpd/udp(DB): Destination UDP ipcp resolved at 51.38.114.133.
==01781== ipcpd/udp(DB): Flow to 51.38.114.133 pending on fd 64.
==01749== irmd(II): Flow on flow_id 0 allocated.
==01781== ipcpd/udp(DB): Flow allocation completed on eids (64, 64).
==01749== irmd(DB): Partial deallocation of flow_id 0 by process 1800.
==01749== irmd(II): Completed deallocation of flow_id 0 by process 1781.
==01781== ipcpd/udp(DB): Flow with fd 64 deallocated.
==01749== irmd(DB): Dead process removed: 1800.
```

If connecting to _ouroboros.rocks.oping_ failed, you are probably
behind a NAT firewall that is actively blocking outbound UDP port
3435.

[^1]: This is the IP address of our server and the MD5 hash of the
      string _ouroboros.rocks.oping_. To check if this is configured
      correctly, you should be able to ping the server with ```ping
      1bf2cb4fb361f67a59907ef7d2dc5290``` from the command line.

[^2]: The ipcpd-udp allows setting up a (private) DDNS server and
      using the Ouroboros ```irm name``` API to populate it, instead
      of requiring each node to manually edit the ```/etc/hosts```
      file. While we technically could also set up such a DNS on our
      server for demo purposes, it is just too likely that it would be
      abused. The Internet is a nasty place.
