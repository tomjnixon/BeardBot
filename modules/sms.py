from base_module import *
import re
import urllib, urllib2

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	@on_addressed_match("(?:sms|txt|text) (\w+) (.*)", re.I)
	def text(self, source_name, source_host, message, name, msg):
		params = {
			"action": "create",
			"token" : open("tropotoken_sms","r").read(),
			"frm"   : source_name,
			"name"  : name,
			"msg"   : msg,
		}
		
		url = "https://api.tropo.com/1.0/sessions?%s"%urllib.urlencode(params)
		urllib2.urlopen(url).read()
