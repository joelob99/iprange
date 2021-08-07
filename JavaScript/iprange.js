/*!
* ============================================================================
*
* IP range
*
* iprange.js
*
* Copyright (c) 2021 joelob99
*
* Released under the MIT License, see LICENSE.txt.
*
* History
*   2021-08-07: First Release, v1.0.0.
*
* @file This script provides classes that IP range to subnets conversion.
* @copyright joelob99 2021
* @license MIT License
* @version v1.0.0
*
* ============================================================================
*/

'use strict';

/**
* This class is the base class of ip range exception classes.
*
* See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
*/
class IPRangeException extends Error {
    constructor(...params) {
        super(...params);
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, IPRangeException)
        }
        this.name = this.constructor.name;

    }
}

/**
* This class is the exception class for ip range address error.
*
*/
class IPRangeAddressError extends IPRangeException {
    constructor(...params) {
        super(...params);
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, IPRangeAddressError)
        }
        this.name = this.constructor.name;
    }
}

/**
* This class is the base class of ip range classes.
*
*/
class IPRange {
    /**
    * This constructor defines variables for IPRange class.
    *
    */
    constructor() {
        this._intStartAddr = undefined;
        this._intEndAddr = undefined;
        this._arraySubnet = undefined;
    }

    /**
    * This getter returns the subnet strings array.
    *
    * @return {Array} Subnet strings array.
    * @throws {IPRangeAddressError}
    *   Will throw if the address range is not set.
    *
    */
    get subnet() {
        if (this._arraySubnet == undefined) {
            throw new IPRangeAddressError();
        }
        return this._arraySubnet;
    }
}

/**
* This class operates the IPv4 address range.
*
*/
class IPv4Range extends IPRange {
    /**
    * This getter returns the IPv4 address range string.
    *
    * @return {string} IPv4 address range string.
    * @throws {IPRangeAddressError} Will throw if the address range is not set.
    *
    * @example
    *   intStartAddr intEndAddr    Return
    *   ------------------------------------------------------
    *   3232235521   3232235620 -> '192.168.0.1-192.168.0.100'
    */
    get iprange() {
        if (this._intStartAddr == undefined || this._intEndAddr == undefined) {
            throw new IPRangeAddressError();
        }
        return _toIPv4AddrString(this._intStartAddr) + '-' + _toIPv4AddrString(this._intEndAddr);
    }

    /**
    * This setter saves integers of the start and end address of the specified
    * IPv4 address range string and makes the subnet lists.
    *
    * @param {string} strIPv4Range - IPv4 address range string.
    * @throws {IPRangeAddressError} Will throw if the invalid address range.
    *
    * @example
    *   strIPv4Range                   intStartAddr intEndAddr arraySubnet
    *   ---------------------------------------------------------------------------
    *   '192.168.0.1'               -> 3232235521   3232235521 ['192.168.0.1/32']
    *   '192.168.0.1-192.168.0.1'   -> 3232235521   3232235521 ['192.168.0.1/32']
    *   '192.168.0.1-192.168.0.100' -> 3232235521   3232235620 ['192.168.0.1/32',
    *                                                           '192.168.0.2/31',
    *                                                           '192.168.0.4/30',
    *                                                           '192.168.0.8/29',
    *                                                           '192.168.0.16/28',
    *                                                           '192.168.0.32/27',
    *                                                           '192.168.0.64/27',
    *                                                           '192.168.0.96/30',
    *                                                           '192.168.0.100/32']
    */
    set iprange(strIPv4Range) {
        const array = strIPv4Range.indexOf('-') != -1 ? strIPv4Range.split('-') : [strIPv4Range, strIPv4Range];
        if (!_isIPv4Addr(array[0]) || !_isIPv4Addr(array[1])) {
            throw new IPRangeAddressError();
        }
        this._intStartAddr = _toIPv4AddrInteger(array[0]);
        this._intEndAddr = _toIPv4AddrInteger(array[1]);

        if (this._intStartAddr > this._intEndAddr) {
            throw new IPRangeAddressError();
        }

        this._arraySubnet = [];
        _makeIPv4SubnetFromRange(this._intStartAddr, this._intEndAddr, this._arraySubnet);
    }
}

/**
* This class operates the IPv6 address range.
*
*/
class IPv6Range extends IPRange {
    /**
    * This getter returns the IPv6 address range string.
    *
    * @return {string} IPv6 address range string.
    * @throws {IPRangeAddressError} Will throw if the address range is not set.
    *
    * @example
    *   intStartAddr                           intEndAddr                                Return
    *   ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    *   42540766411282592856903984951653826561 42540766411282592856903984951653826660 -> '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064'
    */
    get iprange() {
        if (this._intStartAddr == undefined || this._intEndAddr == undefined) {
            throw new IPRangeAddressError();
        }
        return _toIPv6AddrString(this._intStartAddr) + '-' + _toIPv6AddrString(this._intEndAddr);
    }

