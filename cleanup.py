import argparse
import os
import re

from sh import df
from sh import grep

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

def bigger_than_100mb(filename):
	return file_size_mb(filename) > 100

def file_size_mb(filename):
	return int(os.stat(filename).st_size) / 1024 / 1024

def get_last_access(filename):
	return os.stat(filename).st_atime

def get_deletion_candidates(watch_dir):
	candidates = []

	for root, dirs, files in os.walk(watch_dir):
		abs_files = map(lambda ff: os.path.join(os.path.abspath(root), ff) , files)
		for f in filter(bigger_than_100mb, abs_files):
			last_access = get_last_access(f)
			size = file_size_mb(f)
			candidates.append((last_access, size, f))

		for d in dirs:
			candidates = candidates + get_deletion_candidates(d)

	return candidates



####################################
#	argument parsing
####################################
parser = argparse.ArgumentParser(description='Removes files of disk space gets scares.')
parser.add_argument('-w', '--warn-lvl', type=int , required=True, 
	help="Start warning about wich files will be deleted of free spaces gets less than this ( in MB).")
parser.add_argument('-c', '--critical-lvl', type=int , required=True, 
	help="Start deleting files if free space is below CRITICAL-LVL MB until, WARN-LVL MB are free again.")
parser.add_argument('watch_dir', help="Directory to operate on.")


args = parser.parse_args()

warn_lvl = args.warn_lvl
critical_lvl = args.critical_lvl
watch_dir = os.path.abspath(args.watch_dir)

####################################
#	main
####################################
free_mb = get_free_mb(watch_dir)

for t in sorted(get_deletion_candidates(watch_dir), key=lambda e: e[0]):
	print t

# if (free_mb < warn_lvl):
	# get_deletion_candidates(watch_dir)





