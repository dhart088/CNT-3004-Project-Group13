import time
startTime = 0
transactionID = 0
startDate = time.ctime()
endDate = time.ctime()
chunkNum = 0
chunkSize = 0
totalFileSize = 0

transmissionRecord = [{
  "source": "server",
  "start time": 0,
  "end time": 0,
  "start date": "--",
  "end date": "--",
  "transmission time": 0,
  "download rate": 0,
  "upload rate": 0,
  "response time": 0
  "ID": 0
}]

def startTime():
  global startTime
  startTime = time.time()
  global startDate
  startDate = time.ctime()
  return

def getStart():
  return startTime

def getStartDate():
  return startDate

def updateChunk(chunk):
  global chunkSize
  chunkSize = max(chunk, chunkSize)
  global totalFileSize 
  totalFileSize += chunk
  global chunkNum
  chunkNum++
  return

def calculate(location, up_or_down):
  elapsedTime = time.time() - getStart()
  endDate = time.ctime()
  global transactionID
  transactionID++
  rate = totalFileSize / elapsedTime
  
  if up_or_down == "down":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "download rate": rate, "response time": TODO, "ID": transactionID)
  elif up_or_down == "up":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "upload rate": f"{rate} bytes per second", "response time": TODO, "ID": transactionID)
  
  global chunkSize
  chunkSize = 0
  global chunkNum
  chunkNum = 0
  global totalFileSize
  totalFileSize = 0
  global startTime
  startTime = 0
