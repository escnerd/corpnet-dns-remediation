import re
import time
import autofix
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Global Variables
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
breaker = False
l_remove = []
l_add = []
l_cname = []
l_ignored = []
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Regex Patterns
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
pat_ip = re.compile("(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])(\.){0,1}){4}$")
pat_serial = re.compile("^[Ss]e?\d{1}-\d{1}-(\d-)?.*\.corpnet\.ebay\.com\.")
pat_capture_1st_group = re.compile(".*(?=\s+\d+\s+)")
pat_cname_capture_2nd_group = re.compile("(?<=CNAME\s).*\.ebay\.com\.$")
pat_wrong_vlan = re.compile("^[Vv](lan|-)\d*\..*\.corpnet\.ebay\.com\.")
pat_wrong_hsrp = re.compile("^[Hh][Ss][Rr][Pp].*\.corpnet\.ebay\.com\.")
pat_wrong_fe = re.compile("^[Ff](a|as)?(\d|-).*\.corpnet\.ebay\.com\.")
pat_wrong_ge = re.compile("^[Gg](i|e-\d|ig)?(\d|-).*\.corpnet\.ebay\.com\.")
pat_wrong_te = re.compile("^[Tt](i|e-\d|en)?(\d|-).*\.corpnet\.ebay\.com\.")
#pat_wrong_site_fl_dev = re.compile("^([A-Z]{3}|[A-Z][a-z]{2})\d-\d{1,2}-\w{2}\d{2}\.corpnet\.ebay\.com\.")
#pat_wrong_site_dev = re.compile("^([A-Z]{3}|[A-Z][a-z]{2})\d-[a-z]{2}.*\.corpnet\.ebay\.com\.")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Main fucntion(s)
# Currently only .corpnet.ebay.com. A records are vetted. But other(s) may be
# implemented in the future, such as other main functions that would handle:
# - its.ebay.com.
# - sjc.ebay.com.
# - corp.ebay.com.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def corpnet(line):
	"""Figure out what type of .corpnet entry it is, then fix it accordingly"""
	global breaker

	while not breaker:
		int_vlan(line)
		if breaker: break
		int_dev(line)
		if breaker: break
		hsrp(line)
		if breaker: break
		int_serial(line)
		break
	breaker = False
	return

def cname(line):
	"""Detect CNAME entries, then put them in a list"""
	global l_cname
	
	hostname = re.search(pat_capture_1st_group, line)
	c = re.search(pat_cname_capture_2nd_group, line)
	if not c:											#*handles single case where CNAME points to an IP string
		c = re.search(pat_ip,line)						#*assign this to 'c' and resume normally
	l_cname.append(hostname.group() + ' ' + c.group() + '\n')
	print time.strftime("%b%d-%H:%M:%S") + ": CNAME detected:\t" + line.rstrip()
	return

def igln(line):
	"""Create a list for entries that are ignored."""
	global l_ignored

	l_ignored.append(line)
	print time.strftime("%b%d-%H:%M:%S") + ": Line Ignored:\t" + line.rstrip()
	return
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Called by corpnet() to handle different types of entries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def int_dev(line):
	""" 100/gig/ten interface, hostname
	examples: 
		te3-5.2018-ash0-wr01.corpnet.ebay.com
		ge-0-0-bdl1-vr01.corpnet.ebay.com
		fe0-0-dub1-wr02.corpnet.ebay.com
	"""
	global breaker
	global l_remove
	global l_add

	hostname = re.search(pat_wrong_te, line)
	if hostname:
		ip = re.search(pat_ip, line)
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append(autofix.wrong_te(hostname, ip) + '\n')
		breaker = True
		return

	hostname = re.search(pat_wrong_ge, line)
	if hostname:
		ip = re.search(pat_ip, line)
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append(autofix.wrong_ge(hostname, ip) + '\n')
		breaker = True
		return

	hostname = re.search(pat_wrong_fe, line)
	if hostname:
		ip = re.search(pat_ip, line)
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append(autofix.wrong_fe(hostname, ip) + '\n')
		breaker = True
		return

def int_serial(line):
	""" Detects outdated serial interface entries; dns entries should be removed.
	examples: 
	s1-0-aus3-wr01.corpnet.ebay.com
	se1-0-phx1-wr02.corpnet.ebay.com
	"""
	global breaker
	global l_remove
	global l_add

	hostname = re.search(pat_serial, line)
	if hostname:
		ip = re.search(pat_ip, line)
		print time.strftime("%b%d-%H:%M:%S") + ': ' + "Serial Port that probably needs to be removed: " + hostname.group() + ' ' + ip.group()
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append('\tSerial Interface - Remove only\n')
		breaker = True

def int_vlan(line):
	global breaker
	global l_remove
	global l_add

	hostname = re.search(pat_wrong_vlan, line)
	if hostname:
		ip = re.search(pat_ip,line)
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append(autofix.wrong_vlan_int(hostname, ip) + '\n')
		breaker = True

def hsrp(line):
	global breaker
	global l_remove
	global l_add

	hostname = re.search(pat_wrong_hsrp, line)
	if hostname:
		ip = re.search(pat_ip,line)
		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
		l_add.append(autofix.wrong_hsrp(hostname, ip) + '\n')
		breaker = True
#def site_fl_dev(line):
#	""" 3 char site code, building #, floor #, device name, dev #
#	example: sjc15-3-ca01, aus3-3-wl01
#
#	*Currently not in use anymore as of b0.6.0 revision.
#	"""
#	global breaker
#	global l_remove
#	global l_add
#
#	hostname = re.search(pat_wrong_site_fl_dev, line)
#	if hostname:
#		ip = re.search(pat_ip, line)
#		breaker = True
#		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
#		l_add.append(autofix.wrong_site_fl_dev(hostname, ip) + '\n')
#		return
#def site_dev(line):
#	""" 3 char site code, building #, device name, dev #
#	example: chi1-ts01, nyb1-wr01
#
#	*Currently not in use anymore as of b0.6.0 revision.
#	"""
#	global breaker
#	global l_remove
#	global l_add
#
#	hostname = re.search(pat_wrong_site_dev, line)
#	if hostname:
#		ip = re.search(pat_ip, line)
#		breaker = True
#		l_remove.append(hostname.group() + ' ' + ip.group() + '\n')
#		l_add.append(autofix.wrong_site_dev(hostname, ip) + '\n')
#		return
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Output
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def flush_out():
	global l_add
	global l_remove
	global l_cname
	global l_ignored

	fh_rm = open('dnsVet-output-remove.txt',"w")
	fh_add = open('dnsVet-output-add.txt',"w")
	fh_cname = open('dnsVet-output-cname.txt','w')
	fh_ignored = open('dnsVet-output-ignored.txt','w')

	fh_rm.write("#The following are DNS entries that need to be removed:\n")
	for line in l_remove:
		fh_rm.write(line)

	fh_add.write("#The following are DNS entries that need to be added (that replace the removed entries):\n")
	for line in l_add:
		fh_add.write(line)

	fh_cname.write("#Here is a list of detected CNAMEs:\n")
	for line in l_cname:
		fh_cname.write(line)

	fh_ignored.write("#Here is a list of entries that were ignored:\n")
	for line in l_ignored:
		fh_ignored.write(line)

	fh_rm.close()
	fh_add.close()
	fh_cname.close()
	fh_ignored.close()

	print """Files written/overwritten:
    dnsVet-output-remove.txt
    dnsVet-output-add.txt
    dnsVet-output-cname.txt
    dnsVet-output-ignored.txt\n"""