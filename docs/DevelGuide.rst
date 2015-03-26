Development Guide
=================

Find out what AT commands your modem supports
---------------------------------------------
Most of the mobile devices implement an ``AT+CLAC`` command. It outputs a list of comma-separated AT commands (without the 'AT' prefix) supported by the device.

You can list the AT commands that your device supports in the following way:

.. code:: python

    >>> import humod
    >>> from humod.at_commands import Command
    >>> m = humod.Modem()
    >>> list_all = Command(m, '+CLAC')
    >>> supported_commands_string = list_all.run()[0]
    >>> at_cmd_list = supported_commands_string.split(',')
    >>> at_cmd_list
    ['C', '&amp;D', '&amp;F', '&amp;V', 'E', 'I', 'L', ... ]
    >>> len(at_cmd_list)
    188

My Huawei E270 Modem supports 188 AT commands.

Implement new methods
---------------------
The ``humod.at_commands.Command`` class can be used to implement AT command functionality. 
Let's assume that the 'AT+CMD' is a generic AT command. From any mobile device viewpoint, you can issue an AT command in 4 ways: 

* ``AT+CMD`` - tell the modem to do something, (**run**)
* ``AT+CMD?`` - query the current setting in the memory or the current state, (**get**)
* ``AT+CMD=?`` - see what are the possible values to set, (**dsc** for describe)
* ``AT+CMD=value`` - set a value for a given command/setting. (**set**)

The ``humod.at_commands.Command`` class implements four methods to run, query or set values of the AT commands. The methods names are run(), get(), dsc() and set(). 

Sample command with prefixed output
-----------------------------------
Let's take the ``AT^SN`` command as an example. The command only supports the **run** operation and when issued to a modem it returns a string containing the command prefix (``'^SN: '``) followed by a serial number of the device. 

You can use the the ``Command`` class in order to extract the serial number into a Python object. 

.. code:: python

    >>> show_sn = Command(m, '^SN')
    >>> show_sn.run()
    ['1234567890...']

What happened?
~~~~~~~~~~~~~~
1. You created a Command instance and told it to issue the ``AT^SN`` AT command.
2. With help of the ``run()`` method, you have sent the ``AT^SN\r\n`` string to the modem.
3. In response, one line of output was returned (one and only element in the list). The modem returned the ``^SN: 1234567890...`` string (prefixed with command name),
4. The .run() method stripped the prefix, packed the line into a list and returned it.

Sample command with unprefixed output
-------------------------------------
By default, any method of the Command class instance will only accept output prefixed with the AT-command + colon + space combination (i.e. ``'^SN: '``). This behaviour can be altered by specifying ``prefixed=False`` during Command class instanciation. 
The class of ``AT+GM[IMR]`` commands return unprefixed output, i.e. each line returned from the modem is the actual output value and should not be stripped any further. 
Let's implement ``AT+GMM`` from scratch.

.. code:: python

    >>> show_model = Command(m, '+GMM', prefixed=False)
    >>> show_model.run()
    ['E270']

Setting / getting commands
--------------------------
In most cases, the same AT command exists to set and get a value. The only difference is in the way we issue the command to a modem. We set values by sending "``AT+CMD="value"\r\n``" string. The values can be retrieved using the same command, but followed by a different parameter - "``AT+CMD?``" - simply followed by a question mark. 
This is a job of the ``.set()`` and ``.get()`` methods of the ``Command`` class.

Sample value setter/getter
--------------------------
In this example we will use the ``+CMGF`` AT command which is responsible for switching between the Text and PDU modes. To see which mode we are in, we should query the modem with the ``.get()`` method of Command class instance. 
In order to switch between modes, the ``.set()`` method of the same instance must be used. If we set ``+CMGF``'s value to 1 it means we are just entered the Text mode. A value of 0 reflects PDU mode.

.. code:: python

    >>> mode_cmd = Command(m, '+CMGF')
    >>> set_mode = mode_cmd.set
    >>> get_mode = mode_cmd.get
    >>> get_mode()
    ['1']
    >>> set_mode("0")
    >>> get_mode()
    ['0']
    >>> set_mode("1")
    >>> get_mode()
    ['1']


Respond to events
=================
`Event handling <EventHandling.rst>`_ functionality will help you build interactive apps for your modem: respond to RSSI change, new message delivery, incoming call flow report and any other event that is indicated via the control port. 

Understanding events
--------------------
An event happens when modem sends a **message** to its control port and a ``prober`` instance picks it up in order to match it with an **action**. Please refer to `Event Handling <EventHandling.rst>`_ to find out how to start and stop ``prober``.

A **message** is a string, here are some examples of messages that are sent to control port: 
::
    ^BOOT:12659389,0,0,0,58
    ^RSSI:4
    ^DSFLOWRPT:00002406,00000000,00000000,00000000000A D023,00000000002FA192,0003E800,0003E800
    +CMTI: "SM",0
    ...

An **action** is a predefined Python function of the following format: 

.. code:: python

    def <action_name>(modem, message):
        """<Docstring.>"""
        <code>

Matching patterns to actions
----------------------------
While running, the ``prober`` matches **patterns** to **actions** by checking if a **message** matches predefined regex. If it does, the action associated with the regex is executed.  
A **pattern-action** combo is a Python tuple consisting of a compiled regex and an **action** function respectively.

.. code:: python

    sample_pattern = re.compile(pattern_string)
    def samlpe_action(modem, message):
        sample_code(message)
        sample_combo = (sample_pattern, sample_action)

Feeding the pattern-action list to ``prober``
---------------------------------------------
The ``prober`` becomes aware of your predefined pattern-actions list when it is started with the list as its argument.

.. code:: python

    pa_list = [sample_combo1, sample_combo2]
    modem_instance.prober.start(pa_list)

----------------

**Question**

| I am trying to check my balance using AT commands, ``AT+CUSD=1,"131#"``
| I try to implement that as ``cmd = Command(m, '+CUSD=1,"131#"')``
| Not getting anything back after cmd.run().
| Tried ``cmd = Command(m, '+CUSD=1,"131#"', prefixed=False)`` as well.
| ``cmd = Command(m, '+CUSD=1', prefixed=False)`` then
| ``cmd.set("**131#")`` gives an error.


**Answer**

The reply comes from the control port so you have to write a regex and compile it then parse to modem.prober.start. I got it working using: 

.. code:: python

    def new_bal(modem, message):
        print(message)
    ussd_ex = re.compile(r'^\+CUSD:.')
    ussd_act = (ussd_ex, new_bal)
    actions = ussd_act
    m.prober.start(actions)
    ussd = Command(m, "+CUSD")
    ussd.set("1,\"131#\",15")
