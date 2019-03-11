import time
import inflect
import sys
import nltk
import requests
import string
from bs4 import BeautifulSoup
from queue import Queue
from googlesearch import search
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag, map_tag


#if 'not' is in question, calculates things with least hits
def not_score (answer_count, answerSplit):

        confidence = answer_count[0] - min(answer_count[1], answer_count[2])
        final_answer = 0

        if(answer_count[1] < answer_count[final_answer]):
            confidence = answer_count[final_answer] - answer_count[1]
            final_answer = 1
        if(answer_count[2] < answer_count[final_answer]):
            confidence = answer_count[final_answer] - answer_count[2]
            final_answer = 2

        

        return (final_answer, confidence)

#tiebreaker if simple and advanced dont return a high enough confidence level
def tiebreaker(question, all_text, answerSplit, not_type):
    
    print(question)
    
    answer_count = [0, 0, 0, 0]
    counter = 0
    print('...')
    print('Confidence level too low...')
    print('Running tiebreaker search...')

    engine = inflect.engine()


    #ignores common punctuation
    #tie breaker search that counts for each instance regardless if it is in same text_strip
    for data in all_text:
        data_strip = [x.strip(string.punctuation) for x in (data.text).split()]
        for x in answerSplit:
            #Breaks answers up word by word and searches for them
            for word in x.split() :
                for numWords in data_strip:
                    #Compares words regardless of plurality ..
                    if counter == 3:
                        counter = 0

                    if(engine.compare(word.upper(), numWords.upper())):
                        answer_count[counter] += 1
                     
            counter += 1


    if (not_type == False):
        confidence = answer_count[0] - max(answer_count[1], answer_count[2])
        final_answer = 0

        if(answer_count[1] > answer_count[final_answer]):
            confidence = answer_count[1] - answer_count[final_answer]
            final_answer = 1
        if(answer_count[2] > answer_count[final_answer]):
            confidence = answer_count[2] - answer_count[final_answer]
            final_answer = 2
    else:
        result_not = not_score(answer_count, answerSplit)
        final_answer = result_not[0]
        confidence = result_not[1]


    #print scores, confidence level, and answers
    f = open('results.txt', 'w+')

    f.write(answerSplit[0]+' score: '+ str(answer_count[0])+'\n')
    f.write(answerSplit[1]+' score: '+ str(answer_count[1])+'\n')
    f.write(answerSplit[2]+' score: '+ str(answer_count[2])+'\n\n')

    f.write('Confidence level is {}'.format(round(confidence/3, 2))+'\n')
    f.write('\nFinal answer is: \n'+ str(final_answer+1) + '.) ' + answerSplit[final_answer]+'\n')
    f.close()

#advanced search using keywords from question instead of just whole question
def advancedSearch(question, answerSplit, not_type):
    answer_count = [0, 0, 0, 0]
    counter = 0
    print('...')
    print('Confidence level too low...')
    print('Running advanced search...')

    #extract important words out of question and scrapes web
    question = keywords(question)
    question = ' '.join(question)
    a = Analysis(question)
    all_text = a.run()

    #Takes all the scraped text and searches through it for the answers
    already_counted = False
    engine = inflect.engine()

    #Advanced search
    #ignores common punctuation
    for data in all_text:
        data_strip = [x.strip(string.punctuation) for x in (data.text).split()]
        for x in answerSplit:
            #Breaks answers up word by word and searches for them
            for word in x.split() :
                for numWords in data_strip:
                    #Compares words regardless of plurality ..
                    if counter == 3:
                        counter = 0
                    if(engine.compare(word.upper(), numWords.upper()) and already_counted == False):
                        already_counted = True
                        answer_count[counter] += 1
                    
            already_counted = False
            counter += 1

    #figuring out final answer and confidence

    if (not_type == False):
        confidence = answer_count[0] - max(answer_count[1], answer_count[2])
        final_answer = 0
        
        if(answer_count[1] > answer_count[final_answer]):
            confidence = answer_count[1] - answer_count[final_answer]
            final_answer = 1
        if(answer_count[2] > answer_count[final_answer]):
            confidence = answer_count[2] - answer_count[final_answer]
            final_answer = 2
    else:
        result_not = not_score(answer_count, answerSplit)
        final_answer = result_not[0]
        confidence = result_not[1]

    confidence = round(confidence, 2)

    if confidence < 2:
        tiebreaker(question, all_text,answerSplit, not_type)

    else:
        
        f = open('results.txt', 'w+')

        f.write(answerSplit[0]+' score: '+ str(answer_count[0])+'\n')
        f.write(answerSplit[1]+' score: '+ str(answer_count[1])+'\n')
        f.write(answerSplit[2]+' score: '+ str(answer_count[2])+'\n\n')

        f.write('Confidence level is {}'.format(round(confidence/3, 2))+'\n')
        f.write('\nFinal answer is: \n'+ str(final_answer+1) + '.) ' +  answerSplit[final_answer]+'\n')
        f.close()

