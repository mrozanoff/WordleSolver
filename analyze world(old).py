#Matthew Rozanoff Wordle Solver

import csv
import re

answers = open("wordle-answers-alphabetical.txt").read()

alpha = "abcdefghijklmnopqrstuvwxyz"

total = (len(answers)-2314)/5
#print(total,"\n")

letper = []

for letter in alpha:
        
    letper.append(round(answers.count(letter)/total,6))
        
    #print("{0} : {1:4} : {2:.2f}%".format(letter, answers.count(letter),
                                        #answers.count(letter)/total))

##################################################### finding pairs

pairs = ['th','he','an','in','er','nd','re','ed','es','ou','to',
         'ha','en','ea','st','nt','on','at','hi','as','it','ng',
         'is','or','et','of','ti']

paird = {}

for pair in pairs:
    paird[pair] = answers.count(pair)
    #print(answers.count(pair))

#print(paird)

###################################################### finding letter placement %
    
answers2 = open("wordle-answers-alphabetical.txt").readlines()

letplac = []

for letter in alpha:

    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    
    for word in answers2:
        if word[0] == letter:
            one += 1
        if word[1] == letter:
            two += 1
        if word[2] == letter:
            three += 1
        if word[3] == letter:
            four += 1
        if word[4] == letter:
            five += 1

    letplac.append([round(one/answers.count(letter),6),
                   round(two/answers.count(letter),6),
    round(three/answers.count(letter),6), round(four/answers.count(letter),6),
    round(five/answers.count(letter),6)])

    #print("{0} : {1:5.2f}% {2:5.2f}% {3:5.2f}% {4:5.2f}% {5:5.2f}%".format(letter, one/answers.count(letter)*100, two/answers.count(letter)*100,
          #three/answers.count(letter)*100, four/answers.count(letter)*100,
          #five/answers.count(letter)*100))

for i in range(len(letper)): #multiplying tables
    for j in range(5):
        letplac[i][j] = round(letplac[i][j]*letper[i]*100,3)

for i in range(len(letplac)): #adding letters for easier csv reading
    letplac[i].insert(0,(alpha[i]))
    
#print(letplac)

