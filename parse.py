from ics import Calendar, Event
from ics.grammar.parse import Container, ContentLine
from consts import COURSE_CODE_KEY_LOOKUP_ORDER, HUMAN_SLOT_TYPE
from utils import parse_to_arrow


class ICSCalendar:
	def __init__(self,response_json):
		self.calendar = self.__produce_calendar(response_json)


	def __extract_events(self, response_json, course_name_lookup):
		res = []
		for i in response_json["result"]:
			type = HUMAN_SLOT_TYPE[i["Slot_Type"]]

			course = ""
			for key in COURSE_CODE_KEY_LOOKUP_ORDER:
				course = i.get(key,"")
				if(course!=""):
					break

			room = i.get("Room_no","")
			event_name = " - ".join(filter(lambda x: x!="", [type,room,course]))

			day_code = i["Day"][:2].upper()

			start_t_str = i["Time"].split('-')[0]
			end_t_str = i["Time"].split('-')[1]

			start_t = parse_to_arrow(start_t_str, day_code)
			end_t = parse_to_arrow(end_t_str, day_code)

            # recur for next 6 months
			until_date = start_t.shift(months=6).replace(hour=23, minute=59, second=59)

			e = Event()
			e.name = event_name
			e.begin = start_t
			e.end = end_t
			e.description = course_name_lookup.get(course, "")

			rrule = Container("RRULE")
			rrule.append(ContentLine(name="FREQ", value="WEEKLY"))
			rrule.append(ContentLine(name="BYDAY", value=day_code))
			rrule.append(ContentLine(name="UNTIL", value=until_date.strftime("%Y%m%dT%H%M%SZ")))

			e.extra.append(rrule)
			res.append(e)
		return res


	def __extract_course_names(self, response_json):
		m = {}
		for i in response_json["CourseList"]:
			try:
				m[i["SubjectCode"]] = i["SubjectName"]
			except:
				pass
		return m

	def __produce_calendar(self,response_json):
		c = Calendar()
		course_name_lookup = self.__extract_course_names(response_json)
		events = self.__extract_events(response_json, course_name_lookup)
		for ev in events:
			c.events.add(ev)

		return c

	def save(self,path):
		with open(path, 'w') as icsf:
			icsf.writelines(self.calendar.serialize_iter())
