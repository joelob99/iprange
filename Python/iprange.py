# ============================================================================
#
# IP range
#
# iprange.py
#
# Copyright (c) 2021 joelob99
#
# Released under the MIT License, see LICENSE.txt.
#
# History
#   2021-08-07: First Release, v1.0.0.
#   2021-08-12: Update to v1.0.1.
#               - Fix _isIPv4Addr and _isIPv6Addr.
#               - Fix to throw an error message when exception.
#               - Change example's address.
#
# ============================================================================
"""IP range module.

This module provides classes that IP range to subnets conversion.
"""
__version__ = "1.0.1"

_EXCEPTION_MSG_IP_RANGE_NOT_SET   = "IP address range not set."
_EXCEPTION_MSG_INVALID_IP_ADDRESS = "Invalid IP address contained."
_EXCEPTION_MSG_INVALID_IP_RANGE   = "Invalid IP address range specified."

class IPRangeException(Exception):
    pass


class IPRangeAddressError(IPRangeException):
    pass


class IPRange:
    def __init__(self):
        self._intStartAddr = None
        self._intEndAddr = None
        self._listSubnet = None

    @property
    def subnet(self):
        """Retrieve subnet strings list.

        :return: Subnet strings list.
        :rtype: List[str]
        :raises IPRangeAddressError: Will throw if the invalid address
            range.

        Test:
            >>> iprange = IPRange()
            >>> print(iprange.subnet)
            Traceback (most recent call last):
                ...
            IPRangeAddressError: IP address range not set.
        """
        if (self._listSubnet is None):
            raise IPRangeAddressError(_EXCEPTION_MSG_IP_RANGE_NOT_SET)
        return self._listSubnet


class IPv4Range(IPRange):
    @property
    def iprange(self):
        """Retrieve IPv4 address range string.

        :return: IPv4 address range string.
        :rtype: str
        :raises IPRangeAddressError: Will throw if the address range is
            not set.

        Example::

            intStartAddr intEndAddr    Return
            --------------------------------------------------
            3221225985   3221226084 -> '192.0.2.1-192.0.2.100'

        Test:
            >>> ipv4range = IPv4Range()
            >>> print(ipv4range.iprange)
            Traceback (most recent call last):
                ...
            IPRangeAddressError: IP address range not set.
            >>> ipv4range.set_iprange('192.0.2.1-192.0.2.100')
            >>> print(ipv4range._intStartAddr)
            3221225985
            >>> print(ipv4range._intEndAddr)
            3221226084
            >>> print(ipv4range.iprange)
            192.0.2.1-192.0.2.100
        """
        if (self._intStartAddr is None or self._intEndAddr is None):
            raise IPRangeAddressError(_EXCEPTION_MSG_IP_RANGE_NOT_SET)
        return _toIPv4AddrString(self._intStartAddr) + '-' + _toIPv4AddrString(self._intEndAddr)

    def set_iprange(self, strIPv4Range):
        """Set IPv4 address range.

        This method saves integers of the start and end address of the
        specified IPv4 address range string and makes the subnets list.

        :param str strIPv4Range: IPv4 address range string.
        :return: None
        :raises IPRangeAddressError: Will throw if the invalid address
            range.

        Example::

            strIPv4Range               intStartAddr intEndAddr listSubnet
            ---------------------------------------------------------------------
            '192.0.2.1'             -> 3221225985   3221225985 ['192.0.2.1/32']
            '192.0.2.1-192.0.2.1'   -> 3221225985   3221225985 ['192.0.2.1/32']
            '192.0.2.1-192.0.2.100' -> 3221225985   3221226084 ['192.0.2.1/32',
                                                                '192.0.2.2/31',
                                                                '192.0.2.4/30',
                                                                '192.0.2.8/29',
                                                                '192.0.2.16/28',
                                                                '192.0.2.32/27',
                                                                '192.0.2.64/27',
                                                                '192.0.2.96/30',
                                                                '192.0.2.100/32']

        Test:
            >>> ipv4range = IPv4Range()
            >>> ipv4range.set_iprange('192.0.2.1')
            >>> print(ipv4range._intStartAddr)
            3221225985
            >>> print(ipv4range._intEndAddr)
            3221225985
            >>> print(ipv4range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['192.0.2.1/32']
            >>> ipv4range.set_iprange('192.0.2.1-192.0.2.1')
            >>> print(ipv4range._intStartAddr)
            3221225985
            >>> print(ipv4range._intEndAddr)
            3221225985
            >>> print(ipv4range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['192.0.2.1/32']
            >>> ipv4range.set_iprange('192.0.2.1-192.0.2.100')
            >>> print(ipv4range._intStartAddr)
            3221225985
            >>> print(ipv4range._intEndAddr)
            3221226084
            >>> print(ipv4range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['192.0.2.1/32',
             '192.0.2.2/31',
             '192.0.2.4/30',
             '192.0.2.8/29',
             '192.0.2.16/28',
             '192.0.2.32/27',
             '192.0.2.64/27',
             '192.0.2.96/30',
             '192.0.2.100/32']
            >>> ipv4range.set_iprange('192.0.2.1-192.0.2.256')
            Traceback (most recent call last):
                ...
            IPRangeAddressError: Invalid IP address contained.
            >>> ipv4range.set_iprange('192.0.2.100-192.0.2.1')
            Traceback (most recent call last):
                ...
            IPRangeAddressError: Invalid IP address range specified.
        """
        list = strIPv4Range.split('-') if strIPv4Range.find('-') != -1 else [strIPv4Range, strIPv4Range]
        if (not _isIPv4Addr(list[0]) or not _isIPv4Addr(list[1])):
            raise IPRangeAddressError(_EXCEPTION_MSG_INVALID_IP_ADDRESS)

        self._intStartAddr = _toIPv4AddrInteger(list[0])
        self._intEndAddr = _toIPv4AddrInteger(list[1])

        if (self._intStartAddr > self._intEndAddr):
            raise IPRangeAddressError(_EXCEPTION_MSG_INVALID_IP_RANGE)

        self._listSubnet = []
        _makeIPv4SubnetFromRange(self._intStartAddr, self._intEndAddr, self._listSubnet)


