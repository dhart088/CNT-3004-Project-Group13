import time
startTimeVal = 0
transactionID = 0
startDate = time.ctime()
endDate = time.ctime()
chunkNum = 0
chunkSize = 0
totalFileSize = 0
responseTimeVal = 0

transmissionRecord = [{ # format that the recorded data is stored
  "source": "server",
  "start time": 0,
  "end time": 0,
  "start date": "--",
  "end date": "--",
  "transmission time": 0,
  "download rate": 0,
  "upload rate": 0,
  "response time": 0,
  "ID": 0
}]

def startTime(): # records the numerical value of the time that the transmission started
  global startTimeVal
  startTimeVal = time.time()
  global startDate
  startDate = time.ctime()
  return

def responseTime(): # records the numerical value of the time that the other system recieved a response
  global responseTimeVal
  responseTimeVal = time.time()
  return

def getResponseTime(): # returns the numerical value of the time that the other system recieved a response
    global responseTimeVal
    return responseTimeVal

def getStart(): # returns the numerical value of the time the transmission started
  global startTimeVal
  return startTimeVal

def getStartDate(): # returns the value of the time that the transmission started
    global startDate
    return startDate

def updateChunk(chunk): # updates the total file size of the file being transmitted
  global chunkSize
  chunkSize = max(chunk, chunkSize)
  global totalFileSize 
  totalFileSize += chunk
  global chunkNum
  chunkNum = chunkNum + 1
  return

def calculate(location, up_or_down): # function that adds a dictionary containing information from each transmission
  elapsedTime = time.time() - getStart()
  global endDate
  endDate = time.ctime()
  global transactionID
  transactionID = transactionID + 1
  global totalFileSize
  rate = totalFileSize / elapsedTime
  
  if up_or_down == "down":
    transmissionRecord.append({"source": location, "start time": getStart(), "end time": time.time(), "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "download rate": f"{rate} bytes per second", "response time": (getResponseTime() - getStart()), "ID": transactionID})
  elif up_or_down == "up":
    transmissionRecord.append({"source": location, "start time": getStart(), "end time": time.time(), "start date": getStartDate(), "end date": endDate, "transmission time": elapsedTime, "upload rate": f"{rate} bytes per second", "response time": (getResponseTime() - getStart()), "ID": transactionID})
  
  global chunkSize
  chunkSize = 0
  global chunkNum
  chunkNum = 0
  totalFileSize = 0
  global startTimeVal
  startTimeVal = 0

def printRecord(): # function that creates record file
  with open("record.txt", "w") as file:
    for item in transmissionRecord:
        file.write(f"{item}\n")
  return
