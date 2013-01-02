# coding=UTF-8
from base_module import *
from urllib2 import urlopen
import re, lxml.html

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def on_channel_message(self, source_name, source_host, message):
		match_urls = re.compile("""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""")
		urlFound = match_urls.search(message)
		if urlFound != None:
			title = lxml.html.parse(urlopen(urlFound.group(0))).find(".//title").text
			self.bot.say(source_name + " linked to: " + title)
