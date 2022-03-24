#Calculate pairs

from collections import Counter

def getPairs():
	answers = word_file = open("wordle-answers-alphabetical.txt")

	word_list = []

	for word in word_file:
			word_list.append(word.strip())

	pairs = []

	for word in word_list:
		for i in range(4):
			pair = word[i]+word[i+1]
			pairs.append(pair)

	#print(pairs)

	#print(Counter(pairs).keys()) # equals to list(set(words))
	#print(Counter(pairs).values()) # counts the elements' frequency

	keys = list(Counter(pairs).keys())
	values = list(Counter(pairs).values())
	#print(sum(values))
	values = [x/sum(values) for x in values]

	data = []

	for i in range(len(keys)):
		data.append([keys[i], values[i]])

	data.sort(key=lambda x : x[1], reverse=True)

	return data
