Sample applications
===================

sms_exec.py
-----------
The program executes remote commands sent in via SMS and replies with the command output.

.. code:: python

    #!/usr/bin/env python
    # sms_exec.py
    # A sample application
    
    import os
    import humod
    def sms_exec(modem, message):
        """Execute a shell command from an text message."""
        # Stripping message header and \r\n trailer.
        msg_num = int(message[12:].strip())
        command = modem.read_message(msg_num)
        for msg_header in modem.sms_list():
            if msg_header[0]==msg_num:
                textback_num = msg_header[2]
                break
        print('Executing %r' % command)
    
        cmd_exec = os.popen(command)
        output = cmd_exec.read()
        print('Sending the output back to %s output: %s' % (textback_num, output))
        modem.send_text(textback_num, output)
    
    if __name__=='__main__':
        modem = humod.Modem()
        sms_action = (humod.actions.PATTERN['new sms'], sms_exec)
        actions = [sms_action]
        modem.enter_text_mode()
        modem.enable_nmi(True)
        modem.prober.start(actions)
        print('Waiting for commands. CTRL+C to exit.')
        while 1:
            try:
                input()
            except KeyboardInterrupt:
                break
                modem.prober.stop()
        print('Exiting.')
