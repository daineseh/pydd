#!/usr/bin/env python2.7

import os
import re
import sys

def usage():
    msg = '''
Usage: %s <arg1> <arg2> <arg3>

Arguments:
    <arg1> :            Set the input source.
    /path/to/file       # Set a path to a file or fifo

    <arg2> :            Set the output destination.
    /path/to/file       # Output to a file.

    <arg3> :            Set the blocksize (Default 1MB).
    256, 512            # bytes presentation
    16k or 32kb         # kilobytes presentation
    64M or 128MB        # megabytes presentation

    --help :           Show this help screen.
    '''
    print msg

def human_readable_size_converter(bytes_size):
    kbyte = 1024
    mbyte = (kbyte ** 2)
    gbyte = (kbyte ** 3)
    tbyte = (kbyte ** 4)
    pbyte = (kbyte ** 5)
    ebyte = (kbyte ** 6)
    zbyte = (kbyte ** 7)

    if bytes_size < kbyte:
        retv = '%dB' % int(bytes_size)
        return '%9s' % retv
    elif bytes_size >= kbyte and bytes_size < mbyte:
        retv = '%04.02fKB' % (float(bytes_size) / float(kbyte))
        return '%9s' % retv
    elif bytes_size >= mbyte and bytes_size < gbyte:
        retv = '%04.02fMB' % (float(bytes_size) / float(mbyte))
        return '%9s' % retv
    elif bytes_size >= gbyte and bytes_size < tbyte:
        retv = '%04.02fGB' % (float(bytes_size) / float(gbyte))
        return '%9s' % retv
    elif bytes_size >= tbyte and bytes_size < pbyte:
        retv = '%04.02fTB' % (float(bytes_size) / float(tbyte))
        return '%9s' % retv
    elif bytes_size >= pbyte and bytes_size < ebyte:
        retv = '%04.02fPB' % (float(bytes_size) / float(pbyte))
        return '%9s' % retv
    elif bytes_size >= ebyte and bytes_size < zbyte:
        retv = '%04.02fEB' % (float(bytes_size) / float(ebyte))
        return '%9s' % retv
    else:
        retv = '%04.02fZB' % (float(bytes_size) / float(zbyte))
        return '%9s' % retv


def bs_size_conv(size):
    assert isinstance(size, str)
    if not size.isdigit():
        pass
    return int(size)


def bs_format_checker(bs_str):
    re_pat = re.compile(r'(?P<VALUE>\d+)(?P<UNIT>[A-Za-z]{0,2})')
    result = re_pat.search(bs_str)
    if not result:
        return False

    if result.group('UNIT'):
        unit = result.group('UNIT').lower()
        if unit not in ['k', 'kb', 'm', 'mb', 'g', 'gb', 't', 'tb',
                        'p', 'pb', 'e', 'eb', 'z', 'zb']:
            return False

    if result.group('VALUE'):
        value = int(result.group('VALUE'))
        if value <= 0:
            return False

    return True


class BS(object):
    def __init__(self):
        self._search_pat = re.compile(r'(?P<NUMBER>\d+)(?P<UNIT>[A-Za-z]{0,2})')
        self._unit = 'bytes'
        self._number = 0

    def _get_size(self):
        kbyte = 1024
        mbyte = (kbyte ** 2)
        gbyte = (kbyte ** 3)
        tbyte = (kbyte ** 4)
        pbyte = (kbyte ** 5)
        ebyte = (kbyte ** 6)
        zbyte = (kbyte ** 7)

        if self._unit == 'bytes':
            return self._number
        elif self._unit == 'kbyte':
            return self._number * kbyte
        elif self._unit == 'mbyte':
            return self._number * mbyte
        elif self._unit == 'gbyte':
            return self._number * gbyte
        elif self._unit == 'tbyte':
            return self._number * tbyte
        elif self._unit == 'pbyte':
            return self._number * pbyte
        elif self._unit == 'ebyte':
            return self._number * ebyte
        elif self._unit == 'zbyte':
            return self._number * zbyte

    def set_data(self, raw_str):
        result = self._search_pat.search(raw_str)
        if not result:
            return False

        if result.group('UNIT'):
            unit = result.group('UNIT').lower()
            if unit in ['k', 'kb']:
                unit = 'kbyte'
            elif unit in['m', 'mb']:
                unit = 'mbyte'
            elif unit in['g', 'gb']:
                unit = 'gbyte'
            elif unit in['t', 'tb']:
                unit = 'tbyte'
            elif unit in['p', 'pb']:
                unit = 'pbyte'
            elif unit in['e', 'eb']:
                unit = 'ebyte'
            elif unit in['z', 'zb']:
                unit = 'zbyte'
            else:
                return False

            self._unit = unit


        if result.group('NUMBER'):
            number = int(result.group('NUMBER'))
            if number <= 0:
                return False

            self._number = number

        return True

    def get_value_by_bytes(self):
        return self._get_size()

    def get_default_value_by_bytes(self):
        kbyte = 1024
        mbyte = (kbyte ** 2)
        return mbyte  # 1mb


def main():
    if sys.argv[1] == '--help':
        usage()
        sys.exit(0)

    if len(sys.argv) < 3:
        usage()

    src = sys.argv[1]
    src_fp = open(src, 'r')
    src_size = float(os.stat(src).st_size)

    dst = sys.argv[2]
    dst_fp = open(dst, 'w+')

    bs_obj = BS()
    if len(sys.argv) == 4:
        if not bs_obj.set_data(sys.argv[3]):
            return
        bs = bs_obj.get_value_by_bytes()
    else:
        bs = bs_obj.get_default_value_by_bytes()

    total_size = 0.0
    try:
        buff = src_fp.read(bs)
        while buff:
            dst_fp.write(buff)
            total_size += len(buff)
            buff = src_fp.read(bs)
            print format(total_size / src_size, '.2%')
        print "Done!"
    except KeyboardInterrupt:
        print
        sys.exit(1)

if __name__ == '__main__':
#     sys.argv.extend(['SOURCE', 'DESTINATION', 'BITRATE])
    sys.argv.extend(['--help'])
    main()