    /**
    * This setter saves integers of the start and end address of the specified
    * IPv6 address range string and makes the subnet lists.
    *
    * @param {string} strIPv6Range - IPv6 address range string.
    * @throws {IPRangeAddressError} Will throw if the invalid address range.
    *
    * @example
    *   strIPv6Range                                                                         intStartAddr                           intEndAddr                             arraySubnet
    *   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    *   '2001:0db8:0000:0000:0000:0000:0000:0001'                                         -> 42540766411282592856903984951653826561 42540766411282592856903984951653826561 ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
    *   '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0001' -> 42540766411282592856903984951653826561 42540766411282592856903984951653826561 ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
    *   '2001:0db8:0000:0000:0000:0000:0000:0001-2001:0db8:0000:0000:0000:0000:0000:0064' -> 42540766411282592856903984951653826561 42540766411282592856903984951653826660 ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0002/127',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0004/126',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0008/125',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0010/124',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0020/123',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0040/123',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0060/126',
    *                                                                                                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0064/128']
    */
    set iprange(strIPv6Range) {
        const array = strIPv6Range.indexOf('-') != -1 ? strIPv6Range.split('-') : [strIPv6Range, strIPv6Range];
        if (!_isIPv6Addr(array[0]) || !_isIPv6Addr(array[1])) {
            throw new IPRangeAddressError();
        }
        this._intStartAddr = _toIPv6AddrInteger(array[0]);
        this._intEndAddr = _toIPv6AddrInteger(array[1]);

        if (this._intStartAddr > this._intEndAddr) {
            throw new IPRangeAddressError();
        }

        this._arraySubnet = [];
        _makeIPv6SubnetFromRange(this._intStartAddr, this._intEndAddr, this._arraySubnet);
    }
}

/**
* This function confirms whether the specified address is an IPv4 address.
*
* @param {string} strIPv4Addr - IPv4 address string.
* @return {boolean} true when the specified address an is IPv4 address.
*
* @example
*   strIPv4Addr        Return
*   -------------------------
*   '192.168.0.1'   -> True
*   '192.168.1'     -> False
*   '192.168.0.256' -> False
*   '192.168.0.-1'  -> False
*/
function _isIPv4Addr(strIPv4Addr) {
    const arrayStrIPv4Octet = strIPv4Addr.split('.');
    if (arrayStrIPv4Octet.length != 4) {
        return false;
    }
    for (let i=0; i<4; ++i) {
        let intOctet = parseInt(arrayStrIPv4Octet[i], 10);
        if (intOctet >= 256 || intOctet < 0) {
            return false;
        }
    }
    return true;
}

/**
*  This function confirms whether the specified address is an IPv6 address.
*
*  @param {string} strIPv6Addr -
*    IPv6 address string that adopted the full represented.
*  @return {boolean} true when the specified address is an IPv6 address.
*
*  @example
*    strIPv6Addr                                  Return
*    ---------------------------------------------------
*    '2001:0db8:0000:0000:0000:0000:0000:0001' -> True
*    '2001:0db8:0000:0000:0000:0000:0001'      -> False
*    '2001:0db8:0000:0000:0000:0000:0000:001'  -> False
*    '2001:0db8:0000:0000:0000:0000:0000:000g' -> False
*/
function _isIPv6Addr(strIPv6Addr) {
    const arrayStrIPv6Hextet = strIPv6Addr.split(':');
    if (arrayStrIPv6Hextet.length != 8) {
        return false;
    }
    for (let i=0; i<8; ++i) {
        let strHextet = arrayStrIPv6Hextet[i]
        if (strHextet.length != 4) {
            return false;
        }

        let c1 = strHextet.substring(0, 1);
        let c2 = strHextet.substring(1, 2);
        let c3 = strHextet.substring(2, 3);
        let c4 = strHextet.substring(3, 4);
        if (((c1 >= '0' && c1 <= '9') || (c1 >= 'a' && c1 <= 'f')) &&
            ((c2 >= '0' && c2 <= '9') || (c2 >= 'a' && c2 <= 'f')) &&
            ((c3 >= '0' && c3 <= '9') || (c3 >= 'a' && c3 <= 'f')) &&
            ((c4 >= '0' && c4 <= '9') || (c4 >= 'a' && c4 <= 'f'))) {
            // Nothing to do.
        } else {
            return false;
        }
    }
    return true;
}

