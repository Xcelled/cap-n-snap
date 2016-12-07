# Cap'n Snap

Cross-platform quick-share utility similar to puush or screencloud.

#Features:

- lol I take screenshots

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
Hotkeys require pywin32.

### Linux-specific

To enable hotkeys, Linux users need the python-xlib package from pip.
`sudo -H pip3 install python-xlib`

Alternatively, you can use [xcffib](https://github.com/tych0/xcffib).

# Running

`python3 main.py`

#TODO:

- UI
- Settings
- Plugins
- Other sources (via plugins?)
  - Clipboard
- Other content types (via plugins?)
  - Text
  - Binary
- Upload locations (plugins)
  - imgur
  - pastebin?
  - Screencloud (for the lolz)
  - others