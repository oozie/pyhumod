How to connect/disconnect to the Internet
=========================================
Connecting to a 3G network can be as easy as this: 

<pre>>>> import humod
>>> modem = humod.Modem()
>>> modem.connect()</pre>
and when you are done and want to disconnect: 

<pre>>>> modem.disconnect()</pre>
<h1>Details</h1>
When you call the connect() method of the Modem class the following happens.
<ol>
    <li>The predefined ``_``dial_num attribute of the class instance is read. It represents the number to dial. By default it's value is equal to '``*``99#' which works for most of the networks. However if it doesn't work for yours, you can change the value of this attribute to one specific to your provider. E.g. Some Australian VF users will do the following before connecting: 
    <pre>>>> modem._dial_num = '*99***2#'</pre></li>
    <li>The number to dial is passed to the data port of the modem following the ATDT Hayes command. </li>
    <li>If the CONNECT response is received from the data port, the modem is ready to connect and humod module executes pppd that looks after creating network interfaces and further negotiation.  </li>
</ol>
Please note that for pppd to start in a privileged mode the 'humod' file must be available in /etc/ppp/peers, i.e. you must properly install humod package or create a 'humod' file in /etc/ppp/peers with 'noauth' as it's content. 

<h3>Next: Learn how to `SendReceiveText.rst">send and receive SMS</a></h3>
<hr>

Comment
I've problems getting connection to a 3G network. SMS works fine, but connect() hung up always. Only a CTRL-C brings command back. APN-Setting in pdp-context looks fine and the default dial no is also OK. Is there any way to get more informations where my system stucks? 

The Traceback of my last attempt to connect:
<pre>
>>> m.connect() ^C
Traceback (most recent call last):
File "&lt;stdin>", line 1, in &lt;module> 
File "/humod/humodem.py", line 258, in connect 
    data_port.return_data() 
File "/humod/humodem.py", line 179, in return_data 
    input_line = self.readline().rstrip() 
File "/usr/lib/python2.5/site-packages/serial/serialutil.py", line 147, in readline 
    c = self.read(1) 
File "/usr/lib/python2.5/site-packages/serial/serialposix.py", line 442, in read 
    ready,,  = select.select(self.fd?,,, self.timeout) 
KeyboardInterrupt? >>>
</pre>