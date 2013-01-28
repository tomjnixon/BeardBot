from base_module import *
from packagetrack import *
from packagetrack.xml_dict import xml_to_dict
from datetime import datetime, date, time
import shelve
import os.path

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.packages = shelve.open(self.bot.channel + "_upstrack.db")

	@on_private_match("Track package (\w{18})", re.I)
	def track(self, source_name, source_host, message, trackingNumber):
		try:
			package = Package(trackingNumber)
			info = package.track()
			self.packages[source_name] = package
			self.bot.pm(source_name, "OK. I'll keep an eye on it")
			return
		except KeyError:
			self.bot.pm(source_name, "There's something wrong with that number")

	@on_private_match("Where'?s my package", re.I)
	def checkPackage(self, source_name, source_host, message):
		if source_name not in self.packages:
			self.bot.pm(source_name, "I don't seem to be tracking any of your packages")
			return
		package = self.packages[source_name]
		root = xml_to_dict(get_interface(package.shipper).send_request(package.tracking_number))['TrackResponse']['Shipment']
		info = root['Package']

		activity = info['Activity']
		lastUpdateDate = datetime.strptime(activity['Date'], "%Y%m%d").date()
		lastUpdateTime = datetime.strptime(activity['Time'], "%H%M%S").time()
		lastUpdate = datetime.combine(lastUpdateDate, lastUpdateTime)
		location = activity['ActivityLocation']['Address']['City'] + ", " + activity['ActivityLocation']['Address']['CountryCode']
		status = activity['Status']['StatusType']['Description']
		estimateDescription = info['Message']['Description']
		estimateDate = datetime.strptime(root['ScheduledDeliveryDate'],"%Y%m%d")

		self.bot.pm(source_name, "Last update: " + lastUpdate.strftime("%Y-%m-%d %H:%M") + " -- " + status + " -- " + location + " -- " + estimateDescription + ". Est delivery date: " + estimateDate.strftime("%Y-%m-%d"))

	@on_private_match("clear my package", re.I)
	def clearPackage(self, source_name, source_host, message):
		if source_name not in self.packages:
			self.bot.pm(source_name, "Don't worry. I'm not tracking any of your packages anyway.")
		else:
			del self.packages[source_name]
			self.bot.pm(source_name, "OK. I'll stop tracking it.")

	def die(self):
		self.packages.close()

