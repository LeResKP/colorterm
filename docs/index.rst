.. colorterm documentation master file, created by
   sphinx-quickstart on Sat Nov  2 16:12:16 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

colorterm's documentation!
##########################

.. toctree::
   :maxdepth: 2

colorterm is a package to write some formatted message in your terminal. It supports 16 colors. You can set:

    * formatting like underline, bold, ...
    * color
    * background color


Supported format
================

You can visit `this page <http://misc.flogisoft.com/bash/tip_colors_and_formatting>`_ to see the rendering of each formats.

formatting
----------

    * bold
    * dim
    * underline
    * blink
    * reverse
    * hidden

color
-----

    The same colors are supported for the foreground like the background

    * default
    * black
    * red
    * green
    * yellow
    * blue
    * magenta
    * cyan
    * light_gray
    * dark_gray
    * light_red
    * light_green
    * light_yellow
    * light_blue
    * light_magenta
    * light_cyan
    * white


Usage
=====

Predefined functions
--------------------

::

    from colorterm import colorterm
    print colorterm.underline_red_on_yellow('Hello world')


.. raw:: html

    The above example will render: <span style="color: red; background-color: yellow; text-decoration: underline;">Hello world</span>


You can combine all the formatting and the colors. See examples::

    from colorterm import colorterm
    print colorterm.underline('Hello world')
    print colorterm.red('Hello world')
    print colorterm.on_yellow('Hello world')
    print colorterm.red_on_yellow('Hello world')
    print colorterm.underline_red_on_yellow('Hello world')


Formatter
---------

You can use the formatter to make some custom renderings::

    from colorterm import formatter
    print formatter('{red}Hello{/red} {underline}world')

.. raw:: html

    The above example will render: <span style="color: red">Hello</span> <span style="text-decoration: underline">world</span>

You can use the formatting and colors like you want.

.. note:: You can't use for example {red_on_yellow} in the formatter, you should use them separated like in the following example

::

    from colorterm import formatter
    print formatter('{red}{on_yellow}Hello{/red} {underline}world')

.. raw:: html

    The above example will render: <span style="background-color: yellow;"><span style="color: red">Hello</span> <span style="text-decoration: underline">world</span></span>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

