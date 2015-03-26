How to connect to the Internet
==============================
Connecting to a 3G network can be as easy as this: 

.. code:: python

    >>> import humod
    >>> modem = humod.Modem()
    >>> modem.connect()

and when you are done and want to disconnect: 

.. code:: python

    >>> modem.disconnect()

Details
-------
When you call the ``connect()`` method of the Modem class the following happens.

1. The predefined ``_dial_num`` attribute of the class instance is read. It represents the number to dial. By default it's value is equal to ``'*99#'`` which works for most of the networks. However if it doesn't work for yours, you can change the value of this attribute to one specific to your provider. E.g. Some Australian VF users will do the following before connecting:

.. code:: python

    >>> modem._dial_num = '*99***2#'

2. The number to dial is passed to the data port of the modem following the ATDT Hayes command.
3. If the CONNECT response is received from the data port, the modem is ready to connect and humod module executes pppd that looks after creating network interfaces and further negotiation.

Please note that for pppd to start in a privileged mode the 'humod' file must be available in ``/etc/ppp/peers``, i.e. you must properly install humod package or create a 'humod' file in ``/etc/ppp/peers`` with 'noauth' as its content. 

Next: Learn how to `send and receive SMS <SendReceiveText.rst>`_.
-------------------