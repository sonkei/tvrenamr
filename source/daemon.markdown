---
layout: default
body_id: daemon
---

The Tv Renamr Daemon project was started to create an automated version of the utility that can run as a dameon/service to watch a folder and then rename files as they are placed in the folder.

The idea originated from seeing how the BitTorrent client [Deluge](http://deluge-torrent.org) used watch folders to add new torrents when torrent files were dropped in a specified directory and the ability of the XBox Media Centre ([XBMC](http://xbmc.org)) to know when new files have been added to the index.

The idea was to have a daemon running on the completed directory of a torrent client that called Tv Renamr when a new file was detected

Coupled with the config file this adds a new dimension to the project. Rather than just being setup to run for freshly downloaded files, a user can now run the daemon with all the options for various shows in the config file and also use it as a faux-GUI interface. Files can be dropped into the specified folder and renamed at the user's will.

There are three different versions of the daemon for different operating systems:

* Linux: tvrenamrd
* OSX: tvrenamr-launchd
* Windows: tvrenamr-service


## Installation
### PyPi


### GitHub
Download your choice of daemon:

* [Linux](http://github.com/ghickman/tvrenamrd)
* [OSX](http://github.com/ghickman/tvrenamr-launchd)
* [Windows](http://github.com/ghickman/tvrenamr-service)

You'll then need to build the project to install it so run:
    python setup.py clean -a
    python setup.py build

## Usage
The daemon is a wrapper for the main tvrenamr project so any config is done in the config.yml of your tvrenamr installation. For more info consult [here](/usage.html#config).

### Linux
In your shell of choice

Start: `tvrd-start <watch directory>`

Stop: `tvrd-stop`

### OSX
Open Terminal.app from Applications/Utilities

Start: `launchd load com.TvRenamr.plist`

Stop:  `launchd load com.TvRenamr.plist`

### Windows
