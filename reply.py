from base_module import *
from os.path import exists
import re, string

replyFile = "./data/replyFile"

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		
		self.replyList = []
		
		if exists(replyFile):
				for line in filter(lambda l: len(l) and l[0] != '$', map(string.strip, open(replyFile).xreadlines())):
					regex, reply = map(string.strip, line.split('\t', 1))
					self.replyList.append((re.compile(regex, re.I), reply))
		
	def on_channel_message(self, source_name, source_host, message):
		for regex, reply in self.replyList:
			if regex.search(message):
				self.bot.say(reply)
