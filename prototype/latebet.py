import sys

running = True

def lateBet():
	print()
	name = input("What is your slack username: ")
	if name.startswith("@") == False:
		name = "@" + name 
	name.strip(" ")
	printWelcomeMessage()
	while running:
		checkInput(input(name + ": "))

def checkInput(command):
	command = command.strip()
	if command.startswith("@latebet") == False and command != "":
		if command == "exit":
			running = False
			sys.exit()
		#print(command)
	elif command == "@latebet help":
		printHelp()
	elif command == "":
		printWelcomeMessage()
	else:
		print("'" + command + "'" +  " command not recognised.")

def printHelp():
	print("")
	print("Welcome to Late Bet, a slackbot app made by SMOKE DADDIES")
	print()
	print("Commands:")
	print("@latebet show bets : ", "shows the current bets")
	print("")

def printWelcomeMessage():
		print()
		print("Welcome to the late bet application for slack. Type '@latebet help' to begin")
		print()
	

if  __name__ == "__main__":
		lateBet()