/**
* This function converts the IPv4 address string to the IPv4 address integer.
*
* @param {string} strIPv4Addr - IPv4 address string.
* @return {number} IPv4 address integer.
*
* @example
*   strIPv4Addr      Return
*   ---------------------------
*   '192.168.0.1' -> 3232235521
*/
function _toIPv4AddrInteger(strIPv4Addr) {
    const arrayIPv4Octet = strIPv4Addr.split('.');
    return (parseInt(arrayIPv4Octet[0], 10) * 16777216 +
            parseInt(arrayIPv4Octet[1], 10) * 65536 +
            parseInt(arrayIPv4Octet[2], 10) * 256 +
            parseInt(arrayIPv4Octet[3], 10));
}

/**
* This function converts the IPv4 address integer to the IPv4 address string.
*
* @param {number} intIPv4AddrInteger - IPv4 address integer.
* @return {string} IPv4 address string.
*
* @example
*   intIPv4AddrInteger    Return
*   -----------------------------------
*   3232235521         -> '192.168.0.1'
*/
function _toIPv4AddrString(intIPv4AddrInteger) {
    return (((intIPv4AddrInteger >>> 24) & 0xFF).toString(10) + '.' +
            ((intIPv4AddrInteger >>> 16) & 0xFF).toString(10) + '.' +
            ((intIPv4AddrInteger >>>  8) & 0xFF).toString(10) + '.' +
            ( intIPv4AddrInteger         & 0xFF).toString(10));
}

/**
* This function converts the IPv6 address string to the IPv6 address integer.
*
* @param {string} strIPv6Addr -
*   IPv6 address string that adopted the full represented.
* @return {number} IPv6 address integer.
*
* @example
*   strIPv6Addr                                  Return
*   ------------------------------------------------------------------------------------
*   '2001:0db8:0000:0000:0000:0000:0000:0001' -> 42540766411282592856903984951653826561n
*/
function _toIPv6AddrInteger(strIPv6Addr) {
    const arrayIPv6Hextet = strIPv6Addr.split(':');
    return (
        BigInt('0x' + arrayIPv6Hextet[0]) * 5192296858534827628530496329220096n + // 2n**112n
        BigInt('0x' + arrayIPv6Hextet[1]) * 79228162514264337593543950336n +      // 2n**96n
        BigInt('0x' + arrayIPv6Hextet[2]) * 1208925819614629174706176n +          // 2n**80n
        BigInt('0x' + arrayIPv6Hextet[3]) * 18446744073709551616n +               // 2n**64n
        BigInt('0x' + arrayIPv6Hextet[4]) * 281474976710656n +                    // 2n**48n
        BigInt('0x' + arrayIPv6Hextet[5]) * 4294967296n +                         // 2n**32n
        BigInt('0x' + arrayIPv6Hextet[6]) * 65536n +                              // 2n**16n
        BigInt('0x' + arrayIPv6Hextet[7]));
}

