# PX

`px` is a `guix` and `flatpak` overlay that aims to automate certain steps, and offer additional guidance where necessary.

## Introduction

Unless otherwise noted below, all _guix_ commands work as usual:

```
px package -s <package>
px system reconfigure /etc/system.scm
```

Let's have a look at _px_ specific commands:

### Update

To run a update, do:

```
px update
px update apply # skip prompt after pull
```

This will differentiate between `root` and `user` automatically. This command assumes to find the system configuration at `/etc/system.scm`.

What it does is:

1. `guix pull --disable-authentication`
2. depending on user:
   - (root) `guix system reconfigure /etc/system.scm`
   - (else) `guix package -u`
3. (else) `flatpak --user --assumeyes --noninteractive update`

#### Flatpak support

Flatpak support is limited to updating applications installed with `--user` flag. No additional commands are supported.

`px-update` will by default attempt to install Flatpak and Flatpak-application updates.