from base_module import *
import shelve, datetime

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.swearing = False
	
	@on_channel_match("^medibot$", re.I)
	def on_medibot(self, source_name, source_host, message):
		self.bot.say("MEDIBOT")
	
	@on_channel_match("^beardbot$", re.I)
	def on_beardbot(self, source_name, source_host, message):
		self.bot.say("BEARDBOT")

	@on_channel_match("^Thanks beardbot$", re.I)
	def on_thanks_beardbot(self, source_name, source_host, message):
		self.bot.say("Theardbot")

	@on_channel_match("^Thanks ants$", re.I)
	def on_thanks_ants(self, source_name, source_host, message):
		self.bot.say("Thants")

	@on_channel_match("^magnets$", re.I)
	def on_magnets(self, source_name, source_host, message):
		self.bot.say("how do they work")
		
	@on_channel_match("(^|.*\s)wikipedia(\s.*|$)", re.I)
	def on_wikipedia(self, source_name, source_host, message, first, last):
		if self.swearing:
			self.bot.say("%swiki-fucking-pedia%s" %(first, last,))

		
	@on_addressed_match("^keep it clean$", re.I)
	def on_no_swearing(self, source_name, source_host, message):
		self.swearing = False
		self.bot.say("Sorry. I'll stop with the flipping language.")
		
	@on_addressed_match("^speak freely$", re.I)
	def on_swearing(self, source_name, source_host, message):
		self.swearing = True
		self.bot.say("Fuck you!")
