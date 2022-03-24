
import random

def processGuess(theAnswer, theGuess):

	clue = ''

	gletters = ['','','','','']
	yletters = ['','','','','']
	bletters = ['','','','','']

	numbers = [0,1,2,3,4]

	
	for i in range(len(theGuess)):
		if theGuess[i] == theAnswer[i]:
			gletters[i] = theGuess[i]
			numbers.remove(i)
		elif theGuess[i] != theAnswer[i] and theGuess[i] not in theAnswer:
			bletters[i] = theGuess[i]
	'''
	print(gletters)
	print(yletters)
	print(bletters)'''

	for i in range(len(theGuess)):
		if theGuess[i] == theAnswer[i]:
			clue += 'g'
		elif theGuess[i] != theAnswer[i] and theGuess[i] not in theAnswer:
			clue += 'b'
		elif theGuess[i] != theAnswer[i] and theGuess[i] in theAnswer:
			bol = False
			for j in range(len(numbers)):
				if theGuess[i] == theAnswer[numbers[j]] and theGuess[i] not in yletters:
					clue += 'y'
					yletters[i] = theGuess[i]
					bol = True
			if bol == False:
				clue += 'b'


	#print('the answer: ', theAnswer)
	print('Result: ', clue)
	return clue


def game(answer, guess):
	return str(processGuess(answer, guess))


def createWord():
    word_list = []
    word_file = open("wordle-answers-alphabetical.txt")

    for word in word_file:
        word_list.append(word.strip())

    answer = random.choice(word_list)

    return answer