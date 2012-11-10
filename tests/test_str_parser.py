from str_parser import *
from nose.tools import raises
from nose.tools import eq_

def test_get_to_seconds_factor():
	eq_(get_to_seconds_factor('s'), 1)
	eq_(get_to_seconds_factor('m'), 60)
	eq_(get_to_seconds_factor('h'), 60 * 60)
	eq_(get_to_seconds_factor('d'), 60 * 60 * 24)

def test_extract_secounds_valid_input():
	eq_(extract_secounds('1s'), 1)
	eq_(extract_secounds('15s'), 15)
	eq_(extract_secounds('1m'), 60)
	eq_(extract_secounds('10m'), 600)
	eq_(extract_secounds('1h'), 60 * 60)
	eq_(extract_secounds('1d'), 60 * 60 * 24)
	eq_(extract_secounds('1d'), 60 * 60 * 24)

@raises(ValueError)
def test_extract_secounds_invalid_input():
	extract_secounds('1')
	extract_secounds('s')
	extract_secounds('1sa')
	extract_secounds('s1')
	extract_secounds('1x')


def test_get_to_kb_factor_valid_input():
	# KB
	eq_(get_to_kb_factor('k'), 1)
	eq_(get_to_kb_factor('K'), 1)

	# MB
	eq_(get_to_kb_factor('m'), 1024)
	eq_(get_to_kb_factor('M'), 1024)

	# GB
	eq_(get_to_kb_factor('g'), 1024 * 1024)
	eq_(get_to_kb_factor('G'), 1024 * 1024)

	# TB
	eq_(get_to_kb_factor('t'), 1024 * 1024 * 1024)
	eq_(get_to_kb_factor('T'), 1024 * 1024 * 1024)

def test_extract_kb():
	eq_(extract_kb('1k'), 1)
	eq_(extract_kb('12k'), 12)
	eq_(extract_kb('1K'), 1)

	eq_(extract_kb('1m'), 1024)
	eq_(extract_kb('1M'), 1024)

	eq_(extract_kb('1g'), 1024 * 1024)
	eq_(extract_kb('1G'), 1024 * 1024)

	eq_(extract_kb('1t'), 1024 * 1024 * 1024)
	eq_(extract_kb('1T'), 1024 * 1024 * 1024)

