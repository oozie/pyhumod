Getting Started
===============

Installation
--------------

The installation of the package takes place in four steps: downloading the source, extracting it and system-wide installation on the elevated priviledges. The following should work for most Unix derivatives.

<pre>$ wget http://example.com/files/download.tar.gz
$ tar xzf download.tar.gz
$ cd download
$ sudo python setup.py install</pre>
Please note this package requires `http://pyserial.wiki.sourceforge.net/pySerial">pySerial</a> and detect module uses `http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.rst">dbus-python</a> to talk to HAL. pySerial is a required dependency, dbus-python can be installed if you want to take advantage of the humod.detect module.  


Usage Guide
--------------

Once installed, you can write your own scripts or this package from an interpreter. In both cases Python requires you to import humod first. 

<h3>Writing your own scripts</h3>
An example script could look as follows: 
<pre>#!/usr/bin/env python
# An example script.
import humod
m = humod.Modem()
model = m.show_model()
print('You are using %s 3G modem.' % model)
</pre>
<h3>Using a Python interpreter</h3>
I use ipython, however, most of the interpreter examples here are run from the standard ``/usr/bin/python``. 
<pre>$ ipython
Python 2.5.4 (r254:67916, May 21 2009, 22:07:14)
Type "copyright", "credits" or "license" for more information.
IPython 0.9.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object'. ?object also works, ?? prints more.
In [1]: import humod
In [2]: mod = humod.Modem('/dev/ttyUSB0', '/dev/ttyUSB1')
In [3]: mod.show_model()
Out[3]:'E270'</pre>

Instantiating a Modem()
--------------

The key task that must be accomplished every time you want to talk to the modem is to instantiate a Modem() class. In order for instatiation to suceed you must know where the required data and control ports are. For most Linux users the data port will be located in ``/dev/ttyUSB0`` and the control port in ``/dev/ttyUSB1`` and these are the values that the Modem() class defaults to. Custom values for data and control ports can be passed to the Modem() class as the first and the second argument respectively. In other words, the statement  
<pre>m = humod.Modem()</pre>is equal to 
<pre>m = humod.Modem('/dev/ttyUSB0', '/dev/ttyUSB1')</pre>but some MacOS X users may want to execute the following: 
<pre>m = humod.Modem('/dev/cu.HUAWEIMobile-Modem', '/dev/cu.HUAWEIMobile-Pcui')</pre>
<h3>Next: You can now try to `ConnectDisconnect.rst">connect to or disconnect from</a> the 3G network.</h3>