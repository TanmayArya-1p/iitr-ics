import json
import os
from consts import ICS_OUTPUT_DIR, RESPONSE_JSON_DIR
from parse import ICSCalendar
from utils import check_unique


if __name__ == "__main__":
	if not check_unique(os.listdir(RESPONSE_JSON_DIR)):
		exit(101)

	for i in os.listdir(RESPONSE_JSON_DIR):
		if not i.endswith(".json"):
			continue

		print("PARSING", i)
		with open(f"{RESPONSE_JSON_DIR}/{i}", "r") as rsp:
			mp = json.load(rsp)
			cal = ICSCalendar(mp)
			cal.save(f"{ICS_OUTPUT_DIR}/{i.split(".")[0]}.ics")
