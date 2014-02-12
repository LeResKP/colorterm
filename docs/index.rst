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


Output redirection
==================

colorterm supports correctly the output redirection to another program. Example with the a python file named test.py which contains::


    from colorterm import colorterm
    print colorterm.underline('Hello world')


::

    $ python test.py

.. raw:: html

    The above example will render: <span style="text-decoration: underline">Hello world</span>


Now redirect the output to a less::

    $ python test.py | less

.. raw:: html

    We will have displayed in the less 'Hello world' without any special characters nor formatting


Table formatting
================

colorterm support to display table as output::

    from colorterm import Table
    table = Table('ID', 'Name')
    rows = [('id1', 'name1'), ('id2', 'name2')]
    for ident, name in rows:
        table.add_row({
            'ID': ident,
            'Name': name,
        })
    print table.display()


It will display the following table in your shell:

    .. raw:: html

        <table>
        <tr>
        <td style="text-decoration: underline;">ID </td><td style="text-decoration: underline;"> Name </td>
        </tr><tr>
        <td>id1</td><td> name1</td>
        </tr><tr>
        <td>id2</td><td> name2</td>
        </tr>
        </table>


Table options
-------------

    ``column_separator``

        Default: '  '. The column separator, you can put ' | ' for example.

    ``header_convert``

        Default: colorterm.underline. A function to apply on the display of the header.


    Example::

        from colorterm import Table, colorterm
        table = Table('ID', 'Name', column_separator = ' | ', header_convert=colorterm.red_underline)
        rows = [('id1', 'name1'), ('id2', 'name2')]
        for ident, name in rows:
            table.add_row({
                'ID': ident,
                'Name': name,
            })
        print table.display()


    Output:

    .. raw:: html

        <table>
        <tr>
        <td style="text-decoration: underline; color: red;">ID </td>
        <td>|</td>
        <td style="text-decoration: underline; color: red;"> Name </td>
        </tr><tr>
        <td>id1</td>
        <td> | </td>
        <td>name1</td>
        </tr><tr>
        <td>id2</td>
        <td> | </td>
        <td>name2</td>
        </tr>
        </table>



Column options
--------------

    ``convert``

        Default: None. A function to apply formatting on the cells from this column

    ``align``

        Default: 'left'. Where to display the text of the cells from this column.
        One of 'left' or 'right'.


    Example::

        from colorterm import Table, colorterm
        table = Table('ID',
                      {'name': 'Name',
                      'convert': colorterm.red,
                      'align': 'right'})
        rows = [('id1', 'name1'), ('id2', 'name2')]
        for ident, name in rows:
            table.add_row({
                'ID': ident,
                'Name': name,
            })
        print table.display()


    Output:

    .. raw:: html

        <table>
        <tr>
        <td style="text-decoration: underline;">ID</td>
        <td style="text-decoration: underline; color: red; text-align: right;">Name</td>
        </tr><tr>
        <td>id1</td>
        <td style="color: red; text-align: right;">name1</td>
        </tr><tr>
        <td>id2</td>
        <td style="color: red; text-align: right;">name2</td>
        </tr>
        </table>


Cell options
------------

    ``convert``

        Default: None. A function to appy formatting to the cell

    ``align``

        Default: 'left'. Where to display the text. One of 'left', 'right'.


    Example::

        from colorterm import Table, colorterm
        table = Table('ID', 'Long name')
        rows = [
            ('id1', {
                'value': 'name1',
                'convert': colorterm.red,
                'align': 'right'}),
            ('id2', 'name2')]
        for ident, name in rows:
            table.add_row({
                'ID': ident,
                'Long name': name,
            })
        print table.display()


    Output:

    .. raw:: html

        <table>
        <tr>
        <td style="text-decoration: underline;">ID </td><td style="text-decoration: underline;">Long name </td>
        </tr><tr>
        <td>id1</td><td style="color: red; text-align: right;"> name1</td>
        </tr><tr>
        <td>id2</td><td> name2</td>
        </tr>
        </table>


Row options
-----------

    ``convert``

        Default: None. A function to appy formatting to the row


    Example::

        from colorterm import Table, colorterm
        table = Table('ID', 'Name')
        rows = [
            ('id1', 'name1'),
            ('id2', 'name2')]
        for ident, name in rows:
            table.add_row({
                'ID': ident,
                'Name': name,
            }, convert=colorterm.red)
        print table.display()


    Output:

    .. raw:: html

        <table>
        <tr>
        <td style="text-decoration: underline;">ID </td><td style="text-decoration: underline;">Name </td>
        </tr><tr>
        <td style="color: red;">id1</td><td> name1</td>
        </tr><tr>
        <td style="color: red;">id2</td><td> name2</td>
        </tr>
        </table>
