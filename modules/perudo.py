from base_module import *

from math import ceil
from random import randint
import re

NUM_STARTING_DICE = 5

HEAD = 1

class BadBet(Exception):
	pass


class Bet(object):
	
	def __init__(self, face=None, num=None):
		self._face = None
		self._num  = None
		
		self.face = face
		self.num  = num
	
	
	def set_face(self, value):
		face = int(value)
		if face < 1 or face > 6:
			raise BadBet("There cannot be a %d%s face on a die!"%(
				face,
				"st" if face%10 == 1 else
				"nd" if face%10 == 2 else
				"rd" if face%10 == 3 else
				"th"
			))
		
		self._face = face
	
	def get_face(self):
		return self._face
	
	face = property(fget = get_face, fset = set_face)
	
	
	def set_num(self, value):
		num = int(value)
		if num < 1:
			raise BadBet("Bet must be at least one die!")
		
		self._num = num
	
	def get_num(self):
		return self._num
	
	num = property(fget = get_num, fset = set_num)
	
	
	def __repr__(self):
		return "Bet(%d, %d)"%(self.face, self.num)
	
	
	def __str__(self):
		return "%d %ss"%(self.num, self.face if self.face != HEAD else "head")


class Player(object):
	
	def __init__(self, game, name):
		self.game = game
		self.name = name
		
		self._num_dice = NUM_STARTING_DICE
		self.dice = None
	
	
	def set_num_dice(self, value):
		self._num_dice = value
		if value == 1:
			self.game.one_die_mode = True
	
	def get_num_dice(self):
		return self._num_dice
	
	num_dice = property(fget = get_num_dice, fset = set_num_dice)
	
	
	def roll_dice(self):
		self.dice = [randint(1, 6) for i in range(self.num_dice)]
	
	
	def check_bet(self, new_bet):
		"Return True if a bet is valid. If not raise an exception."
		old_bet = self.game.current_bet
		
		if old_bet == None:
			# Can't start with heads (unless one-die-rules)
			if new_bet.face == HEAD and not self.game.one_die_mode:
				raise BadBet("Can't start with heads.")
			
			return True
		
		# Is the player allowed to change the bet?
		if (new_bet.face != old_bet.face
		    and self.game.one_die_mode
		    and not self.num_dice == 1):
			raise BadBet("You cannot change the face as this round is one-die mode --"
			             + " you must have only one die to change the face.")
		
		# Is the number of dice bet less/equal to before?
		if new_bet.num <= old_bet.num:
			# Have we switched to heads?
			if old_bet.face != HEAD and new_bet.face == HEAD:
				# Is the number not at least ceil(half old num)?
				min_head_bet = ceil(old_bet.num / 2.0)
				if new_bet.num < min_head_bet:
					raise BadBet("Bet must be at least %d heads!"%min_head_bet)
			# Have we gone to a higher-face?
			elif new_bet.face > old_bet.face:
				# The number must stay the same
				if new_bet.num < old_bet.num:
					raise BadBet("Bet must be at least %d."%old_bet.num)
			else:
				# No more exceptions, the bet must be bad
				raise BadBet("Bet must be >%d."%old_bet.num)
		
		# Is the user going from heads to non-heads?
		if old_bet.face == HEAD and new_bet.face != HEAD:
			# Is the bet at least double+1 the old one?
			min_head_bet = (old_bet.num * 2) + 1
			if new_bet.num < min_head_bet:
				raise BadBet("Bet must be at least %d!"%min_head_bet)
		
		return True
	
	
	def place_bet(self, new_bet):
		assert(self.check_bet(new_bet))
		
		self.game.current_bet = new_bet
		self.game.next_turn()
	
	
	def challenge(self):
		"""
		Challenge the last bet. Returns boolean indicating success and sets next
		round's mode.
		"""
		self.game.one_die_mode = False
		
		if len(self.game.matching_dice) >= self.game.current_bet.num:
			# Challenger looses!
			self.num_dice -= 1
			self.starts()
			return False
		else:
			# Challenger wins!
			self.game.previous_player.num_dice -= 1
			self.game.previous_player.starts()
			return True
	
	
	def starts(self):
		"Order the player-queue so this player starts the next round."
		while self.game.players[0] != self:
			self.game.rotate_players()



