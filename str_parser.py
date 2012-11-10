##############################################
# time
##############################################
def get_to_seconds_factor(time_unit):
	units = {
		's': 1,
		'm': 60,
		'h': 60 * 60,
		'd': 60 * 60 * 24,
	}
	try:
		return units[time_unit]
	except (KeyError):
		return ValueError("%s is not a valid input: <int>[%s]" % (time_unit, "|".join(units.keys())))

def extract_secounds(time_str):
	to_sec_fac = get_to_seconds_factor(time_str[-1])
	n = int(time_str[:len(time_str)-1])
	return n * to_sec_fac

##############################################
# data sizes
##############################################
def get_to_kb_factor(data_size_unit):
	units = {
		'K': 1,
		'M': 1024,
		'G': 1024 * 1024,
		'T': 1024 * 1024 * 1024,
	}
	try:
		return units[data_size_unit.upper()]
	except (KeyError):
		return ValueError("%s is not a valid input: <int>[%s]" % (data_size_unit, "|".join(units.keys())))

def extract_kb(data_size_str):
	to_kb_fac = get_to_kb_factor(data_size_str[-1])
	n = int(data_size_str[:len(data_size_str)-1])
	return n * to_kb_fac


