def getDate(string):
	return string.split("T")[0]
	

def getTime(string):
	string = string[:-1]
	return string.split("T")[1]
