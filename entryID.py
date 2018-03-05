import re
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Regex Patterns
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
pat_A_record = re.compile("(?=\\b(\d)+(\s)+IN(\s)+A\\b)")
pat_AAAA_record = re.compile("(?=\\b(\d)+(\s)+IN(\s)+AAAA\\b)")
pat_CNAME_record = re.compile("(?=\\b(\d)+(\s)+IN(\s)+CNAME\\b)")
pat_comment = re.compile("(?=^(;)+)")
pat_NS_record = re.compile("(?=\\b(\d)+(\s)+IN(\s)+NS\\b)")
pat_SOA_record = re.compile("(?=\\b(\d)+(\s)+IN(\s)+SOA\\b)")
pat_weird_ip = re.compile("(?=^(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){4})")
pat_its_zone = re.compile("(?=\.its\.ebay\.com\.(\s)+(\d)+)")
pat_sjc_zone = re.compile("(?=\.sjc\.ebay\.com\.(\s)+(\d)+)")
pat_corpnet = re.compile("(?=\.corpnet\.ebay\.com\.(\s)+(\d)+)")
pat_corp = re.compile("(?=\.corp\.ebay\.com\.(\s)+(\d)+)")
pat_csr = re.compile()
pat_whitespace = re.compile("^\s+$")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The following tests to see what type of DNS record the input line is
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def is_A_record(line):
    """Is this line an A record?"""
    if re.search(pat_A_record, line):
        return True

def is_AAAA_record(line):
    """Is this line an AAAA record?"""
    if re.search(pat_AAAA_record, line):
        return True

def is_CNAME_record(line):
    """Is this line an SOA record?"""
    if re.search(pat_CNAME_record, line):
        return True

def is_comment(line):
    """Is this line a comment?"""
    if re.search(pat_comment, line):
        return True

def is_NS_record(line):
    """Is this line an NS record?"""
    if re.search(pat_NS_record, line):
        return True

def is_SOA_record(line):
    """Is this line an SOA record?"""
    if re.search(pat_SOA_record, line):
        return True

def is_whitespace(line):
    """Is this line just whitespace?"""
    if re.search(pat_whitespace, line):
        return True
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The following tests  to see what type of A record entry the input line is
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def is_weird_ip(line):
    """Is this line that single ip entry (10.244.80.36.)"""
    if re.search(pat_weird_ip, line):
        return True

def is_its_zone(line):
    """Is this line an .its.ebay.com. entry"""
    if re.search(pat_its_zone, line):
        return True

def is_sjc_zone(line):
    """Is this line an .sjc.ebay.com. entry?"""
    if re.search(pat_sjc_zone, line):
        return True

def is_corpnet(line):
    """Is this line a .corpnet.ebay.com. entry?"""
    if re.search(pat_corpnet, line):
        return True

def is_corp(line):
    """Is this line a .corp.ebay.com. entry? """
    if re.search(pat_corp, line):
        return True
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The following tests to see what type of .corpnet record entry the input line is
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def is_corpnet(line):
    """Is this a 'csr' device?"""
    if re.search(pat_csr, line):
        return True

