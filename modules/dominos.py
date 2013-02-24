from base_module import *
import time, threading, re, urllib2

stepCode = ['', 'step1-selected', 'step2-selected', 'step3-selected', 'step4-selected', 'step5-delivery-selected', 'step5-delivery-past']
stepStatus = ['', 'Dominos order place', 'Your order is being prepared', 'Your Dominos order is being baked', 'Your Dominos order is in quality control', 'Your Dominos order is out for delivery', 'Your Dominos order has been delivered']

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""A Dominos order tracking module. Track your order with:
*   Track pizza <pizza ID>
where <pizza ID> is the sequence of characters after id= in the tracking URL."""

	def getStep(self, orderID):
		page = urllib2.urlopen("http://www.dominos.co.uk/checkout/pizzaTrackeriFrame.aspx?id=%s" % (orderID)).read()
		for step in range(1,7):
			if re.search(stepCode[step], page) != None:
				return step
		return None

	def pizzaThread(self, nick, orderID):
		self.bot.say("Ok. I'll keep an eye on it.")
		step = 0

		while step != 6:
			newStep = self.getStep(orderID)
			if newStep == None:
				self.bot.say("Invalid return from Dominos website")
				break
			if newStep != step:
				step = newStep
				self.bot.say("%s: %s" % (nick, stepStatus[step]))
			time.sleep(60)

	@on_channel_match("^Track pizza (\w+)", re.I)
	def on_ping(self, source_name, source_host, message, orderID):
		thread = threading.Thread(target=self.pizzaThread, args=(source_name, orderID))
		thread.start()