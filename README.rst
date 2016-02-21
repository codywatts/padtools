padtools
--------------------

|PyPI Version|

Description
~~~~~~~~~~~~~~~~~~~~
A Python package for the popular iOS & Android game "Puzzle & Dragons" (PAD).

Installation
~~~~~~~~~~~~~~~~~~~~
.. code::

	pip install padtools

Example Usage
~~~~~~~~~~~~~~~~~~~~
.. code:: python

	>>> import padtools
	>>> na_server = padtools.regions.north_america.server
	>>> jp_server = padtools.regions.japan.server
	>>> na_server.version
	'8.62'
	>>> jp_server.version
	'8.70'
	>>> len(na_server.assets)
	2124
	>>> len(jp_server.assets)
	2727
	>>> jp_server.assets[0].url
	'http://dl.padsv.gungho.jp/ext/mon16021916321966505024756c6c50308dff/mons_001.bc'

.. |PyPI Version| image:: http://img.shields.io/pypi/v/padtools.svg
	:target: https://pypi.python.org/pypi/padtools/
