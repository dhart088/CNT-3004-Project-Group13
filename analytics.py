import time
startTime = 0
transactionID = 0
startDate

transmissionRecord = [{
  "source": "server",
  "start time": 0,
  "end time": 0,
  "transmission time": 0,
  "download rate": 0,
  "upload rate": 0,
  "response time": 0
  "ID": 0
}]

def startTime(start, startDate):
  startTime = start
  return

def getStart():
  return startTime

def getStartDate():
  return startDate

def calculate(end, location, up_or_down):
  transactionID++
  elapsedTime = end - getStart()
  if up_or_down == "down":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "transmission time": elapsedTime, "download rate": TODO, "response time": TODO, "ID": transactionID)
  elif up_or_down == "up":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "transmission time": elapsedTime, "upload rate": TODO, "response time": TODO, "ID": transactionID)
