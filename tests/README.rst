Tests
=====

Prerequisites
-------------

You should have a reasonably up to date Mac OS X, Ubuntu, Debian, Arch, Fedora or Mac.

On Mac OS X::

On the Mac, you need to have Xcode and brew preinstalled. Then::

    $ xcode-select --install
    $ brew install python python3
    $ pip install --upgrade hitch virtualenv

On Ubuntu/Debian::

    $ sudo apt-get install python3 python-pip python-virtualenv
    $ sudo pip install --upgrade hitch

On Arch::

    $ sudo pacman -Sy python python-virtualenv
    $ sudo pip install --upgrade hitch

On Fedora/RHEL/CentOS::

    $ sudo yum install python3 python-virtualenv python-pip python3
    $ sudo pip install --upgrade hitch

.. note::

    The 'hitch' package (the bootstrapper) is a small python package with no dependencies that can
    be safely installed outside of a virtualenv.


Running tests
-------------

To run these tests, check out this code and run the following commands in this directory::

    $ hitch init

    $ hitch test .

For more information on hitch, see the documentation at https://hitchtest.readthedocs.org/

If the above does not work on your machine, please raise a ticket.
