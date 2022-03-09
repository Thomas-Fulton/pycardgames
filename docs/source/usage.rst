Usage
=====

Getting started
---------------

Pycardgames simulates traditional card games using a 52 card deck from the command line. Make sure the package has been downloaded and installed (see :ref:`Installation<installation>`).  

The program is started by typing ``pycardgames``, followed by optional arguments, into the command line. For the full list of command line arguments, see :ref:`below<command_line>`, or type ``pycardgames --help``.


Example: Poker 
--------------

To play any game, the most important arguments are the ``--game <game>`` and ``--player <player name>`` flags. For example, to start a game of poker, run:

.. code-block:: bash

   pycardgames --game poker --player Tom --player Fred

At least two players are required for a game of poker, so the ``--player`` flag is used twice, adding a new player each time.


> There is currently no AI opponent, so both players must be played.

.. _command_line:

Command line arguments
----------------------

.. argparse::
   :ref: cardgames.__main__.create_parser
   :prog: pycardgames


