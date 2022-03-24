#Matthew Rozanoff Wordle Solver 2.0

import csv
import WordleGame as g
import WordlePairs as p

############################################# OG Code

answers = open("wordle-answers-alphabetical.txt").read()

alpha = "abcdefghijklmnopqrstuvwxyz"
total = (len(answers)-2314)
#print(total)
letper = []
for letter in alpha:   
    letper.append(round(answers.count(letter)/total,6))       
    #print("{0} : {1:4} : {2:.2f}%".format(letter, answers.count(letter),
                                        #answers.count(letter)/total))

############################################### Finding individual percentages

def letperCalc(thelist):
    #print(thelist)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    letper = []
    total = len(thelist)*5
    #print(total)
    for letter in alpha:
        count = 0
        for word in thelist:
            count += word.count(letter)
                                
        letper.append(round(count/total,6))
        
        #print("{0} : {1:4} : {2:.2f}%".format(letter, answers.count(letter),
                                        #answers.count(letter)/total))
    #print(letper)
    return letper

#print(letperCalc(answers))

######################################## Finding placement percentages

answers2 = open("wordle-answers-alphabetical.txt").readlines()

letplac = []

for letter in alpha:

    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    
    for word in answers2:
        word = word.strip()
        
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

####################################################### let plac function

def createLetplac(thelist):
    letplac = []
    letper = letperCalc(thelist)



    for letter in alpha:

        one = 0
        two = 0
        three = 0
        four = 0
        five = 0
        
        for word in thelist:
            #word = word.strip()
            
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

       # print("{0} : {1:5.2f}% {2:5.2f}% {3:5.2f}% {4:5.2f}% {5:5.2f}%".format(letter, one/answers.count(letter)*100, two/answers.count(letter)*100,
             # three/answers.count(letter)*100, four/answers.count(letter)*100,
             # five/answers.count(letter)*100))

    for i in range(len(letper)): #multiplying tables
        for j in range(5):
            letplac[i][j] = round(letplac[i][j]*letper[i]*100,3)

    for i in range(len(letplac)): #adding letters for easier csv reading
        letplac[i].insert(0,(alpha[i]))

   # print(letplac)
    return letplac



###################################################### Starter Word

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



##################################################### Answer List

#make this into a funciont to recalculate values based on current words
def makeAnswerList():
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
    return answerlist

######################################################### Getting Updated Lists

def updateList(thelist): 
    thelist = listClean(thelist)
    letplac = createLetplac(thelist)
    pairdata = p.getPairs()
    #print(letplac)
    #print(thelist)
    updatedlist = []
    for word in thelist:
        value = 0
        spot = 0
        #print(word, word[0], word[0][0])
        for letter in word:
            for j in range(26):
                if letter == letplac[j][0]:
                    value += letplac[j][spot+1]                
            spot += 1        
        updatedlist.append([word, round(value,3)])

    updatedlist.sort(key=lambda x: x[1], reverse = True)
    #print('BEFORE', updatedlist[:10])
    '''
    for pair in pairdata: #Added pair data, good but slow
        for i in range(len(updatedlist)):
            if pair[0] in updatedlist[i][0]:
                #print(updatedlist[i][1] , pair[1])
                updatedlist[i][1] = round(updatedlist[i][1] + pair[1],3)'''

    updatedlist.sort(key=lambda x: x[1], reverse = True)
    #print('AFTER',updatedlist[:10])
    return updatedlist

############################################################# Clean list

def listClean(thelist):
    newlist = []
    for stuff in thelist:
        newlist.append(stuff[0])
    return newlist

######################################################### Checking for Double Letter

def checkDouble(ylet, blet):
    for i in range(len(ylet)):
        for j in range(len(blet)):
            if ylet[i][1] == blet[j][1] and len(ylet[i][1]) > 0:
                return True

######################################################### Getting Black Letter Placement

def getBplac(ylet, blet):
    for i in range(len(ylet)):
        for j in range(len(blet)):
            if ylet[i][1] == blet[j][1] and len(ylet[i][1]) > 0:
                return blet[j]

############################################################ Getting Non Double BLetters

def getOtherB(ylet, blet):
    others = []
    #print(ylet)
    #print(blet)
    for i in range(len(ylet)):
        for j in range(len(blet)):
            if ylet[i][1] != blet[j][1] and len(ylet[i][1]) > 0 and len(blet[i][1]) > 0:
                 others.append(blet[j])
                 print(ylet[i][1], blet[j][1], len(ylet[i][1]))
    return others

