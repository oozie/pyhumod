Sending and receiving text messages
===================================
Once the modem is properly detected and initialized, you can send, read and delete text messages. One important step at the start is to enter a so called 'TEXT mode', as sending texts in 'PDU mode' is not yet supported. Once this is accomplished you can start sending, reading and deleting messages.
::
    >>> modem.enable_textmode(True)

Sending texts
-------------
To send a text, call the ``sms_send()`` method with two string arguments:

1. A number to send to, e.g. '+353987654321'
2. The contents of the message.
::
    >>> modem.sms_send('+353987654321', 'Are you free for dinner?')

Listing texts
-------------
To list texts call the ``sms_list()`` method.
::
    >>> modem.sms_list()
    ['0,"REC READ","00353?????????",,"09/06/19,14:23:14+04"',
    '1,"REC READ","+353?????????",,"09/06/27,14:43:09+04"']

Reading texts
-------------
To read a messages, call the ``sms_read()`` method with message ID as an argument.
::
    >>> modem.sms_read(0)
    'Result out this evening. Gud luck'

Deleting texts
--------------
In a similar way, in order to delete a message, call the ``sms_del()`` method with message ID as an argument.
::
    >>> modem.sms_del(0)

New message notifications
-------------------------
By default new message notifications are not enabled. There are two steps to enable NMI:

1. Start the prober service
2. Call enable_nmi() method with True as argument
::
    >>> modem.prober.start()
    >>> modem.enable_nmi(True)

Once this is done, a new message can be handled by some code of your choice. By default it's a method living in ``humod.actions.new_message()`` and it's a trivial one: 
::
    def new_message(modem, message):
        """New message action."""
        print('New message arrived.')

You can create your own action-handling functions. See `EventHandling <EventHandling.rst>` to find out how. 

Next: Find out more about your modem by reading `its static data <ShowStaticInfo.rst>`_
----------------------

----------

**Question**

Regarding read_message: I have received an SMS that was sort of encoded.  Other messages were in plain text but this particular message send via cellphone was in some sort of encoding (it was a two part message if that helps). 

Is this normal? what encoding do cellphones use to send their messages?  Can anybody point me in the right direction. thanks.

**Answer**

This is GSM0338 encoded message. See `codec <https://github.com/dsch/gsm0338>`_.

**Question**

Wondering how I can select messages based on sender? So far used message ID but only returns the message, I need to select only messages from certain numbers to operate on.

**Answer**

I think that should do::

    #!/usr/bin/env python
    import humod
    class MyModem(humod.Modem):
        def sms_list_by_num(self, number):
            """Lists messages from a particular sender."""
            messages = []
            for message in self.sms_list():
                if number in message[2]:
                    messages.append(message)
            return messages
    
    modem = MyModem()
    print(modem.sms_list_by_num('12345678'))

----------

**Question**

Is there any way to detect the callerID of an incoming call (received via humod.actions.PATTERN call)?  The message content comes in as 'RING'.

...