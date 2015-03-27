Installation
============

Install from the latest source code::

    sudo pip install git+git://github.com/oozie/pyhumod.git

or::

    git clone https://github.com/oozie/pyhumod.git
    cd pyhumod
	sudo python setup.py install
 
Note: To detect your modem, copy ``conf/humod`` to ``/etc/ppp/peers`` 
otherwise ``Modem.connect()`` will fail.

Next: `getting started <docs/GettingStarted.rst>`_.
------------------
