from base_module import *
import time, threading

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""A ping module. Ping a nick and it'll report the ping time or timeout.
Ping someone:
*   <nick>: ping
Ping someone with custom timeout:
*   <nick>: ping <timeout>
Return ping:
*   pong"""
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)

		self.pingList = {}
		self.pongTime = {}

	def pingThread(self, nick, timeout = 120):
		startTime = time.time()

		for i in range(timeout):
			if self.pingList[nick].is_set():
				pingTime = self.pongTime[nick] - startTime
				break
			time.sleep(1)

		if self.pingList[nick].is_set():
			self.bot.say("Ping time for %s: %fsecs" % (nick, pingTime))
		else:
			self.bot.say("Ping timeout %isecs for %s" % (timeout, nick))


	@on_channel_match("^(\w+): ping$", re.I)
	def on_ping(self, source_name, source_host, message, nick):
		self.pingList[nick.lower()] = threading.Event()
		thread = threading.Thread(target=self.pingThread, args=(nick.lower(), ))
		thread.start()


	@on_channel_match("^(\w+): ping (\d*)$", re.I)
	def on_ping_timed(self, source_name, source_host, message, nick, time):
		self.pingList[nick.lower()] = threading.Event()
		thread = threading.Thread(target=self.pingThread, args=(nick.lower(), int(time)))
		thread.start()


	@on_channel_match(".*pong.*", re.I)
	def on_pong(self, source_name, source_host, message):
		if source_name.lower() in self.pingList:
			self.pongTime[source_name.lower()] = time.time()
			self.pingList[source_name.lower()].set()
