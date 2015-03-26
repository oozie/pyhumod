Extracting static information from the device
=============================================

**Static information** can't be easily modified or changed; a change most likely follows some firmware update. Most 3G modems implement a number of standarized AT Hayes commands for reading static information about the device.  

The ``show_\*`` methods
======================
The ``show_*`` methods implemented in the Modem class are responsible for extracting static information from the device. None of the ``show_\*`` methods takes external arguments. 

show_manufacturer()
-------------------
Returns a string containing device manufacturer name.

.. code:: python
 
    >>> modem.show_manufacturer()
    'huawei'

show_model()
------------
Returns a string containing the device model.

.. code:: python
 
    >>> modem.show_model()
    'E270'</pre>

show_revision()
---------------
Returns a string containing the firmware revision.

.. code:: python
 
    >>> modem.show_revision()
    '11.304.16.00.00'
	
show_sn()
---------

Returns a string with the serial number of the device.

.. code:: python
 
    >>> modem.show_sn()
    'CD2AE12345678901'

show_imei()
-----------
Returns a string with the IMEI number.

.. code:: python
 
    >>> modem.show_imei()
    '???????????????'

show_hardcoded_operators()
--------------------------
Returns a dictionary with operator IDs and operator names strings as key and value pairs respectively.

.. code:: python
 
    >>> modem.show_hardcoded_operators()
    {'544011': 'Blue Sky', '35230': 'DIGICEL', '61104': 'CKY-Areeba', '358030': 'Cingular', '61101': 'Spacetel Guinee ', '40555': [...]}

show_who_locked()
-----------------
Returns a list with two operator IDs strings. I'm not sure why the modem returns a pair of operator IDs, so I decided that the method does the same just in case.

.. code:: python
 
    >>> modem.show_who_locked()
    ['27202', '27202']
    >>> ops = modem.show_hardcoded_operators()
    >>> lockop = modem.show_who_locked()[0]
    >>> ops[lockop]
    '02 - IRL'

Unfortunately, of all the modems that got through my hands the only one to support this feature is E270.

Next: Find out more about the modem state by reading `dynamic device information <GetDynamicInfo.rst>`_.
-------------------------
