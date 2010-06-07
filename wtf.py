from base_module import *
from os.path import exists
import re, string


word_lists = ["/usr/share/misc/acronyms", "/usr/share/misc/acronyms.comp"]
web_dict = "http://acronyms.thefreedictionary.com/"
google_search = "http://www.google.co.uk/search?q="



requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):

	@on_channel_match("wtf is (\S*[^\?])\??")
	def define(self, source_name, source_host, message, word):
		description = self.translate(word)
		if description:
			self.bot.say(description)
		else:
			self.bot.say("Fuck knows!? Try " + web_dict + word)


	@on_channel_match("wtf else is (\S*[^\?])\??")
	def refer(self, source_name, source_host, message, word):
		#probably not the nicest way to do it. Feel free to clean up
		file_exists = True
		for file_name in word_lists:
			if not exists(file_name):
				file_exists = False
		if file_exists:
			self.bot.say("Fine! Don't listen to me! Try " + web_dict + word)
		else:
			self.bot.say("LMGTFY " + google_search + word)
		
		

	def translate(self, word_to_find):
		#probably not the nicest way to do it. Feel free to clean up
		for file_name in word_lists:
			if not exists(file_name):
				return "Not sure but try " + web_dict + word_to_find
		for file_name in word_lists:
			for line in filter(lambda l: len(l) and l[0] != '$',
					   map(string.strip,
					       open(file_name).xreadlines())):
				word, desc = map(string.strip, line.replace('\t', ' ').split(' ', 1))
				if word_to_find.upper() == word:
					return desc
		
