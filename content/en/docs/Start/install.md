---
title: "Install from source"
author: "Dimitri Staessens"
date:  2019-07-23
weight: 30
draft: false
description: >
    Installation instructions.
---

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