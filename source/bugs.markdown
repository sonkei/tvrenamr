---
layout: default
body_id: bugs
---
# Known Issues
Tv Renamr currently has a few known issues that might affect how you rename your tv shows.

## Illegal File System Characters
All filesystems have a black list of characters that they don't allow. The most obvious one of these for a tv show file is the colon. Python is sympathetic to this and by default will replace those characters with a backslash.

Personally I'm not a fan of the paltry backslash, especially when it will give you files that look like poor 24: 24 - 101 - Day 1 - 12\00 A.M.-1\00 A.M..avi. By default Tv Renamr is set to replace the dirty backslash in your filenames with a comma, it's not perfect but it's a start.

You can go one step further than this though, using the config file, and specify both a global replacement for the backslash and even a show specific one.


## Multi-episode Files
Files that contain more than one episode are currently not supported. While they are on the list of things to fix, they are not very high up due to the relatively infrequent nature of them occurring and that I've not found enough to get made at myself for not fixing them!

Currently Tv Renamr will rename them to the first show in the file name. So if you have a show that goes something this: show.s01e01&s01e02.avi then it will get renamed to 


# Reporting bugs
The [Lighthouse](http://tvrenamr.lighthouseapp.com/projects/53048-tvrenamr-core/overview) site for Tv Renamr is the number one place to report bugs.

However you can also contact me directly on [Github](http://github.com/ghickman), [Twitter](http://twitter.com/ghickman) or by email: george [AT] ghickman -DOT- co -DOT uk