---
title: "Install Ouroboros"
draft: false
---

We recommend creating a build directory:

```
$ mkdir build && cd build
```

Run cmake providing the path to where you cloned the Ouroboros
repository. Assuming you created the build directory inside the
repository directory, do:

```
$ cmake ..
```

Build and install Ouroboros:

```
$ sudo make install
```

### Advanced options

Ouroboros can be configured by providing parameters to the cmake
command:

```
$ cmake -D<option>=<value> ..
```

Alternatively, after running cmake and before installation, run
[ccmake](https://cmake.org/cmake/help/v3.0/manual/ccmake.1.html) to
configure Ouroboros:

```
$ ccmake .
```

A list of all options can be found [here](/compopt).

### Remove Ouroboros

To uninstall Ouroboros, simply execute the following command from your
build directory:

```
$ sudo make uninstall
```