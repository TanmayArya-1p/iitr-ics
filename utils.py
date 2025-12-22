import arrow
from consts import DAY_CODES

def parse_to_arrow(time_str, day_code):
	hour = int(time_str.split(".")[0])
	minute = int(time_str.split(".")[1])
	dt = arrow.now("Asia/Kolkata").shift(weekday=DAY_CODES.index(day_code)).replace(hour=hour, minute=minute)
	return dt


def check_unique(lst):
	if(len(lst) > len(set(lst))):
		return False
	else:
		return True
