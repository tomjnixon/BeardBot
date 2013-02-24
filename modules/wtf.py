from base_module import *
from os.path import exists
import re, string
from urllib2 import urlopen, Request
from sre import findall
from socket import setdefaulttimeout


word_lists = ["./data/acronyms", "./data/acronyms.comp"]
web_dict = "http://acronyms.thefreedictionary.com/"
google_search = "http://www.google.co.uk/search?q="



requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""Defines acronyms.
Get the definition of an acronym:
*   wtf is [acronym]
Get another definition of an acronym"
*   wtf else is [acronym]
"""
	@on_channel_match("wtf is (\S*[^\?])\??")
	def define(self, source_name, source_host, message, word):
		description = self.translate(word)
		if description:
			self.bot.say(description)
		else:
			self.bot.say(self.online(word))


	@on_channel_match("wtf else is (\S*[^\?])\??")
	def refer(self, source_name, source_host, message, word):
		if self.translate(word):
			self.bot.say("Fine! " + self.online(word))
		else:
			self.bot.say("LMGTFY " + google_search + word)
		
		

	def translate(self, word_to_find):
		for file_name in word_lists:
			if exists(file_name):
				for line in filter(lambda l: len(l) and l[0] != '$',
						   map(string.strip,
						       open(file_name).xreadlines())):
					word, desc = map(string.strip, line.replace('\t', ' ').split(' ', 1))
					if word_to_find.upper() == word:
						return desc
		
	def online(self, word_to_find):
		setdefaulttimeout(5)
		website = urlopen(Request(web_dict + word_to_find)).read()
		if findall('<META NAME="ROBOTS" CONTENT="NOINDEX,FOLLOW">', website):
			return "LMGTFY " + google_search + word_to_find
		else:
			return "Try " + web_dict + word_to_find