class IPv6Range(IPRange):
    @property
    def iprange(self):
        """Retrieve IPv6 address range string.

        :return: IPv6 address range string.
        :rtype: str
        :raises IPRangeAddressError: Will throw if the address range is
            not set.

        Example::

            intStartAddr                           intEndAddr                                Return
            ------------------------------------------------------------------------------------------------------------------------------------------------------------------
            42540766411282592856903984951653826561 42540766411282592856903984951653826660 -> '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064'

        Test:
            >>> ipv6range = IPv6Range()
            >>> print(ipv6range.iprange)
            Traceback (most recent call last):
                ...
            IPRangeAddressError: IP address range not set.
            >>> ipv6range.set_iprange('2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064')
            >>> print(ipv6range._intStartAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range._intEndAddr)
            42540766411282592856903984951653826660
            >>> print(ipv6range.iprange)
            2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064
        """
        if (self._intStartAddr is None or self._intEndAddr is None):
            raise IPRangeAddressError(_EXCEPTION_MSG_IP_RANGE_NOT_SET)
        return _toIPv6AddrString(self._intStartAddr) + '-' + _toIPv6AddrString(self._intEndAddr)

    def set_iprange(self, strIPv6Range):
        """Set IPv6 address range.

        This method saves integers of the start and end address of the
        specified IPv6 address range string and makes the subnets list.

        :param str strIPv6Range: IPv6 address range string.
        :return: None
        :raises IPRangeAddressError: Will throw if the invalid address
            range.

        Example::

            strIPv6Range                                                                         intStartAddr                           intEndAddr                             listSubnet
            ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            '2001:0dB8:0000:0000:0000:0000:0000:0001'                                         -> 42540766411282592856903984951653826561 42540766411282592856903984951653826561 ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
            '2001:0dB8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0001' -> 42540766411282592856903984951653826561 42540766411282592856903984951653826561 ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
            '2001:0dB8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064' -> 42540766411282592856903984951653826561 42540766411282592856903984951653826660 ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0002/127',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0004/126',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0008/125',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0010/124',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0020/123',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0040/123',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0060/126',
                                                                                                                                                                                '2001:0db8:0000:0000:0000:0000:0000:0064/128']

        Test:
            >>> ipv6range = IPv6Range()
            >>> ipv6range.set_iprange('2001:0dB8:0000:0000:0000:0000:0000:0001')
            >>> print(ipv6range._intStartAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range._intEndAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
            >>> ipv6range.set_iprange('2001:0dB8:0000:0000:0000:0000:0000:0001-2001:0dB8:0000:0000:0000:0000:0000:0001')
            >>> print(ipv6range._intStartAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range._intEndAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
            >>> ipv6range.set_iprange('2001:0dB8:0000:0000:0000:0000:0000:0001-2001:0dB8:0000:0000:0000:0000:0000:0064')
            >>> print(ipv6range._intStartAddr)
            42540766411282592856903984951653826561
            >>> print(ipv6range._intEndAddr)
            42540766411282592856903984951653826660
            >>> print(ipv6range.subnet)  # doctest: +NORMALIZE_WHITESPACE
            ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
             '2001:0db8:0000:0000:0000:0000:0000:0002/127',
             '2001:0db8:0000:0000:0000:0000:0000:0004/126',
             '2001:0db8:0000:0000:0000:0000:0000:0008/125',
             '2001:0db8:0000:0000:0000:0000:0000:0010/124',
             '2001:0db8:0000:0000:0000:0000:0000:0020/123',
             '2001:0db8:0000:0000:0000:0000:0000:0040/123',
             '2001:0db8:0000:0000:0000:0000:0000:0060/126',
             '2001:0db8:0000:0000:0000:0000:0000:0064/128']
            >>> ipv6range.set_iprange('2001:0dB8:0000:0000:0000:0000:0000:0001-2001:0dB8:0000:0000:0000:0000:0000:000g')
            Traceback (most recent call last):
                ...
            IPRangeAddressError: Invalid IP address contained.
            >>> ipv6range.set_iprange('2001:0dB8:0000:0000:0000:0000:0000:0064-2001:0dB8:0000:0000:0000:0000:0000:0001')
            Traceback (most recent call last):
                ...
            IPRangeAddressError: Invalid IP address range specified.
        """
        list = strIPv6Range.split('-') if strIPv6Range.find('-') != -1 else [strIPv6Range, strIPv6Range]
        if (not _isIPv6Addr(list[0]) or not _isIPv6Addr(list[1])):
            raise IPRangeAddressError(_EXCEPTION_MSG_INVALID_IP_ADDRESS)

        self._intStartAddr = _toIPv6AddrInteger(list[0])
        self._intEndAddr = _toIPv6AddrInteger(list[1])

        if (self._intStartAddr > self._intEndAddr):
            raise IPRangeAddressError(_EXCEPTION_MSG_INVALID_IP_RANGE)

        self._listSubnet = []
        _makeIPv6SubnetFromRange(self._intStartAddr, self._intEndAddr, self._listSubnet)


