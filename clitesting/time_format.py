def get_date(string):
	return string.split("T")[0]

def get_time(string):
	string = string[:-1]
	return string.split("T")[1]