###################################################### Narrow Down Function

def guess(thelist, starter, result): #narrow down list of possible answers for next guess

    list1 = []
    list1_2 = []
    list2 = []
    list3 = []

    correct = [['',''],['',''],['',''],['',''],['','']]
    bletters = [['',''],['',''],['',''],['',''],['','']]
    yletters = [['',''],['',''],['',''],['',''],['','']]

    for i in range(5): #Record letter knowledge
        if result[i] == 'g':
            del correct[i]
            correct.insert(i, [i,starter[i]])
        if result[i] == 'b':
            del bletters[i]
            bletters.insert(i, [i,starter[i]])
        if result[i] == 'y':
            del yletters[i]
            yletters.insert(i, [i,starter[i]])
    #print("Correct: ", correct)
    #print("Yletters: ", yletters)
    #print("Bletters: ", bletters, "\n")
    '''
    if checkDouble(yletters, correct) == True:
        #print("TRUE")
    else:
        #print("FALSE")'''
            
    gcount = result.count('g') #keep track of amount of green
    
    gplace = []
    for i in range(5):
        if result[i] == 'g':
            gplace.append(i)
  
    '''if checkDouble(yletters, correct) == True:
        x = getBplac(correct, yletters)
        y = getBplac(yletters, correct)
        print(x, y)
        z = []
        z.append(x)
        z.append(y)
        print(len(z))
        numbers = [0,1,2,3,4]
        for i in range(len(z)):
            numbers.remove(z[i][0])
        print(numbers)
        for i in range(len(numbers)):
            for j in range(len(thelist)):
                if thelist[j][0][numbers[i]] == x[1]:
                    list1.append(thelist[j])'''
    
    if checkDouble(yletters, correct) == True:
        x = getBplac(correct, yletters)
        #print(x)

        for j in range(len(thelist)):
            double = 0
            for k in range(5):
                if thelist[j][0][k] == x[1]:
                    #print(thelist[j][0][i], x[1])
                    double += 1
            if double == 2:
                list1_2.append(thelist[j])

        if gcount == 1: #if there is only one green letter
            for i in range(5):
                if result[i] == 'g':
                    for j in range(len(list1_2)):
                        if list1_2[j][0][i] == starter[i]:
                            list1.append(list1_2[j])
                            
        if gcount > 1: #if there is more than one green letter
            for i in range(5):
                if result[i] == 'g':
                    del correct[i]
                    correct.insert(i, [starter[i]])
                    for j in range(len(list1_2)):
                        allgood = 0
                        for k in range(len(gplace)):
                            if list1_2[j][0][gplace[k]] == starter[gplace[k]]:
                                #print(thelist[j], thelist[j][0][gplace[k]], starter[gplace[k]])
                                allgood += 1
                        if allgood == len(gplace) and list1_2[j] not in list1:    
                            list1.append(list1_2[j])

        print('list1_2:',len(list1_2)) ###############################################
        list1_2.sort(key=lambda x: x[1], reverse = True) ##   END OF GREEN CHECK  ## 
        print(list1_2[:10]) ###############################   START OF YELLOW     ##
        print()

    else:

        if gcount == 1: #if there is only one green letter
            for i in range(5):
                if result[i] == 'g':
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

    if result.count('g') == 0: #if no green letters
        list1 = thelist
        
    print('list1:',len(list1)) ###############################################
    list1.sort(key=lambda x: x[1], reverse = True) ##   END OF GREEN CHECK  ## 
    print(list1[:10]) ###############################   START OF YELLOW     ##
    print() ##################################################################

    '''yplace = [] #for black sorting
    for i in range(5):
        if result[i] == 'y':
            yplace.append(i)'''

    for i in range(5):
        if result[i] == 'y':
            for j in range(len(list1)):
                if list1[j][0][i] == starter[i] or starter[i] not in list1[j][0]:
                    del list1[j][0]
                    list1[j].insert(0, '-----')

    for word in list1:
        if word[0] != '-----':
            list2.append(word)

    print('List2:',len(list2)) ###############################################
    list2.sort(key=lambda x: x[1], reverse = True) ##   END OF YELLOW CHECK ## 
    print(list2[:10]) ###############################   START OF BLACK     ##
    print() ##################################################################

    '''if checkDouble(yletters, bletters) == True:
        #print("TRUE")
    else:
        #print("FALSE")'''


    if checkDouble(yletters, bletters) == True:

        x = getBplac(yletters, bletters)
        #print(x[0])
        y = getOtherB(yletters, bletters)
        #print(y)

        for j in range(len(list2)): #get rid of all words with black double letter
            if list2[j][0][x[0]] == x[1]:
                del list2[j][0]
                list2[j].insert(0, '-----')

        numbers = [0,1,2,3,4]
        for i in range(len(gplace)):
            numbers.remove(gplace[i])
        #print(numbers)
        numbers.remove(x[0])
        #print(numbers)
        #print(list2[:100])
        #print(len(y))
        if len(y) > 5:
            print('fuck up')
            y = y[0:5]
        #print(y)
        for i in range(len(y)):
            for j in range(len(list2)):
                for k in range(5):
                    if y[i][1] == list2[j][0][k]:
                        #print(list1[j], letter, list1[j][0][numbers[k]])
                        del list2[j][0]
                        list2[j].insert(0, '-----')
        #print(list2[:100])

    else:
        numbers = [0,1,2,3,4]
        for i in range(len(gplace)):
            numbers.remove(gplace[i])
        #print(numbers)
        
        for i in range(5):
            if result[i] == 'b':
                for j in range(len(list2)):
                    for k in range(len(numbers)):
                        if starter[i] == list2[j][0][numbers[k]]:
                            #print(list1[j], letter, list1[j][0][numbers[k]])
                            del list2[j][0]
                            list2[j].insert(0, '-----')
                          


    for word in list2:
        if word[0] != '-----':
            list3.append(word)

    print('List3:',len(list3)) ###############################################
    list3.sort(key=lambda x: x[1], reverse = True) ##   END OF BLACK CHECK ## 
    print(list3[:10]) ###############################                     ##
    print() ##################################################################

    return list3
    
    #print(updateList(list3)[:10])