def _isIPv4Addr(strIPv4Addr):
    """Confirm whether the specified address is an IPv4 address.

    :param str strIPv4Addr: IPv4 address string.
    :return: True when the specified address is an IPv4 address.
    :rtype: bool

    Example::

        strIPv4Addr        Return
        -------------------------
        '192.0.2.1'   -> True
        '192.0.2'     -> False
        '192.0.2.256' -> False
        '192.0.2.-1'  -> False
        '192.0..1'    -> False
        '192.0.a.1'   -> False

    Test:
        >>> _isIPv4Addr('192.0.2.1')
        True
        >>> _isIPv4Addr('192.0.2')
        False
        >>> _isIPv4Addr('192.0.2.256')
        False
        >>> _isIPv4Addr('192.0.2.-1')
        False
        >>> _isIPv4Addr('192.0..1')
        False
        >>> _isIPv4Addr('192.0.a.1')
        False
    """
    listStrIPv4Octet = strIPv4Addr.split('.')
    if (len(listStrIPv4Octet) != 4):
        return False

    for i in range(4):
        strOctet = ("00" + listStrIPv4Octet[i])[-3:]
        c1 = strOctet[0:1]
        c2 = strOctet[1:2]
        c3 = strOctet[2:3]
        if ((c1 < '0' or c1 > '9') or
            (c2 < '0' or c2 > '9') or
            (c3 < '0' or c3 > '9')):
            return False

        if (int(strOctet, 10) >= 256):
            return False

    return True


