Changing device settings
========================
A *setting* is an attribute of the device that can be set programatically and will not change even if the device is rebooted. Changing settings of a modem device is done by the ``set_*`` methods of the ``Modem()`` class.

The ``set_*`` methods
=====================

``set_pdp_context(pdp_id, proto, apn, ip_addr, d_comp, h_comp)``
----------------------------------------------------------------
Sets `Packet Data Protocol <http://www.tutorialspoint.com/gprs/gprs_pdp_context.htm>`_ context.

``set_service_center(sca, tosca)``
----------------------------------
Sets the service center address and the type of the service center address, where ``tosca`` is one of the following:

* 128 - unknown
* 129 - national
* 145 - international
* 161 - national

Next: Learn how to `handle events <EventHandling.rst>`_
-------------------------------------------------------
