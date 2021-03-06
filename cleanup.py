#!/usr/bin/python
import argparse
import os
import re
import sys
import time
import humanize

from email.mime.text import MIMEText

import str_parser as sp

from sh import df
from sh import grep
from sh import rm
from sh import sendmail

####################################
#	helper functions
####################################
def is_int(i):
	try:
		int(i)
		return True
	except ValueError:
		return False

def get_free_mb(folder):
	df_result = grep(df("-k", folder), "/")

	kb_sizes = map( int, filter(is_int, df_result.split(" ")))
	available_mb = kb_sizes[2] / 1024

	return available_mb

def file_size_mb(filename):
	return int(os.stat(filename).st_size) / 1024 / 1024

def get_last_access(filename):
	return os.stat(filename).st_atime

def get_last_modified(filename):
	return os.stat(filename).st_ctime

def get_relavant_files(watch_dir, min_file_size):
	rel_files = []

	for root, dirs, files in os.walk(watch_dir):
		abs_files = map(lambda ff: os.path.join(os.path.abspath(root), ff) , files)
		filtered = [i for i in abs_files if file_size_mb(i) > min_file_size]
		for f in filtered:
			order_criteria = get_last_modified(f)
			size = file_size_mb(f)
			rel_files.append((order_criteria, size, f))

		for d in dirs:
			rel_files = rel_files + get_relavant_files(d, min_file_size)

	return rel_files

def get_to_seconds_factor(time_unit):
	if(time_unit == "s"):
		return 1
	if(time_unit == "m"):
		return 60
	if(time_unit == "h"):
		return 60 * 60
	if(time_unit == "d"):
		return 60 * 60 * 24
	return None

def send_email(frm, to, subject, text):
	if("__iter__" in dir(to)):
		to = ",".join(to)

	msg = MIMEText(text)

	msg['Subject'] = subject
	msg['From']    = frm
	msg['To']      = to

	sendmail(to, _in=msg.as_string())


def annouce_del_candidates(candidates):
	if (args.email_to):
		subject = "[cleanup-after-me] this files will be deleted in %s" % humanize.naturaltime(polling_interval, future=True)
		text = "\n".join(map(str, candidates))
		send_email(args.email_from, args.email_to, subject, text)

def annouce_deletions(deletions):
	if (args.email_to):
		subject = "[cleanup-after-me] this files have been DELETED"
		text = "\n".join(map(str, deletions))
		send_email(args.email_from, args.email_to, subject, text)


####################################
#	argument parsing
####################################
parser = argparse.ArgumentParser(description='Removes files of disk space gets scares.')
parser.add_argument('-w', '--warn-lvl', type=str , required=True, 
	help="Start warning if free spaces gets less than this. Format: <int>[K|M|G|T]")
parser.add_argument('-c', '--critical-lvl', type=str , required=True, 
	help="Start deleting files if free space is below CRITICAL-LVL, WARN-LVL. Format: <int>[K|M|G|T]")
parser.add_argument('-m', '--min-file-size', type=str , default=100, 
	help="Minimun file size. Files smaller will be ignored. Format: <int>[K|M|G|T]")
parser.add_argument('-p', '--polling-interval', type=str , default="12h", 
	help="Checking / deleting interval: <number>(s|m|h|d)")
parser.add_argument('-n', '--no-deleting', type=bool , default=False, 
	help="Set -n True to disable deleting. This is mainly for testing.")

parser.add_argument('--email-from', type=str , default="cleanup-after-me", 
	help="The email adress used in the notification mail.")
parser.add_argument('--email-to', type=str , nargs='*',
	help="The email adress to send the notifications to. If this argument issnt set no emails will be send.")

parser.add_argument('watch_dir', help="Directory to operate on.")



args = parser.parse_args()

warn_lvl      = int(sp.extract_kb(args.warn_lvl) / 1024)
critical_lvl  = int(sp.extract_kb(args.critical_lvl) / 1024)
min_file_size = int(sp.extract_kb(args.min_file_size) / 1024)
watch_dir     = os.path.abspath(args.watch_dir)
dont_delete   = args.no_deleting

if (critical_lvl >= warn_lvl):
	sys.exit("critical_lvl has to be lower that warn_lvl");


polling_interval = max(sp.extract_secounds(args.polling_interval), 1)

print "Watching directory: " + watch_dir
print "Polling every %.1f seconds." % polling_interval
print "Ignoring files smaller than %.1fMB." % min_file_size
print "Starting to delte files if free space drops below %.1fMB, until %.1fMB are free again." % (critical_lvl, warn_lvl)

####################################
#	main
####################################

deletion_candidates = set()
while True:
	try:
		free_mb = get_free_mb(watch_dir)
		print time.strftime("%a, %d %b %Y %H:%M:%S") + " checking...  free: %.1f warning: %.1f critial: %.1f" % (free_mb, warn_lvl, critical_lvl)

		if free_mb < critical_lvl:
			if( not dont_delete):
				for doomed in deletion_candidates:
					rm(doomed[2])
					print "REMOVED: %s" % doomed[2]
				annouce_deletions(map(lambda e: e[2], deletion_candidates))

		if free_mb < warn_lvl:
			relevant_files = sorted(get_relavant_files(watch_dir, min_file_size), key=lambda e: e[0])

			new_del_candidates = set()
			mb_to_be_deleted = 0
			for candidate in relevant_files:
				if mb_to_be_deleted < (warn_lvl - free_mb):
					new_del_candidates.add(candidate)
					mb_to_be_deleted += candidate[1]

			diff = (new_del_candidates - deletion_candidates)
			if (len(diff) > 0):
				print "This files might be deleted in the next run:"

				annouce_del_candidates(map(lambda e: e[2], diff))

				for candidate in diff:
					print candidate[2]

			deletion_candidates = new_del_candidates

		sys.stdout.flush()
		time.sleep(polling_interval)
	except KeyboardInterrupt:
		print "Got KeyboardInterrupt. Bye :) ."
		sys.exit()





