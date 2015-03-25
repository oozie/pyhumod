PyHumod INSTALL
===============

Installation from the latest source code
----------------------------------------
``$ git clone https://github.com/oozie/pyhumod.git``
``$ cd pyhumod``
``$ sudo python setup.py install``
 
Notes
-----
* It's important that the conf/humod file is copied to /etc/ppp/peers, 
otherwise the Modem.connect() method will fail.
