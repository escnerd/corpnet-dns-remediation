import re
import time
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Regex Patterns
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
pat_fix_wrong_fe_hostname = re.compile("^[Ff](as?)?-?(?=-?\d{1,2})")
pat_fix_wrong_ge_hostname = re.compile("^[Gg](ig?|e)?-?(?=-?\d{1,2})")
pat_fix_wrong_te_hostname = re.compile("^[Tt](en?)?-?(?=-?\d{1,2})")
pat_fix_wrong_vlan_int = re.compile("^([Vv](lan|-)|V)")
pat_fixable_wrong_hsrp = re.compile("^([Hh][Ss][Rr][Pp]).*?(\d+)(?=-)")
# pat_fix_wrong_site_fl_dev = re.compile("^[A-Za-z]{3}(?=\d{1,2}-\d{1,2}-)")
# pat_fix_wrong_site_dev = re.compile("^[A-Za-z]{3}(?=\d{1,2}-)")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Called by formatVet.py functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def wrong_fe(hostname, ip):
    """ Uses substitution method to replace errant 'fe' interface spelling(s) """
    corrected_format = re.sub(pat_fix_wrong_fe_hostname,'fe',hostname.group()) + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ": Bad fast ethernet interface entry detected:\t" + hostname.group() + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*5 + corrected_format.lower()
    return corrected_format.lower()


def wrong_ge(hostname, ip):
    """ Uses substitution method to replace errant 'ge' interface spelling(s) """
    corrected_format = re.sub(pat_fix_wrong_ge_hostname,'ge',hostname.group()) + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ": Bad gigabit ethernet interface entry detected:\t" + hostname.group() + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*5 + corrected_format.lower()
    return corrected_format.lower()


def wrong_te(hostname, ip):
    """ Uses substitution method to replace errant 'te' interface spelling(s) """
    corrected_format = re.sub(pat_fix_wrong_te_hostname,'te',hostname.group()) + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ": Bad ten gigabit ethernet interface entry detected:\t" + hostname.group() + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*6 + corrected_format.lower()
    return corrected_format.lower()


def wrong_vlan_int(hostname, ip):
    """ Uses substitution method to fix vlan entry format """
    corrected_format = re.sub(pat_fix_wrong_vlan_int,'v',hostname.group()) + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ": Bad vlan interface entry detected:\t" + hostname.group() + ' ' + ip.group()
    print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*4 + corrected_format.lower()
    return corrected_format.lower()


def wrong_hsrp(hostname, ip):
    """ Uses substitution method w/ repl_hsrp() to fix hsrp entry format """
    fixable_hsrp = re.search(pat_fixable_wrong_hsrp, hostname.group())
    if fixable_hsrp:
        corrected_format = re.sub(pat_fixable_wrong_hsrp,repl_hsrp,hostname.group()) + ' ' + ip.group()
        print time.strftime("%b%d-%H:%M:%S") + ": Bad hsrp entry detected:\t" + hostname.group() + ' ' + ip.group()
        print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*3 + corrected_format.lower()
        return corrected_format.lower()
    else:
        # exmaples of hsrp entries that aren't fixable because the entry itself does not contain enough information:
        # hsrp-v11.corpnet.ebay.com -- There's no site code; hsrp-v11 of what?
        # hsrp.sjc-7206.corpnet.ebay.com -- Looks like this one is in its own .sjc-7206 subdomain, no site code either
        print time.strftime("%b%d-%H:%M:%S") + ": Unfixable hsrp entry detected (probably should just be deleted):\t" + hostname.group() + ' ' + ip.group()
        return '\tNot fixable & should probably just be deleted:' + hostname.group()


#def wrong_site_fl_dev(hostname, ip):
#	""" Currently, entries that land here only need to be lower-cased to correct.
#	Refex pattern is already created, though commented out on top """
#	corrected_format = hostname.group() + ' ' + ip.group()
#	print time.strftime("%b%d-%H:%M:%S") + ": Bad site-fl-dev entry detected:\t" + hostname.group() + ' ' + ip.group()
#	print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*3 + corrected_format.lower()
#	return corrected_format.lower()
#
#
#def wrong_site_dev(hostname, ip):
#	""" Currently, entries that land here only need to be lower-cased to correct.
#	Refex pattern is already created, though commented out on top """
#	corrected_format = hostname.group() + ' ' + ip.group()
#	print time.strftime("%b%d-%H:%M:%S") + ": Bad site-dev entry detected:\t" + hostname.group() + ' ' + ip.group()
#	print time.strftime("%b%d-%H:%M:%S") + ': Should be:' + '\t'*3 + corrected_format.lower()
#	return corrected_format.lower()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Replacement functions for re.sub
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def repl_hsrp(matchobj):
    """ matchobj(2) should be the vlan number """
    return 'v' + matchobj.group(2) + '-hsrp'
