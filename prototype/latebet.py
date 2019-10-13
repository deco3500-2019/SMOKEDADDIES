import sys
import json
import threading
import time
from pynput.keyboard import Key, Controller

running = True

bets = 1
name = "Hello world"


"""
bet1 = {
	"bet_id": 1,
	"punter": "Dan",
	"target": "Dmitri",
	"session": "U01",
	"points": 10
}

bet_table = [bet1]


user1 = {
	"user_id": 1,
	"name": "Dimfili",
	"sessions": ["U01", "P01"],
	"points": 100
}

user2 = {
	"user_id": 2,
	"name": "Daniel",
	"sessions": ["U02", "P01"],
	"points": 80
}

leaderboard = [user1, user2]

keyboard = Controller()
"""

def sampleBet():
	time.sleep(5)
	print()
	print()
	placeBet("@lorns", name, "U01", "9")
	print("******************** BET NOTIFICATION *********************")
	print("@lorns has placed a bet on {} (That's you!) being late to U01 for 9 points.".format(name))
	print()
	print("WHAT ARE YOU GONNA DO????")
	print('Option 1: @latebet double down - Double down on the bet')
	print('Option 2: @latebet rage - Send an angry emoji')
	print()
	print("@lorns: Don't be late!!!!")
	print("")
	print("____________________________________________________________")
	print("(Press Enter)")
	print("____________________________________________________________")
	#if (input(name + ": ") == "@latebet double down"):
		#print("Bet doubled")



def lateBet():
	print()
	loadBets()
	loadLeaderboard()
	global name
	name = input("What is your slack username: ")
	if name.startswith("@") == False:
		#name = "@" + name
		pass
	name = name.strip(" ")
	checkUser()
	#addUser()
	printWelcomeMessage()
	t = threading.Thread(target=sampleBet)
	t.daemon = True
	t.start()
	run()

def run():
	while running:
		checkInput(input("@" + name + ": "))

def checkInput(command):
	command = command.strip()
	if command.startswith("@latebet") == False and command != "":
		if command == "exit":
			running = False
			sys.exit()
		#print(command)
	elif command == "@latebet help":
		printHelp()
	elif command == "@latebet info":
		printInfo()
	elif command == "@latebet leaderboard":
		printLeaderboard()
	elif command == "@latebet show bets":
		printShowBets()
	elif command == "@latebet place bet":
		print("")
		target = input("Who would you like to place a bet on?: ")
		session = input("What class do you think they will be late to?: ")
		points = input("How many points would you like to bet?: ")
		placeBet(name, target, session, int(points))
		print("Bet placed on {} being late to {} for {} points.".format(target, session, points))
		print()
		saveBets()
	elif command == "@latebet save":
		saveBets()
	elif command == "@latebet load":
		loadBets()
	elif command == "@latebet rage":
		rage()
	elif command == "":
		#printWelcomeMessage()
		pass
	else:
		print("'" + command + "'" +  " command not recognised.")

def printHelp():
	print("")
	print("Welcome to latebet, a slackbot app made by SMOKE DADDIES")
	print()
	print("Commands:")
	print("@latebet leaderboard : ", "shows the leaderboard")
	print("@latebet show bets : ", "shows the current bets")
	print("@latebet place bet : ", "opens a dialog to place a bet")
	print("")

def printInfo():
	print()
	print("******************** INFORMATION ********************")
	print()
	print("CREATORS: SMOKE DADDIES")
	print()
	print("'latebet' is a slack application aimed at improving tardiness behaviour through the use of a")
	print("tokenised gambling system. The friendly competition between classmates")
	print("aims to encourage class members to arrive to class on time as their precious points are at stake.")
	print()
	print("Gamble responsibly.")
	print()

def printWelcomeMessage():
	print()
	print("Welcome to the latebet application for slack. Type '@latebet help' to begin")
	print()

def printShowBets():
	global bet_table
	
	id = 0
	punter = ""
	target = ""
	session = ""
	points = 0

	print("")
	print("******************** CURRENT BETS ********************")

	for bet in bet_table:
		bet_id = bet.get("bet_id")
		punter = bet.get("punter")
		target = bet.get("target")
		session = bet.get("session")
		points = bet.get("points")
		print("{}. {} has placed a bet on {} on being late to: {} for {} points.".format(bet_id, punter, target, session, points))
	print("")
	
def placeBet(punter, target, session, points):
	bet_id = len(bet_table) + 1
	bet = {
		"bet_id": bet_id,
		"punter": punter,
		"target": target,
		"session": session,
		"points": points
	}
	bet_table.append(bet)

def saveBets():
	with open("bets.json", "w") as write_file:
		json.dump(bet_table, write_file)


def loadBets():
	with open("bets.json", "r") as read_file:
		global bet_table
		bet_table = json.load(read_file)
		#printShowBets()

#def loadLeaderboard():
		#with open("users.json", "r") as read_file:
		#global leaderboard
		#leaderboard = json.load(read_file)
		#printShowBets()

def printLeaderboard():
	global leaderboard

	user_id = 0
	name = ""
	sessions = []
	points = 0

	newlist=sorted(leaderboard, key = lambda k:k['points'], reverse=True)

	print("")
	print("******************** LEADERBOARD ********************")
	print("POINTS   |    NAME")
	

	for users in newlist:
		user_id = users.get("user_id")
		name = users.get("name")
		#sessions = users.get("sessions")
		points = users.get("points")
		#print("POINTS   |    NAME")
		print("{}       |   @{}".format(points, name))
	print("")

def addUser():
	userx = {
	"user_id": len(leaderboard),
	"name": name,
	"sessions": ["U01", "P01"],
	"points": 100
	}
	leaderboard.append(userx)

def saveLeaderboard():
	with open("leaderboard.json", "w") as write_file:
		json.dump(leaderboard, write_file)

def loadLeaderboard():
	with open("leaderboard.json", "r") as read_file:
		global leaderboard
		leaderboard = json.load(read_file)

def checkUser():
	for users in leaderboard:
		if users.get("name") == name:
			return True
	registerUser()

def registerUser():
	print()
	print("It looks like you haven't registered with us before! Please answer the following questions.")
	attr1 = input("What studio session do you attend? e.g U01, U02 etc.: ")
	attr2 = input("What practical session do you attend? e.g P01, P02 etc.: ")
	usr_sessions = [attr1, attr2]
	userx = {
		"user_id": len(leaderboard),
		"name": name,
		"sessions": usr_sessions,
		"points": 100
	}
	leaderboard.append(userx)
	saveLeaderboard()

def rage():
	print()
	print("@" + name + ": @lorns >:( ")
	print()
	t2 = threading.Thread(target=rageResponse)
	t2.daemon = True
	t2.start()

def rageResponse():
	time.sleep(3)
	print()
	print()
	print("@lorns: :P")
	print()
	print("____________________________________________________________")
	print("(Press Enter)")
	print("____________________________________________________________")


if  __name__ == "__main__":
		lateBet()