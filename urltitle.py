# coding=UTF-8
from base_module import *
from bs4 import BeautifulSoup
import re, urllib2

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [('user-agent', 'Mozilla/5.0')]

	def on_channel_message(self, source_name, source_host, message):
		match_urls = re.compile("""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""")
		urlFound = match_urls.search(message)
		if urlFound != None:
			title = BeautifulSoup(self.opener.open(urlFound.group(0)).read()).title.string
			self.bot.say(source_name + " linked to: " + title)
