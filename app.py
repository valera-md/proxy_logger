import datetime
import json

# scheme / interface 
class Logger:
 def log(self, information):
  raise TypeError("Logger is an abstract class,\
                  you can't use it directly\
                  extend it, override the log() method")
class ConsoleLogger(Logger):
 def log(self, information):
  print(f"LOGGER: {information}")
class FileLogger(Logger):
 def __init__(self, filename):
  self.filename = filename
 def log(self, information):
  file = open(self.filename, "a")
  file.write(f"{information}\n")
  file.close()
class JSONFileLogger(Logger):
 def __init__(self, filename):
    self.filename = filename
 def log(self, timestamp, information):
  dict = {"timestamp": timestamp, "information": information}
  try:
   file = open(self.filename, "r")
  except FileNotFoundError:
   file = open(self.filename, "w")
   file.close()
   file = open(self.filename, "r")
  if file.read() == "":
   file.close()
   list = []
   list.append(dict)
   file = open(self.filename, "w")
   json_data = json.dumps(list, indent=4)
   file.write(json_data)
   file.close()
  else:
   file.close()
   file = open(self.filename, "r")
   json_data = file.read()
   list = json.loads(json_data)
   file.close()
   list.append({"timestamp": timestamp, "information": information})
   file = open(self.filename, "w")
   json_data = json.dumps(list, indent = 1)
   file.write(json_data)
   file.close()

class Bot:
 def __init__(self, name):
  self.name = name
  self.logger = None
 def replyTo(self, message):
  #hw1*: use match case
  match message:
   case "hi":
    reply = "hello!"
   case "bye":
    reply = "goodbye!"
   case _:
    reply = None
  #reply = None
  #if message == "hi":
   #reply = "hello!"
  #elif message == "bye":
   #reply = "goodbye!"
  if self.logger != None and type(self.logger) != JSONFileLogger:
   # hm2: add this format timestamp "2024-01-20 10:00:01:" as prefix
   # add bot name in the log
   if reply != None:
    self.logger.log(f'{self.name}: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}: received \"{message}\", replied with \"{reply}\"')
   else:
    self.logger.log(f'{self.name}: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}: could not reply to \"{message}\"')
  elif self.logger != None and type(self.logger) == JSONFileLogger:
   if reply != None:
    self.logger.log(f'{self.name}: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}:', f'received \"{message}\", replied with \"{reply}\"')
   else:
    self.logger.log(f'{self.name}: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}:', f'could not reply to \"{message}\"')
  return reply

bot = Bot("support")
#bot.logger = Logger()
#bot.logger = ConsoleLogger()
#bot.logger = FileLogger("log.txt")
bot.logger = JSONFileLogger("log.json")
print(bot.replyTo("hi"))
print(bot.replyTo("bye"))
print(bot.replyTo("how are you?"))
'''
hm3: add a logger that stores in JSON(* xml, csv)
JSONFileLogger
log.json
[
 {
  timestamp: "...",
  information: "..."
 },
 {
  timestamp: "...",
  information: "..."
 },
 {
  timestamp: "...",
  information: "..."
 },
]
'''