---
title: "Contribution Guidelines"
linkTitle: "Contribution Guidelines"
date:  2020-01-18
weight: 110
description: >
  How to contribute to Ouroboros.
---

### Communication

There are 2 ways that will be used to communicate: The mailing list
(ouroboros@freelists.org) will be used for almost everything except
for day-to-day chat. For that we use a public slack channel
[slack](https://odecentralize.slack.com) (invite link in footer)
bridged to a
[matrix space](https://matrix.to/#/#ODecentralize:matrix.org).
Use whatever login name you desire.

Introduce yourself, use common sense and be polite!

### Coding guidelines

The coding guidelines of the main Ouroboros stack are similar as those
of the Linux kernel
(https://www.kernel.org/doc/html/latest/process/coding-style.html) with the
following exceptions:

- Soft tabs are to be used instead of hard tabs
- A space is to be inserted between a pointer and its object name upon
  declaration or in function signatures. Example:

   ```C
   int * a;
   ```

instead of

   ```C
   int *a;
   ```

- Don't explicitly cast malloc, but do

   ```C
   ptr = malloc(sizeof(*ptr) * len);
   ```

- When checking for invalid pointers use

   ```C
   if (ptr == NULL)
   ```

instead of

   ```C
   if (!ptr)
   ```

When in doubt, just browse the code a bit. It's not rocket science.

### Development workflow

Git is used as a version tooling for the code. Releases are identified
through a git tag by a number MAJOR.MICRO.PATCHLEVEL. Incrementing
MAJOR is done to indicate a big step ahead in terms of features; it is
discussed when new features are planned. Incrementing MICRO is done
when APIs/ABIs are not necessarily compatible. The PATCHLEVEL is
incremented when an urgent bugfix is incorporated.

#### Repository structure

The main git repository can be found at:
https://ouroboros.rocks/cgit/ouroboros

It contains the following branches:

- master: Contains the most stable versions of Ouroboros.
- testing: Contains tested code but may still contain bugs.
- be: Contains untested but compiling code.

All new contributions are integrated into 'be' through patches sent to
the mailing list. Once a version of 'be' is tested enough, it is
merged into 'testing'. When a 'testing' version is considered stable
enough, it is merged into 'master'. Users should ALWAYS use master
unless told otherwise.

#### Contributions

Providing contributions can be done by sending git patches to the
mailing list (ouroboros@freelists.org).

New development is ALWAYS done against the 'be' branch of the main git
repository. Contributions are always made using your real name and
real e-mail address.

#### Commit messages

A commit message should follow these 10 simple rules, based on
(http://chris.beams.io/posts/git-commit/)

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Precede the subject line by indicating the component where changes were made
7. Wrap the body at 72 characters
8. Use the body to explain what and why vs. how
9. If the commit addresses a bug, reference it in the body
10. Sign off your commits using the signoff feature in git

#### Bugs

Bugs are reported through the Bugzilla issue tracker
(https://ouroboros.rocks/bugzilla/). The process of reporting
a bug is the following:

1. Provide a description of the bug
2. Provide system logs
3. Provide a minimal code example to reproduce the bug if possible
4. Check if the bug is still present in the be branch
5. Sync with the HEAD of the most stable branch where the bug is present
6. Provide a bug fix if you can, send a patch to the mailing list

Note that the first 2 steps are always required by the bug
reporter.

### New features

New features can be always be requested through the mailing list. They
will be taken into account when a next version of the prototype is
discussed.

We're a small community. Rome wasn't built in a day.
