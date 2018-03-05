#!/usr/bin/env python
import sys
import time
import entryID
import formatVet


def main(argv):
    fh_dns = open(sys.argv[1], "r")

    for line in fh_dns:
        if entryID.is_A_record(line):

            if entryID.is_corpnet(line):
                formatVet.corpnet(line)
            elif entryID.is_corp(line):
                formatVet.igln(line)
            elif entryID.is_its_zone(line):
                formatVet.igln(line)
            elif entryID.is_sjc_zone(line):
                formatVet.igln(line)
            elif entryID.is_weird_ip(line):
                formatVet.igln(line)
            else:
                print time.strftime("%b%d-%H:%M:%S") + ": Unrecognized A record detected:\t" + line.rstrip()

        elif entryID.is_CNAME_record(line):
            formatVet.cname(line)
        elif entryID.is_AAAA_record(line):
            formatVet.igln(line)
        elif entryID.is_comment(line):
            formatVet.igln(line)
        elif entryID.is_NS_record(line):
            formatVet.igln(line)
        elif entryID.is_SOA_record(line):
            formatVet.igln(line)
        elif entryID.is_whitespace(line):
            formatVet.igln(line)
        else:
            print time.strftime("%b%d-%H:%M:%S") + ": Unrecognized type of entry detected:\t" + line.rstrip()

    fh_dns.close()
    formatVet.flush_out()


if __name__ == "__main__":
    main(sys.argv[1:])