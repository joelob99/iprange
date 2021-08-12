# iprange

**No warranty of any kind: use at your own risk.**

## Summary

This library provides a module that converts IP range to subnets.

## Getting Started

[Download the ZIP file](https://github.com/joelob99/iprange) from the branch and extracts it.
Put the extracted directory under the appropriate directory and execute commands as follows.

- JavaScript

  - Linux

        $ cd iprange/JavaScript
        $ node
        > ipv4range = new (require('./iprange').IPv4Range)()
        > ipv4range.iprange = '192.0.2.1-192.0.2.100'
        > ipv4range.iprange
        '192.0.2.1-192.0.2.100'
        > ipv4range.subnet
        [
          '192.0.2.1/32',
          '192.0.2.2/31',
          '192.0.2.4/30',
          '192.0.2.8/29',
          '192.0.2.16/28',
          '192.0.2.32/27',
          '192.0.2.64/27',
          '192.0.2.96/30',
          '192.0.2.100/32'
        ]
        > ipv6range = new (require('./iprange').IPv6Range)()
        > ipv6range.iprange = '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064'
        > ipv6range.iprange
        '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064'
        > ipv6range.subnet
        [
          '2001:0db8:0000:0000:0000:0000:0000:0001/128',
          '2001:0db8:0000:0000:0000:0000:0000:0002/127',
          '2001:0db8:0000:0000:0000:0000:0000:0004/126',
          '2001:0db8:0000:0000:0000:0000:0000:0008/125',
          '2001:0db8:0000:0000:0000:0000:0000:0010/124',
          '2001:0db8:0000:0000:0000:0000:0000:0020/123',
          '2001:0db8:0000:0000:0000:0000:0000:0040/123',
          '2001:0db8:0000:0000:0000:0000:0000:0060/126',
          '2001:0db8:0000:0000:0000:0000:0000:0064/128'
        ]

    If install using tarball, execute the following commands for an example.

        $ cd iprange/JavaScript
        $ npm pack
        $ cp iprange-1.0.1.tgz /tmp
        $ cd /tmp
        $ npm install iprange-1.0.1.tgz
        $ node
        > ipv4range = new (require('iprange').IPv4Range)()
        (---Subsequent command omitted. See the above example.)
        > ipv6range = new (require('iprange').IPv6Range)()
        (---Subsequent command omitted. See the above example.)

  - Windows

        C:\Users\foo> cd iprange\JavaScript
        C:\Users\foo\iprange\JavaScript> node
        > ipv4range = new (require('./iprange').IPv4Range)()
        (---Subsequent command omitted. See Linux example.)

    If install using tarball, execute the following commands for an example.

        C:\Users\foo> cd iprange\JavaScript
        C:\Users\foo\iprange\JavaScript> npm pack
        C:\Users\foo\iprange\JavaScript> copy iprange-1.0.1.tgz C:\Tmp
        C:\Users\foo\iprange\JavaScript> cd C:\Tmp
        C:\Tmp> npm install iprange-1.0.1.tgz
        C:\Tmp> node
        > ipv4range = new (require('iprange').IPv4Range)()
        (---Subsequent command omitted. See Linux example.)

- Python 3

  - Linux

        $ cd iprange/Python
        $ python3
        >>> import iprange
        >>> ipv4range = iprange.IPv4Range()
        >>> ipv4range.set_iprange('192.0.2.1-192.0.2.100')
        >>> ipv4range.iprange
        '192.0.2.1-192.0.2.100'
        >>> ipv4range.subnet
        ['192.0.2.1/32', '192.0.2.2/31', '192.0.2.4/30', '192.0.2.8/29', '192.0.2.16/28', '192.0.2.32/27', '192.0.2.64/27', '192.0.2.96/30', '192.0.2.100/32']
        >>> ipv6range = iprange.IPv6Range()
        >>> ipv6range.set_iprange('2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064')
        >>> ipv6range.iprange
        '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064'
        >>> ipv6range.subnet
        ['2001:0db8:0000:0000:0000:0000:0000:0001/128', '2001:0db8:0000:0000:0000:0000:0000:0002/127', '2001:0db8:0000:0000:0000:0000:0000:0004/126', '2001:0db8:0000:0000:0000:0000:0000:0008/125', '2001:0db8:0000:0000:0000:0000:0000:0010/124', '2001:0db8:0000:0000:0000:0000:0000:0020/123', '2001:0db8:0000:0000:0000:0000:0000:0040/123', '2001:0db8:0000:0000:0000:0000:0000:0060/126', '2001:0db8:0000:0000:0000:0000:0000:0064/128']

    If install using wheel, execute the following commands for an example.

        $ cd iprange/Python
        $ python3 setup.py bdist_wheel
        $ cp dist/iprange-1.0.1-py3-none-any.whl /tmp
        $ cd /tmp
        $ pip3 install ./iprange-1.0.1-py3-none-any.whl
        $ python3
        >>> import iprange
        (---Subsequent command omitted. See the above example.)

  - Windows

        C:\Users\foo> cd iprange\Python
        C:\Users\foo\iprange\Python> python
        >>> import iprange
        (---Subsequent command omitted. See Linux example.)

    If install using wheel, execute the following commands for an example.

        C:\Users\foo> cd iprange\Python
        C:\Users\foo\iprange\Python> python setup.py bdist_wheel
        C:\Users\foo\iprange\Python> copy dist\iprange-1.0.1-py3-none-any.whl C:\Tmp
        C:\Users\foo\iprange\Python> cd C:\Tmp
        C:\Tmp> pip install iprange-1.0.1-py3-none-any.whl
        C:\Tmp> python
        >>> import iprange
        (---Subsequent command omitted. See Linux example.)

- Python 2

  - Linux

        $ cd iprange/Python
        $ python
        >>> import iprange
        (---Subsequent command omitted. See Python 3 example.)

    If install using egg, execute the following commands for an example.

        $ cd iprange/Python
        $ python setup.py bdist_egg
        $ cp dist/iprange-1.0.1-py2.7.egg /tmp
        $ cd /tmp
        $ easy_install ./iprange-1.0.1-py2.7.egg
        $ python
        >>> import iprange
        (---Subsequent command omitted. See Python 3 example.)

  - Windows

        C:\Users\foo> cd iprange\Python
        C:\Users\foo\iprange\Python> python
        >>> import iprange
        (---Subsequent command omitted. See Python 3 example.)

    If install using egg, execute the following commands for an example.

        C:\Users\foo> cd iprange\Python
        C:\Users\foo\iprange\Python> python setup.py bdist_egg
        C:\Users\foo\iprange\Python> copy dist\iprange-1.0.1-py2.7.egg C:\Tmp
        C:\Users\foo\iprange\Python> cd C:\Tmp
        C:\Tmp> easy_install iprange-1.0.1-py2.7.egg
        C:\Tmp> python
        >>> import iprange
        (---Subsequent command omitted. See Python 3 example.)

## Limitation

- IPv6 range address string must use the non-compressed format. Also, IPv6 subnets are adopted the full represented.