def _isIPv6Addr(strIPv6Addr):
    """Confirm whether the specified address is an IPv6 address.

    :param str strIPv6Addr: IPv6 address string that adopted the full
        represented.
    :return: True when the specified address is an IPv6 address.
    :rtype: bool

    Example::

        strIPv6Addr                                  Return
        ---------------------------------------------------
        '2001:0dB8:0000:0000:0000:0000:0000:0001' -> True
        '2001:0dB8:0000:0000:0000:0000:0001'      -> False
        '2001:0dB8:0000:0000:0000:0000:0000:001'  -> False
        '2001:0dB8:0000:0000:0000:0000:0000:000g' -> False

    Test:
        >>> _isIPv6Addr('2001:0dB8:0000:0000:0000:0000:0000:0001')
        True
        >>> _isIPv6Addr('2001:0dB8:0000:0000:0000:0000:0001')
        False
        >>> _isIPv6Addr('2001:0dB8:0000:0000:0000:0000:0000:001')
        False
        >>> _isIPv6Addr('2001:0dB8:0000:0000:0000:0000:0000:000g')
        False
    """
    listStrIPv6Hextet = strIPv6Addr.split(':')
    if (len(listStrIPv6Hextet) != 8):
        return False

    for i in range(8):
        strHextet = listStrIPv6Hextet[i]
        if (len(strHextet) != 4):
            return False

        c1 = strHextet[0:1]
        c2 = strHextet[1:2]
        c3 = strHextet[2:3]
        c4 = strHextet[3:4]
        if (((c1 >= '0' and c1 <= '9') or (c1 >= 'a' and c1 <= 'f') or (c1 >= 'A' and c1 <= 'F')) and
            ((c2 >= '0' and c2 <= '9') or (c2 >= 'a' and c2 <= 'f') or (c2 >= 'A' and c2 <= 'F')) and
            ((c3 >= '0' and c3 <= '9') or (c3 >= 'a' and c3 <= 'f') or (c3 >= 'A' and c3 <= 'F')) and
            ((c4 >= '0' and c4 <= '9') or (c4 >= 'a' and c4 <= 'f') or (c4 >= 'A' and c4 <= 'F'))):
            pass
        else:
            return False

    return True


def _toIPv4AddrInteger(strIPv4Addr):
    """Convert the IPv4 address string to the IPv4 address integer.

    :param str strIPv4Addr: IPv4 address string.
    :return: IPv4 address integer.
    :rtype: int

    Example::

        strIPv4Addr    Return
        -------------------------
        '192.0.2.1' -> 3221225985

    Test:
        >>> print(_toIPv4AddrInteger('192.0.2.1'))
        3221225985
    """
    listIPv4Octet = strIPv4Addr.split('.')
    return (
        (int(listIPv4Octet[0]) << 24) +
        (int(listIPv4Octet[1]) << 16) +
        (int(listIPv4Octet[2]) <<  8) +
         int(listIPv4Octet[3]))


def _toIPv4AddrString(intIPv4AddrInteger):
    """Convert the IPv4 address integer to the IPv4 address string.

    :param int intIPv4AddrInteger: IPv4 address integer.
    :return: IPv4 address string.
    :rtype: str

    Example::

        intIPv4AddrInteger    Return
        ---------------------------------
        3221225985         -> '192.0.2.1'

    Test:
        >>> _toIPv4AddrString(3221225985)
        '192.0.2.1'
    """
    return (
        str((intIPv4AddrInteger >> 24) & 0xFF) + '.' +
        str((intIPv4AddrInteger >> 16) & 0xFF) + '.' +
        str((intIPv4AddrInteger >>  8) & 0xFF) + '.' +
        str( intIPv4AddrInteger        & 0xFF))


