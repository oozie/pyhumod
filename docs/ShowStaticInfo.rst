Extracting static information from the device
=============================================

*Static information* can't be easily modified or changed; a change most likely follows some firmware update. Most 3G modems implement a number of standarized AT Hayes commands for reading static information about the device.  


<h1><!--The_show__*_methods-->The show``_*`` methods</h1>
The ``show_*`` methods implemented in the Modem class are responsible for extracting static information from the device. None of the ``show_*`` methods takes external arguments. 



show_manufacturer()
--------------

Returns a string containing device manufacturer name. 
<pre>>>> modem.show_manufacturer()
'huawei'</pre>


show_model()
--------------

Returns a string containing the device model. 
<pre>>>> modem.show_model()
'E270'</pre>


show_revision()
--------------

Returns a string containing the firmware revision. 

<pre>>>> modem.show_revision()
'11.304.16.00.00'</pre>

<!--show_sn()-->show_sn()
--------------

Returns a string with the serial number of the device. 
<pre>>>> modem.show_sn()
'CD2AE12345678901'</pre>
<!--show_imei()-->show_imei()<!--show_imei()-->
--------------
Returns a string with the IMEI number. 
<pre>>>> modem.show_imei()
'???????????????'</pre>

show_hardcoded_operators()
--------------

Returns a dictionary with operator IDs and operator names strings as key and value pairs respectively. 
<pre>>>> modem.show_hardcoded_operators()
{'544011': 'Blue Sky', '35230': 'DIGICEL', '61104': 'CKY-Areeba', '358030': 'Cingular', '61101': 'Spacetel Guinee ', '40555': [...]}</pre>

show_who_locked()
--------------

Returns a list with two operator IDs strings. I'm not sure why the modem returns a pair of operator IDs, so I decided that the method does the same just in case. 
<pre>>>> modem.show_who_locked()
['27202', '27202']
>>> ops = modem.show_hardcoded_operators()
>>> lockop = modem.show_who_locked()[0]
>>> ops[lockop]
'02 - IRL'</pre>
Unfortunately, of all the modems that got through my hands the only one to support this feature is E270. 
<h3>Next: Find out more about the modem state by reading `GetDynamicInfo.rst">dynamic device information</a>.</h3>