def get_to_seconds_factor(time_unit):
	try:
		return {
			's': 1,
			'm': 60,
			'h': 60 * 60,
			'd': 60 * 60 * 24,
		}[time_unit]
	except (KeyError):
		return ValueError("%s is not a valid input: <int>[s|m|h|d]")

def extract_secounds(time_str):
	to_sec_fac = get_to_seconds_factor(time_str[-1])
	n = int(time_str[:len(time_str)-1])
	return n * to_sec_fac

def get_to_kb_factor(data_size_unit):
	pass