def _toIPv6AddrInteger(strIPv6Addr):
    """Convert the IPv6 address string to the IPv6 address integer.

    :param str strIPv6Addr: IPv6 address string that adopted the full
        represented.
    :return: IPv6 address integer.
    :rtype: int

    Example::

        strIPv6Addr                                  Return
        -----------------------------------------------------------------------------------
        '2001:0dB8:0000:0000:0000:0000:0000:0001' -> 42540766411282592856903984951653826561

    Test:
        >>> print(_toIPv6AddrInteger('2001:0dB8:0000:0000:0000:0000:0000:0001'))
        42540766411282592856903984951653826561
    """
    listIPv6Hextet = strIPv6Addr.split(':')
    return (
        (int(listIPv6Hextet[0], 16) << 112) +
        (int(listIPv6Hextet[1], 16) <<  96) +
        (int(listIPv6Hextet[2], 16) <<  80) +
        (int(listIPv6Hextet[3], 16) <<  64) +
        (int(listIPv6Hextet[4], 16) <<  48) +
        (int(listIPv6Hextet[5], 16) <<  32) +
        (int(listIPv6Hextet[6], 16) <<  16) +
         int(listIPv6Hextet[7], 16))


def _toIPv6AddrString(intIPv6AddrInteger):
    """Convert the IPv6 address integer to the IPv6 address string.

    :param int intIPv6AddrInteger: IPv6 address integer.
    :return: IPv6 address string that adopted the full represented.
    :rtype: str

    Example::

        intIPv6AddrInteger                        Return
        -----------------------------------------------------------------------------------
        42540766411282592856903984951653826561 -> '2001:0db8:0000:0000:0000:0000:0000:0001'

    Test:
        >>> _toIPv6AddrString(42540766411282592856903984951653826561)
        '2001:0db8:0000:0000:0000:0000:0000:0001'
    """
    return (
        format(intIPv6AddrInteger >> 112 & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 96  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 80  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 64  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 48  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 32  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger >> 16  & 0xFFFF, '04x') + ':' +
        format(intIPv6AddrInteger        & 0xFFFF, '04x'))