def go():
    #lst = updateList(guesslist)

    #print("Best Guesses: ", lst[:5], "\n")


    result = ''
    newdatalist = makeAnswerList()
    theanswer = g.createWord()
    #theanswer = 'eerie'
    guesses = 0
    times = 0
    print('Trying to find: ', theanswer)
    while result != 'ggggg':
        if result == 'ggggg':
            break

        if times == 0:
            guessword = guesslist[0][0]
        else:
            guessword = newdatalist[0][0]
        #guessword = input("Guess:")

        print('Guess', guesses+1, ':', guessword)
        result = g.game(theanswer, guessword)
        

        newdatalist = guess(newdatalist, guessword, result)

        newdatalist = updateList(newdatalist)

        #print("Updated List: ", len(newdatalist))
        #print(newdatalist[:10])

        times += 1
        guesses += 1


    print("Answer is: ", guessword)
    print('Guessed in: ', guesses, 'tries')
    print()

    fails = ''
    if guesses > 6:
        fails = theanswer

    return guesses, fails


##If there are two yellow letters for a word with only one letter, only supposed to be one yellow
##unable to deal with three E's
#Fails: Urine, Hunky, Tiger, Lunch

def automate():
    r = 10000
    

    tot = 0
    fails = []
    errors = []
    failnumber = 0

    for i in range(r):
        try:
            guess, fail = go()
            tot += guess
            fails.append(fail)
        except:
            failnumber += 1

    fails = list(filter(None, fails))
    avg = tot/(r-failnumber)
    print()
    print('Average Guesses: ',avg)
    print('Failed Words: ', fails)

automate()




def takeinput():
    result = ''
    newdatalist = makeAnswerList()
    theanswer = g.createWord()
    theanswer = 'eerie'
    guesses = 0
    times = 0
    while result != 'ggggg':
        if result == 'ggggg':
            break

        guessword = input("Guess:")

        result = g.game(theanswer, guessword)
        print(theanswer, guessword)

        newdatalist = guess(newdatalist, guessword, result)

        newdatalist = updateList(newdatalist)

        print("Updated List: ", len(newdatalist))
        print(newdatalist[:10])

        times += 1
        guesses += 1


    print("Answer is: ", guessword)
    print('guessed in: ', guesses, 'tries')

    fails = ''
    if guesses > 6:
        fails = theanswer

    return guesses, fails

#takeinput()

















            



















