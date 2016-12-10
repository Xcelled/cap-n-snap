# Cap'n Snap

Cross-platform quick-share utility similar to puush or screencloud.

# Features:

- Written fully in Python for ease of contribution
- Extensible plugin-based architecture
- Designed with cross-platformness in mind

# Eventual Features:

- Screenshot utility
  - Supports several areas (region, whole desktop, screen, and window)
  - Support for many different destinations (Clipboard, imgur, file...)
- Support for other capture sources (clipboard, file)
- Support for other data formats (text, files)
- Command line arguments for scripting/external shortcut managers

# Installing

Use the `install.sh` script to install Cap'n Snap automatically

## Required packages

- Python3
- Qt5
- PyQt5*

*PyQt5 can be obtained from at least two different sources on Ubuntu:

- `sudo apt-get install python3-pyqt5`
- `sudo -H pip3 install PyQt5`

## Python packages

Listed in requirements.txt

`sudo -H pip3 install -r requirements.txt`

### Windows-specific
Hotkeys and window capture require pywin32.

### Linux-specific

To enable hotkeys and window capture, Linux users need the xcffib package from pip.
`sudo apt-get install libxcb-render0-dev libffi-dev && sudo -H pip3 install xcffib`

You also need xpybutil:

1. `git clone https://github.com/BurntSushi/xpybutil.git`
2. `cd xpybutil`
3. `sudo python setup.py install`

# Running

`python3 main.py`

# Rational

Why did we decide to develop Yet Another™ screenshot capturing/upload tool?

We wanted something:
 - Cross Platform
 - Fast
 - Powerful
 - Supporting multiple monitors
 - Easy to contribute to
 - Extensible
 - Capable of more than just images

Of the existing options, Screencloud came closest, but it was slow, only handled images, is written in C++, and was missing some other features besides. Additionally, bug reports and feature requests had been piling up for years on the repo, leading the project to feeling abandoned.

So, we took the best parts of Screencloud and rewrote them to be even better. Then we used this as a base for creating Cap'n Snap.

# TODO:

- UI
- Settings
- Plugins
- Other sources
  - Clipboard
  - File
- Other content types
  - Text
  - Binary
- Upload locations (plugins)
  - imgur
  - (S)Ftp
  - pastebin
  - Screencloud
  - Puush
  - Dropbox
  - File
  - External program
  - others