#simple google search
def simpleSearch(question, all_text, answerSplit, not_type): #--------------------------------------------------------------
    answer_count = [0, 0, 0, 0]
    counter = 0

    #Takes all the scraped text and searches through it for the answers
    table = str.maketrans(".,!?:", 5*" ")
    for data in all_text:
        (data.text).translate(table)
        for x in answerSplit:
            if(x.upper() in data.text.upper()):
                answer_count[counter] += 1
            counter += 1
            if counter == 3:
                counter = 0

    #figuring out which answer has the most hits
    if(not_type == False) :
        confidence = answer_count[0] - max(answer_count[1], answer_count[2])
        final_answer = 0

        if(answer_count[1] > answer_count[final_answer]):
            confidence = answer_count[1] - answer_count[final_answer]
            final_answer = 1
        if(answer_count[2] > answer_count[final_answer]):
            confidence = answer_count[2] - answer_count[final_answer]
            final_answer = 2

    else:
        result_not = not_score(answer_count, answerSplit)
        final_answer = result_not[0]
        confidence = result_not[1]
        

    confidence = round(confidence, 2)

    #if confidence too low, runs more advanced search
    if confidence < 2:
        advancedSearch(question, answerSplit, not_type)

    #else prints
    else:


        f = open('results.txt', 'w+')

        f.write(answerSplit[0]+' score: '+ str(answer_count[0])+'\n')
        f.write(answerSplit[1]+' score: '+ str(answer_count[1])+'\n')
        f.write(answerSplit[2]+' score: '+ str(answer_count[2])+'\n\n')

        f.write('Confidence level is {}'.format(round(confidence/3, 2))+'\n')
        f.write('\nFinal answer is: \n'+ str(final_answer+1) + '.) ' +  answerSplit[final_answer]+'\n')
        f.close()

#strips nouns verbs adjectives from text
def keywords(question):
    text = ''.join(question)
    words = word_tokenize(text)
    word_set = (nltk.pos_tag(words))
    simplifiedWords = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in word_set]
    extractedWords = []
    for words in simplifiedWords:
        if (words[1] == 'NOUN' or words[1] == 'ADJ' or words[1] == 'VERB' or words[1] == ''):
            extractedWords.append(words[0])

    return extractedWords
    #print(simplifiedWords)

#--------------------------------------- Splits text into questions and analyzes answers -----------------------------------------------
def findResults(text):
    question = text.split('?')[0]
    questionSplit = question.split()

    answers = text.split('?')[1]
    answerSplit = answers.split('\n')
    
    #filter empty strings from lists
    questionSplit = filter(None, questionSplit)
    answerSplit = list(filter(None,answerSplit))

    print(' '.join(questionSplit))
    print(', '.join(answerSplit))
    print(' ')

    #scraping google web search and returning into all_text variable
    #runs simplesearch algo
    a = Analysis(question)
    all_text = a.run()

    not_type = False
    if 'not'.upper() in question:
        not_type = True
    simpleSearch(question, all_text, answerSplit, not_type)

class Analysis:
    def __init__(self, term):
        self.term = term

        self.url = 'https://www.google.com/search?q={0}'.format(self.term)

    def run (self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        return soup.find_all('span', class_='st') + soup.find_all('h3', class_='r')