class Game(object):
	
	def __init__(self, player_names):
		"""A model of a perudo game with the supplied list of player names."""
		
		# List of player objects
		self.players = []
		for name in player_names:
			self.players.append(Player(self, name))
		
		# Is the game currently in one-die mode following a player having just lost
		# all but one die.
		self.one_die_mode = False
		
		# The current bet
		self.current_bet = None
	
	
	def __iter__(self):
		return iter(self.players)
	
	
	def __getitem__(self, name):
		for player in self.players:
			if player.name == name:
				return player
		
		raise KeyError(name)
	
	
	@property
	def all_dice(self):
		# The values of all the dice in play
		return sum((p.dice for p in self.players), [])
	
	
	@property
	def matching_dice(self):
		# Die which match the bet
		
		bet = self.current_bet
		def die_counts(die):
			return die == bet.face or (die == HEAD and not self.one_die_mode)
		
		return filter(die_counts, self.all_dice)
	
	
	@property
	def current_player(self):
		"The player whose turn it is to place a bet."
		return self.players[0]
	
	
	@property
	def previous_player(self):
		"The player whose turn it was last."
		return self.players[-1]
	
	
	def start_round(self):
		assert(len(self.players) > 1)
		
		# Roll all player's dice
		for player in self.players:
			player.roll_dice()
		
		self.current_bet = None
	
	
	def next_turn(self):
		"Select the next player to take a turn."
		self.rotate_players()
	
	
	def rotate_players(self):
		self.players.append(self.players.pop(0))
	
	
	def knock_out_players(self):
		"Knocks out players with no die and returns their names"
		ko_player_names = []
		for player_num in range(len(self.players)-1, -1, -1):
			if self.players[player_num].num_dice < 1:
				ko_player_names.append(self.players[player_num].name)
				del self.players[player_num]
		
		return ko_player_names



requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""
	Perudo Module
	A module that allows users to play a version of the game Perudo.
	
	Rules:
	Players each start with 5 six-sided, fair dice with a "head" in place of the 1. They shake their dice (and keep them hidden) and take it in turns to place bets on the of number times a particular face appeared in total. Heads count towards the other numbers. For example, if the bet was 3 4s then the number of 4s would be however many 4s there were + the number of heads.
	
	Each person in succession may either increase the bet or challenge it. If they increase the bet they must either increase the number of the face or increase the number of times they think it appears (if they choose a lower-or-equal face). If you pick heads you can divide the number by two (rounding up) as your bet for the number of heads. If the last bet was on heads and you wish to bet on another face you must double the number and add one.
	
	If you challenge someone's bet and there are at least as many of the bet face then you lose a die. If there were less than the bet then you lose a die.
	
	When someone reaches one die then the next round is played in "one-die-mode" which disallows all players with more than one die from changing the face. It also doesn't count heads as the numbers.
	
	When someone runs out of die they are out of the game. The winner is the last player standing.
	
	Each round starts with the loser of the previous round. You cannot start a round with a bet on the number of heads except in one-die-mode.
	"""
	
	def __init__(self, *args, **kwargs):
		ModuleBase.__init__(self, *args, **kwargs)
		
		self.game = None
		self.players = []
	
	
	@on_private_match("(?:play |join )?(new )?perudo(?: game)?", re.I)
	def new_game(self, source_name, source_host, message, new):
		# Is a game in progress?
		if self.game is not None:
			self.game = None
			self.players = []
		
		# If a new game required
		if new == "new ":
			self.players = []
		
		# Has the person already joined
		if source_name in self.players:
			self.bot.reply("You are already in the game.")
			return
		
		# Anounce in the channel
		self.bot.say("%s %s"%(
			source_name,
			"started a new game of Perudo! PM me with 'play perudo' to join!"
			if len(self.players) < 1 else
			"joined %s for a game of Perudo!"%(
				"%s and %s"%(", ".join(self.players[:-1]), self.players[-1])
				if len(self.players) > 1 else
				self.players[0]
			)
		))
		
		# PM the user with instructions
		self.bot.reply("Welcome to Perudo!")
		self.bot.reply("When everyone's joined say 'start perudo game' in  the channel.")
		
		# Add the player to the game
		self.players.append(source_name)
	
	
	@on_addressed_match("(?:start|begin) (?:game|perudo(?: game)?)", re.I)
	def start_game(self, source_name, source_host, message):
		if len(self.players) < 2:
			self.bot.say("At least two players needed for a game of Perudo.")
		else:
			self.bot.say("Starting a new game of Perudo between %s and %s"%(
				", ".join(self.players[:-1]),
				self.players[-1]))
			
			self.game = Game(self.players)
			self.next_round()
	
	
	def next_round(self):
		# Knock-out loosers
		for person in self.game.knock_out_players():
			self.bot.say("%s has no more dice and has been knocked out!"%person)
			self.bot.pm(person, "You have no more dice. You're out of the game!")
		
		# Has the game been won?
		if len(self.game.players) == 1:
			self.bot.say("%s won the game!"%self.game.players[0].name)
			self.game = None
			return
		
		self.game.start_round()
		self.bot.say("Starting round. %d dice in Play. Rolling dice..."%(
			len(self.game.all_dice)
		))
		
		if self.game.one_die_mode:
			self.bot.say(("%s is down to one die! " +
			             "One-Dice-Mode is enabled for this round!")%(
			             self.game.current_player.name))
		
		for player in self.game.players:
			self.bot.pm(player.name, "Dice Rolled: %s"%(
				", ".join(str(x) if x > 1 else "Head" for x in player.dice)
			))
		
		self.next_bet()
	
	
	def next_bet(self):
		if self.game.current_bet is None:
			self.bot.say("%s: Place your bet."%self.game.current_player.name)
		else:
			self.bot.say("%s: Any advance on %s?"%(
				self.game.current_player.name,
				self.game.current_bet
			))
	
	
	@on_addressed_match("(\d+)(?: .*)? (head|[1-6])s?", re.I)
	def place_bet(self, source_name, source_host, message, rnum, rface):
		if self.game is None:
			return
		
		if self.game.current_player.name != source_name:
			self.bot.say("%s: It is not your turn to bet."%source_name)
			return
		
		try:
			num = int(rnum)
			if rface.lower() == "head":
				face = 1
			else:
				face = int(rface)
		except ValueError:
			self.bot.say("Couldn't understand bet.")
		
		try:
			bet = Bet(face, num)
			self.game.current_player.place_bet(bet)
		except BadBet, e:
			self.bot.say("Error: %s"%e)
			return
		
		self.next_bet()
	
	
	@on_addressed_match("challenge|dudo|no ?wai", re.I)
	def challenge(self, source_name, source_host, message):
		if self.game is None:
			return
		
		# Must place a bet first!
		if self.game.current_bet is None:
			self.bot.say("No bets have been placed!")
			return
		
		if self.game.current_player.name != source_name:
			self.bot.say("%s: It is not your turn to bet."%source_name)
			return
		
		
		self.bot.say("%s challenges %s's %d %ss"%(
			self.game.current_player.name,
			self.game.previous_player.name,
			self.game.current_bet.num,
			self.game.current_bet.face if self.game.current_bet.face else "head",
		))
		
		heads = len(filter((lambda x: x == HEAD), self.game.matching_dice))
		number = filter((lambda x: x != HEAD), self.game.matching_dice)
		numbers = len(number)
		
		message = ""
		for player in self.game.players:
			message += "%s had: %s. "%(
				player.name,
				",".join(str(n) if n != HEAD else "head" for n in player.dice)
			)
		message.strip()
		self.bot.say(message)
		
		message = ""
		if heads > 0:
			message += "%d heads "%heads
		
		if heads > 0 and numbers > 0:
			message += "and "
		
		if numbers > 0:
			message += "%d %ds "%(numbers, number[0])
		
		if heads > 0 and numbers > 0:
			message += "= %d %ds "%(heads + numbers, number[0])
		
		previous_player = self.game.previous_player.name
		current_player = self.game.current_player.name
		
		if self.game.current_player.challenge():
			name = previous_player
			message += "so %s lost the challenge!"
		else:
			name = current_player
			message += "so %s challenged incorrectly!"
		
		message.strip()
		self.bot.say(message%name)
		self.bot.pm(name, "You lost a die!")
		
		self.next_round()


if __name__=="__main__":
	global g
	g = Game(["a","b","c"])
	
	g.start_round()
	
	print "All Dice:", g.all_dice
	print "Current Dice:", g.current_player.dice
	
	g.current_player.place_bet(Bet(5, 7))
	g.current_player.place_bet(Bet(HEAD, 4))
	
	print "Bet:", g.current_bet
	print "Matching bet:", g.matching_dice
	print g.current_player.challenge()
	print g.knock_out_players()

