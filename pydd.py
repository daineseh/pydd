#!/usr/bin/env python2.7

import os
import sys

def usage():
    msg = '''
Usage: %s <arg1> <arg2> <arg3>

Arguments:
    <arg1> :            Set the input source.
    /path/to/file       # Set a path to a file or fifo

    <arg2> :            Set the output destination.
    /path/to/file       # Output to a file.

    <arg3> :            Set the blocksize (in bytes only: Default 4096000).

    --help :           Show this help screen.
    '''
    print msg

def main():
    bs = 4096000  # 4MB

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

    if len(sys.argv) == 4 and isinstance(sys.argv[3], int):
        bs = sys.argv[3]

    total_size = 0.0
    try:
        buff = src_fp.read(bs)
        while buff:
            dst_fp.write(buff)
            total_size += len(buff)
            buff = src_fp.read(bs)
#             print total_size, '/', src_size
            print format(total_size / src_size, '.2%')
        print "Bye!"
    except KeyboardInterrupt:
        print
        sys.exit(1)

if __name__ == '__main__':
#     sys.argv.extend(['SOURCE', 'DESTINATION', 'BITRATE(BYTE)])
    sys.argv.extend(['--help'])
    main()
