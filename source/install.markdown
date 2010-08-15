---
layout: default
body_id: install
---

Tv Renamr relies on having a .tvrenamr folder in your home directory so first create one of those. This is for the configuration file and where your logs will live.

Now choose an installation method from below:

## PyPi 

[PyPi](http://pypi.python.org) is the Python Package index and providing you have the Python [setup tools](http://) installed you can install Tv Renamr from there by running: `easy_install tvrenamr`.


## Github

Tv Renamr's source code is hosted on [Github](http://github.com/ghickman/tvrenamr) (much like this site!) where you can git clone or download it.

Once you have the files you'll need to build them with:
    python setup.py clean -a
    python setup.py build

Install the project with:
    python setup.py install
*Note:* you may need to run as an admin/sudo to run install.


## That's It!

If all went well (nothing exploding is usually a good indication of this) Tv Renamr should now be installed to your system.

You can then run it with the command `tvr [options] <FILE/DIR>`.

For more details on how to use Tv Renamr, visit the [usage](/usage.html) page.