from base_module import *
import shelve, datetime

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
	
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

