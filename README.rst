SMS, GSM and 3G connectivity using Huawei modems in Python
==========================================================
Access SMS, GSM and 3G features of Huawei and compatible modems from your own apps via clean and pragmatic Python API.

For a kick-start see `getting started <docs/GettingStarted.rst>`_ or a `sample app <docs/CoolApps.rst>`_. 

.. image:: https://raw.githubusercontent.com/oozie/pyhumod/master/docs/logo.png

Clean API
=========
When finished getting started the following should work for most users:

.. code:: python

    $ python3
    ...
    >>> import humod
    >>> m=humod.Modem()
    >>> m.show_model()
    'E270'
    >>> m.enable_textmode(True)
    >>> m.sms_send('+353?????????', 'hello world')
    52
    >>> m.connect()
    >>> m.disconnect()

Supported features
------------------

- `Connecting and disconnecting to the network with pppd <docs/ConnectDisconnect.rst>`_
- `Sending and receiving text messages <docs/SendReceiveText.rst>`_
    - Getting information about the SMS service center
    - Enabling/disabling sms notifications
    - Listing/reading/deleting messages
- `Showing static device information <docs/ShowStaticInfo.rst>`_
    - Manufacturer, Model, Revision, Serial Number,
    - IMEI number,
    - Hardcoded operators,
    - Locking operator
- `Displaying dynamic device information <docs/GetDynamicInfo.rst>`_
- `Manipulating modem settings <docs/ChangeSettings.rst>`_
- `Event handling <docs/EventHandling.rst>`_
- `SIM Phonebook manipulation <docs/PhoneBook.rst>`_
- `Sample applications <docs/CoolApps.rst>`_

See also `Development Guide <docs/DevelGuide.rst>`_.

------

- `Install <INSTALL.rst>`_
- `Docs <docs/GettingStarted.rst>`_
- `License <LICENSE.rst>`_
- `Blog <http://pyhumod.ooz.ie>`_
- `Home <https://github.com/oozie/pyhumod>`_
