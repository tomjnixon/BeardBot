from base_module import *
import re, string


word_lists = ["/usr/share/misc/acronyms", "/usr/share/misc/acronyms.comp"]


requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):

	@on_channel_match("wtf is (\S*[^\?])\??")
	def define(self, source_name, source_host, message, word):
		description = self.translate(word)
		if description:
			self.bot.say(description)
		else:
			self.bot.say("Fuck knows!? Try http://acronyms.thefreedictionary.com/" + word)


	@on_channel_match("wtf else is (\S*[^\?])\??")
<<<<<<< HEAD
	def refer(self, source_name, source_host, message, word):
=======
	def define(self, source_name, source_host, message, word):
>>>>>>> dd8fb70738144a3e432449eb279ebbc75d1c68b4
		self.bot.say("Fine! Don't listen to me! Try http://acronyms.thefreedictionary.com/" + word)

	def translate(self, word_to_find):
		for file_name in word_lists:
			for line in filter(lambda l: len(l) and l[0] != '$',
					   map(string.strip,
					       open(file_name).xreadlines())):
				word, desc = map(string.strip, line.replace('\t', ' ').split(' ', 1))
				if word_to_find.upper() == word:
					return desc
		
