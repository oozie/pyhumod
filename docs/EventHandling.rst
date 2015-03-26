Event handling & responding to events
=====================================
Event handling functionality helps you interact with your modem: respond to RSSI change, new message delivery, incoming call flow report and more.

To follow the rest of the examples you have to create an instance of a ``Modem`` class: 

.. code:: python

    import humod
    modem = humod.Modem()

Event handling how-to
---------------------
Event handling is possible with the ``Prober()`` class. Each ``humod.Modem`` instance should have exactly one instance of ``Prober``, located at ``instance.prober`` (in our case ``modem.prober``). By default ``Prober`` is stopped, it can be turned on by calling it's ``start()`` method. Analogically, it can be stopped by calling its ``.stop()`` method. 

.. code:: python

    modem.prober.start() # Starts the prober.
    modep.prober.stop() # Stops the prober.

Prober reads the control port every fraction of a second, and if it finds a new message in the control port it refers to the list of predefined pattern-action pairs located in ``humod.actions.STANDARD_ACTIONS``. Patterns are compiled regular expressions, actions are functions to call when a pattern is matched. An example pattern, available in ``humod.actions.PATTERN['rssi update']`` looks as follows: 

.. code:: python

    re.compile(r'^\^RSSI:.*')

Type ``humod.actions.PATTERN.keys()`` to see a list of other predefined patterns.

The ``humod.actions`` module predefines a handful of very basic event handler functions. The simplest one is probably the ``null_action()`` function, that simply does nothing.

.. code:: python

    def null_action(modem, message):
        """Take no action."""
        pass

The function takes two arguments: **modem** and **message**. The **modem** argument will represent a modem that the message came from. The **message** argument contains verbatim message that has been passed to the control port of the modem and caught by the prober. If you'll write your own event handling functions, the only requirement is that they must take those two arguments. 

New message notifications
-------------------------
In order to be notified about the incoming text message you must first enable the NMI functionality, as it is off by default. 

.. code:: python

    modem.enable_nmi(True)

Secondly, start the Prober on your modem.

.. code:: python

    modem.prober.start()

You can now send an SMS to the SIM card in your modem and when it arrives you should see  the "**New message arrived.**" text appearing in the Python interpreter. That is because the predefined pattern 'new sms' has been matched with the predefined handler function ``humod.actions.new_message()``.

Defining your own pattern-action pairs
--------------------------------------
A pattern-action pair list is a list of two element tuples, each containing a regex and an event handling function respectively. You can point prober to your pattern-action list by passing it as the first element to Prober's ``start()`` method. You can define your own patter-action list as follows:

.. code:: python

    # Define a new sms handling function.
    def new_sms(modem, message):
        print('New message arrived: %r' % message)
    # Assign the function to the pattern.
    sms_action = (humod.actions.PATTERN['new sms'], new_sms)
    # Create actions list with patterns-action pairs.
    actions = [sms_action]
    # Enable NMI.
    modem.enable_nmi(True)
    # Start the Prober.
    modem.prober.start(actions)
    # Send a message to yourself.
    modem.sms_send('+353?????????', '1234567')
    New message arrived: '+CMTI: "SM",2\r\n'