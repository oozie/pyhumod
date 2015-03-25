Dynamic device information
==========================
*Reading device status and settings.*
Data that is easily and frequently modified and can be freely read from the modem device can be defined as Dynamic device information. Extract this kind of data using ``get_*`` methods of the Modem() class. None of the ``get_*`` methods take any external arguments. To manipulate SIM Phonebook entries see the `PhoneBook">PhoneBook wiki page</a>. 
<h1><!--The_get_*_methods-->The ``get_*`` methods<!--The_get_*_methods--></h1>In order to run any of the following methods, instanciate the Modem() class: 
<pre>>>> import humod
>>> modem = humod.Modem('/dev/ttyUSB0', '/dev/ttyUSB1')
>>></pre>
<!--get_clock()-->get_clock()<!--get_clock()-->
--------------
Shows the internal modem clock. 
<pre>>>> modem.get_clock()
'1980/01/06,00:49:09'</pre>
<!--get_detailed_error()-->get_detailed_error()<!--get_detailed_error()-->
--------------
Returns descriptive information about an error that occured as last. 
<pre>>>> modem.get_detailed_error()
'No cause information available'</pre>
<!--get_networks()-->get_networks()<!--get_networks()-->
--------------
Scans for networks, and if successful returns a nested list. A list of strings representing a network has a following format: 
``['VAL1','Op long name', 'Op short name', 'Operator Number', 'VAL2']`` 
Where VAL1 and VAL2 have something to do with network types, but I couldn't find any documentation as to what exactly.  
<pre>>>> modem.get_networks()
[[2, '02 - IRL', '02 -IRL', '27202', 2],
[1, '02 - IRL', '02 -IRL', '27202', 0],
[1, '3 IRL', '3 IRL', '27205', 2],
[3, 'IRL - METEOR', 'METEOR', '27203', 2],
[3, 'vodafone IE', 'voda IE', '27201', 2],
[3, 'IRL - METEOR', 'METEOR', '27203', 0],
[3, 'vodafone IE', 'voda IE', '27201', 0],
[0, 1, 2, 3, 4]]</pre>
<!--get_pdp_context()-->get_pdp_context()<!--get_pdp_context()-->
--------------
Displays settings for the Packet Data Protocol context. 
<pre>>>> modem.get_pdp_context()
[[1, 'IP', 'open.internet', '', 0, 0]]</pre>
<!--get_pin_status()-->get_pin_status()<!--get_pin_status()-->
--------------
Informs about the SIM card PIN status. Returns three possible string values: <ul><li>'READY' - if no PIN required, </li><li>'SIM PIN' - if PIN is required, </li><li>'SIM PUK' - if PUK must be entered in order to unlock the card. </li></ul>

<!--get_rssi()-->get_rssi()<!--get_rssi()-->
--------------
Informs about current signal quality strength value by returning an integer in a range from 0 to 31 denoting strength or 99 if no data is available. 

<!--get_service_center()-->get_service_center()<!--get_service_center()-->
--------------
Returns a two element tuple representing SMS service center number as a string and service center type in form of an integer. 
<pre>>>> modem.get_service_center()
('+353868002000', 145)</pre>The service center type can be one of the following: <table><tr><td>number</td><td>type</td></tr> <tr><td>128</td><td> unknown</td></tr> <tr><td>129</td><td> national</td></tr> <tr><td>145</td><td> international</td></tr> <tr><td>161</td><td> national</td></tr> At this stage I'm not entirely sure what is the difference between 129 and 161. </table>

<h3>Next: Learn how to `ChangeSettings.rst">change modem settings</a>.</h3>