from str_parser import *
from nose.tools import raises

def test_get_to_seconds_factor():
	assert(get_to_seconds_factor('s') == 1)
	assert(get_to_seconds_factor('m') == 60)
	assert(get_to_seconds_factor('h') == 60 * 60)
	assert(get_to_seconds_factor('d') == 60 * 60 * 24)

def test_extract_secounds_valid_input():
	assert(extract_secounds('1s') == 1)
	assert(extract_secounds('15s') == 15)
	assert(extract_secounds('1m') == 60)
	assert(extract_secounds('10m') == 600)
	assert(extract_secounds('1h') == 60 * 60)
	assert(extract_secounds('1d') == 60 * 60 * 24)
	assert(extract_secounds('1d') == 60 * 60 * 24)

@raises(ValueError)
def test_extract_secounds_invalid_input():
	extract_secounds('1')
	extract_secounds('s')
	extract_secounds('1sa')
	extract_secounds('s1')
	extract_secounds('1x')