---
title: "Requirements"
author: "Dimitri Staessens"
date:  2019-07-23
weight: 10
draft: false
description: >
    System requirements and software dependencies.
---

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
[*fuse*](https://github.com/libfuse), *dnsutils* and
[*swig*](http://swig.org/).

On GNU/Linux you will need either libgcrypt (≥ 1.7.0) or libssl if your
[*glibc*](https://www.gnu.org/software/libc/) is older than version
2.25.

On OS X, you will need [homebrew](https://brew.sh/). [Disable System
Integrity
Protection](https://developer.apple.com/library/content/documentation/Security/Conceptual/System_Integrity_Protection_Guide/ConfiguringSystemIntegrityProtection/ConfiguringSystemIntegrityProtection.html)
during the [installation](#install) and/or [removal](#remove) of
Ouroboros.

### Install the dependencies

**Debian/Ubuntu Linux:**

```bash
$ apt-get install git protobuf-c-compiler cmake
$ apt-get install libgcrypt20-dev libssl-dev libfuse-dev dnsutils swig cmake-curses-gui
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
$ pacman -S libgcrypt openssl fuse dnsutils swig
```

**FreeBSD 11:**

```bash
$ pkg install git protobuf-c cmake
$ pkg install libgcrypt openssl fusefs-libs bind-tools swig
```

**Mac OS X Sierra / High Sierra:**

```bash
$ brew install git protobuf-c cmake
$ brew install libgcrypt openssl swig
```