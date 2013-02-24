from base_module import *
import random
import json

requiredBeardBotVersion = 0.1


class BeardBotModule(ModuleBase):
	"""A simple game. Put something in the bucket, get a random item back from it.
Put an item in the bucket:
*   I put in [item]
	"""
	
	target_size = 100
	min_size = 3
	
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		
		self.f_name = self.bot.channel + "_bucket.json"
		
		self.last_inserter = "nobody"
	
	@on_channel_match("i put in (.*)", re.I)
	def on_put_in(self, source_name, source_host, message, item):
		self.load()
		
		# Pick and announce a new item.
		if len(self.bucket) < self.min_size:
			(new_item, self.last_inserter) = ("nothing", "nobody")
		elif len(self.bucket) < self.target_size:
			(new_item, self.last_inserter) = self.pick()
		else:
			(new_item, self.last_inserter) = self.remove()
		self.bot.say("You recieve {}.".format(new_item))
		
		self.insert((item, source_name))
		
		self.save()
	
	@on_channel_match("who put that in.*", re.I)
	def on_request_inserter(self, source_name, source_host, message):
		self.bot.say("{} did.".format(self.last_inserter))
	
	def insert(self, item):
		"""Put an item in the bucket."""
		self.bucket.append(item)
	
	def remove(self):
		"""Pick and remove a random item from the bucket."""
		item_idx = random.randrange(len(self.bucket))
		item = self.bucket.pop(item_idx)
		return item
	
	def pick(self):
		"""Pick a random item from the bucket."""
		return self.bucket[random.randrange(len(self.bucket))]
	
	def save(self):
		"""Save the bucket."""
		with open(self.f_name, "w") as f:
			json.dump(self.bucket, f)
	
	def load(self):
		"""Load the bucket."""
		try:
			with open(self.f_name) as f:
				self.bucket = json.load(f)
		except IOError:
			self.bucket = []
