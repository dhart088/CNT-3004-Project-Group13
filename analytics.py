import time
startTime = 0
transactionID = 0
startDate = time.ctime()
endDate = time.ctime()

transmissionRecord = [{
  "source": "server",
  "start time": 0,
  "end time": 0,
  "start date": --,
  "end date": --,
  "transmission time": 0,
  "download rate": 0,
  "upload rate": 0,
  "response time": 0
  "ID": 0
}]

def startTime():
  startTime = time.time()
  startDate = time.ctime()
  return

def getStart():
  return startTime

def getStartDate():
  return startDate

def calculate(location, up_or_down):
  elapsedTime = time.time() - getStart()
  endDate = time.ctime()
  transactionID++
  
  if up_or_down == "down":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "download rate": TODO, "response time": TODO, "ID": transactionID)
  elif up_or_down == "up":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "upload rate": TODO, "response time": TODO, "ID": transactionID)
