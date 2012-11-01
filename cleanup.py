#!/usr/bin/python
import argparse
import os
import re
import sys
import time

from sh import df
from sh import grep
from sh import rm

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

def get_relavant_files(watch_dir, min_file_size):
	rel_files = []

	for root, dirs, files in os.walk(watch_dir):
		abs_files = map(lambda ff: os.path.join(os.path.abspath(root), ff) , files)
		filtered = [i for i in abs_files if file_size_mb(i) > min_file_size]
		for f in filtered:
			last_access = get_last_access(f)
			size = file_size_mb(f)
			rel_files.append((last_access, size, f))

		for d in dirs:
			rel_files = rel_files + get_relavant_files(d, min_file_size)

	return rel_files

def get_to_secounds_factor(time_unit):
	if(time_unit == "s"):
		return 1
	if(time_unit == "m"):
		return 60
	if(time_unit == "h"):
		return 60 * 60
	if(time_unit == "d"):
		return 60 * 60 * 24
	return None



####################################
#	argument parsing
####################################
parser = argparse.ArgumentParser(description='Removes files of disk space gets scares.')
parser.add_argument('-w', '--warn-lvl', type=int , required=True, 
	help="Start warning if free spaces gets less than this (in MB).")
parser.add_argument('-c', '--critical-lvl', type=int , required=True, 
	help="Start deleting files if free space is below CRITICAL-LVL MB until, WARN-LVL MB are free again.")
parser.add_argument('-m', '--min-file-size', type=float , default=100, 
	help="Minimun file size in MB. Files smaller will be ignored.")
parser.add_argument('-p', '--polling-interval', type=str , default="12h", 
	help="Checking / deleting interval: <number>(s|m|h|d)")
parser.add_argument('watch_dir', help="Directory to operate on.")



args = parser.parse_args()

warn_lvl = args.warn_lvl
critical_lvl = args.critical_lvl
watch_dir = os.path.abspath(args.watch_dir)
min_file_size = args.min_file_size

time_number = 0
try:
	time_number = int(args.polling_interval[:len(args.polling_interval)-1])
except ValueError:
	sys.exit("invalid time format: " + args.polling_interval + " call with -h for details.")

time_unit = args.polling_interval[-1]
to_sec_factor = get_to_secounds_factor(time_unit)

if not to_sec_factor:
	sys.exit("Can't parse time unit " + args.polling_interval + " call with -h for details.")

polling_interval = max(int(time_number * to_sec_factor), 1)

print "Watching directory: " + watch_dir
print "Polling every " + str(polling_interval) + " secounds."
print "Ignoring files smaller than " + str(min_file_size) + "MB."
print "Starting to delte files if free space drops below " + str(critical_lvl) + "MB, until " + str(warn_lvl) + "MB are free again."

####################################
#	main
####################################

deletion_candidates = set()
while True:
	try:
		free_mb = get_free_mb(watch_dir)
		print time.strftime("%a, %d %b %Y %H:%M:%S") + " checking...  free: " + str(free_mb) + " warning: " + str(warn_lvl) + " critial: " + str(critical_lvl)

		if free_mb < critical_lvl:
			for doomed in deletion_candidates:
				rm(doomed[2])
				print "REMOVED: " + str(doomed[2])

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
			for candidate in diff:
				print candidate[2]

			deletion_candidates = new_del_candidates


		time.sleep(polling_interval)
	except KeyboardInterrupt:
		print "Got KeyboardInterrupt. Bye :) ."
		sys.exit()





