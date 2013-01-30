from base_module import *
from os.path import exists
import re, string

channelReplyFile = "./data/channelReplyFile"
actionReplyFile = "./data/actionReplyFile"
addressReplyFile = "./data/addressReplyFile"

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		
		self.channelReplyList = []
		self.actionReplyList = []
		self.addressReplyList = []
		
		if exists(channelReplyFile):
				for line in filter(lambda l: len(l) and l[0] != '$', map(string.strip, open(channelReplyFile).xreadlines())):
					regex, reply = map(string.strip, line.split('\t', 1))
					self.channelReplyList.append((re.compile(regex, re.I), reply))

		if exists(actionReplyFile):
				for line in filter(lambda l: len(l) and l[0] != '$', map(string.strip, open(actionReplyFile).xreadlines())):
					regex, reply = map(string.strip, line.split('\t', 1))
					self.actionReplyList.append((re.compile(regex, re.I), reply))

		if exists(addressReplyFile):
				for line in filter(lambda l: len(l) and l[0] != '$', map(string.strip, open(addressReplyFile).xreadlines())):
					regex, reply = map(string.strip, line.split('\t', 1))
					self.addressReplyList.append((re.compile(regex, re.I), reply))

	def on_channel_message(self, source_name, source_host, message):
		for regex, reply in self.channelReplyList:
			if regex.search(message):
				self.bot.say(reply)

	def on_action(self, source_name, source_host, message):
		for regex, reply in self.actionReplyList:
			if regex.search(message):
				self.bot.say(reply)

	def on_addressed_message(self, source_name, source_host, message):
		for regex, reply in self.addressReplyList:
			if regex.search(message):
				self.bot.say(reply)