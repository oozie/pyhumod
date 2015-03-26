Manipulate SIM phonebook entries
================================
Adding, removing, updating and searching for SIM phonebook entries.
-------------------------------------------------------------------

It is possible to manipulate (add, remove, update) the content of the SIM card phonebook and to read and look for phonebook entries. The set of ``pbent_*`` methods of the ``Modem`` class have been implemented for that purpose. 

The ``pbent_*`` methods
-----------------------

    pbent_find (query='')

Searches through the phonebook to find queries starting with the ``query`` string argument. If ``query`` is an empty string (default) then all queries in the phonebook will be returned. 
find_pbent raises AtCommandError if no entries were found. 

    pbent_read (start_index, [end_index])

Reads a phonebook entry in by its index or a range of addresses if two integer arguments are passed. 
If only one argument is specified and the entry exists, it will return a four element list of the following format: ``[ index, phone_number, number_type, text ]`` where

* ``index`` is the message index,
* ``phone_number`` is a string with the phone number stored at the index,
* ``number_type`` is an integer representing phone number type,
* ``text`` is a text string value for the entry index.

If two arguments are specified, it will return a list of lists (the above) in a range between ``start_index`` and ``end_index``. 

If ``end_index`` is greater than ``start_index`` the list will be reversed. 

    pbent_write (index, number, text, numtype=145)

Writes a phonebook entry with values as specified by the four arguments. 

    pbent_del (index)

Clears out a phonebook entry held at ``index``. 
