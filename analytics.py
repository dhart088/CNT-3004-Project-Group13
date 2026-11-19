import time
global startTime = 0
global transactionID = 0
global startDate = time.ctime()
global endDate = time.ctime()
global chunkNum = 0
global chunkSize = 0
global totalFileSize = 0

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

def updateChunk(chunk):
  chunkSize = max(chunk, chunkSize)
  totalFileSize += chunk
  chunkNum++
  return

# def getChunkSize():
#   return chunkSize

# def getTotalFile():
#   return totalFileSize

def calculate(location, up_or_down):
  elapsedTime = time.time() - getStart()
  endDate = time.ctime()
  transactionID++
  rate = totalFileSize / elapsedTime
  
  if up_or_down == "down":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "download rate": rate, "response time": TODO, "ID": transactionID)
  elif up_or_down == "up":
    transmissionRecord.append("source": location, "start time": getStart(), "end time": end, "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "upload rate": f"{rate} bytes per second", "response time": TODO, "ID": transactionID)
  
  chunkSize = 0
  chunkNum = 0
  totalFileSize = 0
  startTime = 0
