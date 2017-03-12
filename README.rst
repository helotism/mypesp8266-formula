==================
mypesp8266-formula
==================

A saltstack formula to connect with an ESP8266 proxy minion running micropython.

.. note::

    See the full `Salt Formulas installation and usage instructions
    <http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html>`_.

    See the MicrPython port for the ESP 8266 documentation at
    <http://docs.micropython.org/en/latest/esp8266/>`_.

Available states
================

.. contents::
    :local:

``mypesp8266``
------------

Connects via serial USB to a board and reads `grains` values. Uses pyboard.py from the MicroPython project as a wrapper around PySerial.
