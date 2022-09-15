# PX

`px` is a `guix` and `flatpak` "wrapper" that aims to automate certain steps, and offer additional guidance where necessary.

## Introduction

Unless otherwise noted below, all _guix_ commands work as usual:

```bash
px package -s <package>
px system reconfigure /etc/system.scm
```

Let's have a look at _px_ specific commands:

### Update

To run a update, do:

```bash
px update
px update apply # skip prompt after pull
```

This will differentiate between `root` and `user` automatically. This command assumes to find the system configuration at `/etc/system.scm`.

What it does is:

1. `guix pull --disable-authentication --channels=/etc/guix/channels.scm`
2. depending on user:
   - (root) `guix system reconfigure /etc/system.scm; guix package -u`
   - (user) `guix package -u`
3. (user) `flatpak --user --assumeyes --noninteractive update`

### Maintenance

If you're running into issues like GTK font's not displaying, or substitutes not downloading, do:

```bash
px maintenance
```

If in doubt, run this as both user and `root`.

#### Flatpak support

Flatpak support is limited to updating applications installed with `--user` flag. No additional commands are supported.

`px-update` will by default attempt to install Flatpak and Flatpak-application updates.

## Development

Quick test:

```bash
rsync -r --exclude={'venv','git','__pycache','tests','scripts'} ../px root@<IP>:/root
cd px; python3 -m venv venv; source venv/bin/activate; pip3 install .; px update apply
```