def _makeIPv4SubnetFromRange(intStartAddr, intEndAddr, listSave):
    """Convert the IPv4 address range to IPv4 subnets.

    This function converts the IPv4 address range to IPv4 subnets
    represented in CIDR format and saves it into the specified list.
    However, network 0.0.0.0/0 is split into subnetworks 0.0.0.0/1 and
    128.0.0.0/1.

    :param int intStartAddr: Start address integer.
    :param int intEndAddr: End address integer.
    :param List[str] listSave: List to save IPv4 subnet strings.
    :return: None

    Example::

        intStartAddr intEndAddr    listSave
        -----------------------------------------------
        3221225985   3221225985 -> ['192.0.2.1/32']
        3221225985   3221226084 -> ['192.0.2.1/32',
                                    '192.0.2.2/31',
                                    '192.0.2.4/30',
                                    '192.0.2.8/29',
                                    '192.0.2.16/28',
                                    '192.0.2.32/27',
                                    '192.0.2.64/27',
                                    '192.0.2.96/30',
                                    '192.0.2.100/32']

    Test:
        >>> list = []
        >>> _makeIPv4SubnetFromRange(3221225985, 3221225985, list)
        >>> print(list)
        ['192.0.2.1/32']
        >>> list = []
        >>> _makeIPv4SubnetFromRange(3221225985, 3221226084, list)
        >>> print(list)  # doctest: +NORMALIZE_WHITESPACE
        ['192.0.2.1/32',
         '192.0.2.2/31',
         '192.0.2.4/30',
         '192.0.2.8/29',
         '192.0.2.16/28',
         '192.0.2.32/27',
         '192.0.2.64/27',
         '192.0.2.96/30',
         '192.0.2.100/32']
    """
    intSegSize = 2 << 30  # 2**31
    for i in range(1, 32 + 1):
        #
        # Example of round up and round down in 8 bits segment.
        #
        #       |<------ segment ------>|
        #     15 16 17 18 19 20 21 22 23 24
        #          |-> round up to 24
        #         round down to 15 <-|
        #
        intBlockStart = (intStartAddr + intSegSize - 1) // intSegSize * intSegSize  # Round up to the start of the next segment.
        intBlockEnd = ((intEndAddr + 1) // intSegSize * intSegSize) - 1  # Round down to the end of the previous segment.

        if (intBlockStart <= intBlockEnd):
            if (intStartAddr < intBlockStart):
                _makeIPv4SubnetFromRange(intStartAddr, intBlockStart - 1, listSave)

            intSegStart = intBlockStart
            intSegEnd = intSegStart + intSegSize - 1
            while (intSegEnd <= intBlockEnd):
                listSave.append(_toIPv4AddrString(intSegStart) + '/' + str(i))
                intSegStart += intSegSize
                intSegEnd = intSegStart + intSegSize - 1

            intStartAddr = intSegStart

            if (intBlockEnd < intEndAddr):
                _makeIPv4SubnetFromRange(intBlockEnd + 1, intEndAddr, listSave)
                intEndAddr = intBlockEnd

        intSegSize = intSegSize // 2


def _makeIPv6SubnetFromRange(intStartAddr, intEndAddr, listSave):
    """Convert the IPv6 address range to IPv6 subnets.

    This function converts the IPv6 address range to IPv6 subnets
    adopted the full represented and saves it into the specified list.
    However, network ::/0 is split into subnetworks ::/1 and 8000::/1.

    :param int intStartAddr: Start address integer.
    :param int intEndAddr: End address integer.
    :param List[str] listSave: List to save IPv6 subnet strings.
    :return: None

    Example::

        intStartAddr                           intEndAddr                                listSave
        --------------------------------------------------------------------------------------------------------------------------------
        42540766411282592856903984951653826561 42540766411282592856903984951653826561 -> ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
        42540766411282592856903984951653826561 42540766411282592856903984951653826660 -> ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0002/127',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0004/126',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0008/125',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0010/124',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0020/123',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0040/123',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0060/126',
                                                                                          '2001:0db8:0000:0000:0000:0000:0000:0064/128']

    Test:
        >>> list = []
        >>> _makeIPv6SubnetFromRange(42540766411282592856903984951653826561, 42540766411282592856903984951653826561, list)
        >>> print(list)
        ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
        >>> list = []
        >>> _makeIPv6SubnetFromRange(42540766411282592856903984951653826561, 42540766411282592856903984951653826660, list)
        >>> print(list)  # doctest: +NORMALIZE_WHITESPACE
        ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
         '2001:0db8:0000:0000:0000:0000:0000:0002/127',
         '2001:0db8:0000:0000:0000:0000:0000:0004/126',
         '2001:0db8:0000:0000:0000:0000:0000:0008/125',
         '2001:0db8:0000:0000:0000:0000:0000:0010/124',
         '2001:0db8:0000:0000:0000:0000:0000:0020/123',
         '2001:0db8:0000:0000:0000:0000:0000:0040/123',
         '2001:0db8:0000:0000:0000:0000:0000:0060/126',
         '2001:0db8:0000:0000:0000:0000:0000:0064/128']
    """
    intSegSize = 2 << 126  # 2**127
    for i in range(1, 128 + 1):
        #
        # Example of round up and round down in 8 bits segment.
        #
        #       |<------ segment ------>|
        #     15 16 17 18 19 20 21 22 23 24
        #          |-> round up to 24
        #         round down to 15 <-|
        #
        intBlockStart = (intStartAddr + intSegSize - 1) // intSegSize * intSegSize  # Round up to the start of the next segment.
        intBlockEnd = ((intEndAddr + 1) // intSegSize * intSegSize) - 1  # Round down to the end of the previous segment.

        if (intBlockStart <= intBlockEnd):
            if (intStartAddr < intBlockStart):
                _makeIPv6SubnetFromRange(intStartAddr, intBlockStart - 1, listSave)

            intSegStart = intBlockStart
            intSegEnd = intSegStart + intSegSize - 1
            while (intSegEnd <= intBlockEnd):
                listSave.append(_toIPv6AddrString(intSegStart) + '/' + str(i))
                intSegStart += intSegSize
                intSegEnd = intSegStart + intSegSize - 1

            intStartAddr = intSegStart

            if (intBlockEnd < intEndAddr):
                _makeIPv6SubnetFromRange(intBlockEnd + 1, intEndAddr, listSave)
                intEndAddr = intBlockEnd

        intSegSize = intSegSize // 2


# ============================================================================
# ============================================================================
if __name__ == "__main__":
    import doctest
    doctest.testmod()


# ============================================================================
# EOF
# ============================================================================
