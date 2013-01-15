from base_module import *
from getpass import getpass
from bcrypt import *
import bot, os, re, shelve

valid_module_name = re.compile("^\w+\.py$")

requiredBeardBotVersion = 0.3
class BeardBotModule(ModuleBase):
	def set_password(self, username, password):
		self.admins[username] = hashpw(password, gensalt())
		self.admins.sync()
	
	def check_password(self, username, password):
		hashed = self.admins[username]
		if hashpw(password, hashed) == hashed:
			return True
		else:
			return False

	def __init__(self, newBot):
		ModuleBase.__init__(self,newBot)
		if self.bot.noadmin:
			return
		
		self.admins = shelve.open(self.bot.channel + "_admin.db")
		if not self.admins:
			username = raw_input('Username: ')
			while not username.isalnum():
				username = raw_input('Username (alphanumeric): ')
			password = getpass('Password: ')
			self.set_password(username, password)
			print('Added ' + username + ' as admin')
			
		self.authenticated = {}
				
	def on_private_message(self, source_name, source_host, message):
		try:
			if message.startswith("identify"):
				self.identify_admin(source_name, message.split(" ", 2)[1:3])
			if self.user_is_admin(source_name):
				if message.startswith("modprobe"):
					self.load_module(source_name, message.split(" ")[1:])
				elif message.startswith("rmmod"):
					self.unload_module(source_name, message.split(" ")[1:])
				elif message == "lsmod":
					self.list_modules(source_name)
				elif message.startswith("addignore"):
					self.add_ignore(source_name, message.split(" ")[1])
				elif message.startswith("rmignore"):
					self.rm_ignore(source_name, message.split(" ")[1])
				elif message == "lsignore":
					self.ls_ignore(source_name)
				elif not self.bot.noadmin:
					if message.startswith("addadmin"):
						self.add_admin(source_name, message.split(" ", 2)[1:3])
					elif message.startswith("rmadmin"):
						self.remove_admin(source_name, message.split(" ", 1)[1])
					elif message.startswith("lsadmin"):
						self.list_admin(source_name)
					elif message.startswith("passwd"):
						self.change_password_admin(source_name, message.split(" ", 2)[1:3])
		except Exception, e:
			self.bot.pm(source_name, "Eh? What does that mean? Take a look at help.")
			print e

	def on_quit(self, source_name, source_host, message):
		if not self.bot.noadmin:
			if source_name in self.authenticated:
				del self.authenticated[source_name]

	def on_change_nick(self, source_nick, source_host, message):
		if not self.bot.noadmin:
			if source_nick in self.authenticated:
				self.authenticated[message] = self.authenticated.pop(source_nick)

	def load_module(self, user, modules):
		for module in modules:
			try:
				self.bot.load_module(module)
				self.bot.pm(user, "I've loaded up %s, if you know what I mean...  ;)"%(module,))
			except bot.IncompatibleModuleError:
				self.bot.pm(user, "%s is not compatible with me. :("%(module,))
			except ImportError:
				self.bot.pm(user, "What are you talking about? That doesn't even exist!")
	
	def unload_module(self, user, modules):
		for module in modules:
			if module == "admin":
					self.bot.pm(user, "I'm afraid I can't let you do that, Dave.")
			else:
				try:
					self.bot.unload_module(module)
					self.bot.pm(user, "%s is *DEAD*!"%(module,))
				except KeyError:
					self.bot.pm(user, "How am I supposed to unload something that isn't loaded?")
	
	def list_modules(self, user):
		mod_names = []
		unloadable_mod_names = []
		for filename in os.listdir(os.getcwd()):
			if valid_module_name.match(filename):
				module_name = filename.partition(".")[0]
				try:
					module = __import__(module_name)
					if module.requiredBeardBotVersion <= bot.__version__:
						mod_names.append(module_name)
				except AttributeError:
					pass
				except Exception, e:
					print "Can't load", module_name, e
					unloadable_mod_names.append((module_name, str(e)))
		self.bot.pm(user, "Available modules: %s" % 
		            ', '.join(sorted(set(mod_names) - set(self.bot.modules))))
		self.bot.pm(user, "Loaded modules: %s" % 
		            ', '.join(sorted(self.bot.modules)))
		self.bot.pm(user, "Un-loadable modules: %s" % 
		            ', '.join(("%s (%s)"%x for x in unloadable_mod_names)))
		
	def add_ignore(self, user, username):
		username = username.encode('ascii', 'ignore')
		if not self.bot.noadmin:
			if username in self.admins:
				self.bot.pm(user, "I can't ignore an admin!")
				return
		self.bot.add_ignore(username)
		self.bot.pm(user, "I'll ignore %s from now on." %(username,))

			
	def rm_ignore(self, user, username):
		username = username.encode('ascii', 'ignore')
		self.bot.rm_ignore(username)
		self.bot.pm(user, "Okay. I'll listen to %s then." %(username,))
		
	def ls_ignore(self, user):
		self.bot.pm(user, "I'm currently ignoring: %s" %
		            ', '.join(sorted(self.bot.ls_ignore())),)

	def add_admin(self, user, details):
		username = details[0].encode('ascii', 'ignore')
		password = details[1].encode('ascii', 'ignore')
		if username in self.admins:
			self.bot.pm(user, "No. I already know %s" %(username, ))
		else:
			self.set_password(username, password)
			self.bot.pm(user, "%s is now my master too" %(username, ))

	def remove_admin(self, user, username):
		username = username.encode('ascii', 'ignore')
		if username == self.authenticated[user]:
			self.bot.pm(user, "I can't remove you!")
		elif not username in self.admins:
			self.bot.pm(user, "Don't worry. I don't even know who %s is" %(username, ))
		else:
			for admin in self.authenticated:
				if self.authenticated[admin] == username:
					del self.authenticated[admin]
			del self.admins[username]
			self.bot.pm(user, "%s is out of my life now" %(username, ))

	def list_admin(self, user):
		self.bot.pm(user, "Current admins are: %s" %
                            ', '.join(sorted(self.admins.keys())))

	def change_password_admin(self, user, details):
		username = details[0].encode('ascii', 'ignore')
		password = details[1].encode('ascii', 'ignore')
		self.set_password(username, password)
		self.bot.pm(user, "Updated %s's password" %(username, ))

	def identify_admin(self, user, details):
		if self.bot.noadmin:
			self.bot.pm(user, "No need for that. We're all admins here!!!")
			return
	
		if user in self.authenticated:
			self.bot.pm(user, "I already know you, silly!")
			return
		
		username = details[0].encode('ascii', 'ignore')
		password = details[1].encode('ascii', 'ignore')
		if self.admins[username]:
			if self.check_password(username, password):
				self.authenticated[user] = username
				self.bot.pm(user, "Authenticated")
			else:
				self.bot.pm(user, "Incorrect password. Are you sure that's you?")
		else:
			self.bot.pm(user, "I have no idea who you are.")
	
	def user_is_admin(self, user):
		if self.bot.noadmin:
			return True
		else:
			if user in self.authenticated:
				return True
			else:
				return False

	def die(self):
		if not self.bot.noadmin:
			self.admins.close()
