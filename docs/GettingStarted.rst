Getting Started
===============

Installation
------------
The installation of the package takes place in four steps: downloading the source, extracting it and system-wide installation on the elevated priviledges. The following should work for most Unix derivatives.
::
    $ wget https://github.com/oozie/pyhumod/archive/master.zip
    $ unzip master.zip
    $ cd download
    $ sudo python setup.py install

Please note this package requires `pySerial <http://pyserial.sourceforge.net>`_ and detect module uses `dbus-python <http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html>`_ to talk to HAL. pySerial is a required dependency, dbus-python can be installed if you want to take advantage of the humod.detect module. 

Usage Guide
-----------
Once installed, you can write your own scripts or this package from an interpreter. In both cases Python requires you to import humod first. 

Writing your own scripts
~~~~~~~~~~~~~~~~~~~~~~~~
An example script could look as follows:

    #!/usr/bin/env python
    
    import humod
    m = humod.Modem()
    model = m.show_model()
    print('You are using %s 3G modem.' % model)

Using a Python interpreter
~~~~~~~~~~~~~~~~~~~~~~~~~~
Most of the examples here are run from the standard python interpreter, but you are welcome to use ipython.
::
    $ python3
    ...
    >>> import humod
    >>> mod = humod.Modem('/dev/ttyUSB0', '/dev/ttyUSB1')
    >>> mod.show_model()
    >>> 'E270'

Instantiating a ``Modem()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The key task that must be accomplished every time you want to talk to the modem is to instantiate a Modem() class. In order for instatiation to suceed you must know where the required data and control ports are. For most Linux users the data port will be located in ``/dev/ttyUSB0`` and the control port in ``/dev/ttyUSB1`` and these are the values that the Modem() class defaults to. Custom values for data and control ports can be passed to the Modem() class as the first and the second argument respectively. In other words, the statement::

    m = humod.Modem()

is equal to::

    m = humod.Modem('/dev/ttyUSB0', '/dev/ttyUSB1')

but some MacOS X users may want to execute the following::

    m = humod.Modem('/dev/cu.HUAWEIMobile-Modem', '/dev/cu.HUAWEIMobile-Pcui')

Next: You can now try to `connect to or disconnect from <ConnectDisconnect.rst>`_ the 3G network.
---------------------------