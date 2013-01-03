from base_module import *
import shelve, re

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.scores = shelve.open(self.bot.channel + "_winning.db")
		self.last_sender = ""
		self.this_sender = ""
		self.quiet = False
	
	def get_best(self):
		if not self.scores:
			return
		
		best = self.scores.iterkeys().next() 
		for person in self.scores:
			if self.scores[person] > self.scores[best]:
				best = person
				
		return best
	
	def say_best(self):
		if not self.scores:
			self.bot.say("Nobody is winning right now")
		else:
			winner = self.get_best()
			if self.scores[winner] == 1:
				self.bot.say("%s is currently winning with 1 win" %(winner,))
			elif self.scores[winner] == 2:
				self.bot.say("%s is currently bi-winning" %(winner,))
			else:
				self.bot.say("%s is currently winning with %i wins" %(winner,
                     self.scores[winner]))
			
	def up_win(self, source_name):
		if source_name not in self.scores:
			self.scores[source_name] = 1
		else:
			self.scores[source_name] += 1
		
		if not self.quiet:
			if self.get_best() == source_name:
				self.say_best()
	def reset_scores(self):
			for person in self.scores.keys():
				del self.scores[person]
			self.bot.say("What a bunch of losers.")
			
	def on_channel_message(self, source_name, source_host, message):
		# Set current/previous sender
		self.last_sender = self.this_sender
		self.this_sender = source_name
		
		if re.match("^(?:((?:I(?: am|'m)? |my )?win(?:ning)?)|(I(?: just)? won))$", message, re.I):
			self.up_win(self.this_sender)
		elif re.match("^you(?:((?: are|'re|r)? win(?:ning)?)|(?: just)? won)$", message, re.I):
			self.up_win(self.last_sender)
		elif re.match("^(\w+)(?:\:|,)? (?:is winning|(?:just )?won)$", message,
			re.I):
			self.up_win(re.match("^(\w+)(?:\:|,)? (?:is winning|(?:just )?won)$",
			message, re.I).group(1).encode('ascii', 'ignore'))

		
	@on_addressed_match("^none of us are winning$", re.I)
	def on_reset_scores(self, source_name, source_host, message):
		self.reset_scores()
		
	@on_addressed_match("^tell (?:me|us) if (?:we|I) win$", re.I)
	def on_set_loud(self, source_name, source_host, message):
		self.quiet = False
		self.bot.say("Shall do")

	@on_addressed_match("^we'?ve won enough$", re.I)
	def on_set_quiet(self, source_name, source_host, message):
		self.quiet = True
		self.bot.say("I'll keep quiet then")
		
	@on_addressed_match("^who(?:'?s| is) winning\??$", re.I)
	def on_check_winning(self, source_name, source_host, message):
		self.say_best()
			
			
	def die(self):
		self.scores.close()
