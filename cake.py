from base_module import *
import random

cake_replies = ["The cake is a lie",
           "What's this about cake?",
           "CAAAAAAAAAKE",
           "This is your fault. I'm going to kill you. And all the cake is gone. You don't even care, do you?",
           "At the end of the experiment, you will be baked and then there will be cake.",
           "But there's no sense crying over every mistake. You just keep on trying till you run out of cake.",
           "Maybe you'll find someone else to help you. Maybe Black Mesa. That was a joke - Ha ha! Fat Chance! Anyway, this cake is great. It's so delicious and moist.",
           "If you thought you were sick of the memes, I was sick of it way ahead of you. For instance, cake. I've had enough cake jokes.",
           "Quit now and cake will be served immediately.",
           "Cake and grief counseling will be available at the conclusion of the test.",
           "Enrichment Center regulations require both hands to be empty before any cake----",
           "Okay. The test is over now. You win. Go back to the recovery annex. For your cake.",
           "Uh oh. Somebody cut the cake. I told them to wait for you, but they did it anyway. There is still some left, though, if you hurry back.",
           "Who's gonna make the cake when I'm gone? You?",
           "There really was a cake...",
]

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
	
	@on_channel_match(".*cake.*", re.I)
	def on_medibot(self, source_name, source_host, message):
		message = random.choice(cake_replies)
		self.bot.say("%s"%(message, ))
