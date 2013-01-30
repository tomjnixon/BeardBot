from base_module import *
import random

methods = ["throws", "bounces", "chucks"]
directions = ["to", "towards", "at"]
botName = ""

requiredBeardBotVersion = 0.4
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		botName = newBot.nick.lower()

	
	@on_action("(?:throws|bounces|chucks) ball (?:to|at|towards) %s" % botName, re.I)
	def on_ball(self, source_name, source_host, message):
		method = random.choice(methods)
		direction = random.choice(directions)
		self.bot.action("%s ball %s %s"%(method, direction, source_name))