/**
* This function converts the IPv6 address integer to the IPv6 address string.
*
* @param {number} bintIPv6AddrInteger - IPv6 address integer.
* @return {string} IPv6 address string that adopted the full represented.
*
* @example
*   bintIPv6AddrInteger                        Return
*   ------------------------------------------------------------------------------------
*   42540766411282592856903984951653826561n -> '2001:0db8:0000:0000:0000:0000:0000:0001'
*/
function _toIPv6AddrString(bintIPv6AddrInteger) {
    return (
        ('000' + (bintIPv6AddrInteger / 5192296858534827628530496329220096n & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 79228162514264337593543950336n      & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 1208925819614629174706176n          & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 18446744073709551616n               & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 281474976710656n                    & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 4294967296n                         & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger / 65536n                              & 0xFFFFn).toString(16)).slice(-4) + ':' +
        ('000' + (bintIPv6AddrInteger                                       & 0xFFFFn).toString(16)).slice(-4));
}
/**
* This function converts the IPv4 address range to IPv4 subnets represented in
* CIDR format and saves it into the specified array. However, network
* 0.0.0.0/0 is split into subnetworks 0.0.0.0/1 and 128.0.0.0/1.
*
* @param {number} intStartAddr - Start address integer.
* @param {number} intEndAddr - End address integer.
* @param {Array} arraySave - Array to save IPv4 subnet strings.
*
* @example
*   intStartAddr intEndAddr    arraySave
*   -----------------------------------------------
*   3232235521   3232235521 -> ['192.168.0.1/32']
*   3232235521   3232235620 -> ['192.168.0.1/32',
*                               '192.168.0.2/31',
*                               '192.168.0.4/30',
*                               '192.168.0.8/29',
*                               '192.168.0.16/28',
*                               '192.168.0.32/27',
*                               '192.168.0.64/27',
*                               '192.168.0.96/30',
*                               '192.168.0.100/32']
*/
function _makeIPv4SubnetFromRange(intStartAddr, intEndAddr, arraySave) {
    let intSegSize = 2147483648;
    for (let i=1; i<=32; ++i) {
        //
        // Example of round up and round down in 8 bits segment.
        //
        //       |<------ segment ------>|
        //     15 16 17 18 19 20 21 22 23 24
        //          |-> round up to 24
        //         round down to 15 <-|
        //
        const intBlockStart = Math.trunc((intStartAddr + intSegSize - 1) / intSegSize) * intSegSize; // Round up to the start of the next segment.
        const intBlockEnd = (Math.trunc((intEndAddr + 1) / intSegSize) * intSegSize) - 1; // Round down to the end of the previous segment.

        if (intBlockStart <= intBlockEnd) {
            if (intStartAddr < intBlockStart) {
                _makeIPv4SubnetFromRange(intStartAddr, intBlockStart - 1, arraySave);
            }
            let intSegStart = intBlockStart;
            let intSegEnd = intSegStart + intSegSize - 1;
            while (intSegEnd <= intBlockEnd) {
                arraySave.push(_toIPv4AddrString(intSegStart) + '/' + i);

                intSegStart += intSegSize;
                intSegEnd = intSegStart + intSegSize - 1;
            }
            intStartAddr = intSegStart;

            if (intBlockEnd < intEndAddr) {
                _makeIPv4SubnetFromRange(intBlockEnd + 1, intEndAddr, arraySave);
                intEndAddr = intBlockEnd;
            }
        }
        intSegSize = Math.trunc(intSegSize / 2);
    }
}
/**
* This function converts the IPv6 address range to IPv6 subnets adopted the
* full represented and saves it into the specified array. However, network
* ::/0 is split into subnetworks ::/1 and 8000::/1.
*
* @param {number} bintStartAddr - Start address integer.
* @param {number} bintEndAddr - End address integer.
* @param {Array} arraySave - Array to save IPv6 subnet strings.
*
* @example
*   bintStartAddr                            bintEndAddr                               arraySave
*   ----------------------------------------------------------------------------------------------------------------------------------
*   42540766411282592856903984951653826561n 42540766411282592856903984951653826561n -> ['2001:0db8:0000:0000:0000:0000:0000:0001/128']
*   42540766411282592856903984951653826561n 42540766411282592856903984951653826660n -> ['2001:0db8:0000:0000:0000:0000:0000:0001/128',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0002/127',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0004/126',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0008/125',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0010/124',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0020/123',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0040/123',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0060/126',
*                                                                                       '2001:0db8:0000:0000:0000:0000:0000:0064/128']
*/
function _makeIPv6SubnetFromRange(bintStartAddr, bintEndAddr, arraySave) {
    let bintSegSize = 170141183460469231731687303715884105728n; // 2n**127n
    for (let i=1n; i<=128n; ++i) {
        //
        // Example of round up and round down in 8 bits segment.
        //
        //       |<------ segment ------>|
        //     15 16 17 18 19 20 21 22 23 24
        //          |-> round up to 24
        //         round down to 15 <-|
        //
        const bintBlockStart = (bintStartAddr + bintSegSize - 1n) / bintSegSize * bintSegSize; // Round up to the start of the next segment.
        const bintBlockEnd = ((bintEndAddr + 1n) / bintSegSize * bintSegSize) - 1n; // Round down to the end of the previous segment.

        if (bintBlockStart <= bintBlockEnd) {
            if (bintStartAddr < bintBlockStart) {
                _makeIPv6SubnetFromRange(bintStartAddr, bintBlockStart - 1n, arraySave);
            }
            let bintSegStart = bintBlockStart;
            let bintSegEnd = bintSegStart + bintSegSize - 1n;
            while (bintSegEnd <= bintBlockEnd) {
                arraySave.push(_toIPv6AddrString(bintSegStart) + '/' + i);

                bintSegStart += bintSegSize;
                bintSegEnd = bintSegStart + bintSegSize - 1n;
            }
            bintStartAddr = bintSegStart;

            if (bintBlockEnd < bintEndAddr) {
                _makeIPv6SubnetFromRange(bintBlockEnd + 1n, bintEndAddr, arraySave);
                bintEndAddr = bintBlockEnd;
            }
        }
        bintSegSize = bintSegSize / 2n;
    }
}

// ===========================================================================
// ===========================================================================

if (typeof module !== 'undefined') { // module is not defined in browsers.
    module.exports = {
        IPRangeException, IPRangeAddressError, IPRange, IPv4Range, IPv6Range,
        _isIPv4Addr, _toIPv4AddrInteger, _toIPv4AddrString, _makeIPv4SubnetFromRange, // Export for testing.
        _isIPv6Addr, _toIPv6AddrInteger, _toIPv6AddrString, _makeIPv6SubnetFromRange, // Export for testing.
    };
}

// ===========================================================================
// EOF
// ===========================================================================