with open('letter_percents.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['letter','place1','place2','place3','place4','place5',])
    writer.writerows(letplac)

##################################################### best starter word

#Search all guesses list, find the one with the highest value

words = open("all-words.txt").readlines()

print()

guesslist = []

for word in words:

    word = word.strip()

    value = 0
    spot = 0
    for letter in word:
        for j in range(26):
            if letter == letplac[j][0]:
                value += letplac[j][spot+1]
                
        spot += 1
        
    guesslist.append([word, round(value,3)])

guesslist.sort(key=lambda x: x[1], reverse = True)

print("best guesses: ", guesslist[:10])
print()

print('NEW STUFF VVV')
print()

############################################################ narrowing down guesses

answerlist = []

for word in answers2: #pulling out the possible answer list
    word = word.strip()
    value = 0
    spot = 0
    for letter in word:
        for j in range(26):
            if letter == letplac[j][0]:
                value += letplac[j][spot+1]                
        spot += 1        
    answerlist.append([word, round(value,3)])
answerlist.sort(key=lambda x: x[1], reverse = True)

#########################################################

def guess(thelist, starter, result): #narrow down list of possible answers for next guess
    
    list1 = []
    list2 = []
    list3 = []

    correct = ['','','','','']

    gcount = result.count('g') #keep track of amount of greens

    
    ycount = result.count('y')
    yletters = []
    
    if ycount > 0:
        for i in range(5):
            if result[i] == 'y':
                yletters.append(starter[i])
    print(yletters)
                
    
    gplace = []

    for i in range(5):
        if result[i] == 'g':
            gplace.append(i)

    
    if gcount == 1: #if there is only one green letter
        for i in range(5):
            if result[i] == 'g' and correct == ['','','','','']:
                del correct[i]
                correct.insert(i, [i,starter[i]])
                for j in range(len(thelist)):
                    if thelist[j][0][i] == starter[i]:
                        list1.append(thelist[j])
    if gcount > 1: #if there is more than one green letter
        for i in range(5):
            if result[i] == 'g':
                del correct[i]
                correct.insert(i, [starter[i]])
                for j in range(len(thelist)):
                    allgood = 0
                    for k in range(len(gplace)):
                        
                        if thelist[j][0][gplace[k]] == starter[gplace[k]]:
                            #print(thelist[j], thelist[j][0][gplace[k]], starter[gplace[k]])
                        
                            allgood += 1
                    if allgood == len(gplace) and thelist[j] not in list1:    
                        list1.append(thelist[j]) 

    if result.count('g') == 0:
        list1 = thelist
        
    
    print('list1:',len(list1)) ###############################################
    list1.sort(key=lambda x: x[1], reverse = True) ##   END OF GREEN CHECK  ## 
    print(list1[:10]) ###############################                       ##
    print() ##################################################################

    bletters = []
    for i in range(5):
        if result[i] == 'b':

            bletters.append(starter[i])
            
    print(bletters)
    bbletters = bletters
    bbletters.append(['',''])
    print(bbletters)
    '''
    for i in range(5):
        if result[i] == 'y' and starter[i] in bletters:
            bplace = i
            for j in range(len(list1)):
                for k in range(len(bbletters)):
                    if list1[j][0][k] == list1[j][0][bbletters[k][0]]:
                        del list1[j][0]
                        list1[j].insert(0, '-----')'''

    

#if a yellow letter is also a black letter, remove all words where the black letter is


    
    numbers = [0,1,2,3,4]
    for i in range(len(gplace)):
        numbers.remove(gplace[i])
    print(numbers)
    for letter in bletters:
         for j in range(len(list1)):
             for k in range(len(numbers)):
                 if letter[0] == list1[j][0][numbers[k]]:
                    #print(list1[j], letter, list1[j][0][numbers[k]])
                    del list1[j][0]
                    list1[j].insert(0, '-----')

    for word in list1:
        if word[0] != '-----':
            list2.append(word)


    print('list2:',len(list2)) ######################
    list2.sort(key=lambda x: x[1], reverse = True) ##   SAREE
    print(list2[:10]) ###############################   YYBBG
    print() ## END OF BLACK CHECK ###################

    
    for i in range(5):
        #numbers = [0,1,2,3,4]
        #numbers.remove(i)
        #print(i, "     ", numbers)
        if result[i] == 'y':
            for j in range(len(list2)):
                if list2[j][0][i] == starter[i] or starter[i] not in list2[j][0]:
                    del list2[j][0]
                    list2[j].insert(0, '-----')

    for word in list2:
        if word[0] != '-----':
            list3.append(word)

    '''
    ycount = result.count('y')

    if ycount == 1:
        for i in range(5):
            if result[i] == 'y':
                for j in range(len(list2)):
                    allgood = 0
                    if list2[j][0] != '-----' and starter[i] in list2[j][0]:
                        if list2[j] not in list3:
                            list3.append(list2[j])


    elif ycount > 1:
        yplace = []
        for i in range(5):
            if result[i] == 'y':
                yplace.append(i)

        for i in range(5):
            if result[i] == 'y':
                for j in range(len(list2)):
                    allgood = 0
                    for k in range(len(yplace)):
                        
                        if list2[j][0][yplace[k]] != starter[yplace[k]]:
                            allgood += 1

                    if allgood == len(yplace) and list2[j] != '-----':    
                        list3.append(list2[j])''' 


    
    '''
                if list2[j][0] == 'no':
                    pass
                else:
                    yes = 0
                    for k in range(len(numbers)):
                        if list2[j][0][numbers[k]] == starter[i]:
                            yes += 1
                    if yes > 0:
                        list3.append(list2[j])
                    elif yes == 0:
                        del list2[j][0]
                        list2[j].insert(0, 'no')'''
                    

                
    print('list3:',len(list3)) #####################################

    list3.sort(key=lambda x: x[1], reverse = True)
    print(list3[:10]) ################################################3
    '''
    print(list3[0][0][0],starter[0])

    for i in range(5):
        if result[i] == 'y':
            for word in list3:
                #print(word[0][i], starter[i])
                if word[0][i] == starter[i]:
                    list3.remove(word)
                    

    print('list3:',len(list3))
    list3.sort(key=lambda x: x[1], reverse = True)
    print(list3[:10])
    print()'''

    print(correct)

    return list3




def takeinput():
    result = ''
    newdatalist = answerlist
    while result != 'ggggg':
        if result == 'ggggg':
            break
        newdatalist = answerlist

        starter = input("starter:")

        result = input("result:")

        newdatalist = guess(newdatalist, starter,result)

    print("Answer is: ", starter)

takeinput()

#y: if in the word, but not at i, append. not s in y place OR in any other place